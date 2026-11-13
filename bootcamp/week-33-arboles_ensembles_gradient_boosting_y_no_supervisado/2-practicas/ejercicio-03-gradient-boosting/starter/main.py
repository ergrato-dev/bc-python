"""Ejercicio 03 · Gradient boosting: cada árbol corrige al anterior.

Ejecuta `uv run python main.py` después de cada paso y compara con el README.
"""

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.ensemble import (
    GradientBoostingRegressor,
    HistGradientBoostingClassifier,
    HistGradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import KFold, StratifiedKFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeRegressor

print("Ejercicio 03 · Gradient boosting")

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

x = air[["hora", "dia", "zona", "humedad", "viento"]]
y = air["pm25"]
folds = KFold(5, shuffle=True, random_state=33)
scoring = "neg_mean_absolute_error"
train_x, test_x, train_y, test_y = train_test_split(x, y, random_state=33)


def pipe(model: object, scale: bool = False) -> Pipeline:
    """La zona en one-hot; el resto, tal cual o escalado (para los modelos lineales)."""
    numbers = ["hora", "dia", "humedad", "viento"]
    prepare = ColumnTransformer(
        [
            ("zona", OneHotEncoder(handle_unknown="ignore"), ["zona"]),
            ("numeros", StandardScaler() if scale else "passthrough", numbers),
        ]
    )
    return Pipeline([("prepare", prepare), ("model", model)])


# ============================================
# PASO 1: Árbol a árbol
# ============================================
# Descomenta las siguientes líneas:
# boosting = pipe(GradientBoostingRegressor(n_estimators=300, max_depth=3, random_state=33))
# boosting.fit(train_x, train_y)
# prepared_train = boosting.named_steps["prepare"].transform(train_x)
# prepared_test = boosting.named_steps["prepare"].transform(test_x)
# model = boosting.named_steps["model"]
# stages = zip(model.staged_predict(prepared_train), model.staged_predict(prepared_test), strict=True)
# for number, (train_pred, test_pred) in enumerate(stages, start=1):
#     if number in [1, 10, 50, 100, 300]:
#         train_mae = mean_absolute_error(train_y, train_pred)
#         test_mae = mean_absolute_error(test_y, test_pred)
#         print(f"{number:>3} árboles: MAE entrenamiento {train_mae:.2f} · prueba {test_mae:.2f}")


# ============================================
# PASO 2: El ritmo de aprendizaje
# ============================================
# Descomenta las siguientes líneas:
# for rate in [1.0, 0.3, 0.1, 0.03]:
#     model = GradientBoostingRegressor(n_estimators=100, learning_rate=rate, random_state=33)
#     mae = -cross_val_score(pipe(model), x, y, cv=folds, scoring=scoring)
#     print(f"learning_rate={rate:<4} · 100 árboles · MAE {mae.mean():.2f}")


# ============================================
# PASO 3: Parar a tiempo
# ============================================
# Descomenta las siguientes líneas:
# stopping = HistGradientBoostingRegressor(
#     max_iter=1000,
#     early_stopping=True,
#     validation_fraction=0.2,
#     n_iter_no_change=10,
#     random_state=33,
# )
# stopping = pipe(stopping).fit(train_x, train_y)
# used = stopping.named_steps["model"].n_iter_
# test_mae = mean_absolute_error(test_y, stopping.predict(test_x))
# print(f"de 1000 árboles posibles usa {used} · MAE prueba {test_mae:.2f}")


# ============================================
# PASO 4: Categorías y huecos, sin preparar
# ============================================
# Descomenta las siguientes líneas:
# raw = x.astype({"zona": "category"})
# raw.loc[raw.sample(frac=0.1, random_state=33).index, "humedad"] = np.nan
# native = HistGradientBoostingRegressor(categorical_features="from_dtype", random_state=33)
# mae = -cross_val_score(native, raw, y, cv=folds, scoring=scoring)
# print(f"zona como categoría y un 10 % de humedad sin dato: MAE {mae.mean():.2f}")


# ============================================
# PASO 5: Cinco modelos, los mismos pliegues
# ============================================
# Descomenta las siguientes líneas:
# contenders = [
#     ("referencia", pipe(DummyRegressor())),
#     ("lineal", pipe(Ridge(), scale=True)),
#     ("árbol", pipe(DecisionTreeRegressor(max_depth=6, random_state=33))),
#     ("bosque", pipe(RandomForestRegressor(100, random_state=33))),
#     ("boosting", pipe(HistGradientBoostingRegressor(random_state=33))),
# ]
# for name, model in contenders:
#     mae = -cross_val_score(model, x, y, cv=folds, scoring=scoring)
#     print(f"{name:<10} MAE {mae.round(2)} · media {mae.mean():.2f}")


# ============================================
# PASO 6: Clasificar las horas de aire malo
# ============================================
# Descomenta las siguientes líneas:
# bad = (y > 35).rename("malo")
# print(f"{bad.mean():.0%} de las horas, PM2.5 por encima de 35")
# stratified = StratifiedKFold(5, shuffle=True, random_state=33)
# for name, model in [
#     ("referencia", pipe(DummyClassifier())),
#     ("logística", pipe(LogisticRegression(), scale=True)),
#     ("boosting", pipe(HistGradientBoostingClassifier(random_state=33))),
# ]:
#     score = cross_val_score(model, x, bad, cv=stratified, scoring="balanced_accuracy")
#     print(f"{name:<10} exactitud equilibrada {score.mean():.3f}")
