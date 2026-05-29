"""Servicio de reportes — Polars."""
from __future__ import annotations

from pathlib import Path
import polars as pl
from sqlmodel import Session, select
from sqlalchemy import func
from ..models import Project, Client, Asset


class ReportService:
    def generate_project_report(self, session: Session) -> pl.DataFrame:
        """
        Retorna DataFrame con columnas:
        project_id | project_name | client_name | budget | asset_count | total_size_mb

        Implementación sugerida:
        1. JOIN Project + Client con LEFT JOIN Asset
        2. GROUP BY project para contar assets y sumar tamaño
        3. Construir lista de dicts y convertir a pl.DataFrame
        4. Ordenar por budget desc
        """
        # TODO
        raise NotImplementedError

    def export_csv(self, df: pl.DataFrame, path: Path) -> None:
        df.write_csv(path)

    def export_parquet(self, df: pl.DataFrame, path: Path) -> None:
        df.write_parquet(path)

    def summary_by_client(self, session: Session) -> pl.DataFrame:
        """
        Agrupado por cliente:
        client_name | project_count | total_budget | avg_budget
        """
        # TODO: basarse en generate_project_report + group_by("client_name")
        raise NotImplementedError


report_service = ReportService()
