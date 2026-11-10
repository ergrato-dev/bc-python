# Ejercicio 03 — SQL con DuckDB

⏱️ 1 h 30 min · Teoría previa: [04](../../1-teoria/04-duckdb-sql-sin-servidor.md)

## Objetivo

Preguntar con SQL a archivos y a tablas de Python, sin instalar ni arrancar ningún servidor:

- una consulta sobre un archivo Parquet, y su resultado como tuplas;
- el CSV del Observatorio, con punto y coma, coma decimal y `NA`;
- un `JOIN` con una tabla de pandas, y qué pasa con una de Polars;
- parámetros `?` frente a texto pegado en la consulta;
- una base de datos en un archivo, que sobrevive al programa;
- una función de ventana, y una conexión que ya no puede tocar el disco.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-26-polars_parquet_y_duckdb/2-practicas/ejercicio-03-sql-con-duckdb/starter
uv run python main.py
```

```
Ejercicio 03 · DuckDB
```

`main.py` guarda las ocho medidas de los ejercicios anteriores en `salida/readings.parquet`. `medidas.csv` es el archivo del Observatorio: `etiqueta;valor`, coma decimal y `NA` si falta. Las consultas usan rutas relativas: ejecuta siempre desde `starter/`.

## Pasos

### 1. SQL sobre un archivo

Descomenta el **PASO 1** y ejecuta:

```
┌─────────┬───────┬────────────────────┐
│ station │   n   │        mean        │
│ varchar │ int64 │       double       │
├─────────┼───────┼────────────────────┤
│ Este    │     1 │               30.0 │
│ Norte   │     3 │ 27.133333333333336 │
│ Sur     │     2 │               8.75 │
│ NULL    │     1 │                5.0 │
└─────────┴───────┴────────────────────┘

columnas: ['station', 'n', 'mean'] · tipos: [VARCHAR, BIGINT, DOUBLE]
filas: [('Este', 1, 30.0), ('Norte', 3, 27.133333333333336), ('Sur', 2, 8.75), (None, 1, 5.0)]
```

- `FROM 'salida/readings.parquet'`: el nombre del archivo hace de tabla. DuckDB ve la extensión y lo lee como Parquet.
- `duckdb.sql` devuelve una **relación**: una consulta preparada. Al imprimirla, DuckDB la ejecuta y dibuja las primeras filas.
- `fetchall()` la ejecuta otra vez y da una lista de tuplas de Python, con `None` donde SQL tiene `NULL`. Es lo que usa tu proyecto.
- `count(value)` cuenta los valores, como `count` en pandas y en Polars; `count(*)` contaría las filas. La fila sin estación forma su propio grupo, `NULL`, como en Polars.
- Ningún servidor: DuckDB es una biblioteca que corre **dentro** de tu proceso de Python, como SQLite.

### 2. El CSV del Observatorio

Descomenta el **PASO 2** y ejecuta:

```
sin opciones: [VARCHAR, VARCHAR]
[VARCHAR, DOUBLE] [('Norte', 12.5), ('Sur', 8.0), ('Centro', None)]
┌───────────┬────────┐
│ etiqueta  │ media  │
│  varchar  │ double │
├───────────┼────────┤
│ Centro    │   NULL │
│ Norte     │   30.7 │
│ Occidente │   61.0 │
│ Oriente   │   55.1 │
│ Sur       │   8.75 │
└───────────┴────────┘
```

- Sin opciones, DuckDB adivina el separador, pero no la coma decimal: `valor` sale como texto.
- `read_csv(..., delim = ';', decimal_separator = ',', nullstr = 'NA')` lo lee como lo escribe tu Observatorio: `valor` es `DOUBLE` y el `NA` es `NULL`.
- `FROM csv`: `csv` es la **variable de Python** del paso, una relación. DuckDB busca en tus variables los nombres que no son tablas.
- `GROUP BY ALL` agrupa por todas las columnas que no son agregaciones; `ORDER BY ALL`, ordena por todas. Te ahorran repetir nombres.

### 3. Tablas de pandas y de Polars

Descomenta el **PASO 3** y ejecuta:

```
[('Norte', 48.9, 'Andina'), ('Este', 30.0, None), ('Norte', 20.0, 'Andina')]
DataFrame (3, 3)
InvalidInputException: No module named 'pyarrow'
```

- `stations` es un `DataFrame` de **pandas**, y el SQL lo usa por su nombre en el `JOIN`. `LEFT JOIN ... USING (station)` es el `merge(how="left", on="station")` de la semana 25.
- `.df()` devuelve el resultado como `DataFrame` de pandas.
- `readings` es un `DataFrame` de **Polars**, y aquí falla: DuckDB pasa las tablas de Polars por Arrow, y para eso necesita la biblioteca `pyarrow`, que no está en este ejercicio (una rueda de 55 MB que se descomprime en varias veces eso). Lo mismo `.pl()`, que devuelve un resultado de Polars.
- Sin `pyarrow`, el puente entre Polars y DuckDB es un **archivo Parquet**: lo que hace tu proyecto.

### 4. Parámetros, no texto pegado

Descomenta el **PASO 4** y ejecuta:

```
pegado: [(8,)]
con ?: [(0,)]
Norte: [(3,)]
```

- `station` viene de fuera (una opción de la CLI, un formulario). Pegada con una *f-string*, la comilla del texto cierra la de la consulta y `OR '1' = '1'` se vuelve SQL: cuenta las 8 filas. Es una **inyección de SQL**, la misma de la semana 19.
- Con `?`, el texto viaja aparte como un **valor**: ninguna estación se llama así, y da 0.
- `duckdb.execute(sql, [valores])` lleva los valores en una lista, uno por `?`; `duckdb.sql` los acepta en `params=`. Usa siempre `?` para los valores que no escribes tú.

### 5. Una base de datos en un archivo

Descomenta el **PASO 5** y ejecuta:

```
filas al volver a abrir: [(9,)]
tablas: [('readings',)]
observatorio.duckdb: 537 kB
```

- `duckdb.connect(ruta)` abre (o crea) una base de datos en un archivo. Sin ruta, como en los pasos anteriores, vive en memoria y desaparece al terminar.
- `CREATE TABLE ... AS SELECT` copia el Parquet a una tabla; `INSERT` añade una fila. Al volver a abrir el archivo, las 9 filas siguen ahí.
- `read_only=True`: varios programas pueden leer a la vez, pero solo uno puede escribir. DuckDB no es PostgreSQL: para muchos usuarios escribiendo a la vez, sigue siendo PostgreSQL.
- 537 kB para nueve filas: el archivo reserva espacio en bloques. Con millones de filas, la proporción se invierte.

### 6. Ventanas y una conexión cerrada al disco

Descomenta el **PASO 6** y ejecuta:

```
[('Norte', 12.5, -14.63), ('Norte', 20.0, -7.13), ('Norte', 48.9, 21.77)]
la tabla sigue: [(8,)]
PermissionException: Cannot access file "medidas.csv" - file system operations are disabled by configuration
```

- `avg(value) OVER (PARTITION BY station)` es una **función de ventana**: la media del grupo en cada fila, sin juntar filas. Es el `over` de Polars del ejercicio 01, con los mismos números.
- `SET enable_external_access = false` corta el acceso a archivos y a la red. La tabla ya cargada sigue disponible; `medidas.csv`, no.
- DuckDB no deja volver a activarlo con la conexión abierta. Es lo que hace tu proyecto antes de ejecutar el SQL que escribe quien usa la CLI.

Cuando acabes, borra `salida/`.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `IO Error: No files found that match the pattern "salida/readings.parquet"` | Ejecuta desde `starter/`: las rutas son relativas a la carpeta donde estás |
| `Parser Error: syntax error at or near ...` | Revisa las comillas: en SQL, los textos y los archivos van entre comillas simples `'...'` |
| `Catalog Error: Table with name csv does not exist!` | Descomenta también la línea que crea la variable `csv` |
| `InvalidInputException: ... No module named 'pyarrow'` en el paso 3 | Es lo esperado: es la línea con `readings`, de Polars |
| `IO Error: Could not set lock on file ...observatorio.duckdb` | Otro programa tiene el archivo abierto para escribir: ciérralo |
| `pegado: [(0,)]` en el paso 4 | Escribiste la consulta con `?`: la versión pegada es la de la *f-string* |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 02 · Evaluación perezosa y Parquet](../ejercicio-02-evaluacion-perezosa-y-parquet/README.md) | **Ejercicio 03 · SQL con DuckDB** | [Ejercicio 04 · Una pregunta, tres herramientas](../ejercicio-04-una-pregunta-tres-herramientas/README.md) |
