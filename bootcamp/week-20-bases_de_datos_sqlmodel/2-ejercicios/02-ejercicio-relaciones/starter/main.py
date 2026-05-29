"""
Ejercicio 02 — Relaciones
==========================
Implementa relaciones one-to-many (Project → Asset) y
many-to-many (Asset ↔ Tag) con SQLModel Relationship.

Tareas:
  1. [models]              Definir Project, Asset, Tag y AssetTagLink con Relationship
  2. [create_with_assets]  Crear un proyecto con sus assets en una sola sesión
  3. [add_tags]            Asociar tags a un asset
  4. [assets_by_tag]       Listar assets que tengan un tag específico
  5. [project_summary]     Dict con nombre del proyecto y lista de assets + tags

Ejecutar: python main.py
"""
from __future__ import annotations

from sqlmodel import SQLModel, Field, Relationship, Session, create_engine, select


# ── Tarea 1 — Modelos con Relationship ────────────────────────────────────────

class AssetTagLink(SQLModel, table=True):
    """Tabla de asociación Asset ↔ Tag."""
    # TODO: asset_id (FK asset.id, PK), tag_id (FK tag.id, PK)
    pass


class Tag(SQLModel, table=True):
    # TODO: id, name (unique, indexed), assets Relationship
    pass


class Project(SQLModel, table=True):
    # TODO: id, name, client
    # TODO: assets Relationship(back_populates="project")
    pass


class Asset(SQLModel, table=True):
    # TODO: id, name, type, size_mb
    # TODO: project_id FK
    # TODO: project Relationship(back_populates="assets")
    # TODO: tags Relationship(link_model=AssetTagLink, back_populates="assets")
    pass


# ── Tarea 2 — Crear proyecto con assets ───────────────────────────────────────

def create_project_with_assets(
    session: Session,
    project_name: str,
    client: str,
    asset_names: list[str],
) -> Project:
    """Crea un proyecto y sus assets en una sola transacción."""
    # TODO: crear Project, crear Assets con project_id, commit
    raise NotImplementedError


# ── Tarea 3 — Asociar tags ────────────────────────────────────────────────────

def add_tags_to_asset(session: Session, asset_id: int, tag_names: list[str]) -> Asset:
    """
    Asocia tags a un asset. Crea el Tag si no existe.
    Retorna el asset actualizado.
    """
    # TODO: get asset
    # TODO: para cada tag_name: buscar o crear Tag
    # TODO: asset.tags = [...], commit, refresh
    raise NotImplementedError


# ── Tarea 4 — Assets por tag ──────────────────────────────────────────────────

def assets_by_tag(session: Session, tag_name: str) -> list[Asset]:
    """Lista todos los assets que tienen el tag dado."""
    # TODO: join Asset → AssetTagLink → Tag, filtrar por Tag.name
    raise NotImplementedError


# ── Tarea 5 — Resumen de proyecto ─────────────────────────────────────────────

def project_summary(session: Session, project_id: int) -> dict:
    """
    Retorna dict con:
    {
      "name": str,
      "client": str,
      "assets": [{"name": str, "tags": [str]}]
    }
    """
    # TODO: get project, navegar relaciones, construir dict
    raise NotImplementedError


# ── Runner ────────────────────────────────────────────────────────────────────

def main() -> None:
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        print("=== Tarea 2: proyecto con assets ===")
        try:
            project = create_project_with_assets(
                session, "Spot Canal 9", "Canal 9",
                ["intro.mp4", "main.mp4", "outro.mp4", "jingle.mp3"]
            )
            session.refresh(project)
            print(f"  Proyecto: {project.name}, assets: {len(project.assets)}")
        except NotImplementedError:
            print("  Tarea 2 no implementada aún"); return

        print("\n=== Tarea 3: agregar tags ===")
        try:
            asset = project.assets[0]
            add_tags_to_asset(session, asset.id, ["hd", "4k", "color-graded"])
            session.refresh(asset)
            print(f"  {asset.name}: tags={[t.name for t in asset.tags]}")
        except NotImplementedError:
            print("  Tarea 3 no implementada aún")

        print("\n=== Tarea 4: assets por tag ===")
        try:
            hd_assets = assets_by_tag(session, "hd")
            print(f"  Assets con tag 'hd': {[a.name for a in hd_assets]}")
        except NotImplementedError:
            print("  Tarea 4 no implementada aún")

        print("\n=== Tarea 5: project summary ===")
        try:
            summary = project_summary(session, project.id)
            print(f"  {summary['name']} ({summary['client']})")
            for a in summary["assets"]:
                print(f"    - {a['name']}: {a['tags']}")
        except NotImplementedError:
            print("  Tarea 5 no implementada aún")


if __name__ == "__main__":
    main()
