"""Ejercicio 04: el módulo itertools.

Descomenta cada PASO cuando el README te lo pida y ejecuta:
    uv run python itertools_lab.py
"""

from itertools import accumulate, batched, chain, combinations, count, groupby, islice, pairwise

print("Ejercicio 04 · itertools")

# ============================================
# PASO 1: chain e islice
# ============================================
# chain encadena iterables sin crear una lista nueva; islice corta un iterador como un slicing.
# Descomenta las siguientes líneas:
# monday = [12.5, 8.0]
# tuesday = [55.1, 61.0, 48.9]
# print("Seguidas:", list(chain(monday, tuesday)))
# ids = count(start=1)  # 1, 2, 3, ... sin fin
# print("Primeros 4 ids:", list(islice(ids, 4)))
# print("Los 2 siguientes:", list(islice(ids, 2)))

# ============================================
# PASO 2: pairwise y accumulate
# ============================================
# pairwise da cada pareja de vecinos; accumulate, el total acumulado (u otra operación).
# Descomenta las siguientes líneas:
# values = [10.0, 15.0, 12.0, 30.0, 28.0]
# print("Parejas:", list(pairwise(values)))
# print("Saltos:", [after - before for before, after in pairwise(values)])
# print("Acumulado:", list(accumulate(values)))
# print("Máximo hasta aquí:", list(accumulate(values, max)))

# ============================================
# PASO 3: groupby agrupa vecinos iguales
# ============================================
# groupby solo junta elementos SEGUIDOS con la misma clave: no es un "group by" de SQL.
# Descomenta las siguientes líneas:
# levels = ["alto", "alto", "bajo", "alto", "alto", "alto", "medio"]
# for level, group in groupby(levels):
#     print(f"  {level}: racha de {len(list(group))}")
# streak = max((len(list(group)) for level, group in groupby(levels) if level == "alto"), default=0)
# print("Racha más larga en alto:", streak)
# print("Sin ordenar:", [level for level, _ in groupby(levels)])
# print("Ordenados:  ", [level for level, _ in groupby(sorted(levels))])

# ============================================
# PASO 4: batched y combinations
# ============================================
# batched corta en lotes de n; combinations da cada grupo posible sin repetir ni importar el orden.
# Descomenta las siguientes líneas:
# readings = [12.5, 8.0, 55.1, 61.0, 48.9, 9.5, 30.1]
# for batch in batched(readings, 3):
#     print(f"  lote {batch} media {sum(batch) / len(batch):.1f}")
# stations = ["Norte", "Sur", "Este", "Oeste"]
# pairs = list(combinations(stations, 2))
# print(f"{len(pairs)} parejas:", pairs)
