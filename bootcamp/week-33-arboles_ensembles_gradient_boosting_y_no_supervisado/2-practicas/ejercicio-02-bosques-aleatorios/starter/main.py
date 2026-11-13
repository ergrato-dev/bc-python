"""Ejercicio 02 · Bosques aleatorios: muchos árboles distintos, una media.

Ejecuta `uv run python main.py` después de cada paso y compara con el README.
"""

import time

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.inspection import permutation_importance
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeRegressor

print("Ejercicio 02 · Bosques aleatorios")

# Medidas horarias de partículas finas (PM2.5) en cuatro zonas. Sube en hora punta (mucho
# más en el Centro, por el tráfico), con el aire en calma (viento < 2 m/s) y baja con lluvia
# (humedad > 85 %). Son umbrales y cruces, no rectas.
rng = np.random.default_rng(33)
n = 1500
hours = np.sort(rng.integers(0, 300 * 24, n))
air = pd.DataFrame(
    {
        "momento": pd.Timestamp("2026-01-05") + pd.to_timedelta(hours, unit="h"),
        "zona": rng.choice(["Centro", "Norte", "Sur", "Este"], n),
        "humedad": rng.uniform(30, 98, n).round(),
        "viento": rng.gamma(2.0, 2.0, n).round(1),
    }
)
air["hora"] = air["momento"].dt.hour
air["dia"] = air["momento"].dt.day_of_week
rush = air["hora"].isin([7, 8, 9, 18, 19, 20])
center = air["zona"] == "Centro"
zone = air["zona"].map({"Centro": 10.0, "Norte": 4.0, "Sur": 0.0, "Este": 6.0})
traffic = rush * np.where(center, 14.0, 4.0)
air["pm25"] = (
    12 + zone + traffic + 10 * (air["viento"] < 2) - 8 * (air["humedad"] > 85) + rng.normal(0, 3, n)
).round(1)
print(f"{len(air)} medidas · de {air['momento'].min():%d/%m} a {air['momento'].max():%d/%m}")

# Una columna de ruido: números al azar que no tienen nada que ver con el PM2.5.
air["ruido"] = rng.uniform(0, 100, n).round(1)
x = air[["hora", "dia", "zona", "humedad", "viento", "ruido"]]
y = air["pm25"]
folds = KFold(5, shuffle=True, random_state=33)
scoring = "neg_mean_absolute_error"


def pipe(model: object) -> Pipeline:
    """La zona en one-hot y el resto tal cual, delante del modelo."""
    prepare = ColumnTransformer(
        [("zona", OneHotEncoder(handle_unknown="ignore"), ["zona"])],
        remainder="passthrough",
        verbose_feature_names_out=False,
    )
    return Pipeline([("prepare", prepare), ("model", model)])


# ============================================
# PASO 1: Un árbol cambia con cada muestra
# ============================================
# Descomenta las siguientes líneas:
# one = x.iloc[[0]]
# print(one.to_string(index=False), f"· PM2.5 de verdad {y.iloc[0]}")
# for name, make in [
#     ("árbol", lambda seed: DecisionTreeRegressor(random_state=seed)),
#     ("bosque", lambda seed: RandomForestRegressor(100, random_state=seed)),
# ]:
#     guesses = []
#     for seed in range(5):
#         train_x, _, train_y, _ = train_test_split(x.iloc[1:], y.iloc[1:], random_state=seed)
#         guesses.append(pipe(make(seed)).fit(train_x, train_y).predict(one)[0])
#     print(f"{name:<6} con cinco muestras: {np.round(guesses, 1)}")


# ============================================
# PASO 2: Un bosque frente a sus árboles
# ============================================
# Descomenta las siguientes líneas:
# models = [
#     ("árbol sin límite", DecisionTreeRegressor(random_state=33)),
#     ("árbol, max_depth=6", DecisionTreeRegressor(max_depth=6, random_state=33)),
#     ("bosque de 100", RandomForestRegressor(100, random_state=33)),
# ]
# for name, model in models:
#     mae = -cross_val_score(pipe(model), x, y, cv=folds, scoring=scoring)
#     print(f"{name:<18} MAE medio {mae.mean():.2f}")


# ============================================
# PASO 3: Cuántos árboles
# ============================================
# Descomenta las siguientes líneas:
# for trees in [1, 5, 20, 100, 300]:
#     start = time.perf_counter()
#     mae = -cross_val_score(
#         pipe(RandomForestRegressor(trees, random_state=33)), x, y, cv=folds, scoring=scoring
#     )
#     print(f"{trees:>3} árboles: MAE {mae.mean():.2f} · {time.perf_counter() - start:.1f} s")


# ============================================
# PASO 4: La nota sin validación cruzada: out-of-bag
# ============================================
# Descomenta las siguientes líneas:
# forest = pipe(RandomForestRegressor(100, oob_score=True, random_state=33)).fit(x, y)
# r2 = cross_val_score(pipe(RandomForestRegressor(100, random_state=33)), x, y, cv=folds)
# oob = forest.named_steps["model"].oob_score_
# print(f"R² out-of-bag {oob:.3f} · validación cruzada {r2.mean():.3f}")


# ============================================
# PASO 5: Importancias por impureza
# ============================================
# Descomenta las siguientes líneas:
# names = forest.named_steps["prepare"].get_feature_names_out()
# impurity = pd.Series(forest.named_steps["model"].feature_importances_, index=names)
# print(impurity.sort_values(ascending=False).round(3).to_string())


# ============================================
# PASO 6: Importancias por permutación
# ============================================
# Descomenta las siguientes líneas:
# train_x, test_x, train_y, test_y = train_test_split(x, y, random_state=33)
# fitted = pipe(RandomForestRegressor(100, random_state=33)).fit(train_x, train_y)
# shuffled = permutation_importance(
#     fitted, test_x, test_y, scoring=scoring, n_repeats=10, random_state=33
# )
# permuted = pd.Series(shuffled.importances_mean, index=x.columns)
# print("cuánto sube el MAE al barajar cada columna:")
# print(permuted.sort_values(ascending=False).round(2).to_string())
