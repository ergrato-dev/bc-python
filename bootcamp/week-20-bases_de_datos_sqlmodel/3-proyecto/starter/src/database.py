"""Engine y gestión de sesiones."""
from __future__ import annotations

from collections.abc import Generator
from sqlmodel import SQLModel, Session, create_engine

DATABASE_URL = "sqlite:///studio_catalog.db"

engine = create_engine(DATABASE_URL, echo=False)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
