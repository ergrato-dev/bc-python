# Glosario — Semana 18: Gestión de Datos con Polars

| Término | Definición |
|---------|-----------|
| Apache Arrow | Formato columnar en memoria que usa Polars. Permite operaciones SIMD y zero-copy entre procesos. |
| `collect()` | Método de `LazyFrame` que ejecuta el query plan optimizado y retorna un `DataFrame` en memoria. |
| `DataFrame` | Estructura 2D de datos en Polars (eager). Cada columna es un `Series` tipado. Sin índice de filas. |
| eager evaluation | Ejecutar cada operación inmediatamente. El modo por defecto con `read_csv()` y `DataFrame`. |
| `explain()` | Muestra el query plan lógico y optimizado de un `LazyFrame` sin ejecutarlo. |
| expresión | Objeto que describe una transformación sobre columnas. No se ejecuta hasta pasarla a `select()`, `filter()`, `agg()`, etc. |
| `fetch(n)` | Ejecuta el query plan sobre los primeros n registros. Útil para pruebas sin cargar todos los datos. |
| `fill_null()` | Reemplaza valores `null` por un valor constante o con estrategia (forward, backward, mean). |
| `filter()` | Selecciona filas que cumplan una condición expresada con `pl.col()`. Equivalente a SQL `WHERE`. |
| `group_by().agg()` | Agrupa filas por columnas y aplica funciones de agregación (sum, mean, n_unique, etc.). |
| GIL (Polars) | Polars evade el GIL usando Rust y múltiples threads para procesamiento paralelo de columnas. |
| lazy evaluation | Construir un plan de operaciones sin ejecutarlas. Se ejecuta todo junto al llamar `collect()`. |
| `LazyFrame` | Versión lazy de un DataFrame. Almacena un query plan que se optimiza antes de ejecutarse. |
| `over()` | Función de ventana: aplica una agregación por grupo sin colapsar filas. Equivalente a SQL `PARTITION BY`. |
| `pivot()` | Transforma valores únicos de una columna en nuevas columnas. Equivalente a Excel pivot table. |
| `pl.col()` | Expresión que referencia una columna por nombre. Base de casi todas las expresiones de Polars. |
| `pl.lit()` | Expresión que representa un valor literal constante en una transformación. |
| `pl.when().then().otherwise()` | Expresión condicional equivalente a SQL `CASE WHEN`. Retorna valores distintos según la condición. |
| predicate pushdown | Optimización de Polars que aplica filtros (`filter`) lo antes posible en el pipeline, antes de cargar datos. |
| projection pushdown | Optimización que lee solo las columnas realmente usadas del archivo (especialmente eficiente en Parquet). |
| Parquet | Formato de archivo columnar y comprimido. Preserva tipos, más eficiente que CSV para almacenamiento. |
| `scan_csv()` | Lee un CSV de forma lazy (no carga en memoria). Retorna `LazyFrame`. Acepta glob patterns. |
| `scan_parquet()` | Lee Parquet de forma lazy. Más eficiente que `scan_csv` (columnar, sin parsing de strings). |
| `select()` | Elige o transforma columnas. Retorna nuevo DataFrame solo con las columnas especificadas. |
| `Series` | Una columna de datos tipada en Polars. Equivalente a `pd.Series` pero sin índice. |
| `unpivot()` | Inverso de `pivot()`: transforma columnas en filas (formato largo). Equivalente a `melt()` en Pandas. |
| `with_columns()` | Añade o reemplaza columnas con expresiones. El DataFrame original no se modifica (inmutable). |
