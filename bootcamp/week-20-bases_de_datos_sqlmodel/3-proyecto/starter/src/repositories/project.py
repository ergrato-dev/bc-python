"""Repositorio de proyectos con queries específicas."""
from __future__ import annotations

from sqlmodel import Session, select
from sqlalchemy import func
from .base import BaseRepository
from ..models import Project, Asset


class ProjectRepository(BaseRepository[Project]):
    def __init__(self) -> None:
        super().__init__(Project)

    def list_active(self, session: Session) -> list[Project]:
        # TODO: filtrar is_active=True, ordenar por name
        raise NotImplementedError

    def list_by_client(self, session: Session, client_id: int) -> list[Project]:
        # TODO: where client_id == client_id
        raise NotImplementedError

    def total_budget(self, session: Session) -> float:
        # TODO: func.sum(Project.budget)
        raise NotImplementedError

    def asset_count_per_project(self, session: Session) -> list[tuple[str, int]]:
        # TODO: JOIN Asset, GROUP BY Project.id, ORDER BY count DESC
        raise NotImplementedError

    def kpis(self, session: Session) -> dict:
        """total, active, total_budget, avg_budget, max_budget"""
        # TODO
        raise NotImplementedError


project_repo = ProjectRepository()
