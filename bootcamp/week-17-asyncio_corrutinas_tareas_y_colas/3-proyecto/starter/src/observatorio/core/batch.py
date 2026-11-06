"""Resumir muchos archivos a la vez, con hilos o con procesos.

Qué: `report_file` resume un archivo en un `FileReport`; `report_files` reparte una
lista de archivos entre varios trabajadores y devuelve los resúmenes en el mismo orden.
Para qué: leer un archivo es casi todo espera (disco, red); mientras un hilo espera,
otro lee. Con `processes=True`, cada trabajador es un proceso con su propio GIL.
Impacto: cada tarea devuelve un valor inmutable y no toca nada compartido, así que no
hace falta ningún Lock. Un archivo que no se puede leer es un resultado más, no una
excepción que tumbe el lote.
"""

from collections.abc import Iterable
from concurrent.futures import Executor, ProcessPoolExecutor, ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from statistics import fmean

from observatorio.core.model import Series
from observatorio.core.sources import open_file
from observatorio.core.storage import DataFileError


@dataclass(frozen=True, slots=True)
class FileReport:
    """El resumen de un archivo: cuántas medidas tiene, cuántas con valor y su media.

    Si el archivo no se pudo leer, `error` dice por qué y los números quedan a cero.
    """

    path: Path
    measurements: int = 0
    with_value: int = 0
    mean: float | None = None
    error: str | None = None


def report_file(path: Path) -> FileReport:
    """Lee un archivo .txt o .csv y lo resume. Un DataFileError queda en `error`."""
    try:
        lines = open_file(path).lines()
    except DataFileError as problem:
        return FileReport(path, error=str(problem))
    series = Series.from_lines(lines)
    values = series.values()
    return FileReport(path, len(series), len(values), fmean(values) if values else None)


def report_files(
    paths: Iterable[Path], *, workers: int = 4, processes: bool = False
) -> list[FileReport]:
    """Resume los archivos con `workers` trabajadores a la vez, en el orden de `paths`.

    Con `processes=True` usa procesos (para trabajo de CPU); si no, hilos (para esperas).
    Una excepción que no sea DataFileError llega hasta aquí y se relanza: un bug no se
    esconde como un archivo con error.
    """
    pool: Executor
    if processes:
        pool = ProcessPoolExecutor(max_workers=workers)
    else:
        pool = ThreadPoolExecutor(max_workers=workers, thread_name_prefix="observatorio")
    # with espera a que terminen todas las tareas y cierra el pool, también si hay error.
    # map devuelve los resultados en el orden de las entradas, no en el que terminan.
    with pool:
        return list(pool.map(report_file, paths))
