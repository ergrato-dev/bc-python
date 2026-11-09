"""Ejercicio 03 · Seleccionar: filas y columnas por etiqueta, por posición y con máscaras.

Ejecuta `uv run python main.py` después de cada paso y compara con el README.
"""

import numpy as np
import pandas as pd

print("Ejercicio 03 · Seleccionar con loc, iloc y máscaras")

READINGS = pd.DataFrame(
    {
        "estacion": ["Norte", "Sur", "Este", "Norte", "Sur", "Este", "Norte", "Sur"],
        "dia": [1, 1, 1, 2, 2, 2, 3, 3],
        "valor": [12.5, 8.0, 48.9, 15.0, np.nan, 52.3, 9.5, 30.1],
    },
    index=pd.RangeIndex(1, 9, name="posicion"),
)


# ============================================
# PASO 1: loc por etiqueta, iloc por posición
# ============================================
# Descomenta las siguientes líneas:
# print(READINGS)
# print("loc[1, 'valor']:", READINGS.loc[1, "valor"], "· iloc[1, 2]:", READINGS.iloc[1, 2])
# print(READINGS.loc[2:4, ["estacion", "valor"]])
# print(READINGS.iloc[1:3, [0, 2]])
# try:
#     READINGS.loc[0]
# except KeyError as problem:
#     print("KeyError:", problem)


# ============================================
# PASO 2: Máscaras
# ============================================
# Descomenta las siguientes líneas:
# high = READINGS["valor"] > 20
# print("máscara:", high.tolist())
# print(READINGS[high])
# print("Norte o Sur y más de 10:", READINGS[READINGS["estacion"].isin(["Norte", "Sur"]) & (READINGS["valor"] > 10)].index.tolist())
# print("entre 10 y 30:", READINGS[READINGS["valor"].between(10, 30)].index.tolist())
# print("no mayor que 20:", READINGS[~high].index.tolist(), "· menor o igual que 20:", READINGS[READINGS["valor"] <= 20].index.tolist())
# try:
#     READINGS[(READINGS["valor"] > 10) and (READINGS["dia"] == 1)]
# except ValueError as problem:
#     print("ValueError:", problem)


# ============================================
# PASO 3: query y loc con máscara
# ============================================
# Descomenta las siguientes líneas:
# print(READINGS.query("dia == 2 and valor > 20"))
# limit = 30
# print("con @limit:", READINGS.query("valor > @limit").index.tolist())
# print(READINGS.loc[READINGS["dia"] == 3, "valor"])


# ============================================
# PASO 4: Otro índice
# ============================================
# Descomenta las siguientes líneas:
# by_station = READINGS.set_index("estacion")
# print(by_station.loc["Este"])
# print("índice único:", by_station.index.is_unique)
# print(by_station.sort_index().head(4))
# print(by_station.reset_index().columns.tolist())


# ============================================
# PASO 5: Ordenar
# ============================================
# Descomenta las siguientes líneas:
# print(READINGS.sort_values("valor", ascending=False).index.tolist())
# print(READINGS.sort_values("valor", na_position="first").index.tolist())
# print(READINGS.sort_values(["estacion", "valor"], ascending=[True, False]).index.tolist())
# print(READINGS.nlargest(2, "valor"))
# ties = pd.DataFrame({"valor": [1.0, 2.0, 1.0] * 20}, index=range(60))
# print("quicksort:", ties.sort_values("valor").index[:6].tolist())
# print("stable:   ", ties.sort_values("valor", kind="stable").index[:6].tolist())


# ============================================
# PASO 6: Cambiar una selección
# ============================================
# Descomenta las siguientes líneas:
# readings = READINGS.copy()
# north = readings[readings["estacion"] == "Norte"]
# north["valor"] = 0.0
# print("north:", north["valor"].tolist(), "· readings:", readings.loc[readings["estacion"] == "Norte", "valor"].tolist())
# readings[readings["estacion"] == "Norte"]["valor"] = 0.0
# print("encadenado:", readings.loc[readings["estacion"] == "Norte", "valor"].tolist())
# readings.loc[readings["estacion"] == "Norte", "valor"] = 0.0
# print("con loc:", readings.loc[readings["estacion"] == "Norte", "valor"].tolist())
