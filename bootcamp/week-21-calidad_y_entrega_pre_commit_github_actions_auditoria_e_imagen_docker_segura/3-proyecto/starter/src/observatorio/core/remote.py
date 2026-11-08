"""Bajar medidas por HTTP: un cliente, reintentos con espera y archivos guardados.

Qué: make_client crea el cliente httpx; get_text pide una URL y reintenta los fallos
pasajeros; download valida lo que llega y lo guarda como .txt; download_all baja varias
URLs a la vez con un límite.
Para qué: las medidas de verdad viven en otros servidores. Lo que llega se valida igual
que un archivo, y el resto del Observatorio lo lee como cualquier otro .txt.
Impacto: el núcleo no lee el entorno ni .env: el token llega como un argumento. Una URL
que falla es un FileReport con error, no una excepción que tumbe la descarga entera.
"""

import asyncio
import logging
from collections.abc import Iterable
from importlib.metadata import version
from pathlib import Path, PurePosixPath

import httpx

from observatorio.core.batch import FileReport
from observatorio.core.schemas import parse_measurements
from observatorio.core.storage import DataFileError

logger = logging.getLogger(__name__)

# Respuestas que pueden salir bien si se repite la petición: demasiadas peticiones (429)
# y fallos del servidor o de lo que hay delante de él (5xx). Un 404 no cambiará.
RETRY_STATUSES = frozenset({429, 500, 502, 503, 504})


class FetchError(Exception):
    """Una descarga que no salió bien: el servidor no contestó o contestó con un error."""


def make_client(
    *,
    token: str | None = None,
    timeout: float = 10.0,
    transport: httpx.AsyncBaseTransport | None = None,
) -> httpx.AsyncClient:
    """Un cliente que se presenta como observatorio/<versión> y espera `timeout` segundos."""
    headers = {"User-Agent": f"observatorio/{version('observatorio')}"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return httpx.AsyncClient(
        headers=headers, timeout=timeout, follow_redirects=True, transport=transport
    )


async def get_text(
    client: httpx.AsyncClient, url: str, *, retries: int = 3, backoff: float = 0.5
) -> str:
    """El texto de `url`. Reintenta hasta `retries` veces los fallos de red y RETRY_STATUSES."""
    failure = ""
    for attempt in range(retries + 1):
        if attempt > 0:
            await asyncio.sleep(backoff * 2 ** (attempt - 1))
        try:
            response = await client.get(url)
        except httpx.TransportError as problem:
            # Sin respuesta: no conecta, se agota el plazo, se corta. El mensaje viene del
            # sistema operativo y cambia de una máquina a otra; el nombre de la clase, no.
            failure = f"sin respuesta de {url} ({type(problem).__name__})"
        else:
            if response.status_code not in RETRY_STATUSES:
                if response.is_error:
                    raise FetchError(f"{url} respondió {response.status_code}")
                return response.text
            failure = f"{url} respondió {response.status_code}"
        logger.debug("intento %d de %d: %s", attempt + 1, retries + 1, failure)
    raise FetchError(f"{failure} tras {retries + 1} intentos")


def target_of(url: str, folder: Path) -> Path:
    """Dónde se guarda lo que se baja de `url`: <folder>/<nombre del archivo de la URL>.txt."""
    name = PurePosixPath(httpx.URL(url).path).stem or "datos"
    return folder / f"{name}.txt"


async def download(
    client: httpx.AsyncClient,
    url: str,
    folder: Path,
    *,
    retries: int = 3,
    backoff: float = 0.5,
) -> FileReport:
    """Baja un JSON de medidas, lo valida y lo guarda en `folder` con una línea por medida."""
    target = target_of(url, folder)
    try:
        text = await get_text(client, url, retries=retries, backoff=backoff)
        series = parse_measurements(text, url)
    except (FetchError, DataFileError) as problem:
        return FileReport(target, error=str(problem))
    content = "".join(f"{measurement}\n" for measurement in series)
    try:
        await asyncio.to_thread(target.write_text, content, encoding="utf-8")
    except OSError as problem:
        return FileReport(target, error=f"no se pudo guardar {target}: {problem.strerror}")
    return FileReport.from_series(target, series)


async def download_all(
    client: httpx.AsyncClient,
    urls: Iterable[str],
    folder: Path,
    *,
    limit: int = 4,
    retries: int = 3,
    backoff: float = 0.5,
) -> list[FileReport]:
    """Baja las URLs a la vez, como mucho `limit` cada vez, en el orden de `urls`."""
    semaphore = asyncio.Semaphore(limit)

    async def guarded(url: str) -> FileReport:
        async with semaphore:
            return await download(client, url, folder, retries=retries, backoff=backoff)

    async with asyncio.TaskGroup() as group:
        tasks = [group.create_task(guarded(url)) for url in urls]
    return [task.result() for task in tasks]
