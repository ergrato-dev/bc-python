from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


@dataclass
class StageResult:
    success: bool
    data: dict[str, object]
    error: str | None = None


class Stage(Protocol):
    name: str

    def process(self, data: dict[str, object]) -> StageResult:
        ...


class IngestStage:
    name = "ingest"

    def process(self, data: dict[str, object]) -> StageResult:
        path = Path(str(data.get("path", "")))
        if not path.exists():
            return StageResult(success=False, data=data, error=f"Archivo no encontrado: {path}")
        size = path.stat().st_size
        if size == 0:
            return StageResult(success=False, data=data, error="Archivo vacío")
        return StageResult(
            success=True,
            data={**data, "size_bytes": size, "stem": path.stem, "suffix": path.suffix.lower()},
        )


class ValidateStage:
    name = "validate"
    ALLOWED_EXT = {".mp4", ".mov", ".mxf", ".mp3", ".wav", ".flac", ".jpg", ".png"}

    def process(self, data: dict[str, object]) -> StageResult:
        suffix = str(data.get("suffix", ""))
        if suffix not in self.ALLOWED_EXT:
            return StageResult(
                success=False, data=data,
                error=f"Extensión no permitida: {suffix}. Permitidas: {self.ALLOWED_EXT}",
            )
        return StageResult(success=True, data={**data, "validated": True})


class ProcessStage:
    name = "process"

    def process(self, data: dict[str, object]) -> StageResult:
        # TODO: llamar al procesador apropiado según suffix (video/audio/imagen)
        # Stub: simular procesamiento exitoso
        return StageResult(
            success=True,
            data={**data, "processed": True, "output_path": str(data.get("path", "")) + ".out"},
        )


class ExportStage:
    name = "export"

    def process(self, data: dict[str, object]) -> StageResult:
        # TODO: subir a S3 y/o Drive según configuración
        # Stub: simular export exitoso
        return StageResult(
            success=True,
            data={**data, "exported": True},
        )
