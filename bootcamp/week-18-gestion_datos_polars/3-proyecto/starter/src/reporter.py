"""reporter.py — Reporte Rich de KPIs."""
from __future__ import annotations

import polars as pl
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def print_kpi_table(kpi: pl.DataFrame) -> None:
    """
    Imprime la tabla de KPIs con Rich.

    TODO: construye una Table con columnas:
    Project, Client, Hours, Cost (USD), Budget (USD), Margin (USD), Margin (%)

    Colores:
    - Margin % >= 50 → green
    - Margin % >= 20 → yellow
    - Margin % < 20  → red
    """
    # TODO: implementar
    raise NotImplementedError


def print_alerts(kpi: pl.DataFrame, threshold_pct: float = 90.0) -> None:
    """
    BONUS: imprime un panel de alerta para proyectos que superaron
    el threshold_pct del presupuesto en costos.
    cost_pct = total_cost_usd / budget_usd * 100
    """
    # TODO: implementar (bonus)
    pass
