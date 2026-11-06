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

from observatorio.core.groups import Record
from observatorio.core.trends import largest_jump, median, values_of

HEADER = ["etiqueta", "valor"]


class DataFileError(Exception):
    """Un archivo de datos que no se puede leer o escribir."""


def read_lines(path: Path) -> list[str]:
    """Devuelve las líneas del archivo de texto UTF-8 `path`, sin el salto de línea.

    Si no existe, lanza DataFileError("no existe el archivo <path>"); si es una carpeta,
    DataFileError("<path> es una carpeta"); si no es UTF-8,
    DataFileError("<path> no es texto UTF-8"). La excepción original queda como causa.
    """
    try:
        with path.open(encoding="utf-8") as file:
            return file.read().splitlines()
    except FileNotFoundError as error:
        raise DataFileError(f"no existe el archivo {path}") from error
    except IsADirectoryError as error:
        raise DataFileError(f"{path} es una carpeta") from error
    except UnicodeDecodeError as error:
        raise DataFileError(f"{path} no es texto UTF-8") from error


def read_csv(path: Path) -> list[str]:
    """Lee un CSV con cabecera "etiqueta;valor" y devuelve sus filas como líneas "etiqueta;valor".

    Las filas salen en el mismo formato que stdin, así process_lines las valida igual.
    Si el archivo está vacío, lanza DataFileError("<path> está vacío"); si la cabecera
    no es exactamente HEADER, DataFileError("cabecera inesperada en <path>: <cabecera>").
    """
    # ponytail: lee por líneas, así un campo entre comillas con un salto de línea dentro
    # se parte; si tus datos lo traen, abre con newline="" y pasa el archivo a csv.reader.
    rows = csv.reader(read_lines(path), delimiter=";")
    header = next(rows, None)
    if header is None:
        raise DataFileError(f"{path} está vacío")
    if header != HEADER:
        raise DataFileError(f"cabecera inesperada en {path}: {';'.join(header)}")
    return [";".join(row) for row in rows]


def read_data(path: Path) -> list[str]:
    """Las líneas de `path`: con read_csv si la extensión es .csv (sin importar mayúsculas)
    y con read_lines si es cualquier otra."""
    if path.suffix.lower() == ".csv":
        return read_csv(path)
    return read_lines(path)


def summary_data(records: list[Record]) -> dict[str, object]:
    """El resumen que se guarda en JSON.

    Claves: "registros" (cuántos), "con_valor" (cuántos tienen valor), "mediana" y
    "mayor_salto", redondeados a 1 decimal; sin valores, las dos últimas son None.
    """
    values = values_of(records)
    return {
        "registros": len(records),
        "con_valor": len(values),
        "mediana": round(median(values), 1) if values else None,
        "mayor_salto": round(largest_jump(values), 1) if values else None,
    }


def write_json(data: dict[str, object], path: Path) -> None:
    """Guarda `data` en `path` como JSON UTF-8, con sangría de 2 y las tildes tal cual.

    Si no se puede escribir (la carpeta no existe, sin permiso), lanza
    DataFileError("no se puede escribir <path>").
    """
    try:
        with path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
            file.write("\n")
    except OSError as error:
        raise DataFileError(f"no se puede escribir {path}") from error


def read_json(path: Path) -> dict[str, object]:
    """Lee un objeto JSON de `path`.

    Los fallos de archivo, como en read_lines; si el texto no es JSON, lanza
    DataFileError("JSON no válido en <path>, línea <n>"); si es JSON pero no un objeto
    ({...}), DataFileError("<path> no contiene un objeto JSON").
    """
    text = "\n".join(read_lines(path))
    try:
        data = json.loads(text)
    except json.JSONDecodeError as error:
        raise DataFileError(f"JSON no válido en {path}, línea {error.lineno}") from error
    if not isinstance(data, dict):
        raise DataFileError(f"{path} no contiene un objeto JSON")
    return data
