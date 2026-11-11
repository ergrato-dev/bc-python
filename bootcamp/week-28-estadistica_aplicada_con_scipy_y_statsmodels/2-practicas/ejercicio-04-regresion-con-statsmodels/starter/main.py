"""Ejercicio 04 · Regresión con statsmodels: tendencias, grupos y predicciones con su incertidumbre.

Ejecuta `uv run python main.py` después de cada paso y compara con el README.
"""

import importlib.metadata
import subprocess
import sys

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats
from statsmodels.stats.anova import anova_lm

print("Ejercicio 04 · Regresión con statsmodels")

# 90 días de la media diaria de tres estaciones. Cada una a su nivel, todas suben 0,04 °C
# al día y tienen ruido de 1,5 °C. Una tabla larga: una fila por día y estación.
rng = np.random.default_rng(28)
LEVELS = {"Norte": 18.0, "Sur": 21.0, "Centro": 19.0}
readings = pd.DataFrame(
    [
        {"day": day, "station": station, "value": round(level + 0.04 * day + rng.normal(0, 1.5), 1)}
        for station, level in LEVELS.items()
        for day in range(90)
    ]
)
norte = readings[readings["station"] == "Norte"]
print(readings.shape, "·", readings["station"].unique().tolist())


# ============================================
# PASO 1: Una recta con SciPy
# ============================================
# Descomenta las siguientes líneas:
# line = stats.linregress(norte["day"], norte["value"])
# print(f"pendiente {line.slope:.4f} °C/día · ordenada {line.intercept:.2f} °C")
# print(f"r = {line.rvalue:.3f} · R² = {line.rvalue**2:.3f} · p = {line.pvalue:.2g}")
# t_crit = stats.t.ppf(0.975, df=len(norte) - 2)
# low, high = line.slope - t_crit * line.stderr, line.slope + t_crit * line.stderr
# print(f"IC 95 % de la pendiente: [{low:.4f}, {high:.4f}] · en 90 días: {line.slope * 90:.2f} °C")


# ============================================
# PASO 2: La misma recta con statsmodels
# ============================================
# Descomenta las siguientes líneas:
# fit = smf.ols("value ~ day", data=norte).fit()
# print(type(fit).__name__)
# table = pd.DataFrame({"coef": fit.params, "error": fit.bse, "p": fit.pvalues})
# print(table.to_string(float_format="{:.4g}".format))
# print(fit.conf_int(alpha=0.05).rename(columns={0: "2,5 %", 1: "97,5 %"}).round(4))
# print(f"R² = {fit.rsquared:.3f} · observaciones = {int(fit.nobs)}")
# print("¿la misma pendiente que SciPy?", np.isclose(fit.params["day"], line.slope))


# ============================================
# PASO 3: Variables con categorías
# ============================================
# Descomenta las siguientes líneas:
# groups = smf.ols("value ~ C(station)", data=readings).fit()
# print(groups.params.round(3))
# means = readings.groupby("station")["value"].mean()
# print("medias:", means.round(3).to_dict())
# print("Sur - Centro con pandas:", round(means["Sur"] - means["Centro"], 3))
# print(anova_lm(groups).to_string(float_format="{:.4g}".format))
# samples = [readings.loc[readings["station"] == s, "value"] for s in sorted(LEVELS)]
# f_oneway = stats.f_oneway(*samples)
# print(f"f_oneway de SciPy: F = {f_oneway.statistic:.2f}, p = {f_oneway.pvalue:.2g}")


# ============================================
# PASO 4: Dos variables, predicciones y residuos
# ============================================
# Descomenta las siguientes líneas:
# both = smf.ols("value ~ day + C(station)", data=readings).fit()
# print(both.params.round(4).to_dict())
# print(f"R² solo con day: {smf.ols('value ~ day', data=readings).fit().rsquared:.3f}")
# print(f"R² con day y estación: {both.rsquared:.3f}")
# future = pd.DataFrame({"day": [100, 100], "station": ["Norte", "Sur"]})
# frame = both.get_prediction(future).summary_frame(alpha=0.05)
# print(frame[["mean", "mean_ci_lower", "mean_ci_upper", "obs_ci_lower", "obs_ci_upper"]].round(2))
# print(f"residuos · media {both.resid.mean():.2g} · error típico {np.sqrt(both.scale):.2f}")
# print(f"Shapiro-Wilk sobre los residuos: p = {stats.shapiro(both.resid).pvalue:.3f}")


# ============================================
# PASO 5: Lo que cuesta cada biblioteca
# ============================================
# Descomenta las siguientes líneas:
# def import_seconds(module: str) -> float:
#     """Lo que tarda en importarse module en un proceso nuevo, en segundos."""
#     code = f"import time; s = time.perf_counter(); import {module}; print(time.perf_counter() - s)"
#     return float(
#         subprocess.run(
#             [sys.executable, "-c", code], check=False, capture_output=True, text=True
#         ).stdout
#     )
#
#
# def installed_mb(*packages: str) -> float:
#     """Lo que ocupan en disco los archivos instalados de packages, en MB."""
#     total = 0
#     for package in packages:
#         files = importlib.metadata.files(package) or []
#         total += sum(f.locate().stat().st_size for f in files if f.locate().exists())
#     return total / 1e6
#
#
# for module in ["scipy.stats", "statsmodels.formula.api"]:
#     import_seconds(module)  # la primera vez, el sistema lee los archivos del disco
#     print(f"import {module}: {import_seconds(module):.2f} s")
# print(f"scipy: {installed_mb('scipy'):.0f} MB")
# print(f"statsmodels, patsy y formulaic: {installed_mb('statsmodels', 'patsy', 'formulaic'):.0f} MB")
