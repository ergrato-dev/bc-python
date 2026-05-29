"""Comandos Typer para assets."""
from __future__ import annotations

import typer
from rich.console import Console
from rich.table import Table
from ..database import get_session_ctx
from ..repositories.asset import asset_repo
from ..exceptions import NotFoundError

console = Console()
assets_app = typer.Typer(help="Gestionar assets multimedia")


@assets_app.command("list")
def assets_list(
    project_id: int = typer.Option(..., help="ID del proyecto"),
) -> None:
    """Lista assets de un proyecto."""
    # TODO: asset_repo.list_by_project → tabla Rich: ID | Nombre | Tipo | MB
    console.print("[yellow]TODO: assets list[/]")


@assets_app.command("add")
def assets_add(
    project_id: int   = typer.Option(...),
    name:       str   = typer.Option(..., prompt=True),
    type:       str   = typer.Option("video"),
    size_mb:    float = typer.Option(0.0),
) -> None:
    """Agrega un asset a un proyecto."""
    # TODO: verificar proyecto existe, crear Asset
    console.print("[yellow]TODO: assets add[/]")


@assets_app.command("tag")
def assets_tag(
    id:   int = typer.Option(..., help="ID del asset"),
    tags: str = typer.Option(..., help="Tags separados por coma: hd,4k"),
) -> None:
    """Asocia tags a un asset."""
    # TODO: para cada tag en tags.split(",") → asset_repo.add_tag(session, id, tag)
    console.print("[yellow]TODO: assets tag[/]")
