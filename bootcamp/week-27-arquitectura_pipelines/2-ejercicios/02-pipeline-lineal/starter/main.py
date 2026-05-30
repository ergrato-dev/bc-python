"""
Ejercicio 02: Pipeline Lineal con Stage Protocol
=================================================
Implementa tres etapas (Ingest, Validate, Export) que se encadenan
en un Pipeline usando el protocolo Stage.

Ejecutar:
    python main.py
"""
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
    """Lee el archivo y agrega su tamaño al contexto."""
    name = "ingest"

    def process(self, data: dict[str, object]) -> StageResult:
        # TODO: verificar que data["path"] existe como Path
        # TODO: agregar data["size_bytes"] y data["stem"]
        # TODO: devolver StageResult(success=False, ...) si no existe
        raise NotImplementedError


class ValidateStage:
    """Verifica que la extensión sea .mp4 o .mov y el tamaño > 0."""
    name = "validate"

    ALLOWED = {".mp4", ".mov", ".mxf"}

    def process(self, data: dict[str, object]) -> StageResult:
        # TODO: verificar extensión en ALLOWED y size_bytes > 0
        raise NotImplementedError


class ExportStage:
    """Simula el export: agrega "exported": True al contexto."""
    name = "export"

    def process(self, data: dict[str, object]) -> StageResult:
        # TODO: return StageResult(success=True, data={**data, "exported": True})
        raise NotImplementedError


class Pipeline:
    def __init__(self, stages: list[Stage]) -> None:
        self._stages = stages

    def run(self, initial_data: dict[str, object]) -> StageResult:
        # TODO: iterar etapas, detener ante primer fallo, pasar data entre etapas
        raise NotImplementedError


if __name__ == "__main__":
    import tempfile, os

    # Crear archivo de prueba
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
