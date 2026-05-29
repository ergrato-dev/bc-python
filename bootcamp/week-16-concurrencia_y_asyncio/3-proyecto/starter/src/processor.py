"""
processor.py — Generación de thumbnails CPU-bound con ProcessPoolExecutor.
TODO: implementar process_assets_cpu.
"""

from __future__ import annotations

import asyncio
import hashlib
from concurrent.futures import ProcessPoolExecutor

from .models import AssetResult


def generate_thumbnail_sync(image_data: bytes, name: str) -> tuple[str, bytes]:
    """
    Función síncrona CPU-bound — adecuada para ProcessPoolExecutor.
    Simula generación de thumbnail con trabajo de CPU.
    """
    # Simula trabajo CPU (en producción: Pillow, ffmpeg, etc.)
    result = hashlib.sha256(image_data).digest()
    for _ in range(200_000):
        result = hashlib.sha256(result).digest()

    thumbnail_path = f"output/thumbs/{name.rsplit('.', 1)[0]}_thumb.jpg"
    return thumbnail_path, result[:64]   # thumbnail ficticio


async def process_assets_cpu(
    results: list[AssetResult],
    asset_types: dict[str, str],
) -> list[AssetResult]:
    """
    TODO: procesar assets de tipo "image" con ProcessPoolExecutor.

    1. Filtrar results donde status="ok" y asset_types[name]="image"
    2. Para cada uno, generar datos ficticios (os.urandom(512))
    3. Usar loop.run_in_executor(ProcessPoolExecutor(), generate_thumbnail_sync, data, name)
    4. Actualizar result.thumbnail_path con el path retornado
    5. Retornar la lista completa de results (modificados in-place)
    """
    # TODO: implementar
    return results
