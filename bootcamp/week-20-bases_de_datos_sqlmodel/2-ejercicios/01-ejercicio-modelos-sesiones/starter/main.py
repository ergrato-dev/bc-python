"""
Ejercicio 01 — Modelos, Engine y Sesiones
==========================================
Practica los fundamentos de SQLModel: definir modelos, crear el engine,
gestionar sesiones y ejecutar CRUD básico con SQLite.

Tareas:
  1. [define_models]    Completar los modelos Project y Asset con los campos correctos
  2. [setup_engine]     Crear el engine SQLite y las tablas
  3. [create_project]   Insertar un proyecto y retornarlo con id generado
  4. [list_projects]    Listar proyectos activos ordenados por nombre
  5. [update_budget]    Actualizar el presupuesto de un proyecto
  6. [soft_delete]      Marcar proyecto como inactivo (no borrar de la DB)

Ejecutar: python main.py
"""
from __future__ import annotations

from datetime import datetime
from sqlmodel import SQLModel, Field, Session, create_engine, select


# ── Tarea 1 — Definir modelos ──────────────────────────────────────────────────

class Project(SQLModel, table=True):
    """
    Campos requeridos:
    - id: entero, PK autoincrementable, nullable en Python
    - name: string, max 100 chars, indexado
    - client: string
    - budget: float, mínimo 0, default 0.0
    - status: string, default "active"
    - created_at: datetime, default=utcnow
    - is_active: bool, default True
    """
    # TODO: definir los 7 campos con Field() donde corresponda
    pass


class Asset(SQLModel, table=True):
    """
    Campos requeridos:
    - id: entero, PK
    - name: string, max 200 chars
    - type: string ("video" | "audio" | "image"), default "video"
    - size_mb: float, mínimo 0
    - project_id: int | None, FK hacia project.id
    """
    # TODO: definir los 5 campos
    pass


# ── Tarea 2 — Engine ──────────────────────────────────────────────────────────

def setup_engine():
    """Crea el engine SQLite en :memory: y las tablas."""
    # TODO: create_engine("sqlite:///:memory:", echo=False)
    # TODO: SQLModel.metadata.create_all(engine)
    # TODO: return engine
    raise NotImplementedError


# ── Tarea 3 — Create ──────────────────────────────────────────────────────────

def create_project(session: Session, name: str, client: str, budget: float) -> Project:
    """Crea un proyecto, lo persiste y retorna el objeto con id."""
    # TODO: construir Project, add, commit, refresh, return
    raise NotImplementedError


# ── Tarea 4 — List ────────────────────────────────────────────────────────────

def list_projects(session: Session) -> list[Project]:
    """Lista proyectos activos (is_active=True) ordenados por nombre asc."""
    # TODO: select(Project).where(...).order_by(...)
    raise NotImplementedError


# ── Tarea 5 — Update ──────────────────────────────────────────────────────────

def update_budget(session: Session, project_id: int, new_budget: float) -> Project | None:
    """Actualiza el presupuesto. Retorna None si no existe."""
    # TODO: session.get, setattr, add, commit, refresh
    raise NotImplementedError


# ── Tarea 6 — Soft delete ─────────────────────────────────────────────────────

def soft_delete(session: Session, project_id: int) -> bool:
    """Marca is_active=False. Retorna True si existía, False si no."""
    # TODO: get, set is_active=False, commit
    raise NotImplementedError


# ── Runner ────────────────────────────────────────────────────────────────────

def main() -> None:
    try:
        engine = setup_engine()
    except NotImplementedError:
        print("Tarea 2 no implementada aún")
        return

    with Session(engine) as session:
        print("=== Tarea 3: crear proyectos ===")
        try:
            p1 = create_project(session, "Spot Canal 9", "Canal 9", 5000.0)
            p2 = create_project(session, "Reel 2025", "Studio BC", 12000.0)
            p3 = create_project(session, "Animación Logo", "Canal 7", 3000.0)
            print(f"  Creados: {p1.id}, {p2.id}, {p3.id}")
        except NotImplementedError:
            print("  Tarea 3 no implementada aún")
            return

        print("\n=== Tarea 4: listar activos ===")
        try:
            projects = list_projects(session)
            for p in projects:
                print(f"  [{p.id}] {p.name} — ${p.budget:.2f}")
        except NotImplementedError:
            print("  Tarea 4 no implementada aún")

        print("\n=== Tarea 5: actualizar presupuesto ===")
        try:
            updated = update_budget(session, p1.id, 7500.0)
            print(f"  {updated.name}: ${updated.budget:.2f}")
        except NotImplementedError:
            print("  Tarea 5 no implementada aún")

        print("\n=== Tarea 6: soft delete ===")
        try:
            deleted = soft_delete(session, p3.id)
            active = list_projects(session)
            print(f"  Deleted={deleted}, activos restantes={len(active)}")
        except NotImplementedError:
            print("  Tarea 6 no implementada aún")


if __name__ == "__main__":
    main()
