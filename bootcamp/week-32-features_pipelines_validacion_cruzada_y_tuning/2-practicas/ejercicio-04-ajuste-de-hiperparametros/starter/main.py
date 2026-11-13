"""Ejercicio 04 · Ajuste de hiperparámetros: buscar el mejor valor, y medirlo sin hacer trampa.

Ejecuta `uv run python main.py` después de cada paso y compara con el README.
"""

import numpy as np
import pandas as pd
from scipy.stats import randint
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.model_selection import (
    GridSearchCV,
    KFold,
    RandomizedSearchCV,
    StratifiedKFold,
    cross_val_score,
    validation_curve,
)
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

print("Ejercicio 04 · Ajuste de hiperparámetros")

# Medidas horarias de partículas finas (PM2.5) en cuatro zonas: más en hora punta y entre
# semana, menos con humedad alta. La humedad a veces falta.
rng = np.random.default_rng(32)
n = 1200
hours = np.sort(rng.integers(0, 300 * 24, n))
air = pd.DataFrame(
    {
        "momento": pd.Timestamp("2026-01-05") + pd.to_timedelta(hours, unit="h"),
        "zona": rng.choice(["Centro", "Norte", "Sur", "Este"], n, p=[0.3, 0.3, 0.3, 0.1]),
        "humedad": rng.uniform(30, 95, n).round(),
    }
)
rush = np.isin(air["momento"].dt.hour, [7, 8, 9, 18, 19, 20])
weekday = air["momento"].dt.day_of_week < 5
zone = air["zona"].map({"Centro": 12.0, "Norte": 4.0, "Sur": 0.0, "Este": 6.0})
noise = rng.normal(0, 3, n)
air["pm25"] = (10 + zone + 8 * rush + 4 * weekday - 0.1 * air["humedad"] + noise).round(1)
air.loc[rng.random(n) < 0.08, "humedad"] = np.nan
print(f"{len(air)} medidas · de {air['momento'].min():%d/%m} a {air['momento'].max():%d/%m}")

air["hora"] = air["momento"].dt.hour
air["finde"] = (air["momento"].dt.day_of_week >= 5).astype(int)
air["punta"] = air["hora"].isin([7, 8, 9, 18, 19, 20]).astype(int)
inputs = ["zona", "humedad", "hora", "finde", "punta"]
x, y = air[inputs], air["pm25"]


def prepare() -> ColumnTransformer:
    """La preparación del ejercicio 01, sin ajustar."""
    return ColumnTransformer(
        [
            ("zona", OneHotEncoder(handle_unknown="ignore"), ["zona"]),
            ("humedad", SimpleImputer(strategy="median", add_indicator=True), ["humedad"]),
            ("hora", StandardScaler(), ["hora"]),
            ("tal_cual", "passthrough", ["finde", "punta"]),
        ]
    )


model = Pipeline([("prepare", prepare()), ("model", KNeighborsRegressor())])
folds = KFold(n_splits=5, shuffle=True, random_state=32)
scoring = "neg_mean_absolute_error"


# ============================================
# PASO 1: La curva de validación
# ============================================
# Descomenta las siguientes líneas:
# neighbors = [1, 3, 10, 30, 100, 300]
# train, test = validation_curve(
#     model, x, y, param_name="model__n_neighbors", param_range=neighbors, cv=folds, scoring=scoring
# )
# for k, train_mae, test_mae in zip(neighbors, -train.mean(axis=1), -test.mean(axis=1), strict=True):
#     print(f"n_neighbors={k:<4} MAE entrenamiento {train_mae:.2f} · validación {test_mae:.2f}")


# ============================================
# PASO 2: Una rejilla con dos hiperparámetros
# ============================================
# Descomenta las siguientes líneas:
# grid = {"model__n_neighbors": [2, 3, 5, 10], "model__weights": ["uniform", "distance"]}
# search = GridSearchCV(model, grid, cv=folds, scoring=scoring)
# search.fit(x, y)
# print(f"{len(search.cv_results_['params'])} combinaciones · mejor: {search.best_params_}")
# results = pd.DataFrame(search.cv_results_).sort_values("rank_test_score").head(3)
# for _, row in results.iterrows():
#     print(f"  {row['params']} · MAE {-row['mean_test_score']:.3f} ± {row['std_test_score']:.3f}")


# ============================================
# PASO 3: Probar al azar
# ============================================
# Descomenta las siguientes líneas:
# randomized = RandomizedSearchCV(
#     model,
#     {"model__n_neighbors": randint(1, 200), "model__weights": ["uniform", "distance"]},
#     n_iter=15,
#     cv=folds,
#     scoring=scoring,
#     random_state=32,
# )
# randomized.fit(x, y)
# print(f"al azar, 15 intentos: {randomized.best_params_} · MAE {-randomized.best_score_:.3f}")


# ============================================
# PASO 4: Un ganador con suerte
# ============================================
# Descomenta las siguientes líneas:
# blind = Pipeline([("scale", StandardScaler()), ("model", KNeighborsClassifier())])
# inner = StratifiedKFold(n_splits=5, shuffle=True, random_state=32)
# attempts = []
# for attempt in range(1, 6):
#     junk, label = rng.normal(size=(80, 10)), rng.choice(["alto", "normal"], 80)
#     lucky = GridSearchCV(
#         blind, {"model__n_neighbors": list(range(1, 31))}, cv=inner, scoring="balanced_accuracy"
#     )
#     lucky.fit(junk, label)
#     attempts.append((lucky, junk, label))
#     print(f"intento {attempt}: {lucky.best_params_} · best_score_ {lucky.best_score_:.3f}")


# ============================================
# PASO 5: Validación anidada
# ============================================
# Descomenta las siguientes líneas:
# outer = StratifiedKFold(n_splits=5, shuffle=True, random_state=55)
# for attempt, (lucky, junk, label) in enumerate(attempts, start=1):
#     nested = cross_val_score(lucky, junk, label, cv=outer, scoring="balanced_accuracy")
#     print(f"intento {attempt}: anidada {nested.mean():.3f}")


# ============================================
# PASO 6: ¿Vecinos o Ridge?
# ============================================
# Descomenta las siguientes líneas:
# outer_folds = KFold(n_splits=5, shuffle=True, random_state=55)
# neighbors_mae = -cross_val_score(search, x, y, cv=outer_folds, scoring=scoring)
# ridge = Pipeline([("prepare", prepare()), ("model", Ridge())])
# alphas = {"model__alpha": [0.01, 0.1, 1, 10, 100]}
# ridge_search = GridSearchCV(ridge, alphas, cv=folds, scoring=scoring)
# ridge_mae = -cross_val_score(ridge_search, x, y, cv=outer_folds, scoring=scoring)
# print(f"vecinos, anidada: MAE {neighbors_mae.round(2)} · media {neighbors_mae.mean():.2f}")
# print(f"Ridge, anidada:   MAE {ridge_mae.round(2)} · media {ridge_mae.mean():.2f}")
