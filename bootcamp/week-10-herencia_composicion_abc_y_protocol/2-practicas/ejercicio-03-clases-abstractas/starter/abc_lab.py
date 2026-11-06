"""Ejercicio 03: clases abstractas.

Descomenta cada PASO cuando el README te lo pida y ejecuta:
    uv run python abc_lab.py
"""

import json
import tempfile
from abc import ABC, abstractmethod
from dataclasses import FrozenInstanceError, dataclass
from pathlib import Path

ROWS = ["Norte;12,5", "Sur;NA"]

print("Ejercicio 03 · clases abstractas")

# ============================================
# PASO 1: una base con NotImplementedError
# ============================================
# La forma antigua: la base "obliga" a escribir export lanzando un error.
# Descomenta las siguientes líneas:
# class OldExporter:
#     def __init__(self, path: Path) -> None:
#         self.path = path
#
#     def export(self, rows: list[str]) -> None:
#         raise NotImplementedError
#
#
# class OldTypo(OldExporter):
#     def exprot(self, rows: list[str]) -> None:
#         print("nunca se llama")
#
#
# base = OldExporter(Path("salida.txt"))
# typo = OldTypo(Path("salida.txt"))
# print("Creados sin problema:", type(base).__name__, "y", type(typo).__name__)
# try:
#     typo.export(ROWS)
# except NotImplementedError:
#     print("Error: NotImplementedError, pero solo al llamar a export")

# ============================================
# PASO 2: ABC y @abstractmethod
# ============================================
# Descomenta las siguientes líneas:
# class Exporter(ABC):
#     def __init__(self, path: Path) -> None:
#         self.path = path
#
#     @abstractmethod
#     def export(self, rows: list[str]) -> None:
#         """Escribe las filas en self.path."""
#
#
# class Typo(Exporter):
#     def exprot(self, rows: list[str]) -> None:
#         print("nunca se llama")
#
#
# for cls in [Exporter, Typo]:
#     try:
#         cls(Path("salida.txt"))
#     except TypeError as error:
#         print("Error:", error)
# print("Abstractos de Exporter:", sorted(Exporter.__abstractmethods__))

# ============================================
# PASO 3: el método plantilla
# ============================================
# La base escribe el archivo y cuenta; cada hija solo decide el texto (render).
# Descomenta las siguientes líneas:
# class FileExporter(ABC):
#     def __init__(self, path: Path) -> None:
#         self.path = path
#
#     @abstractmethod
#     def render(self, rows: list[str]) -> str:
#         """El texto del archivo."""
#
#     def export(self, rows: list[str]) -> int:
#         self.path.write_text(self.render(rows), encoding="utf-8")
#         return len(rows)
#
#
# class CsvExporter(FileExporter):
#     def render(self, rows: list[str]) -> str:
#         return "etiqueta;valor\n" + "\n".join(rows) + "\n"
#
#
# class JsonExporter(FileExporter):
#     def render(self, rows: list[str]) -> str:
#         return json.dumps(rows, ensure_ascii=False)
#
#
# with tempfile.TemporaryDirectory() as folder:
#     for exporter in [CsvExporter(Path(folder) / "a.csv"), JsonExporter(Path(folder) / "a.json")]:
#         count = exporter.export(ROWS)
#         text = exporter.path.read_text(encoding="utf-8")
#         print(f"{exporter.path.name}: {count} filas -> {text!r}")

# ============================================
# PASO 4: una propiedad abstracta
# ============================================
# Descomenta las siguientes líneas:
# class Format(ABC):
#     @property
#     @abstractmethod
#     def suffix(self) -> str:
#         """La extensión del archivo, con el punto."""
#
#
# class CsvFormat(Format):
#     @property
#     def suffix(self) -> str:
#         return ".csv"
#
#
# class NoSuffix(Format):
#     pass
#
#
# print("Extensión:", CsvFormat().suffix)
# try:
#     NoSuffix()
# except TypeError as error:
#     print("Error:", error)

# ============================================
# PASO 5: una base abstracta que es una dataclass
# ============================================
# Descomenta las siguientes líneas:
# @dataclass(frozen=True)
# class Source(ABC):
#     path: Path
#
#     @abstractmethod
#     def lines(self) -> list[str]:
#         """Las líneas del archivo."""
#
#
# class TextSource(Source):
#     def lines(self) -> list[str]:
#         return self.path.read_text(encoding="utf-8").splitlines()
#
#
# class CsvSource(Source):
#     def lines(self) -> list[str]:
#         return self.path.read_text(encoding="utf-8").splitlines()[1:]
#
#
# path = Path("medidas")
# print(repr(TextSource(path)).replace("WindowsPath", "PosixPath"))
# print("¿Iguales?", TextSource(path) == TextSource(path), "·", TextSource(path) == CsvSource(path))
# try:
#     TextSource(path).path = Path("otras")
# except FrozenInstanceError as error:
#     print("Error:", error)
# with tempfile.TemporaryDirectory() as folder:
#     data = Path(folder) / "medidas.csv"
#     data.write_text("etiqueta;valor\nNorte;12,5\n", encoding="utf-8")
#     print("Texto:", TextSource(data).lines(), "· CSV:", CsvSource(data).lines())
