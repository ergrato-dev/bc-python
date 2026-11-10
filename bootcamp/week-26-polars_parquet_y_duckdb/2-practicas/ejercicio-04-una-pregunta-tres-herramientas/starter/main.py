"""Ejercicio 04 · Una pregunta, tres herramientas: pandas, Polars y DuckDB.

Ejecuta `uv run python main.py` después de cada paso y compara con el README. Los archivos
que escribe van a la carpeta salida/, junto a este archivo.
"""

import math
import shutil
import timeit
from collections.abc import Callable
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd
import polars as pl

print("Ejercicio 04 · Una pregunta, tres herramientas")

OUT = Path(__file__).parent / "salida"
shutil.rmtree(OUT, ignore_errors=True)
OUT.mkdir()

# Cómo se lee un CSV del Observatorio: punto y coma, coma decimal y NA si falta.
CSV_OPTIONS = {"separator": ";", "decimal_comma": True, "null_values": "NA"}


def milliseconds(run: Callable[[], object]) -> float:
    """El mejor de cinco tiempos de run(), en milisegundos."""
    return min(timeit.repeat(run, number=3, repeat=5)) / 3 * 1000


# ============================================
# PASO 1: El CSV del Observatorio con Polars
# ============================================
# Descomenta las siguientes líneas:
# plain = pl.read_csv("medidas.csv", separator=";")
# print("sin opciones:", plain.schema)
# frame = pl.read_csv("medidas.csv", **CSV_OPTIONS)
# print("con opciones:", frame.schema)
# print(frame.rename({"etiqueta": "label", "valor": "value"}).head(3).rows())


# ============================================
# PASO 2: Una fila mala
# ============================================
# Descomenta las siguientes líneas:
# print("pandas:", pd.read_csv("rota.csv", sep=";", decimal=",")["valor"].dtype)
# try:
#     pl.read_csv("rota.csv", **CSV_OPTIONS, schema_overrides={"valor": pl.Float64})
# except pl.exceptions.ComputeError as problem:
#     print("Polars, ComputeError:", str(problem).splitlines()[0])
# lenient = pl.read_csv(
#     "rota.csv", **CSV_OPTIONS, schema_overrides={"valor": pl.Float64}, ignore_errors=True
# )
# print("ignore_errors:", lenient.get_column("valor").to_list())


# ============================================
# PASO 3: Un millón de medidas, de CSV a Parquet
# ============================================
# Descomenta las siguientes líneas:
# N = 1_000_000
# rng = np.random.default_rng(26)
# big = pl.DataFrame(
#     {
#         "etiqueta": rng.choice(["Norte", "Sur", "Este", "Oeste", "Centro"], size=N),
#         "valor": rng.uniform(0, 80, size=N).round(1),
#     }
# ).with_columns(valor=pl.when(pl.lit(rng.random(N) < 0.05)).then(None).otherwise("valor"))
# BIG_CSV, BIG_PARQUET = OUT / "grande.csv", OUT / "grande.parquet"
# big.write_csv(BIG_CSV, separator=";", decimal_comma=True, null_value="NA")
# print(BIG_CSV.read_text(encoding="utf-8").splitlines()[:3])
# # sink_parquet lee y escribe por trozos: el archivo no tiene que caber entero en memoria.
# pl.scan_csv(BIG_CSV, **CSV_OPTIONS).sink_parquet(BIG_PARQUET)
# for path in (BIG_CSV, BIG_PARQUET):
#     print(f"{path.name:<15} {path.stat().st_size / 1_000_000:5.1f} MB")


# ============================================
# PASO 4: Una pregunta, tres respuestas
# ============================================
# Descomenta las siguientes líneas:
# def with_pandas() -> list[tuple[str, int, float]]:
#     """Medidas y media por etiqueta, de mayor a menor media, leyendo el CSV con pandas."""
#     table = pd.read_csv(BIG_CSV, sep=";", decimal=",")
#     result = table.groupby("etiqueta")["valor"].agg(["count", "mean"])
#     return list(result.sort_values("mean", ascending=False).itertuples(name=None))
#
#
# def with_polars(source: pl.LazyFrame) -> list[tuple[str, int, float]]:
#     """Lo mismo con Polars, en perezoso: source es scan_csv o scan_parquet."""
#     plan = (
#         source.group_by("etiqueta")
#         .agg(count=pl.col("valor").count(), mean=pl.col("valor").mean())
#         .sort("mean", descending=True)
#     )
#     return plan.collect().rows()
#
#
# def with_duckdb() -> list[tuple[str, int, float]]:
#     """Lo mismo con SQL sobre el Parquet."""
#     return duckdb.sql(
#         f"SELECT etiqueta, count(valor), avg(valor) FROM '{BIG_PARQUET}'"
#         " GROUP BY etiqueta ORDER BY 3 DESC"
#     ).fetchall()
#
#
# answers = {
#     "pandas": with_pandas(),
#     "polars": with_polars(pl.scan_parquet(BIG_PARQUET)),
#     "duckdb": with_duckdb(),
# }
# for name, rows in answers.items():
#     print(f"{name:<7}", [(label, count, round(mean, 2)) for label, count, mean in rows])
# print(
#     "¿la misma respuesta?",
#     all(
#         a[:2] == b[:2] and math.isclose(a[2], b[2])
#         for rows in answers.values()
#         for a, b in zip(rows, answers["pandas"], strict=True)
#     ),
# )


# ============================================
# PASO 5: ¿Cuánto tarda cada una?
# ============================================
# Descomenta las siguientes líneas:
# runs = {
#     "pandas, CSV": with_pandas,
#     "Polars, CSV": lambda: with_polars(pl.scan_csv(BIG_CSV, **CSV_OPTIONS)),
#     "Polars, Parquet": lambda: with_polars(pl.scan_parquet(BIG_PARQUET)),
#     "DuckDB, Parquet": with_duckdb,
# }
# for name, run in runs.items():
#     print(f"{name:<16} {milliseconds(run):7.1f} ms")


# ============================================
# PASO 6: pandas y Parquet
# ============================================
# Descomenta las siguientes líneas:
# try:
#     pd.read_parquet(BIG_PARQUET)
# except ImportError as problem:
#     print("ImportError:", str(problem).splitlines()[0])
# from_duckdb = duckdb.sql(f"SELECT * FROM '{BIG_PARQUET}' WHERE etiqueta = 'Norte'").df()
# print(type(from_duckdb).__name__, from_duckdb.shape, from_duckdb["valor"].dtype)
