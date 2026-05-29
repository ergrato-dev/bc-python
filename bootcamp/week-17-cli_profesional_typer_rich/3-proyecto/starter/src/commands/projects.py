"""projects.py — Comandos del grupo projects."""
from __future__ import annotations
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from ..models import Config, Project
from .. import store

projects_app = typer.Typer(help="Manage Studio BC projects")
console = Console()
err_console = Console(stderr=True)


@projects_app.command("list")
def projects_list(ctx: typer.Context) -> None:
    """List all projects."""
    cfg: Config = ctx.obj
    # TODO: obtén projects con store.get_projects()
    # TODO: muestra Table con columnas: ID, Client, Budget, Assets
    # Assets count: len(store.get_assets(p.id))
    raise NotImplementedError


@projects_app.command("create")
def projects_create(
    ctx: typer.Context,
    project_id: str = typer.Argument(..., help="Unique project ID"),
    client: str = typer.Option(..., "--client", "-c", help="Client name"),
    budget: float = typer.Option(0.0, "--budget", "-b", min=0.0, help="Budget in USD"),
) -> None:
    """Create a new project."""
    # TODO: valida que project_id no exista ya (err_console + Exit(1))
    # TODO: crea Project y llama store.add_project()
    # TODO: muestra Panel con los datos del nuevo proyecto
    raise NotImplementedError


@projects_app.command("status")
def projects_status(
    ctx: typer.Context,
    project_id: str = typer.Argument(..., help="Project ID"),
) -> None:
    """Show project status and asset summary."""
    # TODO: obtén el proyecto. Si no existe, err_console + Exit(1).
    # TODO: muestra Panel con: ID, Client, Budget, total assets, assets por tipo
    raise NotImplementedError
