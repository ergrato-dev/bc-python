"""main.py — App raíz de bc-studio-cli."""
from __future__ import annotations
import typer
from .commands.assets import assets_app
from .commands.projects import projects_app
from .commands.report import report_app
from .models import Config

app = typer.Typer(
    name="bc-studio-cli",
    help="Studio BC — internal production management CLI",
    no_args_is_help=True,
)

app.add_typer(assets_app,   name="assets")
app.add_typer(projects_app, name="projects")
app.add_typer(report_app,   name="report")


@app.callback()
def main(
    ctx: typer.Context,
    verbose: bool = typer.Option(False, "--verbose/--no-verbose", "-v/-V", help="Enable verbose output"),
    api_url: str = typer.Option(
        "https://api.studio.bc",
        "--api-url",
        envvar="BC_API_URL",
        help="Studio BC API URL",
        show_default=True,
    ),
) -> None:
    """Studio BC CLI — manage projects and assets from the terminal."""
    ctx.ensure_object(dict)
    ctx.obj = Config(verbose=verbose, api_url=api_url)


if __name__ == "__main__":
    app()
