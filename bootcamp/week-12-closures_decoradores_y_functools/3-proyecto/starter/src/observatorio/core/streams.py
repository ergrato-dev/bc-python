"""Generadores del Observatorio: leer y procesar medidas de una en una.

Qué: iter_lines lee un archivo línea a línea, iter_measurements convierte líneas en
medidas y running_mean da la media acumulada; las tres son generadores.
Para qué: no hace falta tener todos los datos en memoria para empezar a procesarlos:
cada valor se calcula cuando alguien lo pide, aunque la entrada no termine nunca.
Impacto: con un archivo de millones de líneas o un sensor que no para (fase 3), la
memoria usada no crece con los datos.
"""

from collections.abc import Iterable, Iterator
from pathlib import Path

from observatorio.core.model import Measurement
from observatorio.core.report import is_data_line
from observatorio.core.storage import DataFileError


def iter_lines(path: Path) -> Iterator[str]:
    """Da las líneas del archivo de texto UTF-8 `path` una a una, sin el salto de línea.

    Mismos errores que read_lines, pero llegan en el primer next(), no al llamar:
    crear el generador no abre el archivo.
    """
    try:
        with path.open(encoding="utf-8") as file:
            for line in file:
                yield line.rstrip("\n")
    except FileNotFoundError as error:
        raise DataFileError(f"no existe el archivo {path}") from error
    except IsADirectoryError as error:
        raise DataFileError(f"{path} es una carpeta") from error
    except UnicodeDecodeError as error:
        raise DataFileError(f"{path} no es texto UTF-8") from error


def iter_measurements(lines: Iterable[str]) -> Iterator[Measurement]:
    """Da la medida de cada línea de datos válida, con las reglas de Series.from_lines."""
    for line in lines:
        if is_data_line(line):
            measurement = Measurement.from_line(line.strip())
            if measurement is not None:
                yield measurement


def running_mean(values: Iterable[float]) -> Iterator[float]:
    """Da la media de los valores vistos hasta cada momento: [10, 20, 30] da 10, 15, 20."""
    total = 0.0
    for count, value in enumerate(values, start=1):
        total += value
        yield total / count
