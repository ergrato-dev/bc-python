"""Ejercicio 01 · Análisis exploratorio con pandas: conocer una tabla antes de calcular nada.

Ejecuta `uv run python main.py` después de cada paso y compara con el README.
"""

from pathlib import Path

import numpy as np
import pandas as pd

print("Ejercicio 01 · Análisis exploratorio con pandas")

# Tres estaciones, 60 días, una medida al día: lo que llegaría de verdad de unos sensores.
# Tú no lo sabes todavía, pero la tabla tiene cuatro problemas escondidos. Encuéntralos.
rng = np.random.default_rng(29)
days = pd.date_range("2026-03-01", periods=60, freq="D")
parts = []
for station, level in [("Norte", 14.0), ("Sur", 19.0), ("Este", 16.0)]:
    temperature = level + 0.08 * np.arange(60) + rng.normal(0, 1.5, 60)
    humidity = 80 - 1.5 * (temperature - level) + rng.normal(0, 4, 60)
    parts.append(pd.DataFrame({"fecha": days.strftime("%Y-%m-%d"), "estacion": station,
                               "temperatura": temperature.round(1), "humedad": humidity.round()}))
raw = pd.concat(parts, ignore_index=True)
raw.loc[raw["estacion"] == "Este", "temperatura"] = (raw["temperatura"] * 9 / 5 + 32).round(1)
raw.loc[rng.choice(len(raw), 9, replace=False), "temperatura"] = np.nan
raw.loc[rng.choice(len(raw), 4, replace=False), "humedad"] = 999
for station, typos in [("Norte", ["norte ", "NORTE"]), ("Sur", ["sur", "Sur "])]:
    rows = rng.choice(raw.index[raw["estacion"] == station], 6, replace=False)
    raw.loc[rows, "estacion"] = typos * 3
raw = pd.concat([raw, raw.sample(6, random_state=29)], ignore_index=True)
# salida/ no va a Git: el archivo se vuelve a escribir en cada ejecución.
Path("salida").mkdir(exist_ok=True)
raw.to_csv("salida/medidas.csv", index=False)

frame = pd.read_csv("salida/medidas.csv")
print(f"medidas.csv: {frame.shape[0]} filas, {frame.shape[1]} columnas")


# ============================================
# PASO 1: Forma y tipos
# ============================================
# Descomenta las siguientes líneas:
# print(frame.head(3))
# print(frame.dtypes.to_dict())
# frame["fecha"] = pd.to_datetime(frame["fecha"], format="%Y-%m-%d")
# print(f"de {frame['fecha'].min():%Y-%m-%d} a {frame['fecha'].max():%Y-%m-%d}")


# ============================================
# PASO 2: Lo que falta
# ============================================
# Descomenta las siguientes líneas:
# print(frame.isna().sum().to_dict())
# print(f"filas con algún hueco: {frame.isna().any(axis=1).sum()} de {len(frame)}")
# print(frame[["temperatura", "humedad"]].describe().round(1))


# ============================================
# PASO 3: Etiquetas mal escritas y filas repetidas
# ============================================
# Descomenta las siguientes líneas:
# print(frame["estacion"].value_counts().to_dict())
# frame["estacion"] = frame["estacion"].str.strip().str.title()
# print(frame["estacion"].value_counts().to_dict())
# repeated = frame.duplicated()
# print(f"filas repetidas: {repeated.sum()}")
# frame = frame[~repeated]
# print(f"quedan {len(frame)} filas, {frame.duplicated(['fecha', 'estacion']).sum()} días repetidos")


# ============================================
# PASO 4: Un valor que significa "sin dato"
# ============================================
# Descomenta las siguientes líneas:
# print(frame["humedad"].value_counts().sort_index().tail(3).to_dict())
# frame["humedad"] = frame["humedad"].replace(999, np.nan)
# print(f"humedad: máximo {frame['humedad'].max():.0f} %, huecos {frame['humedad'].isna().sum()}")


# ============================================
# PASO 5: Distribuciones por grupo
# ============================================
# Descomenta las siguientes líneas:
# by_station = frame.groupby("estacion")["temperatura"]
# print(by_station.describe().round(1))
# counts, edges = np.histogram(frame["temperatura"].dropna(), bins=6)
# for count, low, high in zip(counts, edges, edges[1:], strict=False):
#     print(f"{low:5.1f} – {high:5.1f} {'#' * (count // 4)}")
# frame["temperatura"] = frame["temperatura"].where(
#     frame["estacion"] != "Este", ((frame["temperatura"] - 32) * 5 / 9).round(1)
# )
# print(frame.groupby("estacion")["temperatura"].mean().round(1).to_dict())


# ============================================
# PASO 6: Atípicos y relaciones
# ============================================
# Descomenta las siguientes líneas:
# q1, q3 = frame["temperatura"].quantile([0.25, 0.75])
# fence = 1.5 * (q3 - q1)
# outside = frame[(frame["temperatura"] < q1 - fence) | (frame["temperatura"] > q3 + fence)]
# print(f"Tukey: fuera de [{q1 - fence:.1f}, {q3 + fence:.1f}] hay {len(outside)} medidas")
# print(f"correlación temperatura-humedad, todo junto: {frame['temperatura'].corr(frame['humedad']):.2f}")
# within = frame.groupby("estacion")[["temperatura", "humedad"]].corr().xs("temperatura", level=1)
# print("dentro de cada estación:", within["humedad"].round(2).to_dict())
