"""Ejercicio 04: Protocol.

Descomenta cada PASO cuando el README te lo pida y ejecuta:
    uv run python protocol_lab.py
"""

from collections.abc import Iterable, Sized
from pathlib import Path
from typing import Protocol, runtime_checkable

print("Ejercicio 04 · Protocol")

# ============================================
# PASO 1: duck typing
# ============================================
# Dos clases sin nada en común salvo un método lines(), y una función sin tipos.
# Descomenta las siguientes líneas:
# class Fixed:
#     def lines(self) -> list[str]:
#         return ["Norte;12,5", "Sur;8"]
#
#
# class Shouting:
#     def __init__(self, data: list[str]) -> None:
#         self.data = data
#
#     def lines(self) -> list[str]:
#         return [line.upper() for line in self.data]
#
#
# def first_line(source):
#     return source.lines()[0]
#
#
# print("Fixed:", first_line(Fixed()), "· Shouting:", first_line(Shouting(["este;3"])))
# try:
#     first_line(Path("medidas.txt"))
# except AttributeError as error:
#     print("Error:", error)

# ============================================
# PASO 2: un Protocol con nombre
# ============================================
# Descomenta las siguientes líneas:
# class Source(Protocol):
#     def lines(self) -> list[str]: ...
#
#
# def count_lines(source: Source) -> int:
#     return len(source.lines())
#
#
# print("Líneas:", count_lines(Fixed()), "y", count_lines(Shouting(["a;1", "b;2", "c;3"])))
# print("¿Fixed hereda de Source?", Source in Fixed.__mro__)
# try:
#     isinstance(Fixed(), Source)
# except TypeError as error:
#     print("Error:", error)
# try:
#     count_lines(Path("medidas.txt"))
# except AttributeError as error:
#     print("Error:", error)

# ============================================
# PASO 3: @runtime_checkable y sus límites
# ============================================
# Descomenta las siguientes líneas:
# @runtime_checkable
# class CheckedSource(Protocol):
#     def lines(self) -> list[str]: ...
#
#
# class Liar:
#     lines = 42
#
#
# class WrongType:
#     def lines(self) -> str:
#         return "Norte;12,5"
#
#
# for candidate in [Fixed(), Path("medidas.txt"), Liar(), WrongType()]:
#     print(f"  {type(candidate).__name__}: {isinstance(candidate, CheckedSource)}")
# print("Líneas de WrongType:", count_lines(WrongType()))

# ============================================
# PASO 4: los protocolos de collections.abc
# ============================================
# Descomenta las siguientes líneas:
# class Shelf:
#     def __init__(self, books: list[str]) -> None:
#         self.books = books
#
#     def __len__(self) -> int:
#         return len(self.books)
#
#
# shelf = Shelf(["Fluent Python", "Think Python"])
# print("len:", len(shelf), "· ¿Sized?", isinstance(shelf, Sized), "· ¿Iterable?", isinstance(shelf, Iterable))

# ============================================
# PASO 5: un Protocol para las piezas de un objeto
# ============================================
# El Monitor del ejercicio 02, ahora con un tipo que aceptan las dos clases de lecturas.
# Descomenta las siguientes líneas:
# class ReadingStore(Protocol):
#     def add(self, value: float) -> None: ...
#
#     def values(self) -> list[float]: ...
#
#
# class AllReadings:
#     def __init__(self) -> None:
#         self._values: list[float] = []
#
#     def add(self, value: float) -> None:
#         self._values.append(value)
#
#     def values(self) -> list[float]:
#         return list(self._values)
#
#
# class LastReading:
#     def __init__(self) -> None:
#         self._last: float | None = None
#
#     def add(self, value: float) -> None:
#         self._last = value
#
#     def values(self) -> list[float]:
#         return [] if self._last is None else [self._last]
#
#
# def record_all(store: ReadingStore, values: list[float]) -> list[float]:
#     for value in values:
#         store.add(value)
#     return store.values()
#
#
# stores: list[ReadingStore] = [AllReadings(), LastReading()]
# for store in stores:
#     print(f"  {type(store).__name__}: {record_all(store, [10.0, 20.0, 30.0])}")
