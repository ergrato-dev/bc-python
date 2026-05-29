"""Comandos Typer para reportes."""
from __future__ import annotations

from pathlib import Path
from typing import Annotated
import typer
from rich.console import Console
from rich.table import Table
from ..database import get_session_ctx
from ..services.report_service import report_service
from ..services.exchange_service import exchange_service
from ..exceptions import ExternalServiceError

console = Console()
report_app = typer.Typer(help="Reportes de producción")


@report_app.command("generate")
def report_generate(
    export: Annotated[Path | None, typer.Option(help="Exportar a .csv o .parquet")] = None,
) -> None:
    """Genera reporte de proyectos con presupuesto en ARS."""
    # Obtener tipo de cambio (con fallback)
    ars_rate = 1.0
    try:
        ars_rate = exchange_service.get_ars_rate()
        console.print(f"[dim]Tipo de cambio USD/ARS: {ars_rate:,.2f}[/]")
    except ExternalServiceError as e:
        console.print(f"[yellow]Tipo de cambio no disponible ({e}) — usando 1:1[/]")

    try:
        with get_session_ctx() as session:
            df = report_service.generate_project_report(session)
    except NotImplementedError:
        console.print("[red]ReportService no implementado[/]")
        raise typer.Exit(1)

    import polars as pl
    df = df.with_columns((pl.col("budget") * ars_rate).round(2).alias("budget_ars"))

    # Tabla Rich
    # TODO: construir tabla con columnas: Proyecto | Cliente | USD | ARS | Assets | MB
    console.print("[yellow]TODO: renderizar tabla Rich[/]")
    console.print(df)

    if export:
        if export.suffix == ".parquet":
            report_service.export_parquet(df, export)
        else:
            report_service.export_csv(df, export)
        console.print(f"[green]Exportado:[/] {export}")


@report_app.command("kpis")
def report_kpis() -> None:
    """Muestra KPIs del catálogo."""
    try:
        with get_session_ctx() as session:
            kpis = report_service.report_service.kpis(session) if hasattr(report_service, "kpis") else {}
        # TODO: tabla Rich KPI | Valor
        console.print("[yellow]TODO: report kpis[/]")
    except NotImplementedError:
        console.print("[red]kpis no implementado[/]")
        raise typer.Exit(1)


@report_app.command("exchange")
def report_exchange(
    base: str = typer.Option("USD", help="Moneda base"),
) -> None:
    """Muestra tipos de cambio actuales."""
    try:
        import asyncio
        from ..api_clients.exchange import exchange_client
        async def _fetch():
            return await exchange_client.get_rates(base)
        rates = asyncio.run(_fetch())
        table = Table(title=f"Tipos de cambio — base {base}")
        table.add_column("Moneda")
        table.add_column("Tasa", justify="right")
        for currency, rate in sorted(rates.rates.items())[:20]:
            table.add_row(currency, f"{rate:.4f}")
        console.print(table)
    except NotImplementedError:
        console.print("[yellow]ExchangeClient no implementado — usa stub[/]")
    except ExternalServiceError as e:
        console.print(f"[red]{e}[/]")
        raise typer.Exit(1)
