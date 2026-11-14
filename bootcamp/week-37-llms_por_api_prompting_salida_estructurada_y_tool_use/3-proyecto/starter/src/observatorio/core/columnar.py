"""Las medidas en formato columnar: Polars para la tabla, Parquet para el archivo y DuckDB
para preguntarle con SQL.

Como frames y summaries, importa bibliotecas que tardan en cargarse: core/__init__.py no lo
reexporta, y la CLI lo importa solo dentro de los comandos que lo usan.
"""

from pathlib import Path

import duckdb
import polars as pl

from observatorio.core.model import Series

# El nombre de la tabla que ve el SQL de `query`.
TABLE = "medidas"


def frame_of(series: Series) -> pl.DataFrame:
    """Una fila por medida, con label (String) y value (Float64, null si falta)."""
    # El esquema explícito: sin él, una serie vacía, o sin ningún valor, no tendría tipos.
    return pl.DataFrame(
        {"label": [m.label for m in series], "value": [m.value for m in series]},
        schema={"label": pl.String, "value": pl.Float64},
    )


def summary(frame: pl.LazyFrame) -> pl.LazyFrame:
    """Una fila por etiqueta, en el orden en que aparece: count, missing, mean, minimum, maximum.

    Es el mismo resumen que summaries.summary, con null donde pandas pone NaN. Devuelve un
    plan: no calcula nada hasta collect().
    """
    value = pl.col("value")
    # maintain_order: sin él, Polars reparte los grupos entre hilos y el orden cambia.
    return frame.group_by("label", maintain_order=True).agg(
        count=value.count(),
        missing=value.null_count(),
        mean=value.mean(),
        minimum=value.min(),
        maximum=value.max(),
    )


def query(path: Path, sql: str) -> tuple[list[str], list[tuple[object, ...]]]:
    """Las columnas y las filas de sql sobre el Parquet de path, que se llama medidas.

    Lanza duckdb.Error si el archivo no se lee o el SQL falla. El SQL no puede leer ni
    escribir ningún otro archivo.
    """
    with duckdb.connect() as connection:
        connection.execute(f"CREATE TABLE {TABLE} AS SELECT * FROM read_parquet(?)", [str(path)])
        # Desde aquí, sin archivos ni red: el SQL lo escribe quien usa la CLI, y solo tiene que
        # ver la tabla. DuckDB no deja volver a activarlos con la conexión abierta.
        connection.execute("SET enable_external_access = false")
        cursor = connection.execute(sql)
        return [column[0] for column in cursor.description], cursor.fetchall()
