"""
Ejercicio 03 — Queries Avanzadas
==================================
Practica select(), where(), join(), group_by(), aggregaciones y paginación.

Los modelos ya están definidos — solo implementar las funciones de query.

Tareas:
  1. [search_projects]         Búsqueda por nombre (ILIKE) y filtro por cliente
  2. [assets_larger_than]      Assets cuyo size_mb supera un umbral
  3. [projects_with_budget]    Proyectos con presupuesto > promedio del total
  4. [asset_count_by_project]  GROUP BY proyecto — (nombre, cantidad de assets)
  5. [paginate_projects]       Paginación: page + page_size
  6. [project_kpis]            KPIs: total proyectos, presupuesto total, promedio

Ejecutar: python main.py
"""
from __future__ import annotations

from sqlmodel import SQLModel, Field, Session, create_engine, select
from sqlalchemy import func

# ── Modelos (ya definidos) ─────────────────────────────────────────────────────

class Project(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    client: str
    budget: float = Field(default=0.0, ge=0)
    is_active: bool = Field(default=True)


class Asset(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    type: str = Field(default="video")
    size_mb: float = Field(default=0.0, ge=0)
    project_id: int | None = Field(default=None, foreign_key="project.id")


# ── Tarea 1 — Búsqueda ────────────────────────────────────────────────────────

def search_projects(
    session: Session,
    name_contains: str | None = None,
    client: str | None = None,
) -> list[Project]:
    """
    Filtra proyectos activos por nombre (ilike) y/o cliente (exacto).
    Si ambos son None, retorna todos los activos.
    """
    # TODO: construir stmt dinámicamente — añadir .where() solo si el parámetro no es None
    raise NotImplementedError


# ── Tarea 2 — Filtro por tamaño ───────────────────────────────────────────────

def assets_larger_than(
    session: Session,
    min_size_mb: float,
    asset_type: str | None = None,
) -> list[Asset]:
    """Lista assets con size_mb > min_size_mb, opcionalmente filtrados por tipo."""
    raise NotImplementedError


# ── Tarea 3 — Subquery ────────────────────────────────────────────────────────

def projects_above_avg_budget(session: Session) -> list[Project]:
    """Proyectos activos cuyo budget supera el promedio de todos los proyectos."""
    # TODO: avg_stmt = select(func.avg(Project.budget)).scalar_subquery()
    # TODO: .where(Project.budget > avg_stmt)
    raise NotImplementedError


# ── Tarea 4 — GROUP BY ────────────────────────────────────────────────────────

def asset_count_by_project(session: Session) -> list[tuple[str, int]]:
    """
    Retorna lista de (project_name, asset_count) ordenada por asset_count desc.
    Solo proyectos activos, incluye proyectos sin assets (count=0).
    """
    # TODO: select(Project.name, func.count(Asset.id).label("n"))
    # TODO: .join(Asset, isouter=True).group_by(Project.id)
    raise NotImplementedError


# ── Tarea 5 — Paginación ──────────────────────────────────────────────────────

def paginate_projects(
    session: Session,
    page: int = 0,
    page_size: int = 5,
) -> tuple[list[Project], int]:
    """
    Retorna (proyectos_de_la_página, total_proyectos).
    Ordenados por nombre asc.
    """
    # TODO: total = session.exec(select(func.count(Project.id))).one()
    # TODO: items = ... .offset(page * page_size).limit(page_size)
    raise NotImplementedError


# ── Tarea 6 — KPIs ────────────────────────────────────────────────────────────

def project_kpis(session: Session) -> dict:
    """
    Retorna dict:
    {
      "total": int,
      "active": int,
      "total_budget": float,
      "avg_budget": float,
      "max_budget": float,
    }
    """
    raise NotImplementedError


# ── Seed data ─────────────────────────────────────────────────────────────────

def seed(session: Session) -> None:
    projects = [
        Project(name="Spot Canal 9", client="Canal 9", budget=5000),
        Project(name="Reel 2025", client="Studio BC", budget=12000),
        Project(name="Animación Logo", client="Canal 7", budget=3000),
        Project(name="Documental Río", client="Canal 9", budget=25000),
        Project(name="Jingle Navidad", client="Agencia Norte", budget=8000),
        Project(name="Campaña Social", client="ONG Verde", budget=1500, is_active=False),
    ]
    for p in projects:
        session.add(p)
    session.flush()

    assets_data = [
        (projects[0].id, "intro.mp4", "video", 450.0),
        (projects[0].id, "main.mp4", "video", 2100.0),
        (projects[1].id, "reel-final.mp4", "video", 800.0),
        (projects[1].id, "bts.mp4", "video", 3200.0),
        (projects[3].id, "documental.mp4", "video", 15000.0),
    ]
    for pid, name, atype, size in assets_data:
        session.add(Asset(name=name, type=atype, size_mb=size, project_id=pid))
    session.commit()


# ── Runner ────────────────────────────────────────────────────────────────────

def main() -> None:
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        seed(session)

        print("=== Tarea 1: search ===")
        try:
            r = search_projects(session, name_contains="spot")
            print(f"  'spot': {[p.name for p in r]}")
            r2 = search_projects(session, client="Canal 9")
            print(f"  Canal 9: {[p.name for p in r2]}")
        except NotImplementedError:
            print("  No implementado aún")

        print("\n=== Tarea 2: assets > 500 MB ===")
        try:
            big = assets_larger_than(session, 500)
            print(f"  {[(a.name, a.size_mb) for a in big]}")
        except NotImplementedError:
            print("  No implementado aún")

        print("\n=== Tarea 3: above avg budget ===")
        try:
            above = projects_above_avg_budget(session)
            print(f"  {[p.name for p in above]}")
        except NotImplementedError:
            print("  No implementado aún")

        print("\n=== Tarea 4: asset count by project ===")
        try:
            rows = asset_count_by_project(session)
            for name, count in rows:
                print(f"  {name}: {count} assets")
        except NotImplementedError:
            print("  No implementado aún")

        print("\n=== Tarea 5: paginación ===")
        try:
            page, total = paginate_projects(session, page=0, page_size=3)
            print(f"  Página 0 ({len(page)}/{total}): {[p.name for p in page]}")
        except NotImplementedError:
            print("  No implementado aún")

        print("\n=== Tarea 6: KPIs ===")
        try:
            kpis = project_kpis(session)
            for k, v in kpis.items():
                print(f"  {k}: {v}")
        except NotImplementedError:
            print("  No implementado aún")


if __name__ == "__main__":
    main()
