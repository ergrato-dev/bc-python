"""Comandos Typer para clientes."""
from __future__ import annotations

import typer
from rich.console import Console
from rich.table import Table
from sqlmodel import Session, select
from ..database import get_session_ctx
from ..models import Client
from ..exceptions import NotFoundError

console = Console()
clients_app = typer.Typer(help="Gestionar clientes")


def _render_clients(items: list[Client]) -> None:
    if not items:
        console.print("[yellow]Sin clientes registrados.[/]")
        return
    table = Table(title="Clientes", show_lines=True)
    table.add_column("ID",    style="dim", width=6)
    table.add_column("Nombre")
    table.add_column("Email")
    table.add_column("País", width=6)
    for c in items:
        table.add_row(str(c.id), c.name, c.email, c.country)
    console.print(table)


@clients_app.command("list")
def clients_list() -> None:
    """Lista todos los clientes ordenados por nombre."""
    # TODO: with get_session_ctx() as session: session.exec(select(Client).order_by(Client.name))
    console.print("[yellow]TODO: clients list[/]")


@clients_app.command("create")
def clients_create(
    name:    str = typer.Option(..., prompt=True),
    email:   str = typer.Option(..., prompt=True),
    country: str = typer.Option("AR"),
) -> None:
    """Crea un nuevo cliente."""
    # TODO: verificar unicidad de email, insertar, confirmar
    console.print("[yellow]TODO: clients create[/]")


@clients_app.command("delete")
def clients_delete(
    id: int = typer.Option(..., help="ID del cliente"),
    force: bool = typer.Option(False, "--force", help="Sin confirmación"),
) -> None:
    """Elimina un cliente (solo si no tiene proyectos activos)."""
    # TODO: verificar proyectos activos, confirmar con typer.confirm, borrar
    console.print("[yellow]TODO: clients delete[/]")
