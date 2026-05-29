"""report.py — Comandos del grupo report."""
from __future__ import annotations
import json
import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.progress import track
from rich.table import Table
from ..models import Config
from .. import store

report_app = typer.Typer(help="Generate project reports")
console = Console()


@report_app.command("generate")
def report_generate(
    ctx: typer.Context,
    project_id: str = typer.Argument(..., help="Project ID"),
    fmt: str = typer.Option("table", "--format", "-f", help="Output format: table|json|markdown"),
) -> None:
    """Generate a project report."""
    cfg: Config = ctx.obj
    project = store.get_project(project_id)
    if not project:
        console.print(f"[red]Project {project_id!r} not found[/red]")
        raise typer.Exit(code=1)

    assets = store.get_assets(project_id)

    # TODO: si cfg.verbose, usa track(assets, "Building report...") con sleep(0.1)
    # TODO: según fmt:
    #   "table"    → Table con columnas Name, Type, Size
    #   "json"     → console.print_json(json.dumps([...]))
    #   "markdown" → console.print(Markdown("# Report
..."))
    #   otro valor → err_console + Exit(1)
    raise NotImplementedError
