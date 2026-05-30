"""Domain repository interfaces (ports)."""
from __future__ import annotations

from typing import Protocol
from .entities import Job, Asset


class IJobRepository(Protocol):
    """Port — interfaz de persistencia de jobs."""
    # TODO: definir los métodos save, find_by_id, find_all, find_by_status
    # Referencia: ejercicio 03 — IJobRepository Protocol
    ...


class IAssetStore(Protocol):
    """Port — interfaz para subir assets a un storage externo."""
    def upload(self, asset_path: str, asset_id: str, media_type: str) -> str:
        """Sube el asset y devuelve su URL."""
        ...


class ITranscoder(Protocol):
    """Port — interfaz para transcodificar un video."""
    def transcode(self, input_path: str, output_dir: str) -> dict[str, str]:
        """Devuelve {"proxy": path, "web": path, "thumb": path}."""
        ...


class INotifier(Protocol):
    """Port — interfaz para notificar al equipo."""
    def notify(self, project: str, stem: str, url: str) -> None: ...
