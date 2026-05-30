# Health Checks

## 1. ¿Qué es un Health Check?

Un health check es una verificación periódica de que el sistema está operativo. Responde preguntas como:

- ¿El pipeline está procesando jobs?
- ¿Redis está accesible?
- ¿El disco tiene espacio suficiente?
- ¿El último job no tardó demasiado?

---

## 2. Status JSON

```python
from __future__ import annotations

import shutil
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from pathlib import Path


class HealthStatus(StrEnum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


@dataclass
class ComponentHealth:
    name: str
    status: HealthStatus
    message: str = ""
    latency_ms: float = 0.0

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "status": str(self.status),
            "message": self.message,
            "latency_ms": round(self.latency_ms, 2),
        }


def check_disk_space(
    path: Path = Path("."),
    min_free_gb: float = 1.0,
) -> ComponentHealth:
    usage = shutil.disk_usage(path)
    free_gb = usage.free / (1024 ** 3)
    if free_gb < min_free_gb:
        return ComponentHealth(
            "disk", HealthStatus.UNHEALTHY,
            f"Espacio libre insuficiente: {free_gb:.1f} GB (mínimo {min_free_gb} GB)"
        )
    return ComponentHealth("disk", HealthStatus.HEALTHY, f"{free_gb:.1f} GB libres")


def check_redis(host: str = "localhost", port: int = 6379) -> ComponentHealth:
    t0 = time.perf_counter()
    try:
        import redis
        r = redis.Redis(host=host, port=port, socket_connect_timeout=2)
        r.ping()
        latency = (time.perf_counter() - t0) * 1000
        return ComponentHealth("redis", HealthStatus.HEALTHY, "OK", latency)
    except Exception as e:
        return ComponentHealth("redis", HealthStatus.UNHEALTHY, str(e))


def check_state_file(
    state_path: Path,
    max_age_minutes: float = 30.0,
) -> ComponentHealth:
    if not state_path.exists():
        return ComponentHealth("state_file", HealthStatus.DEGRADED, "No existe aún")
    age_s = time.time() - state_path.stat().st_mtime
    if age_s > max_age_minutes * 60:
        return ComponentHealth(
            "state_file", HealthStatus.DEGRADED,
            f"Estado sin actualizar hace {age_s / 60:.0f} min"
        )
    return ComponentHealth("state_file", HealthStatus.HEALTHY)
```

---

## 3. Watchdog Timer

Un watchdog timer resetea con cada actividad del pipeline. Si expira, el sistema considera que el pipeline está bloqueado.

```python
import threading


class WatchdogTimer:
    def __init__(self, timeout_s: float, on_timeout: object) -> None:
        self._timeout_s = timeout_s
        self._on_timeout = on_timeout
        self._timer: threading.Timer | None = None
        self._lock = threading.Lock()

    def reset(self) -> None:
        with self._lock:
            if self._timer:
                self._timer.cancel()
            self._timer = threading.Timer(self._timeout_s, self._on_timeout)
            self._timer.daemon = True
            self._timer.start()

    def stop(self) -> None:
        with self._lock:
            if self._timer:
                self._timer.cancel()
                self._timer = None


def _on_pipeline_stalled() -> None:
    import structlog
    structlog.get_logger().error(
        "watchdog_expired", message="Pipeline sin actividad — watchdog expiró"
    )


watchdog = WatchdogTimer(timeout_s=1800.0, on_timeout=_on_pipeline_stalled)
# En cada job procesado: watchdog.reset()
```

---

## 4. HealthChecker Completo

```python
class HealthChecker:
    def __init__(
        self,
        state_path: Path = Path(".pipeline_state.json"),
        metrics_path: Path = Path(".metrics.json"),
        redis_host: str = "localhost",
    ) -> None:
        self._state_path = state_path
        self._metrics_path = metrics_path
        self._redis_host = redis_host

    def check_all(self) -> dict[str, object]:
        components = [
            check_disk_space(),
            check_state_file(self._state_path),
        ]

        # Redis es opcional
        try:
            components.append(check_redis(self._redis_host))
        except ImportError:
            pass

        overall = HealthStatus.HEALTHY
        for c in components:
            if c.status == HealthStatus.UNHEALTHY:
                overall = HealthStatus.UNHEALTHY
                break
            if c.status == HealthStatus.DEGRADED:
                overall = HealthStatus.DEGRADED

        return {
            "status": str(overall),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "components": [c.to_dict() for c in components],
        }
```

---

## 5. Endpoint de Status (HTTP mínimo)

```python
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import threading


class HealthHandler(BaseHTTPRequestHandler):
    checker: HealthChecker

    def do_GET(self) -> None:
        if self.path == "/health":
            result = self.checker.check_all()
            status_code = 200 if result["status"] == "healthy" else 503
            body = json.dumps(result).encode()
            self.send_response(status_code)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format: str, *args: object) -> None:
        pass  # Silenciar logs HTTP en consola


def start_health_server(checker: HealthChecker, port: int = 8080) -> None:
    HealthHandler.checker = checker
    server = HTTPServer(("", port), HealthHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    print(f"Health check en http://localhost:{port}/health")
```

---

## Resumen

| Componente | Función |
|------------|---------|
| `ComponentHealth` | Estado de un componente individual: healthy/degraded/unhealthy |
| `HealthChecker.check_all()` | Agrega checks de disco, Redis, state file → status global |
| `WatchdogTimer` | Reset con cada actividad; llama `on_timeout` si expira |
| Endpoint `/health` | HTTP GET que devuelve JSON con status global |
| Status codes | `200` = healthy, `503` = degraded o unhealthy |
