"""Repositorio base genérico."""
from __future__ import annotations
from typing import Generic, TypeVar
from sqlmodel import SQLModel, Session, select

ModelT = TypeVar("ModelT", bound=SQLModel)


class BaseRepository(Generic[ModelT]):
    def __init__(self, model: type[ModelT]) -> None:
        self.model = model

    def get(self, session: Session, id: int) -> ModelT | None:
        return session.get(self.model, id)

    def list(self, session: Session) -> list[ModelT]:
        return session.exec(select(self.model)).all()

    def create(self, session: Session, obj: ModelT) -> ModelT:
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj

    def delete(self, session: Session, id: int) -> bool:
        obj = self.get(session, id)
        if obj is None:
            return False
        session.delete(obj)
        session.commit()
        return True
