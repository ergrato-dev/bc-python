"""Ejercicio 01 · Series, índice y tipos: una columna de datos con nombre en cada fila.

Ejecuta `uv run python main.py` después de cada paso y compara con el README.
"""

import numpy as np
import pandas as pd

print("Ejercicio 01 · Series, índice y tipos")


# ============================================
# PASO 1: Una Series y su índice
# ============================================
# Descomenta las siguientes líneas:
# readings = pd.Series([12.5, 8.0, 48.9])
# print(readings)
# print("índice:", readings.index)
# print("valores:", readings.to_numpy(), "·", type(readings.to_numpy()).__name__)
# stations = pd.Series([12.5, 8.0, 48.9], index=["Norte", "Sur", "Este"], name="valor")
# print(stations)
# print("Sur:", stations["Sur"], "· desde un dict:", pd.Series({"A": 1, "B": 2}).to_dict())


# ============================================
# PASO 2: Tipos, y lo que pasa con lo que falta
# ============================================
# Descomenta las siguientes líneas:
# print("enteros:", pd.Series([1, 2, 3]).dtype)
# print("enteros con None:", pd.Series([1, None, 3]).tolist(), pd.Series([1, None, 3]).dtype)
# print("texto:", pd.Series(["Norte", "Sur"]).dtype, "· con None:", pd.Series(["A", None]).tolist())
# print("mezcla:", pd.Series([1, "Norte"]).dtype)
# nullable = pd.Series([1, None, 3], dtype="Int64")
# print("Int64:", nullable.tolist(), nullable.dtype)
# print("a float64:", pd.Series(["1", "2,5"]).str.replace(",", ".").astype("float64").tolist())


# ============================================
# PASO 3: Las operaciones se alinean por el índice
# ============================================
# Descomenta las siguientes líneas:
# monday = pd.Series([10.0, 20.0], index=["Norte", "Sur"])
# tuesday = pd.Series([5.0, 7.0], index=["Sur", "Este"])
# print(monday + tuesday)
# print(monday.add(tuesday, fill_value=0).to_dict())
# print("por posición:", (monday.to_numpy() + tuesday.to_numpy()).tolist())


# ============================================
# PASO 4: Etiqueta o posición
# ============================================
# Descomenta las siguientes líneas:
# codes = pd.Series(["a", "b", "c"], index=[10, 20, 30])
# print("loc[10]:", codes.loc[10], "· iloc[0]:", codes.iloc[0], "· [10]:", codes[10])
# try:
#     codes[0]
# except KeyError as problem:
#     print("KeyError:", problem)
# print("loc[10:20]:", codes.loc[10:20].tolist(), "· iloc[0:2]:", codes.iloc[0:2].tolist())


# ============================================
# PASO 5: NaN se salta solo
# ============================================
# Descomenta las siguientes líneas:
# values = pd.Series([12.5, np.nan, 8.0])
# print(f"pandas mean {values.mean()} · NumPy mean {values.to_numpy().mean()}")
# print(f"count {values.count()} · size {values.size} · sum {values.sum()}")
# print(f"std pandas {values.std():.3f} (ddof=1) · std NumPy {np.nanstd(values.to_numpy()):.3f} (ddof=0)")
# print("isna:", values.isna().tolist(), "· fillna:", values.fillna(0).tolist())
# print("dropna:", values.dropna().to_dict())


# ============================================
# PASO 6: Texto y conteos
# ============================================
# Descomenta las siguientes líneas:
# labels = pd.Series(["Norte", "sur", "Norte", "Este", "Sur ", "Norte"])
# clean = labels.str.strip().str.capitalize()
# print("limpias:", clean.tolist())
# print(clean.value_counts())
# print("distintas:", clean.unique().tolist(), "· cuántas:", clean.nunique())
# print("¿empieza por N?", clean.str.startswith("N").tolist())
