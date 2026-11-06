"""Ejercicio 02: buscar y ordenar.

Descomenta cada PASO cuando el README te lo pida y ejecuta:
    uv run python search_lab.py
"""

import bisect
import heapq

print("Ejercicio 02 · Buscar y ordenar")

# ============================================
# PASO 1: búsqueda lineal
# ============================================
# Mira los elementos uno a uno hasta encontrarlo. Sirve con cualquier lista, ordenada o no.
# Descomenta las siguientes líneas:
# readings = [12.5, 8.0, 55.1, 61.0, 48.9, 9.5, 30.1, 22.4]
# print("¿Está 48.9?", 48.9 in readings, "| posición:", readings.index(48.9))
# print("¿Está 99.0?", 99.0 in readings)

# ============================================
# PASO 2: búsqueda binaria a mano
# ============================================
# En una lista ORDENADA, mira el centro y descarta la mitad donde no puede estar.
# Descomenta las siguientes líneas:
# def binary_search(values: list[int], target: int) -> int:
#     low, high = 0, len(values) - 1
#     while low <= high:
#         middle = (low + high) // 2
#         print(f"  miro [{low}..{high}] -> centro {middle}: {values[middle]}")
#         if values[middle] == target:
#             return middle
#         if values[middle] < target:
#             low = middle + 1
#         else:
#             high = middle - 1
#     return -1
#
#
# ordered = list(range(0, 32, 2))  # 16 números pares: 0, 2, 4, ..., 30
# print("Busco 22:")
# print("Posición:", binary_search(ordered, 22))
# print("Busco 7:")
# print("Posición:", binary_search(ordered, 7))

# ============================================
# PASO 3: bisect, la búsqueda binaria de la biblioteca estándar
# ============================================
# bisect_left/bisect_right dicen en qué posición iría un valor para no romper el orden.
# Descomenta las siguientes líneas:
# ordered_readings = sorted(readings)
# print("Ordenadas:", ordered_readings)
# print("¿Cuántas por debajo de 30?", bisect.bisect_left(ordered_readings, 30))
# print("bisect_left(48.9):", bisect.bisect_left(ordered_readings, 48.9),
#       "| bisect_right(48.9):", bisect.bisect_right(ordered_readings, 48.9))
# bisect.insort(ordered_readings, 40.0)
# print("Tras insort(40.0):", ordered_readings)
#
# thresholds = [10.0, 50.0]
# names = ["bajo", "medio", "alto"]
# for value in [8.0, 10.0, 49.9, 50.0, 61.0]:
#     print(f"  {value:>5} -> {names[bisect.bisect_right(thresholds, value)]}")

# ============================================
# PASO 4: ordenar es estable
# ============================================
# Con claves iguales, sorted conserva el orden en que llegaron los elementos.
# Descomenta las siguientes líneas:
# records = [("Sur", 8.0), ("Norte", 48.9), ("Este", 8.0), ("Norte", 12.5), ("Oeste", 48.9)]
# print("Por valor:         ", sorted(records, key=lambda record: record[1]))
# by_label = sorted(records, key=lambda record: record[0])
# print("Por etiqueta:      ", by_label)
# print("Etiqueta y valor:  ", sorted(by_label, key=lambda record: record[1]))

# ============================================
# PASO 5: los k mayores sin ordenarlo todo
# ============================================
# heapq.nlargest(k, ...) da lo mismo que sorted(..., reverse=True)[:k].
# Descomenta las siguientes líneas:
# print("3 mayores:", heapq.nlargest(3, readings))
# print("Con sorted:", sorted(readings, reverse=True)[:3])
# print("2 menores por valor:", heapq.nsmallest(2, records, key=lambda record: record[1]))
# print("Máximo:", max(readings), "| mínimo:", min(readings))
