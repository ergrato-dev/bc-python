"""Ejercicio 03 · Pruebas de hipótesis: p-valores, errores y lo que no dicen.

Ejecuta `uv run python main.py` después de cada paso y compara con el README.
"""

import numpy as np
from scipy import stats

print("Ejercicio 03 · Pruebas de hipótesis")

# Dos estaciones, 20 días cada una. Sur mide de verdad 1,5 °C más que Norte, y es más
# variable: lo sabes porque las has generado tú; en la vida real, es lo que quieres averiguar.
rng = np.random.default_rng(28)
norte = rng.normal(20.0, 2.0, size=20).round(1)
sur = rng.normal(21.5, 4.0, size=20).round(1)
print(f"Norte: media {norte.mean():.2f}, desviación {norte.std(ddof=1):.2f}")
print(f"Sur:   media {sur.mean():.2f}, desviación {sur.std(ddof=1):.2f}")


# ============================================
# PASO 1: Welch y Student
# ============================================
# Descomenta las siguientes líneas:
# welch = stats.ttest_ind(sur, norte, equal_var=False)
# student = stats.ttest_ind(sur, norte, equal_var=True)
# print(f"Welch:   t = {welch.statistic:.3f}, gl = {welch.df:.1f}, p = {welch.pvalue:.4f}")
# print(f"Student: t = {student.statistic:.3f}, gl = {student.df:.1f}, p = {student.pvalue:.4f}")
# ci = welch.confidence_interval(0.95)
# print(f"Sur - Norte: {sur.mean() - norte.mean():.2f}, IC 95 %: [{ci.low:.2f}, {ci.high:.2f}]")
# print("¿cero dentro del intervalo?", ci.low <= 0 <= ci.high, "· ¿p < 0,05?", welch.pvalue < 0.05)


# ============================================
# PASO 2: El p-valor, por simulación
# ============================================
# Descomenta las siguientes líneas:
# def mean_difference(x: np.ndarray, y: np.ndarray, axis: int = -1) -> np.ndarray:
#     """La diferencia de medias de x e y, a lo largo de axis."""
#     return np.mean(x, axis=axis) - np.mean(y, axis=axis)
#
#
# permutation = stats.permutation_test(
#     (sur, norte), mean_difference, n_resamples=20_000, vectorized=True, rng=28
# )
# observed = mean_difference(sur, norte)
# print(f"diferencia observada: {observed:.2f}")
# share = np.mean(np.abs(permutation.null_distribution) >= abs(observed))
# print(f"repartos al azar con una diferencia igual o mayor: {share:.4f}")
# print(f"p de la permutación: {permutation.pvalue:.4f} · p de Welch: {welch.pvalue:.4f}")


# ============================================
# PASO 3: Una medida extrema: Welch y Mann-Whitney
# ============================================
# Descomenta las siguientes líneas:
# broken = norte.copy()
# broken[0] = 95.0  # un sensor que se vuelve loco una vez
# for name, sample in [("sin el extremo", norte), ("con el extremo", broken)]:
#     p_welch = stats.ttest_ind(sur, sample, equal_var=False).pvalue
#     p_ranks = stats.mannwhitneyu(sur, sample).pvalue
#     print(
#         f"{name}: media Norte {sample.mean():5.2f}"
#         f" · p Welch {p_welch:.4f} · p Mann-Whitney {p_ranks:.4f}"
#     )


# ============================================
# PASO 4: Variables con categorías: chi cuadrado
# ============================================
# Descomenta las siguientes líneas:
# # Cuántos días tuvo cada estación en cada nivel de alerta: bajo, medio, alto.
# table = np.array([[52, 28, 10], [35, 33, 22]])
# chi2 = stats.chi2_contingency(table)
# print(f"chi² = {chi2.statistic:.2f}, gl = {chi2.dof}, p = {chi2.pvalue:.4f}")
# print("lo esperado si el nivel no dependiera de la estación:")
# print(chi2.expected_freq.round(1))


# ============================================
# PASO 5: Muchas pruebas, potencia y tamaño del efecto
# ============================================
# Descomenta las siguientes líneas:
# # 100 comparaciones entre dos grupos que vienen de la MISMA distribución.
# noise = [stats.ttest_ind(rng.normal(20, 3, 20), rng.normal(20, 3, 20)).pvalue for _ in range(100)]
# noise = np.array(noise)
# print("con p < 0,05 sin ninguna diferencia real:", int(np.sum(noise < 0.05)), "de 100")
# print("tras Bonferroni (p < 0,05 / 100):", int(np.sum(noise < 0.05 / 100)))
# print("tras Benjamini-Hochberg:", int(np.sum(stats.false_discovery_control(noise) < 0.05)))
#
#
# def power(size: int, shift: float, repeats: int = 2000) -> float:
#     """Cuántas veces de repeats Welch da p < 0,05 cuando la diferencia real es shift."""
#     first = rng.normal(20, 3, size=(repeats, size))
#     second = rng.normal(20 + shift, 3, size=(repeats, size))
#     return float(np.mean(stats.ttest_ind(first, second, axis=1, equal_var=False).pvalue < 0.05))
#
#
# for size in [10, 30, 100]:
#     print(
#         f"potencia con {size:>3} por grupo y 1,5 °C de diferencia: {power(size, 1.5) * 100:.0f} %"
#     )
# big_a, big_b = rng.normal(20, 3, 200_000), rng.normal(20.05, 3, 200_000)
# d = (big_b.mean() - big_a.mean()) / np.sqrt((big_a.var(ddof=1) + big_b.var(ddof=1)) / 2)
# p_big = stats.ttest_ind(big_b, big_a, equal_var=False).pvalue
# print(f"200 000 por grupo y 0,05 °C: p = {p_big:.2g}, d de Cohen = {d:.3f}")
