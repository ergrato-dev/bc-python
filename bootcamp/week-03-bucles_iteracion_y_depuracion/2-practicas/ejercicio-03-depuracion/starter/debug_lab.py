"""Ejercicio 03: encontrar errores con el traceback, print, pdb y el depurador de VS Code.

Cada PASO trae un error a propósito. Descomenta cuando el README te lo pida y ejecuta:
    uv run python debug_lab.py
"""

print("Ejercicio 03 · Depuración")

# ============================================
# PASO 1: el traceback dice dónde y qué
# ============================================
# La última línea del traceback es el error; las de arriba, el camino hasta él.
# Descomenta las siguientes líneas:
# def average(values: list[float]) -> float:
#     return sum(values) / len(values)
#
#
# print("Promedio de [4.0, 6.0]:", average([4.0, 6.0]))
# print("Promedio de []:", average([]))

# ============================================
# PASO 2: print con = para ver el estado en cada vuelta
# ============================================
# Debería contar 3 valores >= 50 y cuenta 1. El print muestra por qué.
# Descomenta las siguientes líneas:
# def count_high(values: list[float], limit: float) -> int:
#     for value in values:
#         count = 0
#         if value >= limit:
#             count += 1
#         print(f"    {value=} {count=}")
#     return count
#
#
# print("Altos en [60, 20, 70, 80]:", count_high([60.0, 20.0, 70.0, 80.0], 50.0))

# ============================================
# PASO 3: breakpoint() detiene el programa y abre pdb
# ============================================
# La racha más larga de "alto" es 3 y la función devuelve 1. Investígalo en pdb.
# Descomenta las siguientes líneas:
# def longest_run(levels: list[str], level: str) -> int:
#     best = 0
#     current = 0
#     for item in levels:
#         breakpoint()
#         if item == level:
#             current += 1
#         else:
#             best = max(best, current)
#             current = 0
#     return best
#
#
# print("Racha de alto:", longest_run(["alto", "medio", "alto", "alto", "alto"], "alto"))

# ============================================
# PASO 4: el depurador de VS Code
# ============================================
# El total de estas cuatro medidas es 63.75 y sale 4161.0. Míralo con puntos de parada.
# Descomenta las siguientes líneas:
# def parse_reading(text: str) -> float:
#     return float(text.replace(",", ""))
#
#
# lines = ["Norte;12,5", "Sur;8", "Centro;40,25", "Oriente;3"]
# total = 0.0
# for index, line in enumerate(lines):
#     label, _, text = line.partition(";")
#     value = parse_reading(text)
#     total += value
# print("Total:", total)
