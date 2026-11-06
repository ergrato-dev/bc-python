"""Ejercicio 02: composición.

Descomenta cada PASO cuando el README te lo pida y ejecuta:
    uv run python composition_lab.py
"""

from collections import deque
from dataclasses import dataclass, field

print("Ejercicio 02 · composición")

# ============================================
# PASO 1: heredar de list
# ============================================
# Una lista de lecturas que no admite negativos... o eso parece.
# Descomenta las siguientes líneas:
# class ReadingList(list[float]):
#     def append(self, value: float) -> None:
#         if value < 0:
#             raise ValueError(f"lectura negativa: {value}")
#         super().append(value)
#
#
# inherited = ReadingList()
# inherited.append(12.5)
# try:
#     inherited.append(-3.0)
# except ValueError as error:
#     print("Error:", error)
# inherited.insert(0, -5.0)
# inherited.extend([-1.0])
# inherited += [-2.0]
# print("Se colaron:", inherited)
# print("Al sumar:", type(inherited + [1.0]).__name__)

# ============================================
# PASO 2: tener una lista
# ============================================
# Descomenta las siguientes líneas:
# class Readings:
#     def __init__(self) -> None:
#         self._values: list[float] = []
#
#     def add(self, value: float) -> None:
#         if value < 0:
#             raise ValueError(f"lectura negativa: {value}")
#         self._values.append(value)
#
#     def values(self) -> list[float]:
#         return list(self._values)
#
#     def mean(self) -> float:
#         return sum(self._values) / len(self._values)
#
#
# readings = Readings()
# readings.add(12.5)
# readings.add(48.9)
# try:
#     readings.add(-3.0)
# except ValueError as error:
#     print("Error:", error)
# try:
#     readings.insert(0, -5.0)
# except AttributeError as error:
#     print("Error:", error)
# copy = readings.values()
# copy.append(-1.0)
# print("Valores:", readings.values(), "· media:", readings.mean())

# ============================================
# PASO 3: cambiar la pieza de dentro
# ============================================
# La misma clase con un deque de tamaño fijo: solo cambia __init__.
# Descomenta las siguientes líneas:
# class RecentReadings:
#     def __init__(self, limit: int = 3) -> None:
#         self._values: deque[float] = deque(maxlen=limit)
#
#     def add(self, value: float) -> None:
#         if value < 0:
#             raise ValueError(f"lectura negativa: {value}")
#         self._values.append(value)
#
#     def values(self) -> list[float]:
#         return list(self._values)
#
#     def mean(self) -> float:
#         return sum(self._values) / len(self._values)
#
#
# for kind in [Readings(), RecentReadings()]:
#     for value in [10.0, 20.0, 30.0, 40.0]:
#         kind.add(value)
#     print(type(kind).__name__, "->", kind.values(), "· media:", kind.mean())

# ============================================
# PASO 4: un objeto hecho de piezas
# ============================================
# Descomenta las siguientes líneas:
# @dataclass(frozen=True)
# class Scale:
#     unit: str
#     low: float
#     high: float
#
#     def level(self, value: float) -> str:
#         if value < self.low:
#             return "bajo"
#         return "alto" if value >= self.high else "medio"
#
#
# @dataclass
# class Monitor:
#     name: str
#     scale: Scale
#     readings: Readings = field(default_factory=Readings)
#
#     def check(self, value: float) -> str:
#         self.readings.add(value)
#         return f"{self.name}: {value} {self.scale.unit} -> {self.scale.level(value)}"
#
#
# air = Monitor("Centro", Scale("µg/m³", 12.0, 35.0))
# river = Monitor("Puente", Scale("mg/L", 2.0, 6.0), RecentReadings())
# print(air.check(40.0))
# print(river.check(4.5))
# air.scale = Scale("µg/m³", 15.0, 45.0)
# print(air.check(40.0))
# print("Lecturas del aire:", air.readings.values())
