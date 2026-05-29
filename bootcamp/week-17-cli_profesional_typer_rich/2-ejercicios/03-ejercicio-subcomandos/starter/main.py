"""
Ejercicio 03 — Subcomandos y Estado Compartido
Studio BC: CLI con múltiples grupos de comandos y config global.
"""

from dataclasses import dataclass
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()
err_console = Console(stderr=True)

# ─────────────────────────────────────────────
# Config dataclass
# ─────────────────────────────────────────────

@dataclass
class Config:
    verbose: bool = False
    api_url: str = "https://api.studio.bc"


# ─────────────────────────────────────────────
# Apps
# ─────────────────────────────────────────────

app = typer.Typer(help="Studio BC — internal production management CLI")

# TODO: crea assets_app, projects_app y config_app como typer.Typer()
# con sus respectivos `help=` descriptivos.

# assets_app = typer.Typer(help="Manage project assets")
# projects_app = typer.Typer(help="Manage projects")
# config_app = typer.Typer(help="Show CLI configuration")

# TODO: agrega los sub-apps al app raíz con add_typer()
# app.add_typer(assets_app, name="assets")
# ...


# ─────────────────────────────────────────────
# PASO 2 — Callback global
# ─────────────────────────────────────────────

# TODO: implementa el callback global:
# @app.callback()
# def main(
#     ctx: typer.Context,
#     verbose: bool = typer.Option(False, "--verbose/--no-verbose", "-v/-V"),
#     api_url: str = typer.Option(
#         "https://api.studio.bc",
#         "--api-url",
#         envvar="BC_API_URL",
#         help="Studio BC API URL",
#     ),
# ) -> None:
#     """Studio BC CLI — manage projects and assets."""
#     ctx.ensure_object(dict)
#     ctx.obj = Config(verbose=verbose, api_url=api_url)


# ─────────────────────────────────────────────
# PASO 3 — Comandos de assets
# ─────────────────────────────────────────────

# Datos en memoria
_ASSETS: list[dict[str, str]] = [
    {"name": "intro.mp4",  "type": "video", "project": "reel-2025"},
    {"name": "logo.png",   "type": "image", "project": "reel-2025"},
]

# TODO: implementa los 3 comandos de assets_app:
# @assets_app.command("list")
# def assets_list(ctx: typer.Context, project: str = typer.Option("", help="Filter by project")) -> None:
#     """List all assets, optionally filtered by project."""
#     cfg: Config = ctx.obj
#     if cfg.verbose:
#         console.print(f"[dim]Fetching assets from {cfg.api_url}...[/dim]")
#     assets = [a for a in _ASSETS if not project or a["project"] == project]
#     # Muestra tabla con Rich
#     ...

# @assets_app.command("add")
# def assets_add(ctx, name, project, asset_type) -> None: ...

# @assets_app.command("remove")
# def assets_remove(ctx, name) -> None: ...   # usar typer.confirm()


# ─────────────────────────────────────────────
# PASO 3 — Comandos de projects
# ─────────────────────────────────────────────

_PROJECTS: list[dict[str, str]] = [
    {"id": "reel-2025",   "client": "Estudio Norte"},
    {"id": "spot-bc-01",  "client": "BC Media"},
]

# TODO: implementa projects_app.command("list") y projects_app.command("create")


# ─────────────────────────────────────────────
# PASO 3 — Comando de config
# ─────────────────────────────────────────────

# TODO: implementa config_app.command("show") que muestre un Panel con:
# API URL, Verbose mode, Version


if __name__ == "__main__":
    app()
