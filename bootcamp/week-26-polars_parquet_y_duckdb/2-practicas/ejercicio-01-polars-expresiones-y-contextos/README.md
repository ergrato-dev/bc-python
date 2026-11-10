# Ejercicio 01 — Polars: expresiones y contextos

⏱️ 1 h 30 min · Teoría previa: [01](../../1-teoria/01-polars-expresiones-y-contextos.md)

## Objetivo

Hacer con Polars lo que ya sabes hacer con pandas, y ver en qué cambia:

- una tabla sin índice, con un esquema estricto y `null` distinto de `NaN`;
- columnas nuevas con expresiones en `select` y `with_columns`;
- filas elegidas con `filter` y ordenadas con `sort`;
- un resumen por grupos con `group_by` y `agg`;
- la media de su grupo en cada fila con `over`, y un `join`;
- cuánto tarda Polars frente a pandas con un millón de filas.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-26-polars_parquet_y_duckdb/2-practicas/ejercicio-01-polars-expresiones-y-contextos/starter
uv run python main.py
```

```
Ejercicio 01 · Polars
```

`readings` son las ocho medidas de la semana 25, ahora en un `pl.DataFrame`: la del Sur del día 2 no tiene valor (`None`) y la última no sabe de qué estación es.

## Pasos

### 1. Una tabla sin índice

Descomenta el **PASO 1** y ejecuta:

```
shape: (8, 3)
┌─────────┬─────┬───────┐
│ station ┆ day ┆ value │
│ ---     ┆ --- ┆ ---   │
│ str     ┆ i64 ┆ f64   │
╞═════════╪═════╪═══════╡
│ Sur     ┆ 1   ┆ 8.0   │
│ Norte   ┆ 1   ┆ 12.5  │
│ Sur     ┆ 1   ┆ 9.5   │
│ Este    ┆ 1   ┆ 30.0  │
│ Norte   ┆ 2   ┆ 48.9  │
│ Sur     ┆ 2   ┆ null  │
│ Norte   ┆ 2   ┆ 20.0  │
│ null    ┆ 2   ┆ 5.0   │
└─────────┴─────┴───────┘
esquema: Schema({'station': String, 'day': Int64, 'value': Float64})
fila 4: ('Norte', 2, 48.9)
nulos: (1, 0, 1)
null: [False, True, False] · NaN: [False, None, True] · media: nan
```

- La tabla no tiene índice: las filas se cuentan desde 0, como en una lista. `row(4)` da la quinta como una tupla.
- Debajo de cada columna, su tipo. El esquema no cambia por un dato: `value` es `Float64` aunque tenga un `None`.
- Lo que falta es `null`, en **cualquier** tipo, y no un `NaN` disfrazado. En pandas, el `None` de `value` se habría vuelto `NaN`.
- `null` y `NaN` son cosas distintas: `NaN` es un valor de coma flotante (el resultado de `0/0`). `is_null` encuentra el `None`; `is_nan` encuentra el `NaN` y no sabe nada del `null`. La media salta los `null`, pero un `NaN` la contagia.

### 2. Expresiones en select y with_columns

Descomenta el **PASO 2** y ejecuta. Sale `value` por diez y, después:

```
shape: (4, 5)
┌─────────┬─────┬───────┬───────┬────────┐
│ station ┆ day ┆ value ┆ level ┆ tenths │
│ ---     ┆ --- ┆ ---   ┆ ---   ┆ ---    │
│ str     ┆ i64 ┆ f64   ┆ str   ┆ f64    │
╞═════════╪═════╪═══════╪═══════╪════════╡
│ Sur     ┆ 1   ┆ 8.0   ┆ bajo  ┆ 0.8    │
│ Norte   ┆ 1   ┆ 12.5  ┆ medio ┆ 1.2    │
│ Sur     ┆ 1   ┆ 9.5   ┆ bajo  ┆ 1.0    │
│ Este    ┆ 1   ┆ 30.0  ┆ alto  ┆ 3.0    │
└─────────┴─────┴───────┴───────┴────────┘
¿cambió readings? ['station', 'day', 'value']
```

- `pl.col("value") * 10` no calcula nada: es una **expresión**, una receta. La calcula el contexto donde la pones: `select` devuelve solo las columnas que pides; `with_columns` las añade a las que había.
- `pl.when(...).then(...).otherwise(...)` es el `if` de una columna entera. La primera condición que se cumple gana, como en `Scale.level`.
- `round(1)` redondea al par: 1,25 da 1,2, igual que `round` de Python.
- `with_columns` devuelve una tabla **nueva**. `readings` sigue con sus tres columnas: en Polars no existe el `inplace`.

### 3. filter y sort

Descomenta el **PASO 3** y ejecuta:

```
shape: (2, 3)
┌─────────┬─────┬───────┐
│ station ┆ day ┆ value │
│ ---     ┆ --- ┆ ---   │
│ str     ┆ i64 ┆ f64   │
╞═════════╪═════╪═══════╡
│ Norte   ┆ 1   ┆ 12.5  │
│ Este    ┆ 1   ┆ 30.0  │
└─────────┴─────┴───────┘
sin valor, con filter(value <= 10): 3 filas
[48.9, 30.0, 20.0, 12.5, 9.5, 8.0, 5.0, None]
ColumnNotFoundError: unable to find column "valor"; valid columns: ["station", "day", "value"]
```

- Varias condiciones en `filter` se juntan con "y". No hace falta la máscara con `&=` de la semana 24.
- `value <= 10` deja tres filas, no cuatro: comparar un `null` da `null`, y `filter` solo se queda con `True`. La fila sin valor no está ni en `> 10` ni en `<= 10`.
- `nulls_last=True` manda los que faltan al final al ordenar de mayor a menor.
- Una columna mal escrita es un error con la lista de las que existen, no un `KeyError` de una letra.

### 4. group_by y agg

Descomenta el **PASO 4** y ejecuta:

```
shape: (4, 6)
┌─────────┬──────┬───────┬─────────┬───────────┬───────────┐
│ station ┆ rows ┆ count ┆ missing ┆ mean      ┆ days      │
│ ---     ┆ ---  ┆ ---   ┆ ---     ┆ ---       ┆ ---       │
│ str     ┆ u32  ┆ u32   ┆ u32     ┆ f64       ┆ list[i64] │
╞═════════╪══════╪═══════╪═════════╪═══════════╪═══════════╡
│ Sur     ┆ 3    ┆ 2     ┆ 1       ┆ 8.75      ┆ [1, 2]    │
│ Norte   ┆ 3    ┆ 3     ┆ 0       ┆ 27.133333 ┆ [1, 2]    │
│ Este    ┆ 1    ┆ 1     ┆ 0       ┆ 30.0      ┆ [1]       │
│ null    ┆ 1    ┆ 1     ┆ 0       ┆ 5.0       ┆ [2]       │
└─────────┴──────┴───────┴─────────┴───────────┴───────────┘
```

- Es el `agg` con nombre de la semana 25, con expresiones: cada argumento es el nombre de la columna nueva.
- `pl.len()` cuenta las **filas** (el `size` de pandas); `count()` cuenta los **valores**; `null_count()`, los que faltan.
- La fila sin estación **sí** forma un grupo, `null`. pandas la quitaba sin avisar si no le decías `dropna=False`.
- `maintain_order=True` deja los grupos en el orden en que aparecen. Sin él, el orden puede cambiar de una ejecución a otra: Polars reparte los grupos entre los núcleos de tu máquina.
- `days` es una columna de **listas**: `unique().sort()` dentro de `agg` da una lista por grupo.

### 5. over y join

Descomenta el **PASO 5** y ejecuta:

```
shape: (3, 5)
┌─────────┬─────┬───────┬──────────────┬────────┐
│ station ┆ day ┆ value ┆ station_mean ┆ gap    │
│ ---     ┆ --- ┆ ---   ┆ ---          ┆ ---    │
│ str     ┆ i64 ┆ f64   ┆ f64          ┆ f64    │
╞═════════╪═════╪═══════╪══════════════╪════════╡
│ Norte   ┆ 1   ┆ 12.5  ┆ 27.133333    ┆ -14.63 │
│ Norte   ┆ 2   ┆ 48.9  ┆ 27.133333    ┆ 21.77  │
│ Norte   ┆ 2   ┆ 20.0  ┆ 27.133333    ┆ -7.13  │
└─────────┴─────┴───────┴──────────────┴────────┘
shape: (3, 3)
┌─────────┬───────┬──────────┐
│ station ┆ value ┆ region   │
│ ---     ┆ ---   ┆ ---      │
│ str     ┆ f64   ┆ str      │
╞═════════╪═══════╪══════════╡
│ Sur     ┆ null  ┆ Pacífica │
│ Norte   ┆ 20.0  ┆ Andina   │
│ null    ┆ 5.0   ┆ null     │
└─────────┴───────┴──────────┘
inner: 6 filas · left: 8
```

- `.over("station")` calcula la expresión por grupos y devuelve **una fila por fila**: es el `transform` de pandas. Dentro de una expresión más grande, como `gap`, se resta sin pasos intermedios.
- `join` es el `merge` de pandas. Sin `how`, es `inner`: Este y la fila sin estación no están en `stations` y desaparecen (6 filas). Con `how="left"` quedan las 8, con `region` en `null`.
- Un `null` no cruza con nada: la fila sin estación no encuentra pareja ni aunque `stations` tuviera una fila `null`.

### 6. ¿Cuánto se gana?

Descomenta el **PASO 6** y ejecuta. Los tiempos son los de la máquina del bootcamp; los tuyos serán otros:

```
¿las mismas medias? True
pandas    40.7 ms
polars     4.0 ms
```

Un millón de filas y cinco estaciones, la media de cada una. Las dos dan lo mismo; Polars, unas diez veces más rápido. Dos razones: guarda el texto de `station` en un formato compacto (Arrow), y reparte el `group_by` entre todos tus núcleos. pandas lo hace con uno.

No saques más conclusiones de una sola medida: en el ejercicio 04 comparas leer y calcular, que es lo que hace de verdad un programa.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ModuleNotFoundError: No module named 'polars'` | Ejecuta con `uv run python main.py` dentro de `starter/` |
| Sale `[(col("value")) * (dyn int: 10)]` en lugar de una tabla | Imprimiste la expresión, no su resultado: ponla dentro de `select`, `with_columns` o `filter` |
| `ColumnNotFoundError` | Mira la lista `valid columns` del mensaje: el nombre lleva una letra cambiada |
| `ComputeError: cannot compare string with numeric type` | Comparas texto con un número: Polars no convierte por su cuenta |
| El orden de los grupos cambia entre ejecuciones | Falta `maintain_order=True` en `group_by` |
| `NameError: name 'level' is not defined` | Descomenta todo el bloque del paso: `level` ocupa varias líneas |
| Los tiempos del paso 6 son muy distintos | Tu máquina es otra, y Polars usa todos sus núcleos: compara el orden de magnitud |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [05 · Polars, Parquet y DuckDB en un proyecto](../../1-teoria/05-polars-parquet-y-duckdb-en-un-proyecto.md) | **Ejercicio 01 · Polars: expresiones y contextos** | [Ejercicio 02 · Evaluación perezosa y Parquet](../ejercicio-02-evaluacion-perezosa-y-parquet/README.md) |
