# Ejercicio 04 — Una pregunta, tres herramientas

⏱️ 1 h 30 min · Teoría previa: [05](../../1-teoria/05-polars-parquet-y-duckdb-en-un-proyecto.md)

## Objetivo

Llevar un archivo del Observatorio de CSV a Parquet, y contestar la misma pregunta con pandas, Polars y DuckDB:

- leer el CSV del Observatorio con Polars, con sus opciones;
- ver qué hace cada biblioteca con una fila mala;
- convertir un millón de medidas a Parquet sin cargarlas enteras en memoria;
- comprobar que las tres herramientas dan la misma respuesta;
- medir cuánto tarda cada una, leyendo incluido;
- ver qué le falta a pandas para leer Parquet.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-26-polars_parquet_y_duckdb/2-practicas/ejercicio-04-una-pregunta-tres-herramientas/starter
uv run python main.py
```

```
Ejercicio 04 · Una pregunta, tres herramientas
```

`medidas.csv` es el del ejercicio 03. `rota.csv` tiene una fila mala: `Sur;9,5 mm`. `CSV_OPTIONS` son las tres opciones que dicen a Polars cómo es un CSV del Observatorio.

## Pasos

### 1. El CSV del Observatorio con Polars

Descomenta el **PASO 1** y ejecuta:

```
sin opciones: Schema({'etiqueta': String, 'valor': String})
con opciones: Schema({'etiqueta': String, 'valor': Float64})
[('Norte', 12.5), ('Sur', 8.0), ('Centro', None)]
```

- Sin `decimal_comma`, `12,5` no es un número y `valor` sale como texto, igual que en DuckDB sin opciones.
- `separator=";"`, `decimal_comma=True` y `null_values="NA"`: `valor` es `Float64` y `NA` es `null`. `**CSV_OPTIONS` pasa el diccionario como argumentos con nombre.
- `rename` pone las columnas en inglés, como `FILE_COLUMNS` en `frames.py`.

### 2. Una fila mala

Descomenta el **PASO 2** y ejecuta:

```
pandas: str
Polars, ComputeError: could not parse `9,5 mm` as dtype `f64` at column 'valor' (column number 2)
ignore_errors: [12.5, 8.0, None, 48.9]
```

- pandas lee la columna entera como texto, sin avisar: lo viste en la semana 24.
- Con `schema_overrides`, le dices a Polars qué tipo **tiene** que tener `valor`. Una fila que no encaja es un error con el texto, la columna y su número: sabes qué arreglar.
- `ignore_errors=True` convierte lo que no encaja en `null`. Úsalo solo si después cuentas los `null`: si no, pierdes datos sin enterarte.
- Tu Observatorio no lee el CSV con ninguna de las dos: `Series.parse` da un error **por línea**, con su número, y sigue con las demás. Polars entra después, con los datos ya validados.

### 3. Un millón de medidas, de CSV a Parquet

Descomenta el **PASO 3** y ejecuta:

```
['etiqueta;valor', 'Centro;38,2', 'Este;74,5']
grande.csv       10.4 MB
grande.parquet    2.5 MB
```

- `write_csv` con `decimal_comma=True` y `null_value="NA"` escribe como el Observatorio.
- `scan_csv(...).sink_parquet(...)` es un plan que lee el CSV **por trozos** y los va escribiendo en el Parquet: el millón de filas no tiene que estar entero en memoria. Con un CSV de 20 GB en un portátil de 8 GB, es la diferencia entre terminar y no terminar.
- El Parquet ocupa la cuarta parte. Aquí gana menos que en el ejercicio 02 porque no hay fechas: los valores aleatorios se comprimen mal.

### 4. Una pregunta, tres respuestas

Descomenta el **PASO 4** y ejecuta:

```
pandas  [('Norte', 190361, 40.11), ('Oeste', 190521, 40.05), ('Sur', 189453, 40.02), ('Este', 189665, 39.98), ('Centro', 189828, 39.96)]
polars  [('Norte', 190361, 40.11), ('Oeste', 190521, 40.05), ('Sur', 189453, 40.02), ('Este', 189665, 39.98), ('Centro', 189828, 39.96)]
duckdb  [('Norte', 190361, 40.11), ('Oeste', 190521, 40.05), ('Sur', 189453, 40.02), ('Este', 189665, 39.98), ('Centro', 189828, 39.96)]
¿la misma respuesta? True
```

- La pregunta: cuántas medidas y qué media tiene cada etiqueta, de mayor a menor media.
- pandas lee el CSV (no sabe leer Parquet sin ayuda: paso 6); Polars y DuckDB, el Parquet.
- Los conteos son iguales y las medias, iguales salvo en la última cifra: cada una suma en su orden. Por eso `math.isclose` para las medias y `==` para el resto.
- `with_polars` recibe un `LazyFrame`: le da igual que venga de `scan_csv` o de `scan_parquet`. En el paso 5 lo aprovechas.

### 5. ¿Cuánto tarda cada una?

Descomenta el **PASO 5** y ejecuta. Los tiempos son los de la máquina del bootcamp; los tuyos serán otros:

```
pandas, CSV        100.3 ms
Polars, CSV         20.7 ms
Polars, Parquet      8.4 ms
DuckDB, Parquet      6.2 ms
```

- Cada tiempo es **leer y calcular**, como en un programa de verdad.
- Del CSV, Polars es unas cinco veces más rápido que pandas: lee el texto con todos tus núcleos.
- Del Parquet, Polars y DuckDB tardan menos de 10 ms: no hay texto que convertir, y solo leen las dos columnas que necesitan.
- Entre Polars y DuckDB, con estos datos, la diferencia es pequeña. Elige por cómo quieres escribir la pregunta (expresiones o SQL), no por 2 ms.

### 6. pandas y Parquet

Descomenta el **PASO 6** y ejecuta:

```
ImportError: Unable to find a usable engine; tried using: 'pyarrow', 'fastparquet'.
DataFrame (200434, 2) float64
```

- `pd.read_parquet` necesita `pyarrow` o `fastparquet`, y este ejercicio no tiene ninguna de las dos.
- DuckDB sí lee Parquet sin ellas, y `.df()` da el resultado como `DataFrame` de pandas: aquí, las 200 434 medidas del Norte.
- En tu proyecto pasa lo mismo: Polars escribe el Parquet y DuckDB lo lee, sin `pyarrow`. Una dependencia menos es una imagen más pequeña y un aviso de seguridad menos que vigilar.

Cuando acabes, borra `salida/`.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `TypeError: read_csv() got an unexpected keyword argument 'decimal_comma'` | No usas el Polars del ejercicio: ejecuta con `uv run` dentro de `starter/`, que instala la 2.1.0 |
| `pandas: float64` en el paso 2 | Estás leyendo `medidas.csv`, no `rota.csv` |
| `¿la misma respuesta? False` | Comparaste las medias con `==`, o una de las tres no ordena de mayor a menor |
| `IO Error: No files found that match the pattern` en DuckDB | Descomenta el paso 3: es el que escribe `salida/grande.parquet` |
| Los tiempos del paso 5 salen en otro orden | Tu máquina es otra: compara el orden de magnitud, no la cifra |
| El paso 6 no da `ImportError` | Tienes `pyarrow` instalado en ese entorno: está bien, pandas lo usa |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 03 · SQL con DuckDB](../ejercicio-03-sql-con-duckdb/README.md) | **Ejercicio 04 · Una pregunta, tres herramientas** | [Proyecto · Exportar a Parquet y preguntar con SQL](../../3-proyecto/README.md) |
