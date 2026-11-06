"""Ejercicio 01: mypy estricto.

Descomenta cada PASO cuando el README te lo pida y ejecuta:
    uv run python strict_lab.py
    uvx --from mypy==2.4.1 mypy --strict strict_lab.py
"""

import json
from typing import Final, Literal, TypeIs, cast

print("Ejercicio 01 · mypy estricto")

# ============================================
# PASO 1: funciones sin anotar
# ============================================
# Descomenta las siguientes líneas:
# def mean_untyped(values):  # type: ignore[no-untyped-def]
#     return sum(values) / len(values)
#
#
# def mean(values: list[float]) -> float:
#     return sum(values) / len(values)
#
#
# untyped = mean_untyped([12.5, 8.0])  # type: ignore[no-untyped-call]
# print("Sin anotar:", untyped, "· anotada:", mean([12.5, 8.0]))
# try:
#     mean_untyped(["12,5", "8"])  # type: ignore[no-untyped-call]
# except TypeError as error:
#     print("Sin anotar, el error llega al ejecutar:", error)

# ============================================
# PASO 2: Any se cuela
# ============================================
# Descomenta las siguientes líneas:
# def read_limit(text: str) -> float:
#     data = json.loads(text)
#     return data["limit"]  # type: ignore[no-any-return]
#
#
# limit = read_limit('{"limit": "50"}')
# print("mypy cree que es float; en realidad es", type(limit).__name__)
#
#
# def read_limit_checked(text: str) -> float:
#     data: object = json.loads(text)
#     if not isinstance(data, dict):
#         raise TypeError("se esperaba un objeto JSON")
#     value = data.get("limit")
#     if not isinstance(value, int | float):
#         raise TypeError(f"limit debe ser un número, no {value!r}")
#     return float(value)
#
#
# print("Comprobado:", read_limit_checked('{"limit": 50}'))
# try:
#     read_limit_checked('{"limit": "50"}')
# except TypeError as error:
#     print("Comprobado:", error)

# ============================================
# PASO 3: None obliga a comprobar
# ============================================
# Descomenta las siguientes líneas:
# def level(value: float | None) -> str:
#     if value is None:
#         return "sin dato"
#     return "alto" if value > 50 else "bajo"
#
#
# def is_number(value: object) -> TypeIs[float]:
#     return isinstance(value, float)
#
#
# readings: list[object] = [55.1, None, "12,5", 8.0]
# print("Niveles:", [level(value) for value in readings if value is None or is_number(value)])

# ============================================
# PASO 4: Literal y Final
# ============================================
# Descomenta las siguientes líneas:
# type Level = Literal["bajo", "medio", "alto"]
# HIGH: Final = 50.0
#
# COLORS = {"bajo": "verde", "medio": "ámbar", "alto": "rojo"}
#
#
# def color(level: Level) -> str:
#     return COLORS[level]
#
#
# print("alto se pinta de", color("alto"))
# try:
#     color("altísimo")  # type: ignore[arg-type]
# except KeyError as error:
#     print("Python no comprueba el Literal: KeyError", error)
# HIGH = 60.0  # type: ignore[misc]
# print("Final tampoco se comprueba al ejecutar: HIGH vale", HIGH)

# ============================================
# PASO 5: cast promete, no convierte
# ============================================
# Descomenta las siguientes líneas:
# raw = json.loads('{"value": "12,5"}')["value"]
# value = cast(float, raw)
# print("Después de cast:", repr(value), "es", type(value).__name__)
# try:
#     print(value + 1)
# except TypeError as error:
#     print("Y falla al usarlo:", error)
