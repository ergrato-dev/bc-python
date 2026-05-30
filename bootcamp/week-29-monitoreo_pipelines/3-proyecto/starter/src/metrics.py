"""MetricsCollector — per-stage throughput, error rate and latency percentiles."""

from __future__ import annotations

import statistics
import time
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any


@dataclass
class StageMetrics:
    durations: list[float] = field(default_factory=list)
    success_count: int = 0
    error_count: int = 0

    def record(self, duration_s: float, success: bool) -> None:
        """Registra una ejecución de stage: duración y resultado."""
        # TODO: agregar duration_s a self.durations
        # TODO: incrementar success_count o error_count según success
        raise NotImplementedError

    @property
    def total(self) -> int:
        return self.success_count + self.error_count

    @property
    def error_rate(self) -> float:
        return self.error_count / max(self.total, 1)

    @property
    def p50(self) -> float:
        if not self.durations:
            return 0.0
        return statistics.median(self.durations)

    @property
    def p95(self) -> float:
        if len(self.durations) < 20:
            return max(self.durations, default=0.0)
        return statistics.quantiles(self.durations, n=20)[18]


class MetricsCollector:
    def __init__(self) -> None:
        self._stages: dict[str, StageMetrics] = defaultdict(StageMetrics)
        self._jobs_done: int = 0
        self._jobs_failed: int = 0
        self._start_time: float = time.time()

    def record_stage(self, stage: str, duration_s: float, success: bool) -> None:
        """Delega en StageMetrics y actualiza contadores globales."""
        # TODO: llamar self._stages[stage].record(duration_s, success)
        # TODO: incrementar _jobs_done si success, _jobs_failed si no
        raise NotImplementedError

    @property
    def throughput(self) -> float:
        """Jobs exitosos por segundo desde el inicio."""
        elapsed = time.time() - self._start_time
        # TODO: retornar self._jobs_done / elapsed (evitar división por cero)
        raise NotImplementedError

    @property
    def total_error_rate(self) -> float:
        total = self._jobs_done + self._jobs_failed
        return self._jobs_failed / max(total, 1)

    def snapshot(self) -> dict[str, Any]:
        """Devuelve métricas globales y por stage como dict serializable."""
        return {
            "throughput": round(self.throughput, 3),
            "total_error_rate": round(self.total_error_rate, 4),
            "jobs_done": self._jobs_done,
            "jobs_failed": self._jobs_failed,
            "stages": {
                name: {
                    "total": m.total,
                    "error_rate": round(m.error_rate, 4),
                    "p50_s": round(m.p50, 3),
                    "p95_s": round(m.p95, 3),
                }
                for name, m in self._stages.items()
            },
        }

    def get_stage(self, stage: str) -> StageMetrics:
        return self._stages[stage]
