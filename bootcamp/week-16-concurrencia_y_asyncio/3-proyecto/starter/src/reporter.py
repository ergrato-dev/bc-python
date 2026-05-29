"""
reporter.py — Escritura async del reporte final con aiofiles.
TODO: implementar write_report.
"""

from __future__ import annotations

import dataclasses
import json
import os

import aiofiles

from .models import PipelineReport


async def write_report(report: PipelineReport, output_path: str) -> None:
    """
    TODO: serializar PipelineReport a JSON y escribirlo de forma async.

    1. Usar dataclasses.asdict(report) para convertir a dict
    2. Serializar con json.dumps(..., indent=2)
    3. Crear el directorio padre si no existe (os.makedirs)
    4. Abrir el archivo con aiofiles.open(output_path, "w", encoding="utf-8")
    5. Escribir el JSON con await f.write(...)
    """
    # TODO: implementar
    raise NotImplementedError
