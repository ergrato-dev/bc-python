"""
Studio BC — Domain Models
Implement all entities using Protocols, dataclasses, and advanced typing.
Run: mypy --strict src/
"""

from __future__ import annotations

from dataclasses import dataclass, field, KW_ONLY
from datetime import date, datetime
from typing import Protocol


# ============================================================
# PROTOCOLS
# Define the structural contracts for Studio BC entities.
# ============================================================

class Nameable(Protocol):
    # TODO: define a 'name' property that returns str
    pass


class Describable(Protocol):
    # TODO: define a 'description' property that returns str
    pass


class Timestamped(Protocol):
    # TODO: define a 'created_at' property that returns datetime
    pass


class Identifiable(Protocol):
    # TODO: define an 'id' property that returns int
    pass


# ============================================================
# ENTITIES
# Implement as dataclasses following the spec in README.md.
# ============================================================

@dataclass(slots=True)
class Client:
    name: str
    email: str
    _: KW_ONLY
    id: int = 0
    # TODO: add phone, active, created_at fields with correct defaults

    def __post_init__(self) -> None:
        # TODO: validate email contains '@' and '.'
        # TODO: normalize email to lowercase and strip whitespace
        pass


@dataclass(slots=True)
class Project:
    name: str
    start_date: date
    end_date: date
    budget: float
    _: KW_ONLY
    id: int = 0
    client_id: int = 0
    # TODO: add description, tags, created_at, slug fields

    def __post_init__(self) -> None:
        # TODO: validate end_date > start_date
        # TODO: validate budget > 0
        # TODO: compute slug from name
        pass


@dataclass(frozen=True, slots=True)
class Phase:
    name: str
    order: int
    _: KW_ONLY
    id: int = 0
    project_id: int = 0
    # TODO: add description, completed fields


@dataclass(slots=True)
class Deliverable:
    name: str
    due_date: date
    _: KW_ONLY
    id: int = 0
    phase_id: int = 0
    # TODO: add description, approved, created_at fields


@dataclass(slots=True)
class Asset:
    name: str
    asset_type: str
    _: KW_ONLY
    id: int = 0
    file_path: str = ""
    # TODO: add size_mb, project_id, metadata, created_at fields

    def __post_init__(self) -> None:
        valid_types = {"video", "image", "audio", "document"}
        if self.asset_type not in valid_types:
            raise ValueError(
                f"invalid asset_type {self.asset_type!r}, must be one of {valid_types}"
            )
