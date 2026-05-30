"""AlertRule + AlertManager — threshold-based alerting with cooldown."""

from __future__ import annotations

import time
from dataclasses import dataclass, field

import requests


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
        """Retorna True si el valor supera el umbral Y el cooldown expiró."""
        # TODO: comparar value con self.threshold según self.comparison
        # TODO: verificar time.time() - self._last_fired >= self.cooldown_s
        # TODO: si ambas condiciones: actualizar _last_fired, retornar True
        raise NotImplementedError

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
            # TODO: imprimir "[DRY-RUN] ALERT: {alert.rule_name} — {alert.message}"
            raise NotImplementedError
        requests.post(
            self._webhook,
            json={"text": f":rotating_light: *{alert.rule_name}*: {alert.message}"},
            timeout=5,
        )

    def check(self, metrics: dict[str, float]) -> list[Alert]:
        """Evalúa cada regla y dispara alertas si corresponde."""
        fired: list[Alert] = []
        for rule in self._rules:
            # TODO: obtener metrics.get(rule.metric); saltar si None
            # TODO: llamar rule.should_fire(value)
            # TODO: crear Alert, agregar a fired y _history, llamar _send_slack
            raise NotImplementedError
        return fired

    @property
    def history(self) -> list[Alert]:
        return list(self._history)


def build_studio_rules(cooldown_s: float = 60.0) -> list[AlertRule]:
    return [
        AlertRule(
            name="high_error_rate",
            metric="total_error_rate",
            threshold=0.05,
            comparison="gt",
            message_template="Tasa de error {value:.1%} supera {threshold:.1%}",
            cooldown_s=cooldown_s,
        ),
        AlertRule(
            name="low_throughput",
            metric="throughput",
            threshold=0.1,
            comparison="lt",
            message_template="Throughput {value:.2f} jobs/s bajo mínimo {threshold:.1f}",
            cooldown_s=cooldown_s,
        ),
        AlertRule(
            name="slow_ingest_p95",
            metric="ingest_p95_s",
            threshold=15.0,
            comparison="gt",
            message_template="Ingest P95 {value:.1f}s supera {threshold:.0f}s",
            cooldown_s=cooldown_s,
        ),
    ]
