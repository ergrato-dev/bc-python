"""HealthChecker + WatchdogTimer — component health and timeout guard."""

from __future__ import annotations

import os
import shutil
import threading
import time
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Callable


class HealthStatus(StrEnum):
    OK = "ok"
    DEGRADED = "degraded"
    CRITICAL = "critical"


@dataclass
class ComponentHealth:
    name: str
    status: HealthStatus
    detail: str = ""


def check_disk_space(path: str = ".", min_free_gb: float = 5.0) -> ComponentHealth:
    usage = shutil.disk_usage(path)
    free_gb = usage.free / (1024**3)
    if free_gb >= min_free_gb:
        return ComponentHealth("disk", HealthStatus.OK, f"{free_gb:.1f} GB libres")
    if free_gb >= min_free_gb * 0.5:
        return ComponentHealth("disk", HealthStatus.DEGRADED, f"Solo {free_gb:.1f} GB libres")
    return ComponentHealth("disk", HealthStatus.CRITICAL, f"Crítico: {free_gb:.1f} GB libres")


def check_redis(redis_url: str) -> ComponentHealth:
    try:
        import redis  # type: ignore[import-untyped]
        client = redis.from_url(redis_url, socket_connect_timeout=2)
        client.ping()
        return ComponentHealth("redis", HealthStatus.OK, "ping OK")
    except Exception as exc:
        return ComponentHealth("redis", HealthStatus.CRITICAL, str(exc))


def check_state_file(state_file: str) -> ComponentHealth:
    path = Path(state_file)
    if not path.exists():
        return ComponentHealth("state_file", HealthStatus.DEGRADED, "No existe aún")
    age_s = time.time() - path.stat().st_mtime
    if age_s < 300:
        return ComponentHealth("state_file", HealthStatus.OK, f"Modificado hace {age_s:.0f}s")
    return ComponentHealth(
        "state_file", HealthStatus.DEGRADED, f"Sin cambios hace {age_s / 60:.1f} min"
    )


class HealthChecker:
    def __init__(
        self,
        state_file: str = ".sync_state.json",
        redis_url: str = "redis://localhost:6379/0",
        min_free_gb: float = 5.0,
        check_redis_enabled: bool = False,
    ) -> None:
        self._state_file = state_file
        self._redis_url = redis_url
        self._min_free_gb = min_free_gb
        self._check_redis_enabled = check_redis_enabled

    def check_all(self) -> dict[str, ComponentHealth]:
        """Ejecuta todos los checks y retorna dict {nombre: ComponentHealth}."""
        # TODO: ejecutar check_disk_space, check_state_file
        # TODO: si self._check_redis_enabled, también check_redis
        # TODO: retornar dict con nombre como clave
        raise NotImplementedError

    def overall_status(self) -> HealthStatus:
        checks = self.check_all()
        statuses = [c.status for c in checks.values()]
        if HealthStatus.CRITICAL in statuses:
            return HealthStatus.CRITICAL
        if HealthStatus.DEGRADED in statuses:
            return HealthStatus.DEGRADED
        return HealthStatus.OK


class WatchdogTimer:
    """Llama a on_timeout() si no recibe reset() en timeout_s segundos."""

    def __init__(self, timeout_s: float, on_timeout: Callable[[], None]) -> None:
        self._timeout_s = timeout_s
        self._on_timeout = on_timeout
        self._timer: threading.Timer | None = None
        self._lock = threading.Lock()

    def start(self) -> None:
        with self._lock:
            self._timer = threading.Timer(self._timeout_s, self._on_timeout)
            self._timer.daemon = True
            self._timer.start()

    def reset(self) -> None:
        """Reinicia el temporizador. Llama a esto periódicamente para evitar el timeout."""
        # TODO: cancelar self._timer si existe
        # TODO: crear y arrancar un nuevo Timer con self._timeout_s y self._on_timeout
        raise NotImplementedError

    def cancel(self) -> None:
        with self._lock:
            if self._timer is not None:
                self._timer.cancel()
                self._timer = None
