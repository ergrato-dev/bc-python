"""Modelos SQLModel del catálogo de Studio BC."""
from __future__ import annotations

from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship


class AssetTagLink(SQLModel, table=True):
    """Tabla de asociación Asset ↔ Tag."""
    # TODO: asset_id (PK, FK asset.id), tag_id (PK, FK tag.id)
    pass


class Tag(SQLModel, table=True):
    # TODO: id, name (unique, index), assets Relationship
    pass


class Client(SQLModel, table=True):
    # TODO: id, name, email, country, created_at
    # TODO: projects Relationship(back_populates="client_rel")
    pass


class Project(SQLModel, table=True):
    # TODO: id, name, budget (>=0), status (default "active"), created_at, is_active
    # TODO: client_id FK → client.id
    # TODO: client_rel Relationship(back_populates="projects")
    # TODO: assets Relationship(back_populates="project")
    pass


class Asset(SQLModel, table=True):
    # TODO: id, name, type (default "video"), size_mb (>=0), storage_path (optional)
    # TODO: project_id FK → project.id
    # TODO: project Relationship(back_populates="assets")
    # TODO: tags Relationship(link_model=AssetTagLink, back_populates="assets")
    pass
