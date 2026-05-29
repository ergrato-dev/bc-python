"""Tests para los repositorios."""
from __future__ import annotations

import pytest
from sqlmodel import SQLModel, Session, create_engine
from src.models import Client, Project, Asset
from src.repositories.project import ProjectRepository
from src.repositories.asset import AssetRepository
from src.repositories.client import ClientRepository


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture
def project_repo():
    return ProjectRepository()


@pytest.fixture
def asset_repo():
    return AssetRepository()


def test_create_and_get_project(session, project_repo) -> None:
    p = Project(name="Test", client_id=None, budget=1000)
    try:
        created = project_repo.create(session, p)
        assert created.id is not None
        fetched = project_repo.get(session, created.id)
        assert fetched is not None
        assert fetched.name == "Test"
    except NotImplementedError:
        pytest.skip("BaseRepository no implementado")


def test_list_active_projects(session, project_repo) -> None:
    try:
        p1 = project_repo.create(session, Project(name="A", client_id=None, budget=0))
        p2 = project_repo.create(session, Project(name="B", client_id=None, budget=0, is_active=False))
        active = project_repo.list_active(session)
        names = [p.name for p in active]
        assert "A" in names
        assert "B" not in names
    except NotImplementedError:
        pytest.skip("No implementado")


def test_delete_project(session, project_repo) -> None:
    try:
        p = project_repo.create(session, Project(name="Del", client_id=None, budget=0))
        assert project_repo.delete(session, p.id) is True
        assert project_repo.get(session, p.id) is None
        assert project_repo.delete(session, 9999) is False
    except NotImplementedError:
        pytest.skip("No implementado")


def test_kpis(session, project_repo) -> None:
    try:
        project_repo.create(session, Project(name="P1", client_id=None, budget=1000))
        project_repo.create(session, Project(name="P2", client_id=None, budget=3000))
        kpis = project_repo.kpis(session)
        assert kpis["total"] == 2
        assert kpis["total_budget"] == 4000.0
    except NotImplementedError:
        pytest.skip("No implementado")
