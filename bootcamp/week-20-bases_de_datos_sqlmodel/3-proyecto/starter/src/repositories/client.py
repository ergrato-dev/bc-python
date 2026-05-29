"""Repositorio de clientes."""
from __future__ import annotations

from sqlmodel import Session, select
from .base import BaseRepository
from ..models import Client


class ClientRepository(BaseRepository[Client]):
    def __init__(self) -> None:
        super().__init__(Client)

    def find_by_email(self, session: Session, email: str) -> Client | None:
        # TODO
        raise NotImplementedError


client_repo = ClientRepository()
