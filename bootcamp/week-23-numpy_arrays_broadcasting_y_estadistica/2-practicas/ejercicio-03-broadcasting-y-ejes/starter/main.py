"""Ejercicio 03 · Broadcasting y ejes: operar con tablas enteras de una vez.

Ejecuta `uv run python main.py` después de cada paso y compara con el README. Los tiempos
del paso 6 son de tu máquina: compara cuál gana, no el último decimal.
"""

import timeit
from collections.abc import Callable

import numpy as np

STATIONS = np.array(["Norte", "Sur", "Este", "Oeste"])
# Una semana de medidas: 7 días (filas) x 4 estaciones (columnas). La semilla fija hace
# que salgan siempre los mismos números.
rng = np.random.default_rng(23)
WEEK = rng.normal(40, 10, size=(7, 4)).round(1)

print("Ejercicio 03 · Broadcasting y ejes")
print(WEEK)


# ============================================
# PASO 1: Operaciones elemento a elemento
# ============================================
# Descomenta las siguientes líneas:
# print("en décimas:", (WEEK[0] * 10).astype(np.int64))
# print("raíz:      ", np.sqrt(WEEK[0]).round(2))
# print("día 1 - día 0:", WEEK[1] - WEEK[0])
# print("máximo día a día de los dos primeros:", np.maximum(WEEK[0], WEEK[1]))


# ============================================
# PASO 2: Resumir por ejes
# ============================================
# Descomenta las siguientes líneas:
# print(f"media de todo: {WEEK.mean():.2f}")
# by_station = WEEK.mean(axis=0)
# by_day = WEEK.mean(axis=1)
# print("por estación (axis=0):", by_station.round(2), by_station.shape)
# print("por día (axis=1):     ", by_day.round(2), by_day.shape)
# print("la estación de media más alta:", STATIONS[by_station.argmax()])


# ============================================
# PASO 3: Broadcasting por filas y por columnas
# ============================================
# Descomenta las siguientes líneas:
# print("menos la media de su estación, día 0:", (WEEK - WEEK.mean(axis=0))[0].round(2))
# try:
#     WEEK - WEEK.mean(axis=1)
# except ValueError as problem:
#     print("ValueError:", problem)
# by_day_column = WEEK.mean(axis=1, keepdims=True)
# print("keepdims:", by_day_column.shape, "· [:, None]:", by_day[:, None].shape)
# print("menos la media de su día, día 0:  ", (WEEK - by_day_column)[0].round(2))


# ============================================
# PASO 4: Normalizar cada estación
# ============================================
# Descomenta las siguientes líneas:
# z = (WEEK - WEEK.mean(axis=0)) / WEEK.std(axis=0)
# print("medias:", z.mean(axis=0).round(10) + 0.0)
# print("desviaciones:", z.std(axis=0).round(10))
# print("el día más alto de cada estación respecto a su media:", z.argmax(axis=0))


# ============================================
# PASO 5: Tablas de dos ejes
# ============================================
# Descomenta las siguientes líneas:
# print(np.arange(1, 4)[:, None] * np.arange(1, 6))
# thresholds = np.array([30, 40, 50])
# above = WEEK[:, :, None] > thresholds
# print("shape:", above.shape)
# print("días por encima de 30, 40 y 50 en cada estación:")
# print(above.sum(axis=0))


# ============================================
# PASO 6: Bucle o broadcasting
# ============================================
# Descomenta las siguientes líneas:
# big = rng.normal(40, 10, size=(100_000, 4))
# rows = big.tolist()
#
#
# def normalize_loop(table: list[list[float]]) -> list[list[float]]:
#     """Lo mismo que el paso 4, con bucles de Python."""
#     columns = range(len(table[0]))
#     means = [sum(row[c] for row in table) / len(table) for c in columns]
#     stds = [(sum((row[c] - means[c]) ** 2 for row in table) / len(table)) ** 0.5 for c in columns]
#     return [[(row[c] - means[c]) / stds[c] for c in columns] for row in table]
#
#
# def best(function: Callable[[], object]) -> float:
#     """Milisegundos de una llamada: el mínimo de 3 repeticiones."""
#     return min(timeit.repeat(function, number=1, repeat=3)) * 1000
#
#
# print(f"bucles       {best(lambda: normalize_loop(rows)):7.1f} ms")
# print(f"broadcasting {best(lambda: (big - big.mean(axis=0)) / big.std(axis=0)):7.1f} ms")
# same = np.allclose(normalize_loop(rows), (big - big.mean(axis=0)) / big.std(axis=0))
# print("iguales:", same)
