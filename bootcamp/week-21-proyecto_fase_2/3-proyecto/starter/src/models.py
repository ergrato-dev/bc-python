"""Modelos SQLModel del catálogo de Studio BC."""
from __future__ import annotations

from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship


class AssetTagLink(SQLModel, table=True):
    asset_id: int | None = Field(default=None, foreign_key="asset.id", primary_key=True)
    tag_id: int | None = Field(default=None, foreign_key="tag.id", primary_key=True)


class Tag(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    assets: list["Asset"] = Relationship(back_populates="tags", link_model=AssetTagLink)


class Client(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, index=True)
    email: str = Field(unique=True)
    country: str = Field(default="AR")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    projects: list["Project"] = Relationship(back_populates="client_rel")


class Project(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=150)
    budget: float = Field(default=0.0, ge=0)
    status: str = Field(default="active")
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    client_id: int | None = Field(default=None, foreign_key="client.id")
    client_rel: Client | None = Relationship(back_populates="projects")
    assets: list["Asset"] = Relationship(back_populates="project")


class Asset(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=200)
    type: str = Field(default="video")
    size_mb: float = Field(default=0.0, ge=0)
    storage_path: str | None = Field(default=None)
    project_id: int | None = Field(default=None, foreign_key="project.id")
    project: Project | None = Relationship(back_populates="assets")
    tags: list[Tag] = Relationship(back_populates="assets", link_model=AssetTagLink)
