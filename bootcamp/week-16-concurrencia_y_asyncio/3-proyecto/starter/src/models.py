"""
models.py — Dataclasses del pipeline de assets.
TODO: implementar PipelineReport.summary y completar AssetResult.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


@dataclass
class AssetManifest:
    project_id: str
    assets: list[dict[str, str]]   # cada item: {name, url, type}


@dataclass
class AssetResult:
    name: str
    # TODO: añadir status con Literal["ok", "failed"], sin valor por defecto
    # status: Literal["ok", "failed"]
    size_bytes: int = 0
    thumbnail_path: str | None = None
    error: str | None = None


@dataclass
class PipelineReport:
    project_id: str
    started_at: str
    finished_at: str
    results: list[AssetResult] = field(default_factory=list)

    @property
    def summary(self) -> dict[str, int]:
        # TODO: retornar {"ok": N, "failed": M} contando por status en self.results
        return {}
