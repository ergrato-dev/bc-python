"""studio-bc-manager — CLI de gestión de producción para Studio BC."""
from __future__ import annotations

import typer
from src.database import create_tables
from src.commands.clients import clients_app
from src.commands.projects import projects_app
from src.commands.assets import assets_app
from src.commands.report import report_app

app = typer.Typer(
    help="Studio BC Manager — Gestión de producción audiovisual",
    no_args_is_help=True,
)
app.add_typer(clients_app,  name="clients")
app.add_typer(projects_app, name="projects")
app.add_typer(assets_app,   name="assets")
app.add_typer(report_app,   name="report")


@app.callback()
def main_callback() -> None:
    """Inicializa la base de datos al arrancar."""
    create_tables()


if __name__ == "__main__":
    app()
