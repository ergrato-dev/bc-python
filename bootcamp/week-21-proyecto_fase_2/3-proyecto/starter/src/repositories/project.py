"""Repositorio de proyectos."""
from __future__ import annotations
from sqlmodel import Session, select
from sqlalchemy import func
from .base import BaseRepository
from ..models import Project, Client


class ProjectRepository(BaseRepository[Project]):
    def __init__(self) -> None:
        super().__init__(Project)

    def list_active(self, session: Session, client_id: int | None = None) -> list[Project]:
        # TODO: filtrar is_active=True, opcionalmente por client_id
        raise NotImplementedError

    def list_by_client(self, session: Session, client_id: int) -> list[Project]:
        # TODO
        raise NotImplementedError

    def kpis(self, session: Session) -> dict:
        # TODO: total, active, total_budget, avg_budget, max_budget
        raise NotImplementedError

    def asset_count_per_project(self, session: Session) -> list[tuple[str, int]]:
        # TODO: JOIN Asset, GROUP BY Project
        raise NotImplementedError


project_repo = ProjectRepository()
