"""Ejercicio 02: protocolos de contenedor.

Descomenta cada PASO cuando el README te lo pida y ejecuta:
    uv run python container_lab.py
"""

from collections.abc import Iterable, Iterator, Sequence, Sized

print("Ejercicio 02 · Contenedores")

# ============================================
# PASO 1: __len__ y __getitem__
# ============================================
# Una lista de lecturas que solo sabe decir cuántas tiene y dar una por posición.
# Descomenta las siguientes líneas:
# class Readings:
#     def __init__(self, values: list[float]) -> None:
#         self._values = values
#
#     def __len__(self) -> int:
#         return len(self._values)
#
#     def __getitem__(self, index: int) -> float:
#         print(f"    __getitem__({index})")
#         return self._values[index]
#
#
# readings = Readings([12.5, 8.0, 55.1])
# print("len:", len(readings), "· primera:", readings[0], "· última:", readings[-1])
# try:
#     readings[3]
# except IndexError as error:
#     print("Error:", error)

# ============================================
# PASO 2: un for sin __iter__
# ============================================
# Descomenta las siguientes líneas:
# print("for:")
# for value in readings:
#     print("  valor", value)
# print("¿55.1 in readings?", 55.1 in readings)
# print("¿Iterable?", isinstance(readings, Iterable), "· ¿Sized?", isinstance(readings, Sized))

# ============================================
# PASO 3: rebanadas (slices)
# ============================================
# Descomenta las siguientes líneas:
# class Track:
#     def __init__(self, values: list[float]) -> None:
#         self._values = values
#
#     def __repr__(self) -> str:
#         return f"Track({self._values})"
#
#     def __len__(self) -> int:
#         return len(self._values)
#
#     def __getitem__(self, index: int | slice) -> float | Track:
#         print(f"    recibe {index!r}")
#         if isinstance(index, slice):
#             return Track(self._values[index])
#         return self._values[index]
#
#
# track = Track([10.0, 20.0, 30.0, 40.0])
# print("track[1]:", track[1])
# print("track[1:3]:", track[1:3])
# print("track[::-1]:", track[::-1])

# ============================================
# PASO 4: __iter__ y __contains__ propios
# ============================================
# Un registro de medidas por etiqueta: `in` busca etiquetas y for recorre los valores.
# Descomenta las siguientes líneas:
# class Logbook:
#     def __init__(self, entries: dict[str, float]) -> None:
#         self._entries = entries
#
#     def __len__(self) -> int:
#         return len(self._entries)
#
#     def __iter__(self) -> Iterator[float]:
#         return iter(self._entries.values())
#
#     def __contains__(self, label: object) -> bool:
#         print(f"    __contains__({label!r})")
#         return label in self._entries
#
#
# logbook = Logbook({"Norte": 12.5, "Sur": 8.0})
# print("¿Norte in logbook?", "Norte" in logbook, "· ¿12.5 in logbook?", 12.5 in logbook)
# print("Valores:", list(logbook), "· suma:", sum(logbook), "· máximo:", max(logbook))
# print("¿Iterable?", isinstance(logbook, Iterable))

# ============================================
# PASO 5: Sequence te da el resto
# ============================================
# Descomenta las siguientes líneas:
# class Week(Sequence[str]):
#     DAYS = ("lun", "mar", "mié", "jue", "vie", "sáb", "dom")
#
#     def __len__(self) -> int:
#         return len(self.DAYS)
#
#     def __getitem__(self, index: int) -> str:  # type: ignore[override]
#         return self.DAYS[index]
#
#
# week = Week()
# print("¿'vie' in week?", "vie" in week, "· índice:", week.index("vie"), "· cuántos 'lun':", week.count("lun"))
# print("Al revés:", list(reversed(week))[:3])
# print("Gratis de Sequence:", sorted(name for name in ["index", "count", "__contains__", "__iter__", "__reversed__"] if name not in vars(Week)))
#
#
# class OnlyLength(Sequence[str]):
#     def __len__(self) -> int:
#         return 0
#
#
# try:
#     OnlyLength()
# except TypeError as error:
#     print("Error:", error)
