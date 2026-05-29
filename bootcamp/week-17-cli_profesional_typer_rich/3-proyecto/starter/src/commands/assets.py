"""assets.py — Comandos del grupo assets."""
from __future__ import annotations
import typer
from rich.console import Console
from rich.table import Table
from ..models import Asset, Config
from .. import store

assets_app = typer.Typer(help="Manage project assets")
console = Console()
err_console = Console(stderr=True)


@assets_app.command("list")
def assets_list(
    ctx: typer.Context,
    project_id: str = typer.Argument("", help="Filter by project ID"),
    asset_type: str = typer.Option("", "--type", "-t", help="Filter by type"),
) -> None:
    """List assets, optionally filtered by project and type."""
    cfg: Config = ctx.obj
    # TODO: obtén los assets con store.get_assets(project_id or None)
    # TODO: filtra por asset_type si se proporcionó
    # TODO: si no hay assets, muestra aviso y return
    # TODO: construye una Table con columnas Name, Type, Size, Project
    # TODO: si cfg.verbose, imprime f"[dim]API: {cfg.api_url}[/dim]" antes de la tabla
    raise NotImplementedError


@assets_app.command("add")
def assets_add(
    ctx: typer.Context,
    project_id: str = typer.Argument(..., help="Target project ID"),
    name: str = typer.Argument(..., help="Asset filename"),
    asset_type: str = typer.Option("video", "--type", "-t", help="Asset type"),
    size: str = typer.Option("—", "--size", help="File size (e.g. 128 MB)"),
) -> None:
    """Add an asset to a project."""
    cfg: Config = ctx.obj
    # TODO: valida que project_id existe en store. Si no, err_console + Exit(1).
    # TODO: valida que asset_type es video/audio/image. Si no, BadParameter.
    # TODO: crea Asset y llama store.add_asset()
    # TODO: imprime confirmación con green
    raise NotImplementedError


@assets_app.command("remove")
def assets_remove(
    ctx: typer.Context,
    project_id: str = typer.Argument(..., help="Project ID"),
    name: str = typer.Argument(..., help="Asset name to remove"),
) -> None:
    """Remove an asset from a project."""
    # TODO: typer.confirm() antes de eliminar
    # TODO: llama store.remove_asset(). Si False, err_console + Exit(1).
    raise NotImplementedError
