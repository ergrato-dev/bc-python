"""
Studio BC Catalog DB — CLI de demostración.

Uso:
  python main.py projects
  python main.py assets --project-id 1
  python main.py kpis
"""
from __future__ import annotations

import sys
from rich.console import Console
from rich.table import Table
from sqlmodel import Session
from src.database import engine, create_db_and_tables
from src.repositories.project import project_repo
from src.repositories.asset import asset_repo

console = Console()


def cmd_projects(session: Session) -> None:
    """Muestra tabla de proyectos activos."""
    # TODO: project_repo.list_active(session) → Rich Table
    # Columnas: ID, Nombre, Presupuesto, Status
    console.print("[yellow]TODO: implementar cmd_projects[/]")


def cmd_assets(session: Session, project_id: int) -> None:
    """Muestra assets de un proyecto."""
    # TODO: asset_repo.list_by_project(session, project_id) → Rich Table
    # Columnas: ID, Nombre, Tipo, Tamaño MB
    console.print("[yellow]TODO: implementar cmd_assets[/]")


def cmd_kpis(session: Session) -> None:
    """Muestra KPIs del catálogo."""
    # TODO: project_repo.kpis(session) → Rich Table
    console.print("[yellow]TODO: implementar cmd_kpis[/]")


def main() -> None:
    create_db_and_tables()

    if len(sys.argv) < 2:
        console.print("Uso: python main.py [projects|assets|kpis]")
        return

    cmd = sys.argv[1]
    with Session(engine) as session:
        if cmd == "projects":
            cmd_projects(session)
        elif cmd == "assets":
            pid = int(sys.argv[3]) if len(sys.argv) > 3 else 1
            cmd_assets(session, pid)
        elif cmd == "kpis":
            cmd_kpis(session)
        else:
            console.print(f"Comando desconocido: {cmd}")


if __name__ == "__main__":
    main()
