"""
Ejercicio 02: MetricsCollector — Tiempos y Throughput
=====================================================
Implementa un recolector de métricas que registra duración por etapa
y calcula throughput, tasa de error y percentil 95.

Ejecutar: python main.py
"""
from __future__ import annotations

import random
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
        # TODO: devolver errors / count, o 0.0 si count == 0
        raise NotImplementedError

    @property
    def avg_duration(self) -> float:
        # TODO: mean(durations) o 0.0 si vacío
        raise NotImplementedError

    @property
    def p95_duration(self) -> float:
        # TODO: quantiles(durations, n=20)[18] para p95
        # Si hay menos de 2 elementos, devolver el único elemento o 0.0
        raise NotImplementedError


class MetricsCollector:
    def __init__(self) -> None:
        self._stages: dict[str, StageMetrics] = defaultdict(StageMetrics)
        self._jobs_done = 0
        self._jobs_failed = 0
        self._start_time = time.time()

    def record_stage(self, stage: str, duration_s: float, success: bool) -> None:
        # TODO: actualizar self._stages[stage] con duration y success/error
        raise NotImplementedError

    def record_job_done(self) -> None:
        # TODO: self._jobs_done += 1
        raise NotImplementedError

    def record_job_failed(self) -> None:
        # TODO: self._jobs_failed += 1
        raise NotImplementedError

    @property
    def throughput(self) -> float:
        # TODO: jobs_done / elapsed
        raise NotImplementedError

    @property
    def total_error_rate(self) -> float:
        # TODO: jobs_failed / (jobs_done + jobs_failed)
        raise NotImplementedError

    def snapshot(self) -> dict[str, object]:
        # TODO: devolver dict con jobs_done, jobs_failed, throughput_per_s, error_rate, stages
        raise NotImplementedError


if __name__ == "__main__":
    collector = MetricsCollector()
    random.seed(42)

    print("Simulando 20 jobs...")
    for i in range(20):
        for stage in ["ingest", "validate", "process", "export"]:
            d = random.uniform(0.5, 3.0)
            fail = random.random() < 0.1  # 10% de errores
            collector.record_stage(stage, d, not fail)
        if random.random() < 0.15:
            collector.record_job_failed()
        else:
            collector.record_job_done()

    snap = collector.snapshot()
    print(f"Jobs done: {snap['jobs_done']}")
    print(f"Jobs failed: {snap['jobs_failed']}")
    print(f"Throughput: {float(str(snap['throughput_per_s'])):.4f} j/s")
    print(f"Error rate: {float(str(snap['error_rate'])):.1%}")
    stages = snap.get("stages", {})
    for name, s in stages.items():  # type: ignore[union-attr]
        print(f"  {name}: avg={float(str(s['avg_s'])):.2f}s p95={float(str(s['p95_s'])):.2f}s err={float(str(s['error_rate'])):.1%}")

    assert snap["jobs_done"] > 0
    assert float(str(snap["error_rate"])) < 0.5
    print("\nOK — Ejercicio 02 completado")
