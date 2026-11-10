# Glosario — Semana 26

| Término | Definición |
|---|---|
| **`agg`** | En Polars, dentro de `group_by`: una o varias expresiones calculadas por grupo; da **una fila por grupo** |
| **Arrow** | Un formato en memoria para tablas por columnas que comparten Polars, DuckDB y `pyarrow`. Pasar tablas entre ellos en memoria necesita `pyarrow` |
| **`collect`** | Ejecuta el plan de un `LazyFrame` y devuelve un `DataFrame` |
| **`collect_schema`** | Las columnas y los tipos del resultado de un plan, sin calcular ninguna fila |
| **Column chunk** | En Parquet, los valores de una columna dentro de un grupo de filas, juntos y comprimidos |
| **Contexto** | Dónde se calcula una expresión de Polars: `select`, `with_columns`, `filter` o `group_by().agg()` |
| **DuckDB** | Base de datos SQL de análisis que corre dentro de tu proceso, sin servidor, y lee Parquet y CSV directamente |
| **`enable_external_access`** | Opción de DuckDB: con `false`, el SQL no puede tocar archivos, red ni extensiones, y no se puede volver a activar con la conexión abierta |
| **Evaluación perezosa** | Construir el plan entero antes de ejecutar nada, para poder optimizarlo |
| **`explain`** | Escribe el plan de un `LazyFrame`; se lee de abajo arriba |
| **Expresión** | Un cálculo sobre columnas descrito sin hacerlo, como `pl.col("value").mean()`. Lo calcula su contexto |
| **`fetchall`** | Ejecuta una consulta de DuckDB y da sus filas como lista de tuplas, con `None` por cada `NULL` |
| **Hive (particionado)** | Carpetas con el nombre `columna=valor`, una por valor; un filtro por esa columna abre solo su carpeta |
| **`join`** | El `merge` de Polars: `inner` por defecto, y `left`, `full`, `semi` o `anti` |
| **`LazyFrame`** | Una tabla de Polars que es un plan: sus métodos añaden pasos y nada se calcula hasta `collect` |
| **`maintain_order`** | En `group_by`, deja los grupos en el orden en que aparecen; sin él, el orden puede cambiar |
| **`null`** | En Polars y DuckDB, el dato que falta, en cualquier tipo. Distinto de `NaN` |
| **OLAP y OLTP** | Análisis de muchas filas con pocas consultas (DuckDB) frente a muchas escrituras pequeñas a la vez (PostgreSQL) |
| **`over`** | Calcula una expresión por grupos y devuelve una fila por fila: el `transform` de pandas |
| **Parámetro `?`** | Un hueco en el SQL para un valor que viaja aparte; evita la inyección de SQL |
| **Parquet** | Formato de archivo por columnas, comprimido, con el esquema y estadísticas dentro |
| **Pie (footer)** | El final de un Parquet: esquema, dónde empieza cada bloque y su mínimo, máximo y nulos |
| **Polars** | Biblioteca de tablas escrita en Rust: sin índice, con tipos estrictos, en paralelo y con modo perezoso |
| **Pushdown** | Mover un filtro (*predicate*) o una elección de columnas (*projection*) hasta la lectura del archivo |
| **Relación** | En DuckDB, una consulta preparada; cada `fetchall` la vuelve a ejecutar |
| **Row group** | En Parquet, un trozo de la tabla con muchas filas; cada uno guarda sus columnas por separado |
| **`scan_parquet`** | Abre un Parquet como `LazyFrame`, sin leerlo todavía |
| **`sink_parquet`** | Ejecuta un plan por trozos y escribe el resultado en un Parquet, sin tenerlo entero en memoria |
| **Streaming** | Motor de Polars que procesa los datos por trozos: `collect(engine="streaming")` |
| **`with_columns`** | Contexto que devuelve las columnas que había más las nuevas |
| **zstd y snappy** | Compresiones de Parquet: `zstd` ocupa menos (la de Polars por defecto); `snappy` es la más compatible |


---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Videografía](../4-recursos/videografia/README.md) | **Glosario** | [Rúbrica de evaluación](../rubrica-evaluacion.md) |
