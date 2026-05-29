"""Repositorio de assets."""
from __future__ import annotations
from sqlmodel import Session, select
from sqlalchemy import func
from .base import BaseRepository
from ..models import Asset, Tag, AssetTagLink


class AssetRepository(BaseRepository[Asset]):
    def __init__(self) -> None:
        super().__init__(Asset)

    def list_by_project(self, session: Session, project_id: int) -> list[Asset]:
        # TODO
        raise NotImplementedError

    def add_tag(self, session: Session, asset_id: int, tag_name: str) -> Asset:
        # TODO: buscar o crear Tag, asociar a asset
        raise NotImplementedError

    def find_by_tag(self, session: Session, tag_name: str) -> list[Asset]:
        # TODO: JOIN AssetTagLink → Tag
        raise NotImplementedError

    def total_size_by_project(self, session: Session, project_id: int) -> float:
        # TODO: func.sum(Asset.size_mb)
        raise NotImplementedError


asset_repo = AssetRepository()
