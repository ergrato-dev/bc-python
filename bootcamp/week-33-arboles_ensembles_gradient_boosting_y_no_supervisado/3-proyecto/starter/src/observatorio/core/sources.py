"""Las fuentes de líneas del Observatorio: argumentos, stdin, un .txt o un .csv.

Qué: un Protocol (Source), una fuente en memoria (LinesSource), una base abstracta para
archivos (FileSource) con sus dos hijas, y open_file, que elige la hija por la extensión.
Para qué: main solo pide source.lines(), sin saber de dónde salen las líneas.
Impacto: una fuente nueva (una API en la semana 16, PostgreSQL en la 18) es una clase
más con lines(); main no cambia.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, runtime_checkable

from observatorio.core.storage import read_csv, read_lines


@runtime_checkable
class Source(Protocol):
    """Cualquier objeto con un método lines() que devuelve las líneas a analizar."""

    def lines(self) -> list[str]: ...


@dataclass(frozen=True, slots=True)
class LinesSource:
    """Líneas que ya están en memoria: los argumentos o stdin."""

    data: list[str]

    def lines(self) -> list[str]:
        return list(self.data)


@dataclass(frozen=True)
class FileSource(ABC):
    """La base de las fuentes que leen un archivo: guarda la ruta y no se puede crear."""

    path: Path

    @abstractmethod
    def lines(self) -> list[str]:
        """Las líneas del archivo, o DataFileError si no se puede leer."""


class TextFile(FileSource):
    """Un archivo de texto con una medida "etiqueta;valor" por línea."""

    def lines(self) -> list[str]:
        return read_lines(self.path)


class CsvFile(FileSource):
    """Un CSV con cabecera "etiqueta;valor", leído con read_csv."""

    def lines(self) -> list[str]:
        return read_csv(self.path)


def open_file(path: Path) -> FileSource:
    """CsvFile si la extensión es .csv (sin importar mayúsculas) y TextFile si es otra."""
    if path.suffix.lower() == ".csv":
        return CsvFile(path)
    return TextFile(path)
