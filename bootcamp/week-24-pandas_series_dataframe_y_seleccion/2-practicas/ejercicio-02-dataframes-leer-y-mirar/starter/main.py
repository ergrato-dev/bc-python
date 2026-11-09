"""Ejercicio 02 · DataFrames: crear una tabla, leerla de un CSV y mirarla antes de usarla.

Ejecuta `uv run python main.py` después de cada paso y compara con el README.
"""

from pathlib import Path

import pandas as pd

print("Ejercicio 02 · DataFrames: leer y mirar")


# ============================================
# PASO 1: Una tabla desde un diccionario
# ============================================
# Descomenta las siguientes líneas:
# table = pd.DataFrame(
#     {"estacion": ["Norte", "Sur", "Este"], "valor": [12.5, 8.0, 48.9], "sensores": [3, 1, 2]}
# )
# print(table)
# print("forma:", table.shape, "· columnas:", table.columns.tolist())
# print(table.dtypes)
# print("una columna es una Series:", type(table["valor"]).__name__)


# ============================================
# PASO 2: Leer un CSV, a la tercera
# ============================================
# Descomenta las siguientes líneas:
# path = Path("estaciones.csv")
# print("sin sep:", pd.read_csv(path).columns.tolist())
# print("con sep:", pd.read_csv(path, sep=";")["valor"].dtype)
# stations = pd.read_csv(path, sep=";", decimal=",")
# print("con decimal:", stations["valor"].dtype)
# print("países que faltan:", stations["pais"].isna().sum(), "·", stations["pais"].unique().tolist())
# stations = pd.read_csv(
#     path, sep=";", decimal=",", keep_default_na=False, na_values={"valor": ["NA"]}
# )
# print("bien:", stations["pais"].unique().tolist(), "· valores que faltan:", stations["valor"].isna().sum())


# ============================================
# PASO 3: Mirar una tabla antes de usarla
# ============================================
# Descomenta las siguientes líneas:
# print(stations.head(3))
# stations.info()
# print(stations.describe())


# ============================================
# PASO 4: Columnas nuevas, con otro nombre o fuera
# ============================================
# Descomenta las siguientes líneas:
# print(stations[["estacion", "valor"]].tail(2))
# stations["fahrenheit"] = stations["valor"] * 9 / 5 + 32
# print(stations["fahrenheit"].round(1).tolist())
# hot = stations.assign(caliente=stations["valor"] > 25)
# print("caliente:", hot["caliente"].tolist())
# print("¿assign cambió stations?", "caliente" in stations.columns)
# print(stations.rename(columns={"valor": "celsius"}).drop(columns=["pais", "dia"]).head(2))


# ============================================
# PASO 5: Una fila mala lo cambia todo
# ============================================
# Descomenta las siguientes líneas:
# broken = pd.read_csv("rota.csv", sep=";", decimal=",")
# print("tipo de valor:", broken["valor"].dtype, "·", broken["valor"].tolist())
# numbers = pd.to_numeric(broken["valor"].str.replace(",", "."), errors="coerce")
# print("convertidos:", numbers.tolist())
# print(broken[numbers.isna()])


# ============================================
# PASO 6: Escribirla y leerla otra vez
# ============================================
# Descomenta las siguientes líneas:
# original = stations[["estacion", "pais", "dia", "valor"]]
# output = Path("salida.csv")
# original.to_csv(output, sep=";", decimal=",", na_rep="NA", index=False)
# print(output.read_text(encoding="utf-8").splitlines()[:3])
# again = pd.read_csv(
#     output, sep=";", decimal=",", keep_default_na=False, na_values={"valor": ["NA"]}
# )
# print("¿igual?", again.equals(original))
