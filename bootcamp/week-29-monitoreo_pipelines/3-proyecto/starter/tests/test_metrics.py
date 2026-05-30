"""Tests for MetricsCollector and StageMetrics."""

import pytest
from src.metrics import MetricsCollector, StageMetrics


class TestStageMetrics:
    def test_record_success_increments_count(self) -> None:
        m = StageMetrics()
        m.record(1.0, success=True)
        assert m.success_count == 1
        assert m.error_count == 0

    def test_record_error_increments_error_count(self) -> None:
        m = StageMetrics()
        m.record(2.0, success=False)
        assert m.error_count == 1
        assert m.success_count == 0

    def test_error_rate_zero_on_no_errors(self) -> None:
        m = StageMetrics()
        for _ in range(5):
            m.record(1.0, success=True)
        assert m.error_rate == pytest.approx(0.0)

    def test_error_rate_correct(self) -> None:
        m = StageMetrics()
        for _ in range(8):
            m.record(1.0, success=True)
        for _ in range(2):
            m.record(1.0, success=False)
        assert m.error_rate == pytest.approx(0.2)

    def test_p95_returns_max_for_small_sample(self) -> None:
        m = StageMetrics()
        for d in [1.0, 2.0, 3.0, 5.0]:
            m.record(d, success=True)
        assert m.p95 == pytest.approx(5.0)


class TestMetricsCollector:
    def test_throughput_increases_with_jobs(self) -> None:
        collector = MetricsCollector()
        for _ in range(10):
            collector.record_stage("ingest", 0.5, success=True)
        assert collector.throughput > 0

    def test_total_error_rate(self) -> None:
        collector = MetricsCollector()
        for _ in range(9):
            collector.record_stage("ingest", 1.0, success=True)
        collector.record_stage("ingest", 1.0, success=False)
        assert collector.total_error_rate == pytest.approx(0.1)

    def test_snapshot_contains_stage(self) -> None:
        collector = MetricsCollector()
        collector.record_stage("transcode", 3.0, success=True)
        snap = collector.snapshot()
        assert "transcode" in snap["stages"]
