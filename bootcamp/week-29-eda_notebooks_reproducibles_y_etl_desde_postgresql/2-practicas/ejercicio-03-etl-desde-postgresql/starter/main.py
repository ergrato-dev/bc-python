"""Ejercicio 03 · ETL desde PostgreSQL: extraer con pandas, transformar y cargar de vuelta.

Antes de ejecutar, arranca el PostgreSQL del ejercicio: `docker compose up -d --wait`.
Cada ejecución borra y vuelve a crear la tabla: puedes repetir sin miedo.
"""

import time

import pandas as pd
from sqlalchemy import (
    Column,
    DateTime,
    Float,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
    func,
    select,
    text,
)

URL = "postgresql+psycopg://practicas:practicas@127.0.0.1:5433/practicas"

print("Ejercicio 03 · ETL desde PostgreSQL")

engine = create_engine(URL)
metadata = MetaData()
readings = Table(
    "readings",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("station", String(50), nullable=False),
    Column("measured_at", DateTime, nullable=False),
    Column("value", Float),
)
metadata.drop_all(engine)
metadata.create_all(engine)
# 200 000 medidas, una por hora, de cinco estaciones, generadas dentro de PostgreSQL: así no
# viajan por la red al crearlas. setseed fija la secuencia de random(): siempre las mismas.
# Un 3 % de las medidas no tiene valor (NULL).
with engine.begin() as connection:
    connection.execute(text("SELECT setseed(0.29)"))
    connection.execute(text("""
        INSERT INTO readings (station, measured_at, value)
        SELECT (ARRAY['Norte', 'Sur', 'Centro', 'Este', 'Oeste'])[1 + n % 5],
               TIMESTAMP '2026-01-01' + (n / 5) * INTERVAL '1 hour',
               CASE WHEN random() < 0.03 THEN NULL ELSE round((15 + 10 * random())::numeric, 1) END
        FROM generate_series(0, 199999) AS n
    """))
    total = connection.execute(select(func.count()).select_from(readings)).scalar_one()
print(f"readings: {total} filas")


# ============================================
# PASO 1: Extraer con read_sql
# ============================================
# Descomenta las siguientes líneas:
# north = select(readings.c.measured_at, readings.c.value).where(readings.c.station == "Norte")
# with engine.connect() as connection:
#     frame = pd.read_sql(north, connection)
# print(f"Norte: {frame.shape} · {frame.memory_usage(deep=True).sum() / 1e6:.1f} MB en memoria")
# print(frame.dtypes.to_dict())
# print(frame.head(3))


# ============================================
# PASO 2: Fijar los tipos
# ============================================
# Descomenta las siguientes líneas:
# empty = select(readings.c.station, readings.c.value).where(readings.c.value.is_(None)).limit(3)
# with engine.connect() as connection:
#     guessed = pd.read_sql(empty, connection)
#     fixed = pd.read_sql(empty, connection, dtype={"station": "str", "value": "float64"})
# print("deducidos:", guessed.dtypes.to_dict())
# print("fijados:  ", fixed.dtypes.to_dict())
# print("valores:", guessed["value"].tolist(), "→", fixed["value"].tolist())


# ============================================
# PASO 3: Que trabaje PostgreSQL
# ============================================
# Descomenta las siguientes líneas:
# start = time.perf_counter()
# with engine.connect() as connection:
#     everything = pd.read_sql(select(readings.c.station, readings.c.value), connection)
# in_pandas = everything.groupby("station")["value"].mean().round(3)
# pandas_seconds = time.perf_counter() - start
# grouped = (
#     select(readings.c.station, func.avg(readings.c.value).label("value"))
#     .group_by(readings.c.station)
#     .order_by(readings.c.station)
# )
# start = time.perf_counter()
# with engine.connect() as connection:
#     in_sql = pd.read_sql(grouped, connection, index_col="station")["value"].round(3)
# sql_seconds = time.perf_counter() - start
# print(f"pandas: {len(everything)} filas traídas · {pandas_seconds:.2f} s")
# print(f"SQL:    {len(in_sql)} filas traídas · {sql_seconds:.3f} s")
# print("¿las mismas medias?", in_pandas.sort_index().equals(in_sql.sort_index()))


# ============================================
# PASO 4: Parámetros, nunca texto pegado
# ============================================
# Descomenta las siguientes líneas:
# station = "Norte' OR '1'='1"
# pasted = text(f"SELECT count(*) FROM readings WHERE station = '{station}'")
# bound = text("SELECT count(*) FROM readings WHERE station = :station")
# with engine.connect() as connection:
#     print("pegado:   ", connection.execute(pasted).scalar_one(), "filas")
#     print("parámetro:", connection.execute(bound, {"station": station}).scalar_one(), "filas")
#     by_param = pd.read_sql(bound, connection, params={"station": "Sur"})
# print("Sur:", by_param.iloc[0, 0], "filas")


# ============================================
# PASO 5: Por partes, sin traerlo todo
# ============================================
# Descomenta las siguientes líneas:
# count, total, parts = 0, 0.0, 0
# with engine.connect().execution_options(stream_results=True) as connection:
#     for chunk in pd.read_sql(select(readings.c.value), connection, chunksize=50_000):
#         count += int(chunk["value"].count())
#         total += float(chunk["value"].sum())
#         parts += 1
# with engine.connect() as connection:
#     exact = connection.execute(select(func.avg(readings.c.value))).scalar_one()
# print(f"{parts} partes · {count} valores · media {total / count:.4f} · PostgreSQL {exact:.4f}")


# ============================================
# PASO 6: Transformar y cargar de vuelta
# ============================================
# Descomenta las siguientes líneas:
# with engine.connect() as connection:
#     hourly = pd.read_sql(select(readings), connection, dtype={"value": "float64"})
# daily = (
#     hourly.assign(day=hourly["measured_at"].dt.date)
#     .groupby(["station", "day"], as_index=False)
#     .agg(mean=("value", "mean"), measurements=("value", "count"))
#     .round({"mean": 2})
# )
# print(f"transformado: {len(hourly)} medidas → {len(daily)} días")
# for mode in ["replace", "replace", "append"]:
#     with engine.begin() as connection:
#         daily.to_sql("daily", connection, if_exists=mode, index=False)
#         rows = connection.execute(text("SELECT count(*) FROM daily")).scalar_one()
#     print(f"to_sql(if_exists={mode!r}): daily tiene {rows} filas")
# with engine.connect() as connection:
#     print(pd.read_sql(text("SELECT * FROM daily ORDER BY day, station LIMIT 3"), connection))
