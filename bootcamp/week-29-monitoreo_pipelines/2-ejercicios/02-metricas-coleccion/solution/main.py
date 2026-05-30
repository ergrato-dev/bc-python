"""
Ejercicio 02: MetricsCollector — Tiempos y Throughput — SOLUCIÓN
================================================================
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
        return self.errors / self.count if self.count else 0.0

    @property
    def avg_duration(self) -> float:
        return mean(self.durations) if self.durations else 0.0

    @property
    def p95_duration(self) -> float:
        if len(self.durations) < 2:
            return self.durations[0] if self.durations else 0.0
        return quantiles(self.durations, n=20)[18]


class MetricsCollector:
    def __init__(self) -> None:
        self._stages: dict[str, StageMetrics] = defaultdict(StageMetrics)
        self._jobs_done = 0
        self._jobs_failed = 0
        self._start_time = time.time()

    def record_stage(self, stage: str, duration_s: float, success: bool) -> None:
        m = self._stages[stage]
        m.durations.append(duration_s)
        if success:
            m.successes += 1
        else:
            m.errors += 1

    def record_job_done(self) -> None:
        self._jobs_done += 1

    def record_job_failed(self) -> None:
        self._jobs_failed += 1

    @property
    def throughput(self) -> float:
        elapsed = time.time() - self._start_time
        return self._jobs_done / elapsed if elapsed > 0 else 0.0

    @property
    def total_error_rate(self) -> float:
        total = self._jobs_done + self._jobs_failed
        return self._jobs_failed / total if total else 0.0

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


if __name__ == "__main__":
    collector = MetricsCollector()
    random.seed(42)

    print("Simulando 20 jobs...")
    for i in range(20):
        for stage in ["ingest", "validate", "process", "export"]:
            d = random.uniform(0.5, 3.0)
            fail = random.random() < 0.1
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
