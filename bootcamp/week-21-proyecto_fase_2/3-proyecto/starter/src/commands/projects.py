"""Comandos Typer para proyectos."""
from __future__ import annotations

from typing import Annotated
import typer
from rich.console import Console
from rich.table import Table
from ..database import get_session_ctx
from ..services.project_service import project_service
from ..exceptions import NotFoundError, DomainValidationError

console = Console()
projects_app = typer.Typer(help="Gestionar proyectos")


def _render_projects(items) -> None:
    if not items:
        console.print("[yellow]Sin proyectos.[/]")
        return
    table = Table(title="Proyectos", show_lines=True)
    table.add_column("ID", style="dim", width=6)
    table.add_column("Nombre")
    table.add_column("Cliente ID", width=10)
    table.add_column("Presupuesto", justify="right")
    table.add_column("Status")
    for p in items:
        table.add_row(
            str(p.id), p.name, str(p.client_id or "-"),
            f"${p.budget:,.2f}", p.status
        )
    console.print(table)


@projects_app.command("list")
def projects_list(
    client_id: Annotated[int | None, typer.Option(help="Filtrar por cliente")] = None,
) -> None:
    """Lista proyectos activos."""
    try:
        with get_session_ctx() as session:
            items = project_service.list_active(session, client_id=client_id)
        _render_projects(items)
    except NotImplementedError:
        console.print("[red]project_service.list_active no implementado[/]")
        raise typer.Exit(1)


@projects_app.command("create")
def projects_create(
    name:      str   = typer.Option(..., prompt=True),
    client_id: int   = typer.Option(..., prompt=True),
    budget:    float = typer.Option(0.0),
) -> None:
    """Crea un proyecto."""
    try:
        with get_session_ctx() as session:
            project = project_service.create(session, name, client_id, budget)
        console.print(f"[green]Proyecto creado:[/] {project.name} (id={project.id})")
    except NotFoundError as e:
        console.print(f"[red]Error:[/] {e}")
        raise typer.Exit(1)
    except DomainValidationError as e:
        console.print(f"[red]Validación:[/] {e}")
        raise typer.Exit(1)


@projects_app.command("update")
def projects_update(
    id:     int   = typer.Option(...),
    budget: float = typer.Option(...),
) -> None:
    """Actualiza el presupuesto de un proyecto."""
    try:
        with get_session_ctx() as session:
            p = project_service.update_budget(session, id, budget)
        console.print(f"[green]Actualizado:[/] {p.name} → ${p.budget:,.2f}")
    except NotFoundError as e:
        console.print(f"[red]{e}[/]")
        raise typer.Exit(1)


@projects_app.command("deactivate")
def projects_deactivate(
    id: int = typer.Option(...),
    force: bool = typer.Option(False, "--force"),
) -> None:
    """Desactiva un proyecto."""
    if not force:
        typer.confirm(f"¿Desactivar proyecto id={id}?", abort=True)
    try:
        with get_session_ctx() as session:
            p = project_service.deactivate(session, id)
        console.print(f"[yellow]Proyecto desactivado:[/] {p.name}")
    except NotFoundError as e:
        console.print(f"[red]{e}[/]")
        raise typer.Exit(1)
