"""Engine y gestión de sesiones."""
from __future__ import annotations

from collections.abc import Generator
from contextlib import contextmanager
from sqlmodel import SQLModel, Session, create_engine
from .config import settings

engine = create_engine(settings.database_url, echo=False)


def create_tables() -> None:
    SQLModel.metadata.create_all(engine)


@contextmanager
def get_session_ctx() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
