"""Repositorio de clientes."""
from __future__ import annotations
from sqlmodel import Session, select
from .base import BaseRepository
from ..models import Client


class ClientRepository(BaseRepository[Client]):
    def __init__(self) -> None:
        super().__init__(Client)

    def find_by_email(self, session: Session, email: str) -> Client | None:
        # TODO: select(Client).where(Client.email == email)
        raise NotImplementedError

    def list_ordered(self, session: Session) -> list[Client]:
        # TODO: order_by(Client.name)
        raise NotImplementedError


client_repo = ClientRepository()
