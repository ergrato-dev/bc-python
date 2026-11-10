"""Ejercicio 01 · groupby: dividir la tabla en grupos, calcular en cada uno y juntar.

Ejecuta `uv run python main.py` después de cada paso y compara con el README.
"""

import timeit
from collections import defaultdict

import numpy as np
import pandas as pd

print("Ejercicio 01 · groupby")

# Ocho medidas de tres estaciones en dos días. La del Sur del día 2 no tiene valor y la
# última no sabe de qué estación es.
readings = pd.DataFrame(
    {
        "station": pd.Series(["Sur", "Norte", "Sur", "Este", "Norte", "Sur", "Norte", None], dtype="str"),
        "day": [1, 1, 1, 1, 2, 2, 2, 2],
        "value": [8.0, 12.5, 9.5, 30.0, 48.9, None, 20.0, 5.0],
    }
)


# ============================================
# PASO 1: Una media por estación
# ============================================
# Descomenta las siguientes líneas:
# groups = readings.groupby("station")["value"]
# print(groups.mean())
# print("en orden de aparición:", readings.groupby("station", sort=False)["value"].mean().to_dict())
# print("grupos:", groups.ngroups, "· filas del Norte:", groups.get_group("Norte").index.tolist())


# ============================================
# PASO 2: Varias cuentas a la vez
# ============================================
# Descomenta las siguientes líneas:
# print(groups.agg(["count", "size", "mean", "max"]))
# summary = readings.groupby("station").agg(
#     medidas=("value", "count"), media=("value", "mean"), primer_dia=("day", "min")
# )
# print(summary)
# print("columnas:", summary.columns.tolist())


# ============================================
# PASO 3: La fila sin estación
# ============================================
# Descomenta las siguientes líneas:
# print("filas en grupos:", int(readings.groupby("station").size().sum()), "de", len(readings))
# print(readings.groupby("station", dropna=False)["value"].count().to_dict())


# ============================================
# PASO 4: Dos claves
# ============================================
# Descomenta las siguientes líneas:
# by_day = readings.groupby(["station", "day"])["value"].mean()
# print(by_day)
# print("índice:", by_day.index.names, "· Norte día 2:", by_day.loc[("Norte", 2)])
# print(by_day.unstack("day"))
# print(readings.groupby(["station", "day"], as_index=False)["value"].mean().head(3))


# ============================================
# PASO 5: transform y filter
# ============================================
# Descomenta las siguientes líneas:
# station_mean = readings.groupby("station")["value"].transform("mean")
# print("media de su estación:", station_mean.tolist())
# print("diferencia:", (readings["value"] - station_mean).round(2).tolist())
# busy = readings.groupby("station").filter(lambda group: len(group) >= 3)
# print("estaciones con 3 o más filas:", busy["station"].unique().tolist(), "·", len(busy), "filas")


# ============================================
# PASO 6: ¿Cuánto se gana?
# ============================================
# Descomenta las siguientes líneas:
# rng = np.random.default_rng(25)
# big = pd.DataFrame(
#     {
#         "station": rng.choice(["Norte", "Sur", "Este", "Oeste", "Centro"], size=100_000),
#         "value": rng.uniform(0, 80, size=100_000).round(1),
#     }
# ).astype({"station": "str"})
# pairs = list(zip(big["station"].tolist(), big["value"].tolist(), strict=True))
#
#
# def means_loop() -> dict[str, float]:
#     """Medias con un diccionario de listas, como en la semana 06."""
#     values: defaultdict[str, list[float]] = defaultdict(list)
#     for station, value in pairs:
#         values[station].append(value)
#     return {station: sum(vs) / len(vs) for station, vs in values.items()}
#
#
# def best(code: str) -> float:
#     """El mejor de 5 intentos, en milisegundos."""
#     return min(timeit.repeat(code, number=1, repeat=5, globals=globals())) * 1000
#
#
# loop = means_loop()
# pandas = big.groupby("station")["value"].mean()
# print("¿las mismas medias?", all(np.isclose(loop[station], pandas[station]) for station in loop))
# print(f"bucle   {best('means_loop()'):6.1f} ms")
# print(f"groupby {best('big.groupby(\"station\")[\"value\"].mean()'):6.1f} ms")
