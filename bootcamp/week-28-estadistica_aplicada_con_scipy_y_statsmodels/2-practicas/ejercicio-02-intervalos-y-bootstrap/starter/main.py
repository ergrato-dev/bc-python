"""Ejercicio 02 · Intervalos de confianza y bootstrap: cuánto se puede fiar una media.

Ejecuta `uv run python main.py` después de cada paso y compara con el README.
"""

import numpy as np
from scipy import stats

print("Ejercicio 02 · Intervalos de confianza y bootstrap")

# La población entera, que en la vida real nunca ves: la temperatura a mediodía de la
# estación Norte, normal con media 20 °C y desviación 3 °C. Solo tienes una muestra.
rng = np.random.default_rng(28)
TRUE_MEAN, TRUE_STD = 20.0, 3.0
days = rng.normal(TRUE_MEAN, TRUE_STD, size=25).round(1)
print("25 días:", days[:6], "...")


# ============================================
# PASO 1: El error estándar y el intervalo t
# ============================================
# Descomenta las siguientes líneas:
# n, mean, std = days.size, days.mean(), days.std(ddof=1)
# se = std / np.sqrt(n)
# print(f"media {mean:.2f} · desviación {std:.2f} · error estándar {se:.2f}")
# t_crit = stats.t.ppf(0.975, df=n - 1)
# print(f"t crítico con {n - 1} gl: {t_crit:.3f} (la normal daría {stats.norm.ppf(0.975):.3f})")
# low, high = mean - t_crit * se, mean + t_crit * se
# print(f"IC 95 % a mano: [{low:.2f}, {high:.2f}]")
# interval = stats.ttest_1samp(days, popmean=TRUE_MEAN).confidence_interval(0.95)
# print(f"IC 95 % con SciPy: [{interval.low:.2f}, {interval.high:.2f}]")


# ============================================
# PASO 2: Qué significa "95 %"
# ============================================
# Descomenta las siguientes líneas:
# def coverage(size: int, critical: float, repeats: int = 10_000) -> float:
#     """La fracción de muestras de tamaño size cuyo intervalo contiene la media de verdad."""
#     samples = rng.normal(TRUE_MEAN, TRUE_STD, size=(repeats, size))
#     centers = samples.mean(axis=1)
#     halves = critical * samples.std(axis=1, ddof=1) / np.sqrt(size)
#     return float(np.mean((centers - halves <= TRUE_MEAN) & (TRUE_MEAN <= centers + halves)))
#
#
# z = stats.norm.ppf(0.975)
# for size in [5, 25, 100]:
#     t_size = stats.t.ppf(0.975, df=size - 1)
#     print(
#         f"n = {size:>3}: con t {coverage(size, t_size) * 100:.1f} % · con la normal {coverage(size, z) * 100:.1f} %"
#     )


# ============================================
# PASO 3: Cuatro veces más datos, la mitad de ancho
# ============================================
# Descomenta las siguientes líneas:
# for size in [25, 100, 400, 1600]:
#     sample = rng.normal(TRUE_MEAN, TRUE_STD, size=size)
#     result = stats.ttest_1samp(sample, popmean=TRUE_MEAN).confidence_interval(0.95)
#     print(f"n = {size:>4}: ancho {result.high - result.low:.3f}")
# for level in [0.80, 0.95, 0.99]:
#     result = stats.ttest_1samp(days, popmean=TRUE_MEAN).confidence_interval(level)
#     print(
#         f"{level * 100:.0f} %: [{result.low:.2f}, {result.high:.2f}] · ancho {result.high - result.low:.2f}"
#     )


# ============================================
# PASO 4: Bootstrap: remuestrear tu propia muestra
# ============================================
# Descomenta las siguientes líneas:
# resampled = rng.choice(days, size=(10_000, days.size), replace=True)
# medians = np.median(resampled, axis=1)
# print("mediana de la muestra:", np.median(days))
# print("percentiles 2,5 y 97,5 de 10 000 medianas:", np.percentile(medians, [2.5, 97.5]).round(2))
# boot = stats.bootstrap((days,), np.median, confidence_level=0.95, rng=28)
# ci = boot.confidence_interval
# print(
#     f"stats.bootstrap (BCa): [{ci.low:.2f}, {ci.high:.2f}] · error estándar {boot.standard_error:.2f}"
# )


# ============================================
# PASO 5: Cuando los datos no son una campana
# ============================================
# Descomenta las siguientes líneas:
# # Minutos de espera entre alertas: exponencial, media 20. Pocas medidas y muy asimétricas.
# waits = rng.exponential(20, size=15).round(1)
# print("15 esperas:", np.sort(waits).tolist())
# t_ci = stats.ttest_1samp(waits, popmean=20).confidence_interval(0.95)
# boot_ci = stats.bootstrap((waits,), np.mean, rng=28).confidence_interval
# print(f"media {waits.mean():.2f} · t: [{t_ci.low:.2f}, {t_ci.high:.2f}]")
# print(f"           bootstrap: [{boot_ci.low:.2f}, {boot_ci.high:.2f}]")
#
#
# def hits(method: str, repeats: int = 2000) -> float:
#     """Cuántas veces de repeats contiene la media de verdad (20) el intervalo de method."""
#     inside = 0
#     for _ in range(repeats):
#         sample = rng.exponential(20, size=15)
#         if method == "t":
#             result = stats.ttest_1samp(sample, popmean=20).confidence_interval(0.95)
#         else:
#             result = stats.bootstrap(
#                 (sample,), np.mean, n_resamples=999, rng=rng
#             ).confidence_interval
#         inside += result.low <= 20 <= result.high
#     return inside / repeats
#
#
# print(
#     f"cobertura con 15 esperas · t: {hits('t') * 100:.1f} % · bootstrap: {hits('bootstrap') * 100:.1f} %"
# )
