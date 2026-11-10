"""Ejercicio 01 · Polars: tablas sin índice, expresiones y los cuatro contextos.

Ejecuta `uv run python main.py` después de cada paso y compara con el README.
"""

import timeit

import numpy as np
import pandas as pd
import polars as pl

print("Ejercicio 01 · Polars")

# Las ocho medidas de la semana 25: tres estaciones en dos días. La del Sur del día 2 no
# tiene valor y la última no sabe de qué estación es.
readings = pl.DataFrame(
    {
        "station": ["Sur", "Norte", "Sur", "Este", "Norte", "Sur", "Norte", None],
        "day": [1, 1, 1, 1, 2, 2, 2, 2],
        "value": [8.0, 12.5, 9.5, 30.0, 48.9, None, 20.0, 5.0],
    }
)


# ============================================
# PASO 1: Una tabla sin índice
# ============================================
# Descomenta las siguientes líneas:
# print(readings)
# print("esquema:", readings.schema)
# print("fila 4:", readings.row(4))
# print("nulos:", readings.null_count().row(0))
# nan = pl.Series("value", [1.0, None, float("nan")])
# print("null:", nan.is_null().to_list(), "· NaN:", nan.is_nan().to_list(), "· media:", nan.mean())


# ============================================
# PASO 2: Expresiones en select y with_columns
# ============================================
# Descomenta las siguientes líneas:
# print(readings.select("station", pl.col("value") * 10))
# level = (
#     pl.when(pl.col("value") >= 30)
#     .then(pl.lit("alto"))
#     .when(pl.col("value") >= 10)
#     .then(pl.lit("medio"))
#     .otherwise(pl.lit("bajo"))
# )
# with_level = readings.with_columns(
#     level.alias("level"), (pl.col("value") / 10).round(1).alias("tenths")
# )
# print(with_level.head(4))
# print("¿cambió readings?", readings.columns)


# ============================================
# PASO 3: filter y sort
# ============================================
# Descomenta las siguientes líneas:
# print(readings.filter(pl.col("value") > 10, pl.col("day") == 1))
# print("sin valor, con filter(value <= 10):", readings.filter(pl.col("value") <= 10).height, "filas")
# print(readings.sort("value", descending=True, nulls_last=True).get_column("value").to_list())
# try:
#     readings.filter(pl.col("valor") > 10)
# except pl.exceptions.ColumnNotFoundError as problem:
#     print("ColumnNotFoundError:", str(problem).splitlines()[0])


# ============================================
# PASO 4: group_by y agg
# ============================================
# Descomenta las siguientes líneas:
# summary = readings.group_by("station", maintain_order=True).agg(
#     rows=pl.len(),
#     count=pl.col("value").count(),
#     missing=pl.col("value").null_count(),
#     mean=pl.col("value").mean(),
#     days=pl.col("day").unique().sort(),
# )
# print(summary)


# ============================================
# PASO 5: over y join
# ============================================
# Descomenta las siguientes líneas:
# centered = readings.with_columns(
#     station_mean=pl.col("value").mean().over("station"),
#     gap=(pl.col("value") - pl.col("value").mean().over("station")).round(2),
# )
# print(centered.filter(pl.col("station") == "Norte"))
# stations = pl.DataFrame(
#     {"station": ["Norte", "Sur", "Centro"], "region": ["Andina", "Pacífica", "Andina"]}
# )
# print(
#     readings.join(stations, on="station", how="left").select("station", "value", "region").tail(3)
# )
# print(
#     "inner:",
#     readings.join(stations, on="station").height,
#     "filas · left:",
#     readings.join(stations, on="station", how="left").height,
# )


# ============================================
# PASO 6: ¿Cuánto se gana?
# ============================================
# Descomenta las siguientes líneas:
# rng = np.random.default_rng(26)
# big_labels = rng.choice(["Norte", "Sur", "Este", "Oeste", "Centro"], size=1_000_000)
# big_values = rng.uniform(0, 80, size=1_000_000)
# pandas_frame = pd.DataFrame({"station": big_labels, "value": big_values})
# polars_frame = pl.DataFrame({"station": big_labels, "value": big_values})
# pandas_means = pandas_frame.groupby("station")["value"].mean()
# polars_means = polars_frame.group_by("station").agg(pl.col("value").mean()).sort("station")
# print(
#     "¿las mismas medias?",
#     np.allclose(pandas_means.to_numpy(), polars_means.get_column("value").to_numpy()),
# )
# for name, run in [
#     ("pandas", lambda: pandas_frame.groupby("station")["value"].mean()),
#     ("polars", lambda: polars_frame.group_by("station").agg(pl.col("value").mean())),
# ]:
#     seconds = min(timeit.repeat(run, number=10, repeat=5)) / 10
#     print(f"{name:<8} {seconds * 1000:5.1f} ms")
