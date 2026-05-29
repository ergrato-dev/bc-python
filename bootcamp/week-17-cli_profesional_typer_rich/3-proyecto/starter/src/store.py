"""store.py — Estado en memoria compartido entre comandos."""
from __future__ import annotations
from .models import Asset, Project

# Datos iniciales de demostración
_PROJECTS: dict[str, Project] = {
    "reel-2025": Project("reel-2025", "Estudio Norte", 8000.0),
    "spot-bc-01": Project("spot-bc-01", "BC Media", 2500.0),
}

_ASSETS: list[Asset] = [
    Asset("intro.mp4",   "video", "reel-2025",  "128 MB"),
    Asset("logo.png",    "image", "reel-2025",  "2.4 MB"),
    Asset("credits.mp4", "video", "reel-2025",  "42 MB"),
    Asset("jingle.wav",  "audio", "spot-bc-01", "6 MB"),
]


def get_projects() -> list[Project]:
    return list(_PROJECTS.values())

def get_project(project_id: str) -> Project | None:
    return _PROJECTS.get(project_id)

def add_project(project: Project) -> None:
    _PROJECTS[project.id] = project

def get_assets(project_id: str | None = None) -> list[Asset]:
    if project_id:
        return [a for a in _ASSETS if a.project_id == project_id]
    return list(_ASSETS)

def add_asset(asset: Asset) -> None:
    _ASSETS.append(asset)

def remove_asset(name: str, project_id: str) -> bool:
    """Returns True if removed, False if not found."""
    for i, a in enumerate(_ASSETS):
        if a.name == name and a.project_id == project_id:
            _ASSETS.pop(i)
            return True
    return False
