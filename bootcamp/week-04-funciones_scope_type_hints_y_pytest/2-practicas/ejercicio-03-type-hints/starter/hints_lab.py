"""Ejercicio 03: type hints, que Python no comprueba y mypy sí.

Descomenta cada PASO cuando el README te lo pida. Ejecuta y revisa:
    uv run python hints_lab.py
    uv run --with mypy==2.4.1 mypy hints_lab.py
"""

print("Ejercicio 03 · Type hints")

# ============================================
# PASO 1: las anotaciones no cambian lo que pasa al ejecutar
# ============================================
# n: int y -> int son información para personas y herramientas; Python no las comprueba.
# Descomenta las siguientes líneas:
# def double(n: int) -> int:
#     return n * 2
#
#
# print("double(21) =", double(21))
# print("double('ab') =", double("ab"))
# print("Anotaciones:", double.__annotations__)

# ============================================
# PASO 2: X | None obliga a mirar el caso None
# ============================================
# parse_value puede devolver None; usar el resultado sin comprobarlo es un error que mypy ve.
# Descomenta las siguientes líneas:
# def parse_value(text: str) -> float | None:
#     text = text.strip()
#     if text in ("", "NA"):
#         return None
#     return float(text.replace(",", "."))
#
#
# def double_reading(text: str) -> float:
#     return parse_value(text) * 2
#
#
# print("double_reading('12,5') =", double_reading("12,5"))

# ============================================
# PASO 3: tipos de colecciones y de lo que se devuelve
# ============================================
# list[float] es "lista de floats"; tuple[str, float], "pareja de texto y número".
# Descomenta las siguientes líneas:
# def average(values: list[float]) -> float:
#     total = 0.0
#     for value in values:
#         total += value
#     return f"{total / len(values):.1f}"
#
#
# def best_station(names: list[str], values: list[float]) -> tuple[str, float]:
#     best_index = 0
#     for index, value in enumerate(values):
#         if value > values[best_index]:
#             best_index = index
#     return names[best_index], values[best_index]
#
#
# print("Promedio:", average([12.5, 8.0, 55.1]))
# print("Mejor estación:", best_station(["Norte", "Sur", "Centro"], [12.5, 8.0, 55.1]))
