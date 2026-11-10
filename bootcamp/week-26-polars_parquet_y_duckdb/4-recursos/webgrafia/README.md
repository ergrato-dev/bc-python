# Webgrafía — Semana 26

Todo en inglés, de la documentación oficial de cada proyecto. Las guías de Polars y DuckDB siguen la última versión; si algo no coincide con Polars 2.1 o DuckDB 2.0, manda lo que ves al ejecutar.

| Recurso | Para qué |
|---|---|
| [Polars: Getting started](https://docs.pola.rs/user-guide/getting-started/) | Un recorrido corto: leer, `select`, `filter`, `with_columns` y `group_by`. Buen repaso antes del ejercicio 01 |
| [Polars: Expressions and contexts](https://docs.pola.rs/user-guide/concepts/expressions-and-contexts/) | Qué es una expresión y qué hace cada contexto. La referencia de la teoría 01 |
| [Polars: Missing data](https://docs.pola.rs/user-guide/expressions/missing-data/) | `null` frente a `NaN`, `fill_null` y `null_count`. La teoría 01, sección 3 |
| [Polars: Coming from pandas](https://docs.pola.rs/user-guide/migration/pandas/) | Las diferencias de diseño con pandas y cómo se escribe cada operación. Amplía la tabla de la teoría 01 |
| [Polars: Lazy API](https://docs.pola.rs/user-guide/concepts/lazy-api/) | `LazyFrame`, `scan_*` y `collect`. La teoría 02 |
| [Polars: Optimizations](https://docs.pola.rs/user-guide/lazy/optimizations/) | La lista de optimizaciones del plan, con el *pushdown* de filtros y columnas |
| [Polars: Streaming](https://docs.pola.rs/user-guide/concepts/streaming/) | El motor `streaming` para datos más grandes que la memoria, y `sink_parquet` |
| [Polars: Parquet](https://docs.pola.rs/user-guide/io/parquet/) | Leer, escanear y escribir Parquet con Polars |
| [Apache Parquet: File format](https://parquet.apache.org/docs/file-format/) | Cómo es un archivo Parquet por dentro: *row groups*, *column chunks*, páginas y pie. La teoría 03 en profundidad |
| [Why DuckDB](https://duckdb.org/why_duckdb) | Para qué se hizo DuckDB y en qué se diferencia de una base de datos con servidor. La teoría 04, sección 1 |
| [DuckDB: Python API](https://duckdb.org/docs/stable/clients/python/overview) | `duckdb.sql`, conexiones, `fetchall`, `.df()` y las tablas de Python. La teoría 04, sección 4 |
| [DuckDB: Reading and writing Parquet](https://duckdb.org/docs/stable/data/parquet/overview) | `read_parquet` con varios archivos y particiones *hive* |
| [DuckDB: Parquet metadata](https://duckdb.org/docs/stable/data/parquet/metadata) | `parquet_metadata` y `parquet_schema`: el pie de un Parquet visto con SQL |
| [DuckDB: CSV import](https://duckdb.org/docs/stable/data/csv/overview) | Las opciones de `read_csv`: `delim`, `decimal_separator`, `nullstr` y la detección automática |
| [DuckDB: Friendly SQL](https://duckdb.org/docs/stable/sql/dialect/friendly_sql) | `GROUP BY ALL`, `EXCLUDE`, `FROM` primero y las demás comodidades del SQL de DuckDB |
| [DuckDB: Securing DuckDB](https://duckdb.org/docs/stable/operations_manual/securing_duckdb/overview) | `enable_external_access` y el resto de opciones para ejecutar SQL que no escribes tú. La teoría 04, sección 6 |


---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Proyecto](../../3-proyecto/README.md) | **Webgrafía** | [Ebooks gratuitos](../ebooks-free/README.md) |
