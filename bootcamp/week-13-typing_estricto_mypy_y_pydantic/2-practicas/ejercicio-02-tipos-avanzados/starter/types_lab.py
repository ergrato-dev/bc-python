"""Ejercicio 02: tipos avanzados.

Descomenta cada PASO cuando el README te lo pida y ejecuta:
    uv run python types_lab.py
    uvx --from mypy==2.4.1 mypy --strict types_lab.py
"""

from collections.abc import Mapping, Sequence
from typing import Literal, NewType, TypedDict, assert_never, reveal_type

print("Ejercicio 02 · Tipos avanzados")

# ============================================
# PASO 1: TypedDict, un dict con claves fijas
# ============================================
# Descomenta las siguientes líneas:
# class Summary(TypedDict):
#     registros: int
#     mediana: float | None
#
#
# summary: Summary = {"registros": 3, "mediana": 12.5}
# print("Es un dict normal:", type(summary).__name__, summary)
# print("mediana:", summary["mediana"])
# try:
#     print(summary["media"])  # type: ignore[typeddict-item]
# except KeyError as error:
#     print("Una clave mal escrita: KeyError", error)
# incomplete: Summary = {"registros": 3}  # type: ignore[typeddict-item]
# print("Le falta una clave y Python no se queja:", incomplete)

# ============================================
# PASO 2: dict frente a Mapping
# ============================================
# Descomenta las siguientes líneas:
# def count_keys(data: dict[str, object]) -> int:
#     return len(data)
#
#
# def count_keys_readonly(data: Mapping[str, object]) -> int:
#     return len(data)
#
#
# print("Con dict:", count_keys(summary))  # type: ignore[arg-type]
# print("Con Mapping:", count_keys_readonly(summary))
#
#
# def total(values: list[float | None]) -> float:
#     return sum(value for value in values if value is not None)
#
#
# def total_readonly(values: Sequence[float | None]) -> float:
#     return sum(value for value in values if value is not None)
#
#
# readings: list[float] = [12.5, 8.0]
# print("Con list:", total(readings))  # type: ignore[arg-type]
# print("Con Sequence:", total_readonly(readings))

# ============================================
# PASO 3: funciones y clases genéricas
# ============================================
# Descomenta las siguientes líneas:
# def first[T](items: Sequence[T]) -> T:
#     return items[0]
#
#
# class Window[T]:
#     def __init__(self, size: int) -> None:
#         self.size = size
#         self.items: list[T] = []
#
#     def push(self, item: T) -> None:
#         self.items = [*self.items, item][-self.size :]
#
#
# print("first de floats:", first([12.5, 8.0]), "· first de textos:", first(["Norte", "Sur"]))
# reveal_type(first(["Norte", "Sur"]))
# window = Window[float](2)
# for value in [12.5, 8.0, 55.1]:
#     window.push(value)
# print("Las dos últimas:", window.items)
# window.push("alto")  # type: ignore[arg-type]

# ============================================
# PASO 4: alias con type y NewType
# ============================================
# Descomenta las siguientes líneas:
# type Record = tuple[str, float | None]
# Celsius = NewType("Celsius", float)
#
#
# def to_fahrenheit(value: Celsius) -> float:
#     return value * 9 / 5 + 32
#
#
# record: Record = ("Norte", 12.5)
# print("Record es un alias:", record, "· su valor:", Record.__value__)
# print("10 °C:", to_fahrenheit(Celsius(10.0)), "°F")
# print("Celsius(10.0) es un float normal:", type(Celsius(10.0)).__name__)
# print("Sin Celsius(...):", to_fahrenheit(10.0))  # type: ignore[arg-type]

# ============================================
# PASO 5: match exhaustivo con assert_never
# ============================================
# Descomenta las siguientes líneas:
# type Level = Literal["bajo", "medio", "alto"]
#
#
# def advice(level: Level) -> str:
#     match level:
#         case "bajo":
#             return "sin aviso"
#         case "medio":
#             return "vigilar"
#         case "alto":
#             return "alerta"
#         case _:
#             assert_never(level)
#
#
# print("Consejos:", [advice(level) for level in ("bajo", "medio", "alto")])
