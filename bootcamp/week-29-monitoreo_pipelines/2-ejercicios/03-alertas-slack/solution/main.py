"""
Ejercicio 03 — Alertas y Thresholds con Slack — SOLUCIÓN
=========================================================
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field


@dataclass
class AlertRule:
    name: str
    metric: str
    threshold: float
    comparison: str      # "gt" | "lt"
    message_template: str
    cooldown_s: float = 60.0
    _last_fired: float = field(default=0.0, init=False, repr=False)

    def should_fire(self, value: float) -> bool:
        # Verificar umbral
        if self.comparison == "gt":
            triggered = value > self.threshold
        else:
            triggered = value < self.threshold

        if not triggered:
            return False

        # Verificar cooldown
        if time.time() - self._last_fired < self.cooldown_s:
            return False

        self._last_fired = time.time()
        return True

    def format_message(self, value: float) -> str:
        return self.message_template.format(value=value, threshold=self.threshold)


@dataclass
class Alert:
    rule_name: str
    metric: str
    value: float
    message: str
    fired_at: float = field(default_factory=time.time)


class AlertManager:
    def __init__(
        self,
        rules: list[AlertRule],
        slack_webhook: str = "",
        dry_run: bool = True,
    ) -> None:
        self._rules = rules
        self._webhook = slack_webhook
        self._dry_run = dry_run
        self._history: list[Alert] = []

    def _send_slack(self, alert: Alert) -> None:
        if self._dry_run:
            print(f"[DRY-RUN] ALERT: {alert.rule_name} — {alert.message}")
            return
        import requests
        requests.post(
            self._webhook,
            json={"text": f":rotating_light: *{alert.rule_name}*: {alert.message}"},
            timeout=5,
        )

    def check(self, metrics: dict[str, float]) -> list[Alert]:
        fired: list[Alert] = []
        for rule in self._rules:
            value = metrics.get(rule.metric)
            if value is None:
                continue
            if rule.should_fire(value):
                alert = Alert(
                    rule_name=rule.name,
                    metric=rule.metric,
                    value=value,
                    message=rule.format_message(value),
                )
                fired.append(alert)
                self._history.append(alert)
                self._send_slack(alert)
        return fired

    @property
    def history(self) -> list[Alert]:
        return list(self._history)


def build_studio_rules() -> list[AlertRule]:
    return [
        AlertRule(
            name="high_error_rate",
            metric="error_rate",
            threshold=0.05,
            comparison="gt",
            message_template="Tasa de error {value:.1%} supera umbral {threshold:.1%}",
            cooldown_s=30.0,
        ),
        AlertRule(
            name="slow_p95",
            metric="p95_s",
            threshold=10.0,
            comparison="gt",
            message_template="P95 latencia {value:.1f}s supera umbral {threshold:.0f}s",
            cooldown_s=30.0,
        ),
        AlertRule(
            name="low_throughput",
            metric="throughput",
            threshold=0.5,
            comparison="lt",
            message_template="Throughput {value:.2f} jobs/s está bajo mínimo {threshold:.1f}",
            cooldown_s=60.0,
        ),
    ]


def run_simulation() -> None:
    rules = build_studio_rules()
    manager = AlertManager(rules=rules, dry_run=True)

    snapshots = [
        {"error_rate": 0.01, "p95_s": 3.2, "throughput": 2.1},   # OK
        {"error_rate": 0.08, "p95_s": 3.2, "throughput": 2.1},   # → high_error_rate
        {"error_rate": 0.08, "p95_s": 3.2, "throughput": 2.1},   # cooldown activo
        {"error_rate": 0.01, "p95_s": 14.0, "throughput": 2.1},  # → slow_p95
        {"error_rate": 0.01, "p95_s": 3.2, "throughput": 0.2},   # → low_throughput
    ]

    for i, snap in enumerate(snapshots):
        print(f"\n--- snapshot {i + 1}: {snap}")
        fired = manager.check(snap)
        if not fired:
            print("  (sin alertas)")

    print(f"\nHistorial total: {len(manager.history)} alertas")


if __name__ == "__main__":
    run_simulation()
