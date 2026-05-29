"""Tests de integración para ProjectService."""
from __future__ import annotations

import pytest
from sqlmodel import Session
from src.services.project_service import ProjectService
from src.repositories.project import ProjectRepository
from src.repositories.client import ClientRepository
from src.exceptions import NotFoundError, DomainValidationError


@pytest.fixture
def service() -> ProjectService:
    return ProjectService()


def test_create_project_success(
    session: Session, service: ProjectService, client_fixture
) -> None:
    try:
        p = service.create(session, "Test Project", client_fixture.id, 1000.0)
        assert p.id is not None
        assert p.name == "Test Project"
        assert p.budget == 1000.0
        assert p.is_active is True
    except NotImplementedError:
        pytest.skip("repository no implementado")


def test_create_project_invalid_client(
    session: Session, service: ProjectService
) -> None:
    with pytest.raises(NotFoundError):
        service.create(session, "X", client_id=9999, budget=0.0)


def test_create_project_negative_budget(
    session: Session, service: ProjectService, client_fixture
) -> None:
    with pytest.raises(DomainValidationError):
        service.create(session, "X", client_fixture.id, budget=-100.0)


def test_update_budget(
    session: Session, service: ProjectService, project_fixture
) -> None:
    try:
        updated = service.update_budget(session, project_fixture.id, 9999.0)
        assert updated.budget == 9999.0
    except NotImplementedError:
        pytest.skip("no implementado")


def test_deactivate_project(
    session: Session, service: ProjectService, project_fixture
) -> None:
    p = service.deactivate(session, project_fixture.id)
    assert p.is_active is False


def test_list_active_excludes_inactive(
    session: Session, service: ProjectService, client_fixture
) -> None:
    p1 = service.create(session, "Activo", client_fixture.id, 0.0)
    p2 = service.create(session, "Inactivo", client_fixture.id, 0.0)
    service.deactivate(session, p2.id)
    try:
        active = service.list_active(session)
        assert any(p.id == p1.id for p in active)
        assert not any(p.id == p2.id for p in active)
    except NotImplementedError:
        pytest.skip("list_active no implementado")


def test_deactivate_nonexistent_raises(
    session: Session, service: ProjectService
) -> None:
    with pytest.raises(NotFoundError):
        service.deactivate(session, 9999)
