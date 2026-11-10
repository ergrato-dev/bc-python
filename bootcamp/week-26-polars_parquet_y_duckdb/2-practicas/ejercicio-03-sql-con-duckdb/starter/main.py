"""Ejercicio 03 · DuckDB: SQL sobre archivos y tablas, sin servidor.

Ejecuta `uv run python main.py` después de cada paso y compara con el README. Los archivos
que escribe van a la carpeta salida/, junto a este archivo.
"""

import shutil
from pathlib import Path

import duckdb
import pandas as pd
import polars as pl

print("Ejercicio 03 · DuckDB")

HERE = Path(__file__).parent
OUT = HERE / "salida"
shutil.rmtree(OUT, ignore_errors=True)
OUT.mkdir()

# Las ocho medidas de los ejercicios 01 y 02, guardadas en Parquet con Polars.
readings = pl.DataFrame(
    {
        "station": ["Sur", "Norte", "Sur", "Este", "Norte", "Sur", "Norte", None],
        "day": [1, 1, 1, 1, 2, 2, 2, 2],
        "value": [8.0, 12.5, 9.5, 30.0, 48.9, None, 20.0, 5.0],
    }
)
readings.write_parquet(OUT / "readings.parquet")


# ============================================
# PASO 1: SQL sobre un archivo
# ============================================
# Descomenta las siguientes líneas:
# relation = duckdb.sql(
#     "SELECT station, count(value) AS n, avg(value) AS mean FROM 'salida/readings.parquet'"
#     " GROUP BY station ORDER BY station NULLS LAST"
# )
# print(relation)
# print("columnas:", relation.columns, "· tipos:", relation.types)
# print("filas:", relation.fetchall())


# ============================================
# PASO 2: El CSV del Observatorio
# ============================================
# Descomenta las siguientes líneas:
# print("sin opciones:", duckdb.sql("SELECT * FROM 'medidas.csv'").types)
# csv = duckdb.sql(
#     "SELECT * FROM read_csv('medidas.csv', delim = ';', decimal_separator = ',', nullstr = 'NA')"
# )
# print(csv.types, csv.fetchall()[:3])
# print(duckdb.sql("SELECT etiqueta, avg(valor) AS media FROM csv GROUP BY ALL ORDER BY ALL"))


# ============================================
# PASO 3: Tablas de pandas y de Polars
# ============================================
# Descomenta las siguientes líneas:
# stations = pd.DataFrame(
#     {"station": ["Norte", "Sur", "Centro"], "region": ["Andina", "Pacífica", "Andina"]}
# )
# joined = duckdb.sql(
#     "SELECT r.station, r.value, s.region FROM 'salida/readings.parquet' AS r"
#     " LEFT JOIN stations AS s USING (station) ORDER BY r.value DESC NULLS LAST LIMIT 3"
# )
# print(joined.fetchall())
# print(type(joined.df()).__name__, joined.df().shape)
# try:
#     duckdb.sql("SELECT count(*) FROM readings").fetchall()
# except duckdb.InvalidInputException as problem:
#     print("InvalidInputException:", str(problem).rsplit(": ", 1)[1])


# ============================================
# PASO 4: Parámetros, no texto pegado
# ============================================
# Descomenta las siguientes líneas:
# station = "Norte' OR '1' = '1"
# pasted = f"SELECT count(*) FROM 'salida/readings.parquet' WHERE station = '{station}'"
# print("pegado:", duckdb.sql(pasted).fetchall())
# safe = duckdb.execute("SELECT count(*) FROM 'salida/readings.parquet' WHERE station = ?", [station])
# print("con ?:", safe.fetchall())
# print(
#     "Norte:",
#     duckdb.execute(
#         "SELECT count(*) FROM 'salida/readings.parquet' WHERE station = ?", ["Norte"]
#     ).fetchall(),
# )


# ============================================
# PASO 5: Una base de datos en un archivo
# ============================================
# Descomenta las siguientes líneas:
# DATABASE = OUT / "observatorio.duckdb"
# with duckdb.connect(DATABASE) as connection:
#     connection.execute("CREATE TABLE readings AS SELECT * FROM 'salida/readings.parquet'")
#     connection.execute("INSERT INTO readings VALUES ('Este', 3, 31.5)")
# with duckdb.connect(DATABASE, read_only=True) as connection:
#     print(
#         "filas al volver a abrir:", connection.execute("SELECT count(*) FROM readings").fetchall()
#     )
#     print("tablas:", connection.execute("SHOW TABLES").fetchall())
# print(f"{DATABASE.name}: {DATABASE.stat().st_size / 1000:.0f} kB")


# ============================================
# PASO 6: Ventanas y una conexión cerrada al disco
# ============================================
# Descomenta las siguientes líneas:
# with duckdb.connect() as connection:
#     connection.execute("CREATE TABLE readings AS SELECT * FROM 'salida/readings.parquet'")
#     window = connection.execute(
#         "SELECT station, value, round(value - avg(value) OVER (PARTITION BY station), 2) AS gap"
#         " FROM readings WHERE station = 'Norte' ORDER BY value"
#     )
#     print(window.fetchall())
#     connection.execute("SET enable_external_access = false")
#     print("la tabla sigue:", connection.execute("SELECT count(*) FROM readings").fetchall())
#     try:
#         connection.execute("SELECT * FROM 'medidas.csv'")
#     except duckdb.PermissionException as problem:
#         print("PermissionException:", str(problem).split(": ", 1)[1])
