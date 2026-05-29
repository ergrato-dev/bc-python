"""pipeline.py — Lazy pipeline de KPIs para Studio BC."""
from __future__ import annotations

import polars as pl
from pathlib import Path


def build_kpi_pipeline(data_dir: str | Path) -> tuple[pl.DataFrame, pl.DataFrame]:
    """
    Construye el reporte de KPIs usando Lazy API.
    Retorna (kpi_report, weekly_trend).

    TODO: implementar con scan_csv y un único collect() al final.

    Pipeline esperado:
    1. scan_csv timesheets, projects, rates
    2. join timesheets con rates por "employee"
    3. with_columns: cost_usd = hours * hourly_rate_usd
    4. group_by "project_id" → agg KPIs (total_hours, billable_hours, total_cost_usd, team_size)
    5. join con projects por "project_id" (left)
    6. with_columns: margin_usd, margin_pct, billable_pct
    7. collect() una sola vez

    Para weekly_trend:
    1. scan_csv timesheets con try_parse_dates=True
    2. with_columns: week = date.dt.week()
    3. group_by("project_id", "week").agg(total_hours)
    4. collect()
    """
    data_dir = Path(data_dir)

    # TODO: implementar
    raise NotImplementedError


def save_outputs(kpi: pl.DataFrame, trend: pl.DataFrame, output_dir: str | Path) -> None:
    """Guarda los reportes en Parquet y JSON."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # TODO: escribe kpi a output_dir/kpi_report.parquet y kpi_report.json
    # TODO: escribe trend a output_dir/weekly_trend.parquet
    raise NotImplementedError
