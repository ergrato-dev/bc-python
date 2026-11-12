"""Vigilar varios archivos a la vez con asyncio, como si las medidas llegaran en directo.

Qué: `replay` da las medidas de unas líneas de una en una, con una pausa entre ellas;
`watch_file` lee un archivo y lo reproduce; `watch_files` vigila varios a la vez y
devuelve un `FileReport` por archivo, en el orden de entrada.
Para qué: una estación real manda una medida cada pocos segundos. Mientras una espera,
las demás avanzan, todo en un solo hilo. La semana 18 cambiará los archivos por HTTP.
Impacto: aquí solo hay corrutinas. Quien las llama decide cuándo arranca el bucle
(`asyncio.run`) y cuánto tiempo espera (`asyncio.timeout`).
"""

import asyncio
from collections.abc import AsyncIterator, Callable, Iterable
from pathlib import Path

from observatorio.core.batch import FileReport
from observatorio.core.model import Measurement, Series
from observatorio.core.sources import open_file
from observatorio.core.storage import DataFileError
from observatorio.core.streams import iter_measurements

# Lo que recibe cada medida en cuanto llega: el archivo y la medida.
OnReading = Callable[[Path, Measurement], None]


async def replay(lines: Iterable[str], *, interval: float = 0.0) -> AsyncIterator[Measurement]:
    """Da las medidas válidas de `lines`, esperando `interval` segundos antes de cada una.

    La espera es `asyncio.sleep`, que devuelve el control al bucle: con interval=0 no
    tarda nada, pero deja avanzar a las demás tareas.
    """
    for measurement in iter_measurements(lines):
        await asyncio.sleep(interval)
        yield measurement


async def watch_file(
    path: Path, *, interval: float = 0.0, on_reading: OnReading | None = None
) -> FileReport:
    """Lee un archivo, reproduce sus medidas y lo resume. Un DataFileError queda en `error`."""
    try:
        # Leer el disco bloquea: en otro hilo, para que el bucle siga atendiendo al resto.
        lines = await asyncio.to_thread(open_file(path).lines)
    except DataFileError as problem:
        return FileReport(path, error=str(problem))
    series = Series()
    async for measurement in replay(lines, interval=interval):
        series.add(measurement)
        if on_reading is not None:
            on_reading(path, measurement)
    return FileReport.from_series(path, series)


async def watch_files(
    paths: Iterable[Path],
    *,
    interval: float = 0.0,
    limit: int = 4,
    on_reading: OnReading | None = None,
) -> list[FileReport]:
    """Vigila los archivos a la vez, como mucho `limit` cada vez, en el orden de `paths`.

    Una excepción que no sea DataFileError cancela las demás tareas y sale como un
    ExceptionGroup: un bug no se esconde como un archivo con error.
    """
    semaphore = asyncio.Semaphore(limit)

    async def guarded(path: Path) -> FileReport:
        async with semaphore:
            return await watch_file(path, interval=interval, on_reading=on_reading)

    # TaskGroup espera a todas las tareas al salir del bloque; si una falla, cancela el resto.
    async with asyncio.TaskGroup() as group:
        tasks = [group.create_task(guarded(path)) for path in paths]
    return [task.result() for task in tasks]
