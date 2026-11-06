"""Ejercicio 01: contar pasos y medir tiempos.

Descomenta cada PASO cuando el README te lo pida y ejecuta:
    uv run python big_o_lab.py
"""

import math
import time
import timeit

print("Ejercicio 01 · Contar pasos y medir")

# ============================================
# PASO 1: contar los pasos de dos algoritmos
# ============================================
# Un "paso" aquí es una comparación. Contarlos no depende de lo rápida que sea tu máquina.
# Descomenta las siguientes líneas:
# def linear_steps(values: list[int], target: int) -> int:
#     steps = 0
#     for value in values:
#         steps += 1
#         if value == target:
#             break
#     return steps
#
#
# def pair_steps(values: list[int]) -> int:
#     steps = 0
#     for i in range(len(values)):
#         for j in range(i + 1, len(values)):
#             steps += 1
#     return steps
#
#
# for n in [10, 100, 1_000]:
#     values = list(range(n))
#     print(f"n={n:>5} | buscar el último: {linear_steps(values, n - 1):>6} | todas las parejas: {pair_steps(values):>7}")

# ============================================
# PASO 2: medir con perf_counter
# ============================================
# perf_counter da segundos con muchos decimales; solo tiene sentido restar dos lecturas.
# Descomenta las siguientes líneas:
# for n in [100_000, 1_000_000, 10_000_000]:
#     values = list(range(n))
#     start = time.perf_counter()
#     total = sum(values)
#     elapsed = time.perf_counter() - start
#     print(f"sum de {n:>10,} números: {elapsed * 1000:7.2f} ms")

# ============================================
# PASO 3: medir con timeit, lista frente a set
# ============================================
# timeit repite la instrucción `number` veces y devuelve el total en segundos.
# Descomenta las siguientes líneas:
# for n in [1_000, 10_000, 100_000]:
#     data_list = list(range(n))
#     data_set = set(data_list)
#     target = n - 1
#     list_time = timeit.timeit("target in data_list", globals=globals(), number=1_000)
#     set_time = timeit.timeit("target in data_set", globals=globals(), number=1_000)
#     print(f"n={n:>7,} | lista: {list_time * 1000:8.2f} ms | set: {set_time * 1000:6.3f} ms")

# ============================================
# PASO 4: el mismo problema en O(n²) y en O(n)
# ============================================
# ¿Hay algún valor repetido? Comparar cada pareja, o recordar lo visto en un set.
# Descomenta las siguientes líneas:
# def has_duplicates_slow(values: list[int]) -> bool:
#     for i in range(len(values)):
#         for j in range(i + 1, len(values)):
#             if values[i] == values[j]:
#                 return True
#     return False
#
#
# def has_duplicates_fast(values: list[int]) -> bool:
#     seen: set[int] = set()
#     for value in values:
#         if value in seen:
#             return True
#         seen.add(value)
#     return False
#
#
# for n in [1_000, 2_000, 4_000]:
#     values = list(range(n))  # sin repetidos: el peor caso, hay que mirarlo todo
#     slow = timeit.timeit(lambda: has_duplicates_slow(values), number=1)
#     fast = timeit.timeit(lambda: has_duplicates_fast(values), number=1)
#     print(f"n={n:>5,} | O(n²): {slow * 1000:8.1f} ms | O(n): {fast * 1000:6.3f} ms")

# ============================================
# PASO 5: cómo crece cada orden
# ============================================
# Pasos aproximados de cada orden para tres tamaños de entrada.
# Descomenta las siguientes líneas:
# print(f"{'n':>10} {'log n':>6} {'n log n':>12} {'n²':>18}")
# for n in [10, 1_000, 1_000_000]:
#     print(f"{n:>10,} {math.log2(n):>6.0f} {n * math.log2(n):>12,.0f} {n * n:>18,}")
