# Métricas de Pipeline

## 1. Qué Medir

| Métrica | Descripción | Tipo |
|---------|-------------|------|
| Duración por etapa | Tiempo en segundos de cada `Stage` | Histograma |
| Throughput | Jobs completados por segundo | Gauge calculado |
| Tasa de error | Porcentaje de jobs fallidos | Ratio |
| Cola pendiente | Jobs en estado `pending` | Gauge |
| p95 de duración | Percentil 95 de tiempos de etapa | Derivada |

---

## 2. `MetricsCollector`

```python
from __future__ import annotations

import time
from collections import defaultdict
from dataclasses import dataclass, field
from statistics import mean, quantiles


@dataclass
class StageMetrics:
    durations: list[float] = field(default_factory=list)
    errors: int = 0
    successes: int = 0

    @property
    def count(self) -> int:
        return self.successes + self.errors

    @property
    def error_rate(self) -> float:
        return self.errors / self.count if self.count else 0.0

    @property
    def avg_duration(self) -> float:
        return mean(self.durations) if self.durations else 0.0

    @property
    def p95_duration(self) -> float:
        if len(self.durations) < 2:
            return self.durations[0] if self.durations else 0.0
        return quantiles(self.durations, n=20)[18]  # p95 = posición 19 de 20


class MetricsCollector:
    def __init__(self) -> None:
        self._stages: dict[str, StageMetrics] = defaultdict(StageMetrics)
        self._jobs_done = 0
        self._jobs_failed = 0
        self._start_time = time.time()
        self._last_job_time: float | None = None

    def record_stage(self, stage: str, duration_s: float, success: bool) -> None:
        m = self._stages[stage]
        m.durations.append(duration_s)
        if success:
            m.successes += 1
        else:
            m.errors += 1

    def record_job_done(self) -> None:
        self._jobs_done += 1
        self._last_job_time = time.time()

    def record_job_failed(self) -> None:
        self._jobs_failed += 1
        self._last_job_time = time.time()

    @property
    def throughput(self) -> float:
        elapsed = time.time() - self._start_time
        return self._jobs_done / elapsed if elapsed > 0 else 0.0

    @property
    def total_error_rate(self) -> float:
        total = self._jobs_done + self._jobs_failed
        return self._jobs_failed / total if total else 0.0

    @property
    def seconds_since_last_job(self) -> float | None:
        if self._last_job_time is None:
            return None
        return time.time() - self._last_job_time

    def snapshot(self) -> dict[str, object]:
        return {
            "jobs_done": self._jobs_done,
            "jobs_failed": self._jobs_failed,
            "throughput_per_s": round(self.throughput, 4),
            "error_rate": round(self.total_error_rate, 4),
            "stages": {
                name: {
                    "count": m.count,
                    "error_rate": round(m.error_rate, 4),
                    "avg_s": round(m.avg_duration, 3),
                    "p95_s": round(m.p95_duration, 3),
                }
                for name, m in self._stages.items()
            },
        }
```

---

## 3. Integración con el Pipeline (Week 27)

```python
import time
from src.stages import Stage, StageResult


class InstrumentedPipeline:
    def __init__(self, stages: list[Stage], metrics: MetricsCollector) -> None:
        self._stages = stages
        self._metrics = metrics

    def run(self, data: dict[str, object]) -> StageResult:
        for stage in self._stages:
            t0 = time.perf_counter()
            result = stage.process(data)
            duration = time.perf_counter() - t0

            self._metrics.record_stage(stage.name, duration, result.success)

            if not result.success:
                self._metrics.record_job_failed()
                return result
            data = result.data

        self._metrics.record_job_done()
        return StageResult(success=True, data=data)
```

---

## 4. Prometheus Client (introducción)

`prometheus_client` expone métricas en el formato estándar que Prometheus y Grafana consumen:

```python
from prometheus_client import Counter, Histogram, Gauge, start_http_server

JOBS_TOTAL = Counter("pipeline_jobs_total", "Total jobs procesados", ["status"])
STAGE_DURATION = Histogram(
    "pipeline_stage_duration_seconds",
    "Duración de cada etapa",
    ["stage"],
    buckets=[0.1, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0],
)
QUEUE_SIZE = Gauge("pipeline_queue_pending", "Jobs en cola pendiente")


def record_stage_prometheus(stage: str, duration_s: float, success: bool) -> None:
    STAGE_DURATION.labels(stage=stage).observe(duration_s)
    status = "success" if success else "error"
    JOBS_TOTAL.labels(status=status).inc()


# Exponer en puerto 8000 para que Prometheus haga scraping
start_http_server(8000)
```

---

## 5. Exportar Métricas a JSON

```python
import json
from pathlib import Path
from datetime import datetime, timezone


def export_metrics_snapshot(
    collector: MetricsCollector,
    output_path: Path = Path(".metrics.json"),
) -> None:
    snapshot = collector.snapshot()
    snapshot["exported_at"] = datetime.now(timezone.utc).isoformat()
    tmp = output_path.with_suffix(".tmp")
    tmp.write_text(json.dumps(snapshot, indent=2))
    tmp.replace(output_path)
```

---

## Resumen

| Métrica | Cómo calcularla |
|---------|-----------------|
| Throughput | `jobs_done / elapsed_seconds` |
| Tasa de error total | `jobs_failed / (jobs_done + jobs_failed)` |
| p95 de etapa | `statistics.quantiles(durations, n=20)[18]` |
| Tasa de error por etapa | `stage.errors / stage.count` |
| Tiempo sin actividad | `time.time() - last_job_time` |
