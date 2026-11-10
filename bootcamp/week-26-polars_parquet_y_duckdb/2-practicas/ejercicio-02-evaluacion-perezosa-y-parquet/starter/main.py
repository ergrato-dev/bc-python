"""Ejercicio 02 · Evaluación perezosa y Parquet: planes, CSV frente a Parquet y particiones.

Ejecuta `uv run python main.py` después de cada paso y compara con el README. Los archivos
que escribe van a la carpeta salida/, junto a este archivo.
"""

import math
import shutil
import timeit
from collections.abc import Callable
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import polars as pl

print("Ejercicio 02 · Lazy y Parquet")

OUT = Path(__file__).parent / "salida"
shutil.rmtree(OUT, ignore_errors=True)
OUT.mkdir()

# Un millón de medidas de cinco estaciones, una por minuto desde el 1 de enero de 2026, con
# un 5 % sin valor. La semilla hace que salgan siempre las mismas.
N = 1_000_000
START = datetime(2026, 1, 1)
rng = np.random.default_rng(26)
measurements = pl.DataFrame(
    {
        "time": pl.datetime_range(START, START + timedelta(minutes=N - 1), "1m", eager=True),
        "station": rng.choice(["Norte", "Sur", "Este", "Oeste", "Centro"], size=N),
        "value": rng.uniform(0, 80, size=N).round(1),
    }
).with_columns(value=pl.when(pl.lit(rng.random(N) < 0.05)).then(None).otherwise("value"))


def milliseconds(run: Callable[[], object], number: int = 5) -> float:
    """El mejor de cinco tiempos de run(), en milisegundos."""
    return min(timeit.repeat(run, number=number, repeat=5)) / number * 1000


# ============================================
# PASO 1: Un plan, no un resultado
# ============================================
# Descomenta las siguientes líneas:
# print(measurements.head(3))
# print("sin valor:", measurements.get_column("value").null_count())
# plan = (
#     measurements.lazy()
#     .filter(pl.col("station") == "Norte")
#     .with_columns(tenths=pl.col("value") / 10)
#     .select("time", "value")
# )
# print(type(plan).__name__)
# print(plan.explain(optimized=False))
# print(plan.explain())
# print(plan.collect().shape)


# ============================================
# PASO 2: Los errores llegan al ejecutar
# ============================================
# Descomenta las siguientes líneas:
# broken = measurements.lazy().filter(pl.col("valor") > 10)
# print("plan creado:", type(broken).__name__)
# try:
#     broken.collect()
# except pl.exceptions.ColumnNotFoundError as problem:
#     print("ColumnNotFoundError:", str(problem).splitlines()[0])
# print("esquema sin ejecutar:", plan.collect_schema())


# ============================================
# PASO 3: CSV frente a Parquet
# ============================================
# Descomenta las siguientes líneas:
# measurements.write_csv(OUT / "medidas.csv")
# for compression in ["uncompressed", "snappy", "zstd"]:
#     measurements.write_parquet(OUT / f"medidas-{compression}.parquet", compression=compression)
# for path in sorted(OUT.iterdir()):
#     print(f"{path.name:<30} {path.stat().st_size / 1_000_000:6.1f} MB")
# print(f"leer CSV      {milliseconds(lambda: pl.read_csv(OUT / 'medidas.csv')):6.1f} ms")
# print(
#     f"leer Parquet  {milliseconds(lambda: pl.read_parquet(OUT / 'medidas-zstd.parquet')):6.1f} ms"
# )


# ============================================
# PASO 4: Parquet guarda los tipos
# ============================================
# Descomenta las siguientes líneas:
# from_csv = pl.read_csv(OUT / "medidas.csv")
# from_parquet = pl.read_parquet(OUT / "medidas-zstd.parquet")
# print("CSV:    ", from_csv.schema)
# print("Parquet:", from_parquet.schema)
# print("¿igual que en memoria?", from_csv.equals(measurements), from_parquet.equals(measurements))
# print("nulos en Parquet:", from_parquet.get_column("value").null_count())


# ============================================
# PASO 5: Leer solo lo que hace falta
# ============================================
# Descomenta las siguientes líneas:
# PARQUET = OUT / "medidas-zstd.parquet"
# NORTH = pl.col("station") == "Norte"
# MEAN = pl.col("value").mean()
#
#
# def eager() -> float:
#     """Lee el archivo entero y después filtra y calcula."""
#     return pl.read_parquet(PARQUET).filter(NORTH).select(MEAN).item()
#
#
# def lazy() -> float:
#     """Planea primero: Polars lee solo las columnas y las filas que la pregunta necesita."""
#     return pl.scan_parquet(PARQUET).filter(NORTH).select(MEAN).collect().item()
#
#
# print(f"media del Norte: {lazy():.3f} · ¿la misma? {math.isclose(eager(), lazy())}")
# print(pl.scan_parquet(PARQUET).filter(NORTH).select(MEAN).explain().replace(str(OUT), "salida"))
# print(f"read_parquet  {milliseconds(eager):6.1f} ms")
# print(f"scan_parquet  {milliseconds(lazy):6.1f} ms")


# ============================================
# PASO 6: Una carpeta por estación
# ============================================
# Descomenta las siguientes líneas:
# measurements.write_parquet(OUT / "por_estacion", partition_by="station")
# for path in sorted((OUT / "por_estacion").rglob("*.parquet")):
#     print(path.relative_to(OUT), f"{path.stat().st_size / 1_000_000:.1f} MB")
# partitioned = pl.scan_parquet(OUT / "por_estacion", hive_partitioning=True)
# print(partitioned.filter(NORTH).select(MEAN).explain().replace(str(OUT), "salida"))
# print(
#     "¿la misma media?",
#     math.isclose(partitioned.filter(NORTH).select(MEAN).collect().item(), lazy()),
# )
