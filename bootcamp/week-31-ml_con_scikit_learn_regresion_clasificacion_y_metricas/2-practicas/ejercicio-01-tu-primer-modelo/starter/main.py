"""Ejercicio 01 · Tu primer modelo: fit, predict y lo que aprende.

Ejecuta `uv run python main.py` después de cada paso y compara con el README.
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor

print("Ejercicio 01 · Tu primer modelo")

# Cincuenta días: horas de sol, nubosidad (0 a 1) y temperatura. La temperatura sube 1,5
# grados por hora de sol y baja 4 con el cielo cubierto, más un ruido de 1,5 grados.
rng = np.random.default_rng(31)
days = pd.DataFrame(
    {"sol": rng.uniform(0, 12, 50).round(1), "nubes": rng.uniform(0, 1, 50).round(2)}
)
noise = rng.normal(0, 1.5, 50)
days["temperatura"] = (12 + 1.5 * days["sol"] - 4 * days["nubes"] + noise).round(1)
print(f"{len(days)} días, columnas: {', '.join(days.columns)}")


# ============================================
# PASO 1: X e y
# ============================================
# Descomenta las siguientes líneas:
# x = days[["sol"]]
# y = days["temperatura"]
# print(f"X: {x.shape} · y: {y.shape}")
# try:
#     LinearRegression().fit(days["sol"], y)
# except ValueError as problem:
#     print(f"con una dimensión: {str(problem).split('. ')[0]}")


# ============================================
# PASO 2: fit y lo aprendido
# ============================================
# Descomenta las siguientes líneas:
# model = LinearRegression()
# print(f"fit devuelve el mismo objeto: {model.fit(x, y) is model}")
# print(f"coef_: {model.coef_.round(3)} · intercept_: {model.intercept_:.3f}")
# slope, intercept = np.polyfit(days["sol"], y, 1)
# print(f"np.polyfit: {slope:.3f} · {intercept:.3f}")


# ============================================
# PASO 3: predict y score
# ============================================
# Descomenta las siguientes líneas:
# new = pd.DataFrame({"sol": [0.0, 6.0, 12.0]})
# print(f"predicciones para 0, 6 y 12 horas: {model.predict(new).round(1)}")
# print(f"a mano, 6 horas: {model.intercept_ + model.coef_[0] * 6:.1f}")
# print(f"R² en los mismos días: {model.score(x, y):.3f}")


# ============================================
# PASO 4: Varias entradas
# ============================================
# Descomenta las siguientes líneas:
# both = LinearRegression().fit(days[["sol", "nubes"]], y)
# print(f"entradas: {list(both.feature_names_in_)} · coef_: {both.coef_.round(2)}")
# print(f"intercept_: {both.intercept_:.2f}")
# print(f"R² con sol y nubes: {both.score(days[['sol', 'nubes']], y):.3f}")


# ============================================
# PASO 5: Una etiqueta, en one-hot
# ============================================
# Descomenta las siguientes líneas:
# zones = pd.DataFrame(
#     {
#         "zona": ["Norte", "Sur", "Norte", "Centro", "Sur", "Sur", "Norte", "Centro"],
#         "valor": [11.0, 30.0, 13.0, 52.0, 34.0, 32.0, 12.0, 48.0],
#     }
# )
# onehot = pd.get_dummies(zones["zona"], dtype="float64")
# print(onehot.head(3))
# by_zone = LinearRegression().fit(onehot, zones["valor"])
# print(
#     f"predice: {dict(zip(zones['zona'], by_zone.predict(onehot).round(2).tolist(), strict=True))}"
# )
# print(f"medias:  {zones.groupby('zona')['valor'].mean().to_dict()}")


# ============================================
# PASO 6: Otro modelo, la misma interfaz
# ============================================
# Descomenta las siguientes líneas:
# neighbors = KNeighborsRegressor(n_neighbors=5).fit(x, y)
# print(f"5 vecinos, para 0, 6 y 12 horas: {neighbors.predict(new).round(1)}")
# print(f"R² de 5 vecinos: {neighbors.score(x, y):.3f}")
# one = KNeighborsRegressor(n_neighbors=1).fit(x, y)
# print(f"R² de 1 vecino: {one.score(x, y):.3f}")
