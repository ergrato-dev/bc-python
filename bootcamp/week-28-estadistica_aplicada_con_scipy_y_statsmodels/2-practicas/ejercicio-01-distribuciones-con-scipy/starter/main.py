"""Ejercicio 01 · Distribuciones con scipy.stats: modelos, probabilidades y muestras.

Ejecuta `uv run python main.py` después de cada paso y compara con el README.
"""

import numpy as np
from scipy import stats

print("Ejercicio 01 · Distribuciones con scipy.stats")

# Un modelo de la temperatura a mediodía en la estación Norte: normal, media 20 °C y
# desviación 3 °C. La semilla hace que las muestras al azar salgan siempre iguales.
rng = np.random.default_rng(28)
noon = stats.norm(loc=20, scale=3)


# ============================================
# PASO 1: Una distribución y sus cuatro preguntas
# ============================================
# Descomenta las siguientes líneas:
# print("media:", noon.mean(), "· desviación:", noon.std())
# print("densidad en 20 °C:", round(noon.pdf(20), 4), "· en 26 °C:", round(noon.pdf(26), 4))
# print("P(T <= 23):", round(noon.cdf(23), 4))
# print("P(T > 26): ", round(noon.sf(26), 4))
# print("el 95 % de los días, por debajo de:", round(noon.ppf(0.95), 2))
# print("intervalo con el 95 % central:", [round(float(x), 2) for x in noon.interval(0.95)])
# print("¿cdf y ppf se deshacen?", round(noon.ppf(noon.cdf(23)), 10) == 23)


# ============================================
# PASO 2: Muestras al azar y la ley de los grandes números
# ============================================
# Descomenta las siguientes líneas:
# days = noon.rvs(size=30, random_state=rng)
# print("30 días:", days[:5].round(1), "...")
# print(
#     "media de la muestra:",
#     round(days.mean(), 2),
#     "· desviación (ddof=1):",
#     round(days.std(ddof=1), 2),
# )
# for n in [10, 100, 10_000, 1_000_000]:
#     sample = noon.rvs(size=n, random_state=rng)
#     print(f"n = {n:>9_}: media {sample.mean():6.3f} · error {abs(sample.mean() - 20):.3f}")


# ============================================
# PASO 3: Contar sucesos: binomial y Poisson
# ============================================
# Descomenta las siguientes líneas:
# # Un sensor falla en el 10 % de las lecturas; un lote tiene 20 lecturas.
# failures = stats.binom(n=20, p=0.1)
# print("binomial · media:", failures.mean(), "· P(0 fallos):", round(failures.pmf(0), 4))
# print("P(5 o más fallos):", round(failures.sf(4), 4))
# # Llegan de media 3 alertas por hora, cada una por su lado.
# alerts = stats.poisson(mu=3)
# print("Poisson · P(0 alertas):", round(alerts.pmf(0), 4), "· P(más de 6):", round(alerts.sf(6), 4))
# print("alertas por hora en 8 horas:", alerts.rvs(size=8, random_state=rng))
# print(
#     "¿la densidad de un discreto?", hasattr(alerts, "pdf"), "· ¿y su pmf?", hasattr(alerts, "pmf")
# )


# ============================================
# PASO 4: El teorema central del límite
# ============================================
# Descomenta las siguientes líneas:
# # Tiempo entre dos alertas: exponencial, media 20 min. Muy asimétrica: muchas esperas
# # cortas y unas pocas muy largas.
# waits = stats.expon(scale=20)
# raw = waits.rvs(size=100_000, random_state=rng)
# print("esperas · media:", round(raw.mean(), 2), "· asimetría:", round(float(stats.skew(raw)), 2))
# for n in [2, 10, 50]:
#     means = waits.rvs(size=(20_000, n), random_state=rng).mean(axis=1)
#     print(
#         f"medias de {n:>2}: desviación {means.std():5.2f} (20 / √{n} = {20 / np.sqrt(n):5.2f})"
#         f" · asimetría {float(stats.skew(means)):4.2f}"
#     )


# ============================================
# PASO 5: Ajustar un modelo a unos datos
# ============================================
# Descomenta las siguientes líneas:
# loc, scale = stats.norm.fit(days)
# print("normal ajustada a los 30 días:", round(loc, 2), round(scale, 2))
# summary = stats.describe(days)
# print(
#     "n:",
#     summary.nobs,
#     "· mínimo:",
#     round(summary.minmax[0], 2),
#     "· máximo:",
#     round(summary.minmax[1], 2),
# )
# print("asimetría:", round(summary.skewness, 2), "· curtosis:", round(summary.kurtosis, 2))
# fitted = stats.norm(loc, scale)
# print("¿cuántos días de 1000 pasarían de 26 °C?", round(1000 * fitted.sf(26)))
# print("¿y con el modelo de verdad?", round(1000 * noon.sf(26)))
