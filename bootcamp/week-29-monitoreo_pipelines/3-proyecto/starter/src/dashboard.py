"""Rich Live terminal dashboard for studio-monitor."""

from __future__ import annotations

import time
from typing import Any

try:
    from rich.console import Console
    from rich.layout import Layout
    from rich.live import Live
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text
except ImportError:
    raise SystemExit("Instala rich: pip install rich")

from .health import ComponentHealth, HealthStatus
from .metrics import MetricsCollector


console = Console()


def _status_color(status: HealthStatus) -> str:
    return {"ok": "green", "degraded": "yellow", "critical": "red"}[status]


def _rate_color(rate: float) -> str:
    if rate < 0.05:
        return "green"
    if rate < 0.15:
        return "yellow"
    return "red"


def _latency_color(p95: float) -> str:
    if p95 < 5.0:
        return "green"
    if p95 < 10.0:
        return "yellow"
    return "red"


def build_metrics_table(collector: MetricsCollector) -> Panel:
    """Tabla Rich con métricas por stage."""
    # TODO: crear Table con columnas: Stage, Total, Errores, Error %, P95 (s)
    # TODO: iterar collector.snapshot()["stages"] y agregar filas con colores
    # TODO: retornar Panel(table, title="Métricas por Stage", border_style="blue")
    raise NotImplementedError


def build_health_table(checks: dict[str, ComponentHealth]) -> Panel:
    table = Table(show_header=True, header_style="bold")
    table.add_column("Componente")
    table.add_column("Estado")
    table.add_column("Detalle")
    for name, comp in checks.items():
        color = _status_color(comp.status)
        table.add_row(name, Text(comp.status.upper(), style=color), comp.detail)
    return Panel(table, title="Health Checks", border_style="cyan")


def build_status_panel(collector: MetricsCollector, uptime_s: float) -> Panel:
    """Panel de estado global."""
    snap = collector.snapshot()
    er = snap["total_error_rate"]
    color = _rate_color(er)
    if er < 0.05:
        status_label = "OK"
    elif er < 0.15:
        status_label = "DEGRADADO"
    else:
        status_label = "CRÍTICO"

    minutes = int(uptime_s // 60)
    seconds = int(uptime_s % 60)

    text = Text()
    text.append(f"Estado: ", style="bold")
    text.append(f"{status_label}\n", style=f"bold {color}")
    text.append(f"Jobs procesados: {snap['jobs_done']}  |  Fallidos: {snap['jobs_failed']}\n")
    text.append(f"Throughput: {snap['throughput']:.2f} jobs/s  |  Error rate: {er:.1%}\n")
    text.append(f"Uptime: {minutes:02d}:{seconds:02d}")
    return Panel(text, title="Estado Global", border_style="green" if er < 0.05 else "red")


def build_layout(
    collector: MetricsCollector,
    checks: dict[str, ComponentHealth],
    uptime_s: float,
) -> Layout:
    """
    Layout:
    - Top (60 %): métricas por stage
    - Bottom-left (25 %): health checks
    - Bottom-right (15 %): estado global
    """
    # TODO: crear Layout root
    # TODO: split_column: "upper" (ratio 6) y "lower" (ratio 4)
    # TODO: split_row en "lower": "health" (ratio 6) y "status" (ratio 4)
    # TODO: asignar paneles a cada sección y retornar layout
    raise NotImplementedError


def run_dashboard(
    collector: MetricsCollector,
    health_checker: Any,
    refresh_s: float = 1.0,
) -> None:
    """Ejecuta el dashboard en vivo. Ctrl+C para salir."""
    start = time.time()
    try:
        with Live(screen=True, refresh_per_second=int(1 / refresh_s)) as live:
            while True:
                checks = health_checker.check_all()
                uptime = time.time() - start
                live.update(build_layout(collector, checks, uptime))
                time.sleep(refresh_s)
    except KeyboardInterrupt:
        pass
