"""
Ejercicio 03 — Alertas y Thresholds con Slack

Objetivo: implementar un sistema de alertas con umbral + cooldown que envía
notificaciones a Slack cuando una métrica supera el límite configurado.

Pasos:
1. Completar AlertRule con lógica de cooldown
2. Completar AlertManager._send_slack()
3. Completar AlertManager.check() para evaluar reglas
4. Ejecutar la simulación y observar alertas en consola (dry_run=True)
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Callable


# ─── Modelos ────────────────────────────────────────────────────────────────

@dataclass
class AlertRule:
    name: str
    metric: str                     # clave en el dict de métricas
    threshold: float
    comparison: str                 # "gt" | "lt"
    message_template: str           # usa {value} y {threshold}
    cooldown_s: float = 60.0
    _last_fired: float = field(default=0.0, init=False, repr=False)

    def should_fire(self, value: float) -> bool:
        """Retorna True si el valor supera el umbral Y el cooldown expiró."""
        # TODO: verificar comparison ("gt" → value > threshold, "lt" → value < threshold)
        # TODO: verificar que time.time() - self._last_fired >= self.cooldown_s
        # TODO: si ambas condiciones se cumplen, actualizar _last_fired y retornar True
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


# ─── AlertManager ────────────────────────────────────────────────────────────

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
        """Envía el mensaje a Slack vía webhook o imprime si dry_run."""
        if self._dry_run:
            # TODO: imprimir "[DRY-RUN] ALERT: {alert.rule_name} — {alert.message}"
            raise NotImplementedError
        # Producción: POST a self._webhook con JSON {"text": alert.message}
        # (no implementar HTTP real en este ejercicio)

    def check(self, metrics: dict[str, float]) -> list[Alert]:
        """Evalúa todas las reglas contra el dict de métricas y dispara alertas."""
        fired: list[Alert] = []
        for rule in self._rules:
            # TODO: obtener el valor de metrics para rule.metric (saltar si no existe)
            # TODO: llamar rule.should_fire(value) y, si retorna True:
            #   - crear Alert y agregar a fired y a self._history
            #   - llamar self._send_slack(alert)
            raise NotImplementedError
        return fired

    @property
    def history(self) -> list[Alert]:
        return list(self._history)


# ─── Reglas de ejemplo ───────────────────────────────────────────────────────

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


# ─── Simulación ──────────────────────────────────────────────────────────────

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
