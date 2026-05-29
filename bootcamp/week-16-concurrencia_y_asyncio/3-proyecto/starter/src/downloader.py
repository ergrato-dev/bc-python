"""
downloader.py — Descarga async de assets con semáforo y retry.
TODO: implementar download_asset completo.
"""

from __future__ import annotations

import asyncio
import random

from .models import AssetResult

MAX_CONCURRENT = 4
MAX_RETRIES = 2
TIMEOUT_SECS = 5.0


async def _fetch_asset(name: str, url: str) -> bytes:
    """Simula descarga de un asset. Puede fallar con ~25% de probabilidad."""
    # Simula latencia variable (0.5 – 2.0s)
    delay = 0.5 + random.random() * 1.5
    await asyncio.sleep(delay)

    # Simula fallo de red
    if name == "broken.mp4" or random.random() < 0.25:
        raise ConnectionError(f"network error fetching {url}")

    # Retorna datos ficticios (en producción sería response.content)
    return bytes(random.randint(100, 999) for _ in range(64))


async def download_asset(
    sem: asyncio.Semaphore,
    name: str,
    url: str,
) -> AssetResult:
    """
    TODO: implementar con semáforo, retry y timeout.

    Estructura esperada:
    1. async with sem:  (máx MAX_CONCURRENT descargas simultáneas)
    2. Bucle de retry (hasta MAX_RETRIES):
       a. async with asyncio.timeout(TIMEOUT_SECS):
       b. Llamar a _fetch_asset(name, url)
       c. Si éxito: retornar AssetResult(name=name, status="ok", size_bytes=len(data))
       d. Si falla: esperar base_delay * 2^attempt antes de reintentar
    3. Si todos los intentos fallan: retornar AssetResult(name=name, status="failed", error=str(e))
    """
    # TODO: implementar
    raise NotImplementedError
