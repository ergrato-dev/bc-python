"""Ejercicio 02 · Muchas comparaciones: cuántos "hallazgos" son azar, y cómo evitarlos.

Ejecuta `uv run python main.py` después de cada paso y compara con el README.
"""

import numpy as np
from scipy import stats

print("Ejercicio 02 · Muchas comparaciones")

rng = np.random.default_rng(30)


def p_value(shift: float, size: int = 30) -> float:
    """El p de Welch de dos muestras de una campana de desviación 1, separadas por shift."""
    first, second = rng.normal(0, 1, size), rng.normal(shift, 1, size)
    return float(stats.ttest_ind(first, second, equal_var=False).pvalue)


def holm(p: np.ndarray) -> np.ndarray:
    """Holm: el de puesto k (desde 0), por m - k; y ninguno por debajo del anterior."""
    m = len(p)
    adjusted = np.empty(m)
    running = 0.0
    for k, index in enumerate(np.argsort(p)):
        running = max(running, min(1.0, p[index] * (m - k)))
        adjusted[index] = running
    return adjusted


# Veinte comparaciones: las cuatro primeras tienen una diferencia real de 1 desviación;
# las dieciséis siguientes, ninguna.
SHIFTS = [1.0] * 4 + [0.0] * 16
REAL = np.array([shift > 0 for shift in SHIFTS])
print(f"{len(SHIFTS)} comparaciones, {REAL.sum()} con diferencia real")


# ============================================
# PASO 1: Una comparación sin diferencia
# ============================================
# Descomenta las siguientes líneas:
# null = np.array([p_value(0.0) for _ in range(1000)])
# print(f"p < 0.05 en {np.mean(null < 0.05):.1%} de 1000 comparaciones sin diferencia")


# ============================================
# PASO 2: Diez comparaciones sin diferencia
# ============================================
# Descomenta las siguientes líneas:
# families = np.array([[p_value(0.0) for _ in range(10)] for _ in range(1000)])
# print(f"con algún p < 0.05: {np.mean((families < 0.05).any(axis=1)):.1%} de 1000 análisis")
# print(f"la fórmula: {1 - 0.95**10:.1%}")


# ============================================
# PASO 3: Veinte comparaciones, sin corregir
# ============================================
# Descomenta las siguientes líneas:
# p = np.array([p_value(shift) for shift in SHIFTS])
# found = p < 0.05
# print("p:", p.round(3))
# print(f"sin corregir: {found.sum()} hallazgos, {(found & REAL).sum()} reales y {(found & ~REAL).sum()} falsos")


# ============================================
# PASO 4: Bonferroni, Holm y Benjamini-Hochberg
# ============================================
# Descomenta las siguientes líneas:
# methods = {
#     "bonferroni": np.minimum(p * len(p), 1),
#     "holm": holm(p),
#     "bh": stats.false_discovery_control(p, method="bh"),
# }
# for name, adjusted in methods.items():
#     found = adjusted < 0.05
#     print(f"{name}: {found.sum()} hallazgos, {(found & REAL).sum()} reales y {(found & ~REAL).sum()} falsos")


# ============================================
# PASO 5: BH a mano
# ============================================
# Descomenta las siguientes líneas:
# order = np.argsort(p)
# scaled = p[order] * len(p) / np.arange(1, len(p) + 1)
# by_hand = np.empty(len(p))
# by_hand[order] = np.minimum.accumulate(scaled[::-1])[::-1]
# print("los tres menores, a mano:", by_hand[order][:3].round(4))
# print("los tres menores, scipy: ", methods["bh"][order][:3].round(4))
# print(f"iguales: {np.allclose(by_hand, methods['bh'])}")


# ============================================
# PASO 6: Mil análisis de veinte comparaciones
# ============================================
# Descomenta las siguientes líneas:
# corrections = {
#     "ninguna": lambda p: p,
#     "bonferroni": lambda p: np.minimum(p * len(p), 1),
#     "holm": holm,
#     "bh": lambda p: stats.false_discovery_control(p, method="bh"),
# }
# runs = np.array([[p_value(shift) for shift in SHIFTS] for _ in range(1000)])
# print(f"{'corrección':<11} {'reales':>7} {'falsos':>7} {'con algún falso':>16} {'falsos/hallazgos':>17}")
# for name, correct in corrections.items():
#     found = np.array([correct(row) < 0.05 for row in runs])
#     real, false = (found & REAL).sum(axis=1), (found & ~REAL).sum(axis=1)
#     share = np.mean(false / np.maximum(real + false, 1))
#     print(f"{name:<11} {real.mean():>7.2f} {false.mean():>7.2f} {np.mean(false > 0):>16.1%} {share:>17.1%}")
