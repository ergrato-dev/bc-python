from __future__ import annotations

from pathlib import Path

from .base import Stage, StageResult

VIDEO_EXTENSIONS = {".mp4", ".mov", ".mxf", ".avi", ".mkv"}
AUDIO_EXTENSIONS = {".mp3", ".wav", ".flac", ".aac"}
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tif", ".tiff"}
ALL_MEDIA = VIDEO_EXTENSIONS | AUDIO_EXTENSIONS | IMAGE_EXTENSIONS


class IngestStage:
    name = "ingest"

    def process(self, data: dict[str, object]) -> StageResult:
        path = Path(str(data.get("path", "")))
        if not path.exists():
            return StageResult(success=False, data=data, error=f"Archivo no encontrado: {path}")
        size = path.stat().st_size
        if size == 0:
            return StageResult(success=False, data=data, error="Archivo vacío")

        suffix = path.suffix.lower()
        if suffix in VIDEO_EXTENSIONS:
            media_type = "video"
        elif suffix in AUDIO_EXTENSIONS:
            media_type = "audio"
        elif suffix in IMAGE_EXTENSIONS:
            media_type = "image"
        else:
            media_type = "other"

        return StageResult(
            success=True,
            data={
                **data,
                "size_bytes": size,
                "stem": path.stem,
                "suffix": suffix,
                "media_type": media_type,
            },
        )
