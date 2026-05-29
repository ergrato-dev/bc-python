"""
Checkpoint 02 — Servicios + Reportes con Polars
=================================================
Objetivo: añadir la capa de servicios y el comando `report generate`
que usa Polars para aggregaciones y exporta a CSV.

Tareas:
  1. Implementar ProjectService (create, list_active, kpis)
  2. Implementar ReportService (generate_project_report → pl.DataFrame)
  3. Implementar `report generate` con tabla Rich + export CSV opcional
  4. Conectar ExchangeService (stub sin red) para mostrar budget en ARS

Ejecutar: python main.py report generate
          python main.py report generate --export report.csv
          python main.py report kpis
"""
from __future__ import annotations

import asyncio
from contextlib import contextmanager
from collections.abc import Generator
from pathlib import Path
from typing import Annotated

import polars as pl
import typer
from rich.console import Console
from rich.table import Table
from sqlmodel import SQLModel, Field, Session, create_engine, select
from sqlalchemy import func

console = Console()
app = typer.Typer(help="Studio BC Manager — Checkpoint 02")
report_app = typer.Typer(help="Reportes de producción")
app.add_typer(report_app, name="report")

DATABASE_URL = "sqlite:///checkpoint02.db"


# ── Modelos (ya definidos) ─────────────────────────────────────────────────────

class Client(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str
    country: str = "AR"


class Project(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    budget: float = 0.0
    status: str = "active"
    is_active: bool = True
    client_id: int | None = Field(default=None, foreign_key="client.id")


engine = create_engine(DATABASE_URL)

@contextmanager
def get_session_ctx() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


# ── Tarea 1 — ProjectService ──────────────────────────────────────────────────

class ProjectService:
    def list_active(self, session: Session) -> list[Project]:
        # TODO: select activos ordenados por name
        raise NotImplementedError

    def kpis(self, session: Session) -> dict:
        # TODO: total (count), total_budget (sum), avg_budget, max_budget
        raise NotImplementedError


project_service = ProjectService()


# ── Tarea 2 — ReportService ───────────────────────────────────────────────────

class ReportService:
    def generate_project_report(self, session: Session) -> pl.DataFrame:
        """
        Retorna DataFrame con columnas:
        project_name | client_name | budget | status
        Ordenado por budget desc.
        """
        # TODO: JOIN Project + Client, construir lista de dicts, pl.DataFrame(rows)
        raise NotImplementedError

    def export_csv(self, df: pl.DataFrame, path: Path) -> None:
        # TODO: df.write_csv(path)
        raise NotImplementedError


report_service = ReportService()


# ── Tarea 3 — ExchangeService (stub) ─────────────────────────────────────────

class ExchangeService:
    def get_ars_rate(self) -> float:
        """Stub: devuelve tasa fija. En la versión final usa httpx async."""
        # TODO opcional: implementar llamada real con asyncio.run()
        return 1050.0


exchange_service = ExchangeService()


# ── Tarea 4 — report generate ────────────────────────────────────────────────

@report_app.command("generate")
def report_generate(
    export: Annotated[Path | None, typer.Option(help="Exportar a CSV")] = None,
) -> None:
    """Genera reporte de proyectos con presupuesto en ARS."""
    try:
        ars_rate = exchange_service.get_ars_rate()
    except Exception:
        ars_rate = 1.0
        console.print("[yellow]Tipo de cambio no disponible — usando 1:1[/]")

    try:
        with get_session_ctx() as session:
            df = report_service.generate_project_report(session)
    except NotImplementedError:
        console.print("[red]ReportService no implementado aún[/]")
        raise typer.Exit(1)

    # Añadir columna ARS
    df = df.with_columns(
        (pl.col("budget") * ars_rate).alias("budget_ars")
    )

    # TODO: construir tabla Rich con columnas: Proyecto | Cliente | USD | ARS
    # TODO: console.print(table)

    if export:
        try:
            report_service.export_csv(df, export)
            console.print(f"[green]Exportado:[/] {export}")
        except NotImplementedError:
            console.print("[red]export_csv no implementado aún[/]")


@report_app.command("kpis")
def report_kpis() -> None:
    """Muestra KPIs del catálogo."""
    try:
        with get_session_ctx() as session:
            kpis = project_service.kpis(session)
        table = Table(title="KPIs — Studio BC")
        table.add_column("Métrica")
        table.add_column("Valor", justify="right")
        for k, v in kpis.items():
            table.add_row(k, str(v))
        console.print(table)
    except NotImplementedError:
        console.print("[red]ProjectService.kpis no implementado aún[/]")
        raise typer.Exit(1)


# ── Seed + main ───────────────────────────────────────────────────────────────

def seed() -> None:
    with Session(engine) as session:
        if session.exec(select(Client)).first():
            return
        c1 = Client(name="Canal 9", email="prod@canal9.com")
        c2 = Client(name="Agencia Norte", email="info@norte.com")
        session.add_all([c1, c2])
        session.flush()
        session.add_all([
            Project(name="Spot Verano",   client_id=c1.id, budget=5000),
            Project(name="Reel Anual",    client_id=c1.id, budget=12000),
            Project(name="Jingle Navidad",client_id=c2.id, budget=3000),
            Project(name="Campaña Social",client_id=c2.id, budget=8000, status="draft"),
        ])
        session.commit()

@app.callback(invoke_without_command=True)
def main_cb(ctx: typer.Context) -> None:
    SQLModel.metadata.create_all(engine)
    seed()
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())

if __name__ == "__main__":
    app()
