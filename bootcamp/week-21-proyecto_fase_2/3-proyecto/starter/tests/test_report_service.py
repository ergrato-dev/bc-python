"""Tests para ReportService con Polars."""
from __future__ import annotations

import pytest
import polars as pl
from sqlmodel import Session
from src.services.report_service import ReportService
from src.models import Project


@pytest.fixture
def service() -> ReportService:
    return ReportService()


def test_generate_report_returns_dataframe(
    session: Session, service: ReportService, project_fixture
) -> None:
    try:
        df = service.generate_project_report(session)
        assert isinstance(df, pl.DataFrame)
        assert "project_name" in df.columns
        assert "budget" in df.columns
        assert len(df) >= 1
    except NotImplementedError:
        pytest.skip("generate_project_report no implementado")


def test_report_budget_total(
    session: Session, service: ReportService, client_fixture
) -> None:
    session.add_all([
        Project(name="P1", client_id=client_fixture.id, budget=1000.0),
        Project(name="P2", client_id=client_fixture.id, budget=3000.0),
    ])
    session.commit()
    try:
        df = service.generate_project_report(session)
        total = df.select(pl.sum("budget")).item()
        assert total == 4000.0
    except NotImplementedError:
        pytest.skip("no implementado")
