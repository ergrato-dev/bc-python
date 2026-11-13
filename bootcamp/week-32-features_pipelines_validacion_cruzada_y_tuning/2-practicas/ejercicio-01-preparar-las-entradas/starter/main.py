"""Ejercicio 01 · Preparar las entradas: de las columnas a las features.

Ejecuta `uv run python main.py` después de cada paso y compara con el README.
"""

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler

print("Ejercicio 01 · Preparar las entradas")

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


# ============================================
# PASO 1: Mirar los datos
# ============================================
# Descomenta las siguientes líneas:
# print(air.head(3).to_string())
# print(f"huecos: {air.isna().sum().to_dict()}")


# ============================================
# PASO 2: Derivar entradas de la fecha
# ============================================
# Descomenta las siguientes líneas:
# air["hora"] = air["momento"].dt.hour
# air["finde"] = (air["momento"].dt.day_of_week >= 5).astype(int)
# air["punta"] = air["hora"].isin([7, 8, 9, 18, 19, 20]).astype(int)
# by_rush = air.groupby("punta")["pm25"].mean().round(1).tolist()
# by_weekend = air.groupby("finde")["pm25"].mean().round(1).tolist()
# print(f"PM2.5 medio, fuera y en hora punta: {by_rush}")
# print(f"PM2.5 medio, entre semana y en finde: {by_weekend}")


# ============================================
# PASO 3: Escalar con el entrenamiento
# ============================================
# Descomenta las siguientes líneas:
# train, test = train_test_split(air, test_size=0.25, random_state=32)
# scaler = StandardScaler().fit(train[["hora"]])
# print(f"media {scaler.mean_[0]:.2f} · desviación {scaler.scale_[0]:.2f}")
# scaled = scaler.transform(test[["hora"]])
# print(f"la hora de prueba, escalada: de {scaled.min():.2f} a {scaled.max():.2f}")


# ============================================
# PASO 4: Codificar la zona
# ============================================
# Descomenta las siguientes líneas:
# encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False).fit(train[["zona"]])
# print(f"zonas aprendidas: {encoder.categories_[0].tolist()}")
# print(encoder.transform(pd.DataFrame({"zona": ["Sur", "Puerto"]})))


# ============================================
# PASO 5: Rellenar la humedad
# ============================================
# Descomenta las siguientes líneas:
# imputer = SimpleImputer(strategy="median", add_indicator=True).fit(train[["humedad"]])
# print(f"mediana del entrenamiento: {imputer.statistics_[0]}")
# print(imputer.get_feature_names_out())
# sample = pd.concat([test[test["humedad"].isna()].head(1), test[test["humedad"].notna()].head(1)])
# print(imputer.transform(sample[["humedad"]]))


# ============================================
# PASO 6: Todo junto, columna a columna
# ============================================
# Descomenta las siguientes líneas:
# prepare = ColumnTransformer(
#     [
#         ("zona", OneHotEncoder(handle_unknown="ignore"), ["zona"]),
#         ("humedad", SimpleImputer(strategy="median", add_indicator=True), ["humedad"]),
#         ("hora", StandardScaler(), ["hora"]),
#         ("tal_cual", "passthrough", ["finde", "punta"]),
#     ]
# )
# ready = prepare.fit(train).transform(test)
# print(f"la prueba, preparada: {ready.shape[0]} filas × {ready.shape[1]} columnas")
# for name in prepare.get_feature_names_out():
#     print(f"  {name}")
