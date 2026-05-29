"""
Checkpoint 01 — DB + CLI Skeleton
===================================
Objetivo: conectar SQLModel con Typer y verificar que `projects list`
y `clients list` funcionan antes de agregar lógica de negocio.

Tareas:
  1. Completar los modelos Client y Project con los campos indicados
  2. Implementar get_session_ctx() como context manager
  3. Implementar el comando `clients list` → tabla Rich
  4. Implementar el comando `projects list` con filtro --client-id

Ejecutar: python main.py clients list
          python main.py projects list
          python main.py projects list --client-id 1
"""
from __future__ import annotations

from contextlib import contextmanager
from collections.abc import Generator
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table
from sqlmodel import SQLModel, Field, Session, Relationship, create_engine, select

console = Console()
app = typer.Typer(help="Studio BC Manager — Checkpoint 01")
clients_app  = typer.Typer(help="Gestionar clientes")
projects_app = typer.Typer(help="Gestionar proyectos")
app.add_typer(clients_app,  name="clients")
app.add_typer(projects_app, name="projects")

DATABASE_URL = "sqlite:///checkpoint01.db"


# ── Tarea 1 — Modelos ─────────────────────────────────────────────────────────

class Client(SQLModel, table=True):
    # TODO: id (PK), name, email, country (default "AR")
    # TODO: projects: list["Project"] = Relationship(back_populates="client_rel")
    pass


class Project(SQLModel, table=True):
    # TODO: id (PK), name, budget (default 0.0), status (default "active"), is_active (default True)
    # TODO: client_id: int | None = Field(default=None, foreign_key="client.id")
    # TODO: client_rel: Client | None = Relationship(back_populates="projects")
    pass


# ── Tarea 2 — Engine y sesión ─────────────────────────────────────────────────

engine = create_engine(DATABASE_URL, echo=False)

@contextmanager
def get_session_ctx() -> Generator[Session, None, None]:
    # TODO: with Session(engine) as session: yield session
    raise NotImplementedError


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


# ── Tarea 3 — clients list ────────────────────────────────────────────────────

@clients_app.command("list")
def clients_list() -> None:
    """Lista todos los clientes."""
    # TODO: with get_session_ctx() as session:
    #           items = session.exec(select(Client)).all()
    # TODO: tabla Rich: ID | Nombre | Email | País
    console.print("[yellow]TODO: implementar clients list[/]")


@clients_app.command("create")
def clients_create(
    name: str = typer.Option(..., prompt=True),
    email: str = typer.Option(..., prompt=True),
    country: str = typer.Option("AR"),
) -> None:
    """Crea un cliente."""
    # TODO: insertar Client y confirmar con Rich
    console.print("[yellow]TODO: implementar clients create[/]")


# ── Tarea 4 — projects list ───────────────────────────────────────────────────

@projects_app.command("list")
def projects_list(
    client_id: Annotated[int | None, typer.Option(help="Filtrar por cliente")] = None,
) -> None:
    """Lista proyectos activos, opcionalmente filtrados por cliente."""
    # TODO: construir select(Project).where(Project.is_active == True)
    # TODO: si client_id: añadir .where(Project.client_id == client_id)
    # TODO: tabla Rich: ID | Nombre | Cliente | Presupuesto | Status
    console.print("[yellow]TODO: implementar projects list[/]")


@projects_app.command("create")
def projects_create(
    name: str = typer.Option(..., prompt=True),
    client_id: int = typer.Option(..., prompt=True),
    budget: float = typer.Option(0.0),
) -> None:
    """Crea un proyecto."""
    # TODO: verificar que client_id existe; si no, typer.Exit(1)
    # TODO: insertar Project y confirmar con Rich
    console.print("[yellow]TODO: implementar projects create[/]")


# ── Seed + main ───────────────────────────────────────────────────────────────

def seed() -> None:
    """Poblar con datos de prueba si la DB está vacía."""
    with Session(engine) as session:
        if session.exec(select(Client)).first():
            return
        c1 = Client(name="Canal 9", email="prod@canal9.com", country="AR")
        c2 = Client(name="Agencia Norte", email="info@norte.com", country="AR")
        session.add_all([c1, c2])
        session.flush()
        session.add_all([
            Project(name="Spot Verano", client_id=c1.id, budget=5000),
            Project(name="Reel Anual",  client_id=c1.id, budget=12000),
            Project(name="Jingle",      client_id=c2.id, budget=3000),
        ])
        session.commit()

@app.callback(invoke_without_command=True)
def main_cb(ctx: typer.Context) -> None:
    init_db()
    try:
        seed()
    except Exception:
        pass
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())

if __name__ == "__main__":
    app()
