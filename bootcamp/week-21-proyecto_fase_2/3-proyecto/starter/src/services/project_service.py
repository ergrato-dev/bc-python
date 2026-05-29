"""Servicio de proyectos — lógica de negocio."""
from __future__ import annotations

from sqlmodel import Session
from ..models import Project
from ..repositories.project import project_repo
from ..repositories.client import client_repo
from ..exceptions import NotFoundError, DomainValidationError


class ProjectService:
    def create(
        self,
        session: Session,
        name: str,
        client_id: int,
        budget: float,
    ) -> Project:
        """Valida que el cliente exista antes de crear el proyecto."""
        if client_repo.get(session, client_id) is None:
            raise NotFoundError("Client", client_id)
        if budget < 0:
            raise DomainValidationError("El presupuesto no puede ser negativo")
        return project_repo.create(session, Project(
            name=name, client_id=client_id, budget=budget
        ))

    def list_active(
        self, session: Session, client_id: int | None = None
    ) -> list[Project]:
        # TODO: project_repo.list_active(session, client_id)
        raise NotImplementedError

    def update_budget(
        self, session: Session, project_id: int, new_budget: float
    ) -> Project:
        project = project_repo.get(session, project_id)
        if project is None:
            raise NotFoundError("Project", project_id)
        project.budget = new_budget
        session.add(project)
        session.commit()
        session.refresh(project)
        return project

    def deactivate(self, session: Session, project_id: int) -> Project:
        project = project_repo.get(session, project_id)
        if project is None:
            raise NotFoundError("Project", project_id)
        project.is_active = False
        session.add(project)
        session.commit()
        session.refresh(project)
        return project

    def kpis(self, session: Session) -> dict:
        # TODO: project_repo.kpis(session)
        raise NotImplementedError


project_service = ProjectService()
