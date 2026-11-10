# 01 · Polars: expresiones y contextos

⏱️ 50 min

## 🎯 Objetivos

- Explicar qué es Polars y en qué se diferencia de pandas: sin índice, con tipos estrictos y en paralelo.
- Distinguir `null` de `NaN`, y saber qué hace cada operación con los dos.
- Escribir expresiones con `pl.col`, `pl.lit` y `pl.when`, y usarlas en los cuatro contextos: `select`, `with_columns`, `filter` y `group_by().agg()`.
- Calcular por grupos sin juntar filas con `over`, y cruzar tablas con `join`.
- Traducir a Polars lo que ya sabes hacer con pandas.

---

## 1. Otra biblioteca de tablas

En las semanas 24 y 25 aprendiste pandas, la biblioteca de tablas más usada de Python. Polars hace lo mismo con otras decisiones de diseño:

| | pandas | Polars |
|---|---|---|
| Escrito en | Python, C y Cython, sobre NumPy | Rust, sobre el formato Arrow |
| Índice | Sí: etiquetas de fila, alineación | No: las filas son posiciones, como en una lista |
| Tipos | Una columna puede volverse `object` o `str` sin avisar | Cada columna tiene un tipo fijo; si un dato no encaja, error |
| Lo que falta | `NaN` (o `NA`, según el tipo) | `null`, en cualquier tipo |
| Núcleos | Uno | Todos los de tu máquina |
| Ejecución | Cada línea en cuanto la lees | Inmediata o **perezosa**: primero planea, después ejecuta (teoría 02) |
| Cambiar una tabla | `inplace`, asignar a `df["col"]`, *copy-on-write* | Nunca: cada operación devuelve una tabla nueva |

No es "mejor que pandas" en todo. pandas tiene más años, más bibliotecas que lo esperan (las de gráficos de la semana 27, las de estadística de la 28) y mejor soporte para series de tiempo con índice. Polars es más rápido y más estricto, y su API es más pequeña y regular. Conocer las dos te deja elegir.

```python
import polars as pl

readings = pl.DataFrame(
    {
        "station": ["Sur", "Norte", "Sur", None],
        "value": [8.0, 12.5, None, 5.0],
    }
)
readings.schema   # Schema({'station': String, 'value': Float64})
readings.row(1)   # ('Norte', 12.5)
readings.height   # 4 filas; readings.width, 2 columnas
```

`pl.DataFrame` acepta un diccionario de listas, como pandas. Si quieres fijar los tipos (y debes, cuando la tabla puede salir vacía), pasa `schema={"station": pl.String, "value": pl.Float64}`.

---

## 2. Tipos estrictos

Cada columna de Polars tiene un tipo (`pl.Int64`, `pl.Float64`, `pl.String`, `pl.Boolean`, `pl.Date`, `pl.Datetime`, `pl.List(...)`...) y no cambia por su cuenta:

```python
pl.DataFrame({"value": [1.0, "dos"]})
# TypeError: unexpected value while building Series of type Float64; found value of type String: "dos"
```

pandas habría creado una columna `object` con un número y un texto, y el error habría aparecido más tarde, lejos de su causa. Polars falla **donde está el problema**. Lo mismo al leer un CSV con un tipo fijado (ejercicio 04, paso 2) o al comparar texto con números:

```python
readings.filter(pl.col("station") > 3)
# ComputeError: cannot compare string with numeric type (i32)
```

Para cambiar un tipo, lo pides tú: `pl.col("day").cast(pl.String)`.

---

## 3. `null` no es `NaN`

En pandas, un dato que falta en una columna de números es `NaN`, un valor especial de coma flotante. En Polars hay dos cosas distintas:

| | `null` | `NaN` |
|---|---|---|
| Qué es | "No hay dato" | Un resultado de coma flotante indefinido, como `0/0` |
| En qué tipos | Todos: números, texto, fechas | Solo `Float32` y `Float64` |
| Cómo se busca | `is_null()`, `null_count()` | `is_nan()` |
| `mean`, `sum`, `count` | Lo saltan | Lo cuentan: la media da `NaN` |
| Al comparar | Da `null`: `filter` quita la fila | Da `False` |

```python
values = pl.Series([1.0, None, float("nan")])
values.is_null().to_list()   # [False, True, False]
values.is_nan().to_list()    # [False, None, True]
values.mean()                # nan: el NaN contagia; el null no cuenta
```

Un `None` de Python se convierte en `null`. Por eso `columnar.frame_of` de tu proyecto da `null` donde `frames.frame_of` daba `NaN`: los dos significan "esta medida no tiene valor", pero se buscan distinto. Un test que cuenta los que faltan con `is_nan()` daría 0 (lo descubres en el paso 12 del proyecto).

---

## 4. Expresiones

Una **expresión** describe un cálculo sobre columnas, sin hacerlo:

```python
pl.col("value") * 10                       # cada valor por diez
pl.col("value").mean()                     # la media (un solo número)
pl.col("value").fill_null(0)               # los null, a cero
(pl.col("value") / 10).round(1).alias("tenths")   # con otro nombre
pl.lit("Norte")                            # un valor fijo, repetido en cada fila
pl.len()                                   # cuántas filas hay
```

Si imprimes una expresión, ves la receta: `[(col("value")) * (dyn int: 10)]`. Se calcula cuando la pones en un **contexto**.

El `if` de una columna entera se escribe con `pl.when`. La primera condición que se cumple gana:

```python
level = (
    pl.when(pl.col("value") >= 30).then(pl.lit("alto"))
    .when(pl.col("value") >= 10).then(pl.lit("medio"))
    .otherwise(pl.lit("bajo"))
)
```

Un `null` en `value` no cumple ninguna condición, y cae en `otherwise`. Si quieres otro texto para los que faltan, pon primero `pl.when(pl.col("value").is_null()).then(pl.lit("sin dato"))`.

Las expresiones son objetos de Python: las guardas en variables, las pasas a funciones y las reutilizas en varias consultas, como `level`.

---

## 5. Los cuatro contextos

| Contexto | Qué devuelve | En pandas |
|---|---|---|
| `select(expr, ...)` | Solo las columnas que pides | `df[["a", "b"]]`, `df.assign(...)[...]` |
| `with_columns(expr, ...)` | Todas las que había más las nuevas (o reemplazadas) | `df.assign(...)` |
| `filter(expr, ...)` | Las filas donde la expresión es `True` | `df.loc[mascara]` |
| `group_by(...).agg(expr, ...)` | Una fila por grupo | `df.groupby(...).agg(...)` |

```python
readings.select("station", (pl.col("value") * 10).alias("x10"))
readings.with_columns(level.alias("level"))
readings.filter(pl.col("value") > 10, pl.col("station") != "Sur")   # varias: "y"
readings.sort("value", descending=True, nulls_last=True)
```

- Las columnas nuevas se nombran con `alias` o con un argumento con nombre: `with_columns(x10=pl.col("value") * 10)`.
- Dentro de un mismo `select` o `with_columns`, las expresiones se calculan **a la vez**, en paralelo: una no puede usar la columna que crea otra del mismo paréntesis. Encadena dos `with_columns` si la necesitas.
- Nada cambia la tabla de partida: `readings` sigue igual después de todas estas líneas.

### `group_by` y `agg`

```python
readings.group_by("station", maintain_order=True).agg(
    rows=pl.len(),
    count=pl.col("value").count(),
    missing=pl.col("value").null_count(),
    mean=pl.col("value").mean(),
)
```

Es la agregación con nombre de la semana 25, con expresiones. Tres diferencias con pandas:

- **El orden.** Polars reparte los grupos entre núcleos, y el orden del resultado puede cambiar de una ejecución a otra. `maintain_order=True` los deja en orden de aparición (el `sort=False` de pandas). Si no te importa el orden, no lo pongas: es un poco más lento.
- **La clave que falta.** Las filas con `station` `null` forman su propio grupo. pandas las quitaba sin avisar.
- **Cualquier expresión.** `pl.col("day").unique().sort()` dentro de `agg` da una **lista** por grupo; `(pl.col("value") > 30).sum()`, cuántas pasan de 30.

---

## 6. `over` y `join`

`over` calcula una expresión por grupos y devuelve **una fila por fila**: es el `transform` de pandas, pero dentro de cualquier expresión.

```python
readings.with_columns(
    gap=pl.col("value") - pl.col("value").mean().over("station")
)
```

`join` es el `merge` de pandas:

```python
readings.join(stations, on="station", how="left")
```

- Sin `how`, es `inner`. Los demás: `left`, `right`, `full` (el `outer` de pandas), `semi` (las filas de la izquierda que tienen pareja, sin añadir columnas) y `anti` (las que no la tienen).
- `validate="m:1"` (o `"1:1"`, `"1:m"`) comprueba las claves repetidas, como `validate` en pandas.
- Un `null` no cruza con otro `null`, salvo que pidas `nulls_equal=True`.

---

## 7. De pandas a Polars

| pandas | Polars |
|---|---|
| `df["value"]` | `df.get_column("value")` (o `df["value"]`) |
| `df[df["value"] > 10]` | `df.filter(pl.col("value") > 10)` |
| `df.assign(x=df["value"] * 2)` | `df.with_columns(x=pl.col("value") * 2)` |
| `df.groupby("k", sort=False).agg(n=("v", "count"))` | `df.group_by("k", maintain_order=True).agg(n=pl.col("v").count())` |
| `df.groupby("k")["v"].transform("mean")` | `pl.col("v").mean().over("k")` |
| `df.merge(other, on="k", how="outer")` | `df.join(other, on="k", how="full")` |
| `df.sort_values("v", ascending=False, na_position="last")` | `df.sort("v", descending=True, nulls_last=True)` |
| `df["v"].isna()` | `pl.col("v").is_null()` |
| `df.loc[3]` | `df.row(3)` (no hay etiquetas: es la posición) |
| `df.to_csv(...)` | `df.write_csv(...)` |

`pl.from_pandas(df)` y `df.to_pandas()` convierten entre las dos, pero necesitan `pyarrow`, que no está en tu proyecto. Si alguna vez lo necesitas, tendrás que añadirlo como dependencia.

---

## 8. Errores frecuentes

| Error | Por qué está mal | Qué hacer |
|---|---|---|
| Buscar los que faltan con `is_nan()` | En Polars, lo que falta es `null` | `is_null()` y `null_count()` |
| Usar en un `with_columns` la columna que crea otra expresión del mismo paréntesis | Se calculan a la vez | Dos `with_columns` seguidos |
| Confiar en el orden de `group_by` | Cambia entre ejecuciones | `maintain_order=True`, o `sort` después |
| `df["col"] = ...` | Polars no deja cambiar una tabla | `df = df.with_columns(...)` |
| Crear una tabla vacía sin `schema` | Las columnas salen de tipo `Null` | Pasa `schema={...}` |
| Esperar que `inner` conserve todas las filas | Las que no cruzan desaparecen | `how="left"` |

---

## ✅ Qué debes saber al terminar

- [ ] Tres diferencias de diseño entre pandas y Polars.
- [ ] Qué es `null`, qué es `NaN`, y qué hacen con ellos `mean`, `count` y `filter`.
- [ ] Qué es una expresión, y qué devuelve cada uno de los cuatro contextos.
- [ ] Para qué sirve `maintain_order`, y qué pasa con la clave `null` en `group_by`.
- [ ] Cómo se escriben en Polars `transform` y `merge`.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 26](../README.md) | **01 · Polars: expresiones y contextos** | [02 · Evaluación perezosa](02-evaluacion-perezosa.md) |
