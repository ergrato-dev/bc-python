"""
Ejercicio 02: Pipeline Lineal con Stage Protocol — SOLUCIÓN
===========================================================
"""
from __future__ import annotations

import os
import tempfile
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
    """Lee el archivo y agrega su tamaño al contexto."""
    name = "ingest"

    def process(self, data: dict[str, object]) -> StageResult:
        path = Path(str(data.get("path", "")))
        if not path.exists():
            return StageResult(success=False, data=data, error=f"Archivo no encontrado: {path}")
        size = path.stat().st_size
        return StageResult(
            success=True,
            data={**data, "size_bytes": size, "stem": path.stem, "suffix": path.suffix.lower()},
        )


class ValidateStage:
    """Verifica que la extensión sea .mp4 o .mov y el tamaño > 0."""
    name = "validate"

    ALLOWED = {".mp4", ".mov", ".mxf"}

    def process(self, data: dict[str, object]) -> StageResult:
        suffix = str(data.get("suffix", ""))
        size = int(str(data.get("size_bytes", 0)))
        if suffix not in self.ALLOWED:
            return StageResult(
                success=False, data=data,
                error=f"Extensión no permitida: {suffix}. Permitidas: {self.ALLOWED}",
            )
        if size == 0:
            return StageResult(success=False, data=data, error="Archivo vacío")
        return StageResult(success=True, data={**data, "validated": True})


class ExportStage:
    """Simula el export: agrega "exported": True al contexto."""
    name = "export"

    def process(self, data: dict[str, object]) -> StageResult:
        return StageResult(success=True, data={**data, "exported": True})


class Pipeline:
    def __init__(self, stages: list[Stage]) -> None:
        self._stages = stages

    def run(self, initial_data: dict[str, object]) -> StageResult:
        data = initial_data
        for stage in self._stages:
            result = stage.process(data)
            if not result.success:
                return result
            data = result.data
        return StageResult(success=True, data=data)


if __name__ == "__main__":
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
        f.write(b"fake video content")
        tmp_path = f.name

    pipeline = Pipeline([IngestStage(), ValidateStage(), ExportStage()])

    print("=== Archivo válido ===")
    result = pipeline.run({"path": tmp_path})
    assert result.success, f"Debería ser exitoso: {result.error}"
    assert result.data.get("exported") is True
    print("OK:", result.data)

    print("\n=== Archivo inexistente ===")
    result2 = pipeline.run({"path": "/no/existe.mp4"})
    assert not result2.success
    print("Fallo esperado:", result2.error)

    print("\n=== Extensión inválida ===")
    txt_path = tmp_path.replace(".mp4", ".txt")
    Path(txt_path).write_bytes(b"not a video")
    result3 = pipeline.run({"path": txt_path})
    assert not result3.success
    print("Fallo esperado:", result3.error)

    os.unlink(tmp_path)
    os.unlink(txt_path)
    print("\nOK — Ejercicio 02 completado")
