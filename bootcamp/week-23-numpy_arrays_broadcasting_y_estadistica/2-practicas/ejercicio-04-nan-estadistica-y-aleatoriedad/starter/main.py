"""Ejercicio 04 · NaN, estadística y aleatoriedad: datos que faltan, resúmenes y atípicos.

Ejecuta `uv run python main.py` después de cada paso y compara con el README.
"""

import numpy as np

print("Ejercicio 04 · NaN, estadística y aleatoriedad")


# ============================================
# PASO 1: Números aleatorios que se repiten
# ============================================
# Descomenta las siguientes líneas:
# rng = np.random.default_rng(23)
# print("normal:  ", rng.normal(40, 10, size=4).round(1))
# print("enteros: ", rng.integers(0, 100, size=4))
# print("etiquetas:", rng.choice(["Norte", "Sur", "Este"], size=4))
# again = np.random.default_rng(23)
# print("otra vez, misma semilla:", again.normal(40, 10, size=4).round(1))
# other = np.random.default_rng(24)
# print("otra semilla:           ", other.normal(40, 10, size=4).round(1))


# ============================================
# PASO 2: NaN, el dato que falta
# ============================================
# Descomenta las siguientes líneas:
# values = np.array([12.5, np.nan, 55.1, 8.0, np.nan])
# print("nan == nan:", np.nan == np.nan, "· isnan:", np.isnan(values))
# print(f"sum {values.sum()} · mean {values.mean()} · max {values.max()}")
# print(f"nansum {np.nansum(values)} · nanmean {np.nanmean(values):.2f} · nanmax {np.nanmax(values)}")
# present = values[~np.isnan(values)]
# print("presentes:", present, "· faltan:", np.count_nonzero(np.isnan(values)))
# try:
#     np.array([1, np.nan], dtype=np.int64)
# except ValueError as problem:
#     print("ValueError:", problem)


# ============================================
# PASO 3: Avisos en lugar de errores
# ============================================
# Descomenta las siguientes líneas:
# print("media de nada:", np.nanmean(np.array([np.nan, np.nan])))
# with np.errstate(divide="ignore", invalid="ignore"):
#     print("dividir por cero, sin avisos:", np.array([1.0, 0.0]) / 0)
# with np.errstate(divide="raise"):
#     try:
#         np.array([1.0]) / 0
#     except FloatingPointError as problem:
#         print("FloatingPointError:", problem)


# ============================================
# PASO 4: El resumen de una columna
# ============================================
# Descomenta las siguientes líneas:
# sample = rng.normal(40, 10, size=1000)
# sample[rng.random(1000) < 0.05] = np.nan
# present = sample[~np.isnan(sample)]
# print(f"con valor {present.size} · sin dato {sample.size - present.size}")
# print(f"media {present.mean():.2f} · mediana {np.median(present):.2f}")
# print(f"std población {present.std():.3f} · std muestra {present.std(ddof=1):.3f}")
# q1, q2, q3 = np.percentile(present, [25, 50, 75])
# print(f"Q1 {q1:.2f} · Q2 {q2:.2f} · Q3 {q3:.2f} · rango intercuartílico {q3 - q1:.2f}")
# print(f"mínimo {present.min():.2f} · máximo {present.max():.2f}")


# ============================================
# PASO 5: Histograma
# ============================================
# Descomenta las siguientes líneas:
# counts, edges = np.histogram(present, bins=6)
# print("conteos:", counts, "· suman", counts.sum())
# print("bordes: ", edges.round(1))
# for low, high, count in zip(edges[:-1], edges[1:], counts, strict=True):
#     print(f"{low:6.1f} – {high:6.1f}  {'█' * round(count / counts.max() * 30):<30} {count}")


# ============================================
# PASO 6: Puntuaciones z y atípicos
# ============================================
# Descomenta las siguientes líneas:
# spiky = present.copy()
# spiky[[10, 500]] = [120.0, -30.0]
# z = (spiky - spiky.mean()) / spiky.std()
# found = np.flatnonzero(np.abs(z) > 3)
# print("atípicos (|z| > 3):", found, spiky[found].round(1), z[found].round(1))
# share = np.count_nonzero(np.abs(z) > 2) / z.size
# print(f"fuera de 2 desviaciones: {share:.1%} (en una normal, alrededor del 4,6 %)")
