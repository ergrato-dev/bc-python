"""Ejercicio 04 · De Python a pandas: lo que ya tenías con bucles, ahora con una tabla.

Ejecuta `uv run python main.py` después de cada paso y compara con el README.
"""

import json
import timeit
from collections import Counter
from dataclasses import dataclass

import numpy as np
import pandas as pd

print("Ejercicio 04 · De Python a pandas")


@dataclass(frozen=True)
class Measurement:
    label: str
    value: float | None


def classify(value: float | None, low: float = 10, high: float = 50) -> str:
    """El nivel de la semana 2: un valor igual a low ya es "medio"; igual a high, "alto"."""
    if value is None:
        return "sin dato"
    if value < low:
        return "bajo"
    if value < high:
        return "medio"
    return "alto"


SERIES = [
    Measurement("Norte", 12.5),
    Measurement("Sur", 8.0),
    Measurement("Centro", None),
    Measurement("Norte", 50.0),
    Measurement("Sur", 10.0),
]


# ============================================
# PASO 1: De objetos a una tabla
# ============================================
# Descomenta las siguientes líneas:
# frame = pd.DataFrame(
#     {"label": [m.label for m in SERIES], "value": [m.value for m in SERIES]},
#     index=pd.RangeIndex(1, len(SERIES) + 1, name="position"),
# )
# print(frame)
# print(frame.dtypes.to_dict())
# empty = pd.DataFrame({"label": [], "value": []})
# print("vacía, sin tipos:", empty.dtypes.to_dict())
# empty = pd.DataFrame({"label": pd.Series([], dtype="str"), "value": pd.Series([], dtype="float64")})
# print("vacía, con tipos:", empty.dtypes.to_dict())


# ============================================
# PASO 2: Niveles sin bucle
# ============================================
# Descomenta las siguientes líneas:
# loop = [classify(m.value) for m in SERIES]
# cut = pd.cut(frame["value"], bins=[-np.inf, 10, 50, np.inf], labels=["bajo", "medio", "alto"])
# print("cut, right=True: ", cut.tolist())
# cut = pd.cut(frame["value"], bins=[-np.inf, 10, 50, np.inf], labels=["bajo", "medio", "alto"], right=False)
# print("cut, right=False:", cut.tolist(), "·", cut.dtype)
# levels = cut.astype("str").where(cut.notna(), "sin dato")
# print("con sin dato:    ", levels.tolist())
# print("¿igual que el bucle?", levels.tolist() == loop)


# ============================================
# PASO 3: Contar, como Counter
# ============================================
# Descomenta las siguientes líneas:
# counts = frame["label"].value_counts()
# print(counts.to_dict(), "· Counter:", Counter(m.label for m in SERIES).most_common())
# print("tipo de un conteo:", type(counts.iloc[0]).__name__)
# try:
#     json.dumps({"Norte": counts.iloc[0]})
# except TypeError as problem:
#     print("TypeError:", problem)
# print(json.dumps({str(label): int(n) for label, n in counts.items()}))


# ============================================
# PASO 4: Lo que sale de pandas
# ============================================
# Descomenta las siguientes líneas:
# top = frame["value"].max()
# print("max:", top, type(top).__name__, "· float():", type(float(top)).__name__)
# print("tolist:", frame["value"].tolist(), "·", type(frame["value"].tolist()[0]).__name__)
# print("sin dato:", frame["value"].iloc[2], "· isna:", pd.isna(frame["value"].iloc[2]))
# back = [Measurement(label, None if pd.isna(value) else value) for label, value in frame.itertuples(index=False)]
# print("¿vuelta completa?", back == SERIES)


# ============================================
# PASO 5: ¿Cuánto se gana?
# ============================================
# Descomenta las siguientes líneas:
# rng = np.random.default_rng(24)
# labels = rng.choice(["Norte", "Sur", "Este", "Oeste", "Centro"], size=100_000)
# values = rng.uniform(0, 80, size=100_000).round(1)
# big = [Measurement(str(label), float(value)) for label, value in zip(labels, values, strict=True)]
#
#
# def best(code: str) -> float:
#     """El mejor de 5 intentos, en milisegundos."""
#     return min(timeit.repeat(code, number=1, repeat=5, globals=globals())) * 1000
#
#
# table = pd.DataFrame({"label": [m.label for m in big], "value": [m.value for m in big]})
# print(f"convertir a tabla  {best('pd.DataFrame({\"label\": [m.label for m in big], \"value\": [m.value for m in big]})'):6.1f} ms")
# print(f"niveles   bucle    {best('[classify(m.value) for m in big]'):6.1f} ms · pandas {best('pd.cut(table[\"value\"], [-np.inf, 10, 50, np.inf], right=False)'):5.1f} ms")
# print(f"filtrar   bucle    {best('[m for m in big if m.label == \"Sur\" and m.value >= 20]'):6.1f} ms · pandas {best('table[(table[\"label\"] == \"Sur\") & (table[\"value\"] >= 20)]'):5.1f} ms")
# print(f"contar    Counter  {best('Counter(m.label for m in big)'):6.1f} ms · pandas {best('table[\"label\"].value_counts()'):5.1f} ms")


# ============================================
# PASO 6: Memoria de texto
# ============================================
# Descomenta las siguientes líneas:
# as_text = table["label"].memory_usage(deep=True)
# as_category = table["label"].astype("category").memory_usage(deep=True)
# print(f"str {as_text / 1e6:.2f} MB · category {as_category / 1e6:.2f} MB")
# print("categorías:", table["label"].astype("category").cat.categories.tolist())
# print(f"valores float64: {table['value'].memory_usage(index=False) / 1e6:.2f} MB")
