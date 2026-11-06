"""Archivos del Observatorio: leer medidas de texto o CSV y guardar el resumen en JSON.

Qué: las únicas funciones del paquete que tocan el disco, con pathlib y `with`.
Para qué: hasta ahora las medidas llegaban por argumentos o por stdin; desde esta capa
el Observatorio abre sus archivos y deja un resumen que otro programa puede leer.
Impacto: cualquier fallo de archivo (no existe, no es UTF-8, cabecera rara, JSON roto)
sale como DataFileError, con un mensaje en español; main la captura en un solo sitio.
"""

import csv
import json
from pathlib import Path

from observatorio.groups import Record
from observatorio.trends import largest_jump, median, values_of

HEADER = ["etiqueta", "valor"]


class DataFileError(Exception):
    """Un archivo de datos que no se puede leer o escribir."""


def read_lines(path: Path) -> list[str]:
    """Devuelve las líneas del archivo de texto UTF-8 `path`, sin el salto de línea.

    Si no existe, lanza DataFileError("no existe el archivo <path>"); si es una carpeta,
    DataFileError("<path> es una carpeta"); si no es UTF-8,
    DataFileError("<path> no es texto UTF-8"). La excepción original queda como causa.
    """
    raise NotImplementedError("Paso 5: implementa read_lines")


def read_csv(path: Path) -> list[str]:
    """Lee un CSV con cabecera "etiqueta;valor" y devuelve sus filas como líneas "etiqueta;valor".

    Las filas salen en el mismo formato que stdin, así process_lines las valida igual.
    Si el archivo está vacío, lanza DataFileError("<path> está vacío"); si la cabecera
    no es exactamente HEADER, DataFileError("cabecera inesperada en <path>: <cabecera>").
    """
    raise NotImplementedError("Paso 6: implementa read_csv")


def read_data(path: Path) -> list[str]:
    """Las líneas de `path`: con read_csv si la extensión es .csv (sin importar mayúsculas)
    y con read_lines si es cualquier otra."""
    raise NotImplementedError("Paso 7: implementa read_data")


def summary_data(records: list[Record]) -> dict[str, object]:
    """El resumen que se guarda en JSON.

    Claves: "registros" (cuántos), "con_valor" (cuántos tienen valor), "mediana" y
    "mayor_salto", redondeados a 1 decimal; sin valores, las dos últimas son None.
    """
    raise NotImplementedError("Paso 7: implementa summary_data")


def write_json(data: dict[str, object], path: Path) -> None:
    """Guarda `data` en `path` como JSON UTF-8, con sangría de 2 y las tildes tal cual.

    Si no se puede escribir (la carpeta no existe, sin permiso), lanza
    DataFileError("no se puede escribir <path>").
    """
    raise NotImplementedError("Paso 8: implementa write_json")


def read_json(path: Path) -> dict[str, object]:
    """Lee un objeto JSON de `path`.

    Los fallos de archivo, como en read_lines; si el texto no es JSON, lanza
    DataFileError("JSON no válido en <path>, línea <n>"); si es JSON pero no un objeto
    ({...}), DataFileError("<path> no contiene un objeto JSON").
    """
    raise NotImplementedError("Paso 8: implementa read_json")
