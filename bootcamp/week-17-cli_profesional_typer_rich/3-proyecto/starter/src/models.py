"""models.py — Dataclasses del bc-studio-cli."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Literal

type AssetType = Literal["video", "audio", "image"]

@dataclass
class Config:
    verbose: bool = False
    api_url: str = "https://api.studio.bc"

@dataclass
class Asset:
    name: str
    type: AssetType
    project_id: str
    size: str = "—"

@dataclass
class Project:
    id: str
    client: str
    budget: float = 0.0
    assets: list[Asset] = field(default_factory=list)
