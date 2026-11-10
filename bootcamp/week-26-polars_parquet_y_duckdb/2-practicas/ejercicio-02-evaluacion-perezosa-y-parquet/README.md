# Ejercicio 02 — Evaluación perezosa y Parquet

⏱️ 1 h 30 min · Teoría previa: [02](../../1-teoria/02-evaluacion-perezosa.md) y [03](../../1-teoria/03-parquet-un-formato-por-columnas.md)

## Objetivo

Dejar que Polars planee antes de calcular, y guardar las tablas en un formato que no pierde nada:

- un `LazyFrame` y su plan, antes y después de optimizarlo;
- cuándo aparece un error en una consulta perezosa;
- el mismo millón de medidas en CSV y en Parquet con tres compresiones;
- qué tipos sobreviven a cada formato;
- leer solo las columnas y las filas que hacen falta;
- una carpeta por estación, y un plan que lee solo una.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-26-polars_parquet_y_duckdb/2-practicas/ejercicio-02-evaluacion-perezosa-y-parquet/starter
uv run python main.py
```

```
Ejercicio 02 · Lazy y Parquet
```

`measurements` es un millón de medidas de cinco estaciones, una por minuto desde el 1 de enero de 2026, con un 5 % sin valor. Las genera NumPy con la semilla 26: salen siempre las mismas. Cada ejecución borra y vuelve a crear la carpeta `salida/`, donde van los archivos.

## Pasos

### 1. Un plan, no un resultado

Descomenta el **PASO 1** y ejecuta:

```
shape: (3, 3)
┌─────────────────────┬─────────┬───────┐
│ time                ┆ station ┆ value │
│ ---                 ┆ ---     ┆ ---   │
│ datetime[μs]        ┆ str     ┆ f64   │
╞═════════════════════╪═════════╪═══════╡
│ 2026-01-01 00:00:00 ┆ Centro  ┆ 38.2  │
│ 2026-01-01 00:01:00 ┆ Este    ┆ 74.5  │
│ 2026-01-01 00:02:00 ┆ Este    ┆ 42.9  │
└─────────────────────┴─────────┴───────┘
sin valor: 50172
LazyFrame
SELECT [col("time"), col("value")]
   WITH_COLUMNS:
   [(col("value") / 10.0).alias("tenths")]
    FILTER col("station") == "Norte"
    FROM
      DF ["time", "station", "value"]; PROJECT */3 COLUMNS
simple π 2/2 ["time", "value"]
  FILTER col("station") == "Norte"
  FROM
    simple π 3/3 ["time", "value", "station"]
      DF ["time", "station", "value"]; PROJECT */3 COLUMNS
(200434, 2)
```

- `lazy()` convierte la tabla en un `LazyFrame`. `filter`, `with_columns` y `select` no calculan nada: añaden pasos a un **plan**.
- `explain(optimized=False)` es el plan tal como lo escribiste, leído **de abajo arriba**: la tabla, el filtro, la columna nueva y la selección.
- `explain()` es el plan que Polars va a ejecutar. Falta `WITH_COLUMNS`: `tenths` no llega a `select`, así que no se calcula. Esto no lo haría pandas, que ejecuta cada línea en cuanto la lee.
- `collect()` ejecuta el plan: 200 434 medidas del Norte, dos columnas.

### 2. Los errores llegan al ejecutar

Descomenta el **PASO 2** y ejecuta:

```
plan creado: LazyFrame
ColumnNotFoundError: unable to find column "valor"; valid columns: ["time", "station", "value"]
esquema sin ejecutar: Schema({'time': Datetime(time_unit='us', time_zone=None), 'value': Float64})
```

- Un plan con una columna que no existe se crea sin problemas. El error llega con `collect()`.
- `collect_schema()` resuelve el esquema del resultado sin calcular ninguna fila: es la forma barata de comprobar un plan.

### 3. CSV frente a Parquet

Descomenta el **PASO 3** y ejecuta:

```
medidas-snappy.parquet            9.8 MB
medidas-uncompressed.parquet     16.1 MB
medidas-zstd.parquet              5.6 MB
medidas.csv                      37.3 MB
leer CSV        19.1 ms
leer Parquet     5.5 ms
```

- El CSV escribe cada fecha y cada número como texto: 37 MB. Parquet sin comprimir guarda los números en binario y ocupa menos de la mitad.
- Parquet comprime **cada columna por separado**. Una columna tiene datos parecidos (cinco nombres de estación que se repiten, fechas que suben de minuto en minuto), y se comprime mucho mejor que una fila.
- `zstd` es la compresión por defecto de Polars: 5,6 MB, casi siete veces menos que el CSV. `snappy` comprime menos y es la más extendida entre otras herramientas.
- Leer el Parquet es unas tres veces más rápido: no hay texto que convertir en números.

### 4. Parquet guarda los tipos

Descomenta el **PASO 4** y ejecuta:

```
CSV:     Schema({'time': String, 'station': String, 'value': Float64})
Parquet: Schema({'time': Datetime(time_unit='us', time_zone=None), 'station': String, 'value': Float64})
¿igual que en memoria? False True
nulos en Parquet: 50172
```

- Del CSV, `time` vuelve como texto: el formato no dice que esa columna es una fecha. Tendrías que convertirla tú, como con `to_datetime` en la semana 25.
- El Parquet guarda el esquema dentro del archivo. Lo que lees es **igual** a lo que escribiste, con sus tipos y sus 50 172 `null`.

### 5. Leer solo lo que hace falta

Descomenta el **PASO 5** y ejecuta:

```
media del Norte: 40.113 · ¿la misma? True
SELECT [col("value").mean()]
  simple π 1/1 ["value"]
    Parquet SCAN [salida/medidas-zstd.parquet]
    PROJECT 2/3 COLUMNS
    SELECTION: col("station") == "Norte"
    ESTIMATED ROWS: 1000000
read_parquet     7.0 ms
scan_parquet     3.7 ms
```

- `read_parquet` lee el archivo **entero** y después filtra. `scan_parquet` devuelve un `LazyFrame`: el plan sabe de dónde salen los datos.
- En el plan, el filtro y las columnas han bajado **dentro** de `Parquet SCAN`: `PROJECT 2/3 COLUMNS` lee `station` y `value`, y no `time`; `SELECTION` filtra mientras lee. Es el *pushdown* de la teoría 02.
- `math.isclose` y no `==`: las dos formas suman en otro orden, y un `float` puede cambiar en la última cifra.
- La diferencia de tiempo crece con el archivo. Con uno que no cabe en memoria, `read_parquet` falla y `scan_parquet` funciona.

### 6. Una carpeta por estación

Descomenta el **PASO 6** y ejecuta:

```
por_estacion/station=Centro/00000000.parquet 1.1 MB
por_estacion/station=Este/00000000.parquet 1.1 MB
por_estacion/station=Norte/00000000.parquet 1.1 MB
por_estacion/station=Oeste/00000000.parquet 1.1 MB
por_estacion/station=Sur/00000000.parquet 1.1 MB
SELECT [col("value").mean()]
  simple π 1/1 ["value"]
    Parquet SCAN [salida/por_estacion/station=Norte/00000000.parquet]
    PROJECT 2/3 COLUMNS
    SELECTION: col("station") == "Norte"
    ESTIMATED ROWS: 200000
¿la misma media? True
```

- `partition_by="station"` escribe una carpeta por estación, con el valor en el nombre: `station=Norte`. Es el **particionado *hive***, que entienden Polars, DuckDB, Spark y casi cualquier herramienta de datos.
- Con `hive_partitioning=True`, `scan_parquet` lee la carpeta entera y recupera `station` de los nombres.
- El plan solo abre **un** archivo de cinco: el filtro por `station` se resuelve con el nombre de la carpeta, sin leer nada.
- Particiona por la columna con la que más filtras (la estación, el mes) y con pocos valores distintos. Mil carpetas de un kilobyte son peores que un archivo.

Cuando acabes, borra `salida/`: son unos 75 MB.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ModuleNotFoundError: No module named 'polars'` | Ejecuta con `uv run python main.py` dentro de `starter/` |
| El plan del paso 1 sale en otro orden | Se lee de abajo arriba: el `DF` del final es la tabla de partida |
| `ColumnNotFoundError` en el paso 2 sale en la línea de `filter` | Llamaste a `collect()` antes: el error sale al ejecutar el plan, no al escribirlo |
| Tus tamaños del paso 3 no coinciden | Comprueba que los datos son los del README (`sin valor: 50172`); si lo son, la diferencia viene de otra versión de Polars |
| `¿la misma? False` en el paso 5 | Comparaste con `==`: usa `math.isclose` |
| `FileNotFoundError` o rutas que no existen | Ejecuta desde `starter/`: `salida/` se crea junto a `main.py` |
| El paso 6 lee los cinco archivos | Falta `hive_partitioning=True`, o el filtro no es sobre `station` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 01 · Polars: expresiones y contextos](../ejercicio-01-polars-expresiones-y-contextos/README.md) | **Ejercicio 02 · Evaluación perezosa y Parquet** | [Ejercicio 03 · SQL con DuckDB](../ejercicio-03-sql-con-duckdb/README.md) |
