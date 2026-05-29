"""
Ejercicio 01 — Typer Básico
Studio BC: gestión de proyectos desde CLI.
"""

import typer

app = typer.Typer(help="Studio BC — project management CLI")

# Lista en memoria (no persistente entre ejecuciones)
PROJECTS: list[dict[str, object]] = []


# ─────────────────────────────────────────────
# PASO 1 — validador de project_id
# ─────────────────────────────────────────────

# TODO: implementa validate_project_id(value: str) -> str
# - Verifica que value solo contenga letras, dígitos o guiones (-)
# - Si no: raise typer.BadParameter("project-id must use only letters, digits and -")
# - Retorna value.lower()

# def validate_project_id(value: str) -> str:
#     ...


# ─────────────────────────────────────────────
# PASO 1 — comando create
# ─────────────────────────────────────────────

# TODO: implementa el comando create con:
# @app.command()
# def create(
#     project_id: str = typer.Argument(..., callback=validate_project_id, help="Unique project ID"),
#     client: str = typer.Option(..., "--client", "-c", help="Client name"),
#     budget: float = typer.Option(0.0, "--budget", "-b", min=0.0, help="Budget in USD"),
# ) -> None:
#     """Create a new project."""
#     PROJECTS.append({"id": project_id, "client": client, "budget": budget})
#     typer.secho(f"Created: {project_id} for {client} (${budget:.2f})", fg=typer.colors.GREEN)


# ─────────────────────────────────────────────
# PASO 2 — comando list
# ─────────────────────────────────────────────

# TODO: implementa el comando list con:
# @app.command(name="list")
# def list_projects(
#     count: bool = typer.Option(False, "--count/--no-count", help="Show total count"),
# ) -> None:
#     """List all projects."""
#     if not PROJECTS:
#         typer.secho("No projects found.", fg=typer.colors.YELLOW)
#         return
#     for p in PROJECTS:
#         typer.echo(f"  - {p['id']} ({p['client']}) ${p['budget']:.2f}")
#     if count:
#         typer.secho(f"\nTotal: {len(PROJECTS)} project(s)", bold=True)


# ─────────────────────────────────────────────
# PASO 3 — comando delete
# ─────────────────────────────────────────────

# TODO: implementa el comando delete con:
# @app.command()
# def delete(
#     project_id: str = typer.Argument(..., help="Project ID to delete"),
# ) -> None:
#     """Delete a project after confirmation."""
#     confirmed = typer.confirm(f"Delete project '{project_id}'?")
#     if not confirmed:
#         typer.echo("Cancelled.")
#         return
#     # Busca y elimina de PROJECTS. Si no existe, muestra error.
#     ...


if __name__ == "__main__":
    app()
