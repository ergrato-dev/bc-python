"""CLI entry point for studio-monitor."""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

try:
    import typer
except ImportError:
    raise SystemExit("Instala typer: pip install typer")

from .alerts import AlertManager, build_studio_rules
from .config import load_settings
from .health import HealthChecker, WatchdogTimer
from .metrics import MetricsCollector
from .dashboard import run_dashboard

app = typer.Typer(help="studio-monitor — pipeline observability daemon")


def _watchdog_timeout() -> None:
    typer.echo("[WATCHDOG] Timeout! El monitor no respondió. Saliendo.", err=True)
    sys.exit(1)


@app.command()
def monitor(
    state_file: str = typer.Option(".sync_state.json", help="Ruta al archivo de estado del pipeline"),
    slack_webhook: str = typer.Option("", envvar="SLACK_WEBHOOK", help="Webhook de Slack para alertas"),
    dry_run: bool = typer.Option(True, help="No enviar alertas reales"),
    refresh: float = typer.Option(1.0, help="Segundos entre actualizaciones del dashboard"),
    watchdog: float = typer.Option(30.0, help="Timeout del watchdog en segundos"),
) -> None:
    """Arranca el dashboard en vivo con alertas y health checks."""
    settings = load_settings()
    webhook = slack_webhook or settings.slack_webhook

    collector = MetricsCollector()
    rules = build_studio_rules(cooldown_s=settings.alert_cooldown_s)
    alert_mgr = AlertManager(rules=rules, slack_webhook=webhook, dry_run=dry_run)
    health_checker = HealthChecker(state_file=state_file)
    wd = WatchdogTimer(timeout_s=watchdog, on_timeout=_watchdog_timeout)

    wd.start()
    try:
        run_dashboard(collector, health_checker, refresh_s=refresh)
    finally:
        wd.cancel()


@app.command()
def status(
    state_file: str = typer.Option(".sync_state.json", help="Ruta al archivo de estado"),
    json_output: bool = typer.Option(False, "--json", help="Salida en formato JSON"),
) -> None:
    """Muestra el estado actual del pipeline (sin dashboard)."""
    health_checker = HealthChecker(state_file=state_file)
    checks = health_checker.check_all()
    overall = health_checker.overall_status()

    if json_output:
        data = {
            "overall": overall,
            "checks": {name: {"status": c.status, "detail": c.detail} for name, c in checks.items()},
        }
        typer.echo(json.dumps(data, indent=2))
    else:
        typer.echo(f"Estado general: {overall.upper()}")
        for name, comp in checks.items():
            typer.echo(f"  {name}: [{comp.status}] {comp.detail}")


if __name__ == "__main__":
    app()
