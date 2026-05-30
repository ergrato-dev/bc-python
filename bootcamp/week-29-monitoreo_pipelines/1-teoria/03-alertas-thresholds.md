# Alertas y Thresholds

## 1. Modelo de Alerta

Una alerta tiene tres partes:
1. **Regla**: condición evaluada contra las métricas actuales
2. **Threshold**: valor límite que, si se supera, dispara la alerta
3. **Cooldown**: tiempo mínimo entre dos alertas del mismo tipo (evita spam)

```python
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Callable


@dataclass
class AlertRule:
    name: str
    check: Callable[[dict[str, object]], bool]  # True = alerta activa
    message_fn: Callable[[dict[str, object]], str]
    cooldown_s: float = 300.0  # 5 minutos por defecto
    _last_fired: float = field(default=0.0, init=False, repr=False)

    def should_fire(self, metrics: dict[str, object]) -> bool:
        if not self.check(metrics):
            return False
        if time.time() - self._last_fired < self.cooldown_s:
            return False
        return True

    def fire(self, metrics: dict[str, object]) -> str:
        self._last_fired = time.time()
        return self.message_fn(metrics)
```

---

## 2. Reglas de Alerta Comunes

```python
def build_studio_rules() -> list[AlertRule]:
    return [
        AlertRule(
            name="high_error_rate",
            check=lambda m: float(str(m.get("error_rate", 0))) > 0.2,
            message_fn=lambda m: (
                f":red_circle: *Alta tasa de error en pipeline*\n"
                f"Tasa actual: {float(str(m.get('error_rate', 0))):.1%} (umbral: 20%)\n"
                f"Jobs fallidos: {m.get('jobs_failed', 0)}"
            ),
            cooldown_s=300.0,
        ),
        AlertRule(
            name="low_throughput",
            check=lambda m: (
                int(str(m.get("jobs_done", 0))) > 10
                and float(str(m.get("throughput_per_s", 1))) < 0.01
            ),
            message_fn=lambda m: (
                f":warning: *Throughput bajo*\n"
                f"Throughput actual: {float(str(m.get('throughput_per_s', 0))):.4f} jobs/s\n"
                f"Revisar workers y cola pendiente."
            ),
            cooldown_s=600.0,
        ),
        AlertRule(
            name="pipeline_stalled",
            check=lambda m: (
                m.get("seconds_since_last_job") is not None
                and float(str(m.get("seconds_since_last_job", 0))) > 1800
            ),
            message_fn=lambda m: (
                f":stop_sign: *Pipeline detenido*\n"
                f"Sin actividad hace {float(str(m.get('seconds_since_last_job', 0))) / 60:.0f} minutos."
            ),
            cooldown_s=1800.0,
        ),
        AlertRule(
            name="stage_slow",
            check=lambda m: any(
                float(str(stage.get("p95_s", 0))) > 30.0
                for stage in (m.get("stages") or {}).values()  # type: ignore[union-attr]
            ),
            message_fn=lambda m: (
                f":hourglass: *Etapa lenta detectada*\n"
                + "\n".join(
                    f"  `{name}` p95={float(str(s.get('p95_s', 0))):.1f}s"
                    for name, s in (m.get("stages") or {}).items()  # type: ignore[union-attr]
                    if float(str(s.get("p95_s", 0))) > 30.0
                )
            ),
            cooldown_s=900.0,
        ),
    ]
```

---

## 3. AlertManager

```python
import httpx
import structlog

log = structlog.get_logger()


class AlertManager:
    def __init__(
        self,
        rules: list[AlertRule],
        slack_webhook_url: str = "",
        discord_webhook_url: str = "",
    ) -> None:
        self._rules = rules
        self._slack_url = slack_webhook_url
        self._discord_url = discord_webhook_url

    def evaluate(self, metrics: dict[str, object]) -> list[str]:
        fired: list[str] = []
        for rule in self._rules:
            if rule.should_fire(metrics):
                message = rule.fire(metrics)
                log.warning("alert_fired", rule=rule.name, message=message)
                self._send(message)
                fired.append(rule.name)
        return fired

    def _send(self, message: str) -> None:
        if self._slack_url:
            try:
                httpx.post(self._slack_url, json={"text": message}, timeout=5.0).raise_for_status()
            except Exception as e:
                log.error("alert_slack_failed", error=str(e))

        if self._discord_url:
            try:
                httpx.post(self._discord_url, json={"content": message}, timeout=5.0).raise_for_status()
            except Exception as e:
                log.error("alert_discord_failed", error=str(e))
```

---

## 4. Escalamiento de Alertas

```python
@dataclass
class EscalatingAlert:
    """Alerta que escala si no se reconoce en N minutos."""
    name: str
    check: Callable[[dict[str, object]], bool]
    message_fn: Callable[[dict[str, object]], str]
    cooldown_s: float = 300.0
    escalation_s: float = 900.0    # escalar si sigue activa en 15 min
    _last_fired: float = field(default=0.0, init=False, repr=False)
    _acknowledged: bool = field(default=False, init=False, repr=False)

    def acknowledge(self) -> None:
        self._acknowledged = True

    def reset(self) -> None:
        self._acknowledged = False
        self._last_fired = 0.0

    def should_escalate(self, metrics: dict[str, object]) -> bool:
        if not self.check(metrics):
            return False
        elapsed = time.time() - self._last_fired
        return elapsed > self.escalation_s and not self._acknowledged
```

---

## 5. Alertas a Email (via SMTP)

```python
import smtplib
from email.message import EmailMessage


def send_email_alert(
    subject: str,
    body: str,
    to: str,
    smtp_host: str = "smtp.gmail.com",
    smtp_port: int = 587,
    username: str = "",
    password: str = "",
) -> None:
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = username
    msg["To"] = to
    msg.set_content(body)

    with smtplib.SMTP(smtp_host, smtp_port) as s:
        s.starttls()
        s.login(username, password)
        s.send_message(msg)
```

---

## Resumen

| Concepto | Implementación |
|----------|----------------|
| Threshold | `check(metrics) → bool` |
| Cooldown | `time.time() - last_fired < cooldown_s` |
| AlertManager | Evalúa todas las reglas contra el snapshot de métricas |
| Escalamiento | Vuelve a alertar si la condición persiste y no fue reconocida |
| Canal | Slack webhook y/o Discord webhook y/o email SMTP |
