"""Tests for AlertRule and AlertManager."""

import time
import pytest
from src.alerts import AlertManager, AlertRule, build_studio_rules


class TestAlertRule:
    def _make_rule(self, comparison: str = "gt", cooldown_s: float = 0.0) -> AlertRule:
        return AlertRule(
            name="test_rule",
            metric="error_rate",
            threshold=0.05,
            comparison=comparison,
            message_template="value={value:.2f} threshold={threshold:.2f}",
            cooldown_s=cooldown_s,
        )

    def test_fires_when_gt_threshold(self) -> None:
        rule = self._make_rule("gt")
        assert rule.should_fire(0.10) is True

    def test_does_not_fire_below_threshold(self) -> None:
        rule = self._make_rule("gt")
        assert rule.should_fire(0.02) is False

    def test_lt_fires_when_below(self) -> None:
        rule = self._make_rule("lt")
        # threshold=0.05, lt → fires when value < 0.05
        assert rule.should_fire(0.01) is True

    def test_cooldown_prevents_double_fire(self) -> None:
        rule = self._make_rule("gt", cooldown_s=60.0)
        assert rule.should_fire(0.10) is True
        assert rule.should_fire(0.10) is False  # cooldown activo

    def test_cooldown_zero_allows_refire(self) -> None:
        rule = self._make_rule("gt", cooldown_s=0.0)
        assert rule.should_fire(0.10) is True
        assert rule.should_fire(0.10) is True


class TestAlertManager:
    def _make_manager(self) -> AlertManager:
        rules = [
            AlertRule(
                name="high_error",
                metric="error_rate",
                threshold=0.05,
                comparison="gt",
                message_template="Error {value:.1%}",
                cooldown_s=0.0,
            )
        ]
        return AlertManager(rules=rules, dry_run=True)

    def test_check_fires_alert(self, capsys: pytest.CaptureFixture[str]) -> None:
        mgr = self._make_manager()
        fired = mgr.check({"error_rate": 0.10})
        assert len(fired) == 1
        assert fired[0].rule_name == "high_error"

    def test_check_no_alert_below_threshold(self) -> None:
        mgr = self._make_manager()
        fired = mgr.check({"error_rate": 0.02})
        assert len(fired) == 0

    def test_history_accumulates(self, capsys: pytest.CaptureFixture[str]) -> None:
        mgr = self._make_manager()
        mgr.check({"error_rate": 0.10})
        mgr.check({"error_rate": 0.20})
        assert len(mgr.history) == 2

    def test_dry_run_prints_to_stdout(self, capsys: pytest.CaptureFixture[str]) -> None:
        mgr = self._make_manager()
        mgr.check({"error_rate": 0.10})
        captured = capsys.readouterr()
        assert "DRY-RUN" in captured.out or "ALERT" in captured.out
