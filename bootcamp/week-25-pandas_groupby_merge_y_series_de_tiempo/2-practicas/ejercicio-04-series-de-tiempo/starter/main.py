"""Ejercicio 04 · Series de tiempo: fechas, un índice de tiempo, resample y rolling.

Ejecuta `uv run python main.py` después de cada paso y compara con el README.
"""

from datetime import datetime

import pandas as pd

print("Ejercicio 04 · Series de tiempo")

# lecturas.csv: fecha (día/mes/año hora:minuto), estación y valor, con coma decimal. Las
# medidas no llegan a intervalos fijos, una no tiene valor y la última no tiene fecha.
raw = pd.read_csv("lecturas.csv", sep=";", decimal=",")


# ============================================
# PASO 1: De texto a fecha
# ============================================
# Descomenta las siguientes líneas:
# print("tipo leído:", raw["fecha"].dtype, "·", raw["fecha"].iloc[0])
# print("sin formato:", pd.to_datetime("03/11/2026"), "· dayfirst:", pd.to_datetime("03/11/2026", dayfirst=True))
# try:
#     pd.to_datetime(raw["fecha"], format="%d/%m/%Y %H:%M")
# except ValueError as problem:
#     print("ValueError:", str(problem).split(". ")[0])
# raw["time"] = pd.to_datetime(raw["fecha"], format="%d/%m/%Y %H:%M", errors="coerce")
# print("tipo:", raw["time"].dtype, "· sin fecha:", raw.loc[raw["time"].isna(), "fecha"].tolist())
# readings = raw.dropna(subset=["time"]).drop(columns="fecha").rename(columns={"estacion": "station", "valor": "value"})


# ============================================
# PASO 2: Instantes y duraciones
# ============================================
# Descomenta las siguientes líneas:
# first = readings["time"].iloc[0]
# print(type(first).__name__, first, "· hora:", first.hour, "· día:", first.day_name())
# gaps = readings["time"].diff()
# print("huecos:", gaps.iloc[1], "· el mayor:", gaps.max(), "· tipo:", gaps.dtype)
# print("más 90 min:", first + pd.Timedelta("90min"), "· ¿igual?", pd.Timedelta("90min") == pd.Timedelta(hours=1.5))
# print(pd.date_range(datetime(2026, 11, 1), periods=4, freq="6h").strftime("%d %H:%M").tolist())


# ============================================
# PASO 3: Un índice de tiempo
# ============================================
# Descomenta las siguientes líneas:
# timed = readings.set_index("time").sort_index()
# print(type(timed.index).__name__, "· ¿ordenado?", timed.index.is_monotonic_increasing)
# print("el día 2:", timed.loc["2026-11-02", "value"].tolist())
# print("de 11:00 a 08:00:", timed.loc["2026-11-01 11:00":"2026-11-02 08:00", "station"].tolist())
# print("por la mañana:", timed.between_time("07:00", "12:00")["value"].tolist())


# ============================================
# PASO 4: resample, medias por periodo
# ============================================
# Descomenta las siguientes líneas:
# north = timed.loc[timed["station"] == "Norte", "value"]
# print(north.resample("6h").mean())
# print("cuántas:", north.resample("6h").count().tolist())
# print("desde la primera:", north.resample("6h", origin="start").mean().index.strftime("%d %H:%M").tolist())
# print(timed.pivot(columns="station", values="value").resample("1D").agg(["mean", "max"]))


# ============================================
# PASO 5: rolling, shift y diff
# ============================================
# Descomenta las siguientes líneas:
# print("rolling(2):  ", north.rolling(2).mean().tolist())
# print("rolling(\"6h\"):", north.rolling("6h").mean().round(2).tolist())
# print("shift(1):    ", north.shift(1).tolist())
# print("diff():      ", north.diff().tolist())
# print("cada 12 h:   ", north.dropna().asfreq("12h").tolist())


# ============================================
# PASO 6: Zonas horarias
# ============================================
# Descomenta las siguientes líneas:
# local = timed.index.tz_localize("America/Bogota")
# print("Bogotá:", local[0], "· UTC:", local.tz_convert("UTC")[0])
# madrid = pd.date_range("2026-10-25 01:00", periods=3, freq="1h", tz="Europe/Madrid")
# print("Madrid, cambio de hora:", madrid.strftime("%H:%M %Z").tolist())
# try:
#     print(timed.index[0] < local[0])
# except TypeError as problem:
#     print("TypeError:", problem)
