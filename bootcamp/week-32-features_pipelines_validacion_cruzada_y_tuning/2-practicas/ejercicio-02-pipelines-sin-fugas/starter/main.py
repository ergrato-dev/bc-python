"""Ejercicio 02 · Pipelines sin fugas: la preparación y el modelo, un solo estimador.

Ejecuta `uv run python main.py` después de cada paso y compara con el README.
"""

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

print("Ejercicio 02 · Pipelines sin fugas")

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
x_train, x_test, y_train, y_test = train_test_split(
    air[inputs], air["pm25"], test_size=0.25, random_state=32
)


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


# ============================================
# PASO 1: Un pipeline
# ============================================
# Descomenta las siguientes líneas:
# model = Pipeline([("prepare", prepare()), ("model", Ridge(alpha=1.0))])
# model.fit(x_train, y_train)
# print(f"R² en prueba: {model.score(x_test, y_test):.3f}")
# print(f"MAE en prueba: {mean_absolute_error(y_test, model.predict(x_test)):.2f}")


# ============================================
# PASO 2: Predecir con la tabla original
# ============================================
# Descomenta las siguientes líneas:
# new = pd.DataFrame(
#     {
#         "zona": ["Centro", "Centro", "Puerto"],
#         "humedad": [50.0, np.nan, 50.0],
#         "hora": [8, 8, 8],
#         "finde": [0, 0, 0],
#         "punta": [1, 1, 1],
#     }
# )
# print(model.predict(new).round(1))


# ============================================
# PASO 3: Qué aprendió
# ============================================
# Descomenta las siguientes líneas:
# names = model.named_steps["prepare"].get_feature_names_out()
# coefs = model.named_steps["model"].coef_
# for name, coef in sorted(zip(names, coefs, strict=True), key=lambda pair: -abs(pair[1])):
#     print(f"{name:<36} {coef:6.2f}")


# ============================================
# PASO 4: Cambiar un paso
# ============================================
# Descomenta las siguientes líneas:
# for alpha in [1.0, 100.0, 10_000.0]:
#     model.set_params(model__alpha=alpha).fit(x_train, y_train)
#     print(f"alpha={alpha:<8g} R² {model.score(x_test, y_test):.3f}")


# ============================================
# PASO 5: La fuga de elegir columnas
# ============================================
# Descomenta las siguientes líneas:
# x_junk = rng.normal(size=(100, 2000))
# y_level = rng.choice(["alto", "normal"], 100)
# picked = SelectKBest(f_classif, k=10).fit_transform(x_junk, y_level)
# leaky = cross_val_score(LogisticRegression(), picked, y_level, cv=5, scoring="balanced_accuracy")
# print(f"eligiendo antes de validar: {leaky.mean():.2f}")
# honest = Pipeline([("select", SelectKBest(f_classif, k=10)), ("model", LogisticRegression())])
# fair = cross_val_score(honest, x_junk, y_level, cv=5, scoring="balanced_accuracy")
# print(f"eligiendo dentro del pipeline: {fair.mean():.2f}")
