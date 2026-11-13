"""Ejercicio 03 · Validación cruzada: medir con muchos repartos, y elegir cómo repartir.

Ejecuta `uv run python main.py` después de cada paso y compara con el README.
"""

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.model_selection import (
    KFold,
    LeaveOneGroupOut,
    TimeSeriesSplit,
    cross_val_score,
    cross_validate,
    train_test_split,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

print("Ejercicio 03 · Validación cruzada")

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


model = Pipeline([("prepare", prepare()), ("model", Ridge())])


# ============================================
# PASO 1: Diez repartos, diez resultados
# ============================================
# Descomenta las siguientes líneas:
# scores = []
# for seed in range(10):
#     x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=seed)
#     scores.append(model.fit(x_train, y_train).score(x_test, y_test))
# print(f"R² con diez semillas: de {min(scores):.3f} a {max(scores):.3f}")


# ============================================
# PASO 2: Cinco pliegues, frente a la referencia
# ============================================
# Descomenta las siguientes líneas:
# folds = KFold(n_splits=5, shuffle=True, random_state=32)
# r2 = cross_val_score(model, x, y, cv=folds)
# guessed = cross_val_score(DummyRegressor(), x, y, cv=folds)
# print(f"modelo:     {r2.round(3)} · {r2.mean():.3f} ± {r2.std():.3f}")
# print(f"referencia: {guessed.round(3)}")
# print(f"gana en {(r2 > guessed).sum()} de 5 pliegues")


# ============================================
# PASO 3: El error en entrenamiento y en prueba
# ============================================
# Descomenta las siguientes líneas:
# result = cross_validate(
#     model, x, y, cv=folds, scoring="neg_mean_absolute_error", return_train_score=True
# )
# print(f"MAE en prueba:         {-result['test_score'].round(2)}")
# print(f"MAE en entrenamiento:  {-result['train_score'].round(2)}")


# ============================================
# PASO 4: Sin mezclar, con los datos ordenados
# ============================================
# Descomenta las siguientes líneas:
# ranked = air.sort_values("pm25")
# in_order = cross_val_score(model, ranked[inputs], ranked["pm25"], cv=KFold(5))
# print(f"ordenados por PM2.5, sin mezclar: {in_order.round(2)}")
# shuffled = cross_val_score(model, ranked[inputs], ranked["pm25"], cv=folds)
# print(f"ordenados por PM2.5, mezclando:   {shuffled.round(2)}")


# ============================================
# PASO 5: Una zona que nunca vio
# ============================================
# Descomenta las siguientes líneas:
# random_mae = -cross_val_score(model, x, y, cv=folds, scoring="neg_mean_absolute_error")
# print(f"al azar: MAE medio {random_mae.mean():.2f}")
# by_zone = -cross_val_score(
#     model, x, y, cv=LeaveOneGroupOut(), groups=air["zona"], scoring="neg_mean_absolute_error"
# )
# for zone, mae in zip(sorted(air["zona"].unique()), by_zone, strict=True):
#     print(f"{zone} fuera: MAE {mae:.2f}")


# ============================================
# PASO 6: Cuando algo cambia con el tiempo
# ============================================
# Descomenta las siguientes líneas:
# after = (air["momento"] >= "2026-07-01") & (air["zona"] == "Centro")
# changed = y - 8 * after
# center = changed[air["zona"] == "Centro"]
# print(f"Centro, antes y después de julio: {center.groupby(after).mean().round(1).tolist()}")
# for name, splitter in [("al azar", folds), ("por tiempo", TimeSeriesSplit(n_splits=5))]:
#     mae = -cross_val_score(model, x, changed, cv=splitter, scoring="neg_mean_absolute_error")
#     print(f"{name:<10} MAE {mae.round(2)} · media {mae.mean():.2f}")
