"""Repositorio base genérico con CRUD."""
from __future__ import annotations

from typing import Generic, TypeVar
from sqlmodel import SQLModel, Session, select

ModelT = TypeVar("ModelT", bound=SQLModel)


class BaseRepository(Generic[ModelT]):
    def __init__(self, model: type[ModelT]) -> None:
        self.model = model

    def get(self, session: Session, id: int) -> ModelT | None:
        # TODO: session.get
        raise NotImplementedError

    def list(self, session: Session) -> list[ModelT]:
        # TODO: session.exec(select(self.model)).all()
        raise NotImplementedError

    def create(self, session: Session, obj: ModelT) -> ModelT:
        # TODO: add, commit, refresh
        raise NotImplementedError

    def delete(self, session: Session, id: int) -> bool:
        # TODO: get, delete, commit
        raise NotImplementedError
