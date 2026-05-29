"""Fixtures compartidas para todos los tests."""
from __future__ import annotations

import pytest
from sqlmodel import SQLModel, Session, create_engine
from src.models import Client, Project, Asset, Tag


@pytest.fixture(name="engine", scope="function")
def engine_fixture():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="session")
def session_fixture(engine):
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client_fixture")
def client_data_fixture(session: Session) -> Client:
    c = Client(name="Canal 9", email="prod@canal9.com", country="AR")
    session.add(c)
    session.commit()
    session.refresh(c)
    return c


@pytest.fixture(name="project_fixture")
def project_data_fixture(session: Session, client_fixture: Client) -> Project:
    p = Project(name="Spot Verano", client_id=client_fixture.id, budget=5000.0)
    session.add(p)
    session.commit()
    session.refresh(p)
    return p
