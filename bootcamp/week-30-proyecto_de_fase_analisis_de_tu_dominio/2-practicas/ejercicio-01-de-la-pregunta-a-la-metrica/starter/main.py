"""Ejercicio 01 · De la pregunta a la métrica: la misma tabla, tres respuestas.

Ejecuta `uv run python main.py` después de cada paso y compara con el README.
"""

import numpy as np
import pandas as pd
from scipy import stats

print("Ejercicio 01 · De la pregunta a la métrica")

# Dos zonas con dos sensores cada una, en invierno y en verano. No leas cómo se genera:
# el ejercicio es descubrirlo mirando los datos con distintas preguntas.
rng = np.random.default_rng(30)
parts = []
for zone, sensor, season, size in [
    ("Norte", "N1", "invierno", 160),
    ("Norte", "N2", "verano", 40),
    ("Sur", "S1", "invierno", 40),
    ("Sur", "S2", "verano", 160),
]:
    level = (12 if season == "invierno" else 32) + (2 if zone == "Norte" else 0)
    parts.append(pd.DataFrame({"zona": zone, "sensor": sensor, "estacion": season,
                               "valor": rng.normal(level, 3, size).round(1)}))
frame = pd.concat(parts, ignore_index=True)
print(f"{len(frame)} medidas · zonas: {sorted(frame['zona'].unique())}")


# ============================================
# PASO 1: Cuántas medidas, de dónde
# ============================================
# Descomenta las siguientes líneas:
# print(pd.crosstab(frame["zona"], frame["sensor"]))
# print(pd.crosstab(frame["zona"], frame["estacion"]))


# ============================================
# PASO 2: La unidad es la medida
# ============================================
# Descomenta las siguientes líneas:
# by_reading = frame.groupby("zona")["valor"].mean()
# print(by_reading.round(2).to_dict())
# print(f"Sur - Norte, por medida: {by_reading['Sur'] - by_reading['Norte']:.2f}")


# ============================================
# PASO 3: La unidad es el sensor
# ============================================
# Descomenta las siguientes líneas:
# per_sensor = frame.groupby(["zona", "sensor"])["valor"].mean()
# print(per_sensor.round(2).to_dict())
# by_sensor = per_sensor.groupby("zona").mean()
# print(f"Sur - Norte, por sensor: {by_sensor['Sur'] - by_sensor['Norte']:.2f}")


# ============================================
# PASO 4: Por estación
# ============================================
# Descomenta las siguientes líneas:
# table = frame.pivot_table(index="estacion", columns="zona", values="valor", aggfunc="mean")
# table["Sur - Norte"] = table["Sur"] - table["Norte"]
# print(table.round(2))


# ============================================
# PASO 5: Una pregunta, con su respuesta
# ============================================
# Descomenta las siguientes líneas:
# for season, group in frame.groupby("estacion"):
#     north = group.loc[group["zona"] == "Norte", "valor"]
#     south = group.loc[group["zona"] == "Sur", "valor"]
#     welch = stats.ttest_ind(south, north, equal_var=False)
#     low, high = welch.confidence_interval(0.95)
#     print(f"{season}: Sur - Norte {south.mean() - north.mean():.2f}, IC 95 % [{low:.2f}, {high:.2f}]")
