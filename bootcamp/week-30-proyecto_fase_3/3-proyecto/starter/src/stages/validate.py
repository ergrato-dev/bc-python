from __future__ import annotations

from .base import Stage, StageResult
from .ingest import ALL_MEDIA


class ValidateStage:
    name = "validate"
    MAX_SIZE_BYTES = 20 * 1024 * 1024 * 1024  # 20 GB

    def process(self, data: dict[str, object]) -> StageResult:
        suffix = str(data.get("suffix", ""))
        size = int(str(data.get("size_bytes", 0)))
        media_type = str(data.get("media_type", "other"))

        if suffix not in ALL_MEDIA:
            return StageResult(
                success=False, data=data,
                error=f"Extensión no permitida: {suffix}",
            )
        if size > self.MAX_SIZE_BYTES:
            return StageResult(
                success=False, data=data,
                error=f"Archivo demasiado grande: {size / 1e9:.1f} GB (máx 20 GB)",
            )
        if media_type == "other":
            return StageResult(
                success=False, data=data,
                error="Tipo de media no reconocido",
            )

        return StageResult(success=True, data={**data, "validated": True})
