# Ejercicio 01 — Series, índice y tipos

⏱️ 1 h 30 min · Teoría previa: [01](../../1-teoria/01-series-indice-tipos-y-alineacion.md)

## Objetivo

La pieza básica de pandas, una columna con etiquetas:

- crear una `Series` y ver sus valores, su índice y su nombre;
- ver qué tipo sale con enteros, texto, mezclas y datos que faltan;
- sumar dos `Series` con índices distintos;
- elegir por etiqueta y por posición, y caer en la trampa del índice de enteros;
- calcular con datos que faltan;
- limpiar y contar texto.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-24-pandas_series_dataframe_y_seleccion/2-practicas/ejercicio-01-series-indice-y-tipos/starter
uv run python main.py
```

```
Ejercicio 01 · Series, índice y tipos
```

La primera vez, uv instala `pandas==3.1.0` y sus dependencias (NumPy entre ellas) en el entorno del ejercicio.

## Pasos

### 1. Una Series y su índice

Descomenta el **PASO 1** y ejecuta:

```
0    12.5
1     8.0
2    48.9
dtype: float64
índice: RangeIndex(start=0, stop=3, step=1)
valores: [12.5  8.  48.9] · ndarray
Norte    12.5
Sur       8.0
Este     48.9
Name: valor, dtype: float64
Sur: 8.0 · desde un dict: {'A': 1, 'B': 2}
```

- Sin índice, pandas numera desde 0 con un `RangeIndex`.
- `to_numpy()` devuelve el array de NumPy que hay dentro: lo de la semana 23.
- Con `index=` cada valor tiene una etiqueta, y `stations["Sur"]` lo elige por ella. `name` sale debajo: será el nombre de la columna cuando la `Series` esté en una tabla.

### 2. Tipos, y lo que pasa con lo que falta

Descomenta el **PASO 2** y ejecuta:

```
enteros: int64
enteros con None: [1.0, nan, 3.0] float64
texto: str · con None: ['A', nan]
mezcla: object
Int64: [1, <NA>, 3] Int64
a float64: [1.0, 2.5]
```

- Un `None` entre enteros convierte la columna a `float64`: NaN solo existe en coma flotante.
- El texto es `str`, el tipo de texto de pandas 3. Un tutorial antiguo te diría `object`.
- Mezclar números y texto da `object`: lento, como en NumPy.
- `Int64` (con mayúscula) admite enteros con datos que faltan, marcados con `<NA>`.
- Para convertir `"2,5"` a número, primero la coma por punto con `.str.replace`, después `astype`.

### 3. Las operaciones se alinean por el índice

Descomenta el **PASO 3** y ejecuta:

```
Este      NaN
Norte     NaN
Sur      25.0
dtype: float64
{'Este': 7.0, 'Norte': 10.0, 'Sur': 25.0}
por posición: [15.0, 27.0]
```

pandas suma las mismas **etiquetas**: Sur con Sur. Norte y Este solo están en una de las dos y dan NaN. Con `add(..., fill_value=0)` lo que falta cuenta como 0.

La última línea suma los arrays de dentro, por **posición**: 10 + 5 y 20 + 7. Norte con Sur y Sur con Este: números sin sentido, y sin ningún error.

### 4. Etiqueta o posición

Descomenta el **PASO 4** y ejecuta:

```
loc[10]: a · iloc[0]: a · [10]: a
KeyError: 0
loc[10:20]: ['a', 'b'] · iloc[0:2]: ['a', 'b']
```

El índice es `[10, 20, 30]`. Con corchetes, un entero es una **etiqueta**: `codes[10]` funciona y `codes[0]` da `KeyError`, porque no hay ninguna fila con etiqueta 0. `.loc` siempre es etiqueta y `.iloc` siempre posición: úsalos y no hay duda.

En los cortes, `.loc[10:20]` **incluye** el 20, y `.iloc[0:2]` **excluye** la posición 2. Dan las mismas filas por caminos distintos.

### 5. NaN se salta solo

Descomenta el **PASO 5** y ejecuta:

```
pandas mean 10.25 · NumPy mean nan
count 2 · size 3 · sum 20.5
std pandas 3.182 (ddof=1) · std NumPy 2.250 (ddof=0)
isna: [False, True, False] · fillna: [12.5, 0.0, 8.0]
dropna: {0: 12.5, 2: 8.0}
```

- Los métodos de pandas saltan los NaN; el mismo array en NumPy da `nan`.
- `count` cuenta los que tienen valor; `size`, todos.
- La desviación de pandas es la de la muestra (`ddof=1`); la de NumPy, la de la población. Con dos valores, la diferencia es grande.
- `dropna` quita el que falta, pero las etiquetas de los demás (0 y 2) no cambian.

### 6. Texto y conteos

Descomenta el **PASO 6** y ejecuta:

```
limpias: ['Norte', 'Sur', 'Norte', 'Este', 'Sur', 'Norte']
Norte    3
Sur      2
Este     1
Name: count, dtype: int64
distintas: ['Norte', 'Sur', 'Este'] · cuántas: 3
¿empieza por N? [True, False, True, False, False, True]
```

`.str` aplica un método de cadena a todos los valores. Sin limpiar, `"sur"` y `"Sur "` serían dos estaciones más: cambia `clean` por `labels` en la línea de `value_counts` y compruébalo.

`value_counts` cuenta de más a menos. `unique` da los distintos en el orden en que aparecen.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ModuleNotFoundError: No module named 'pandas'` | Ejecuta con `uv run python main.py` dentro de `starter/`, no con `python` a secas |
| `texto: object` en lugar de `str` | Tienes pandas 2: comprueba `uv run python -c "import pandas; print(pandas.__version__)"`, debe ser `3.1.0` |
| `ValueError: could not convert string to float: '2,5'` | Falta el `.str.replace(",", ".")` antes de `astype` |
| `KeyError: 0` en una línea que no es la del `try` | Usas `codes[0]` o `stations[0]`: con etiquetas, `.iloc[0]` |
| La suma del paso 3 da números en lugar de NaN | Has sumado `to_numpy()`: eso suma por posición |
| `NameError: name 'np' is not defined` | No borres el `import numpy as np` del principio |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [05 · pandas en un proyecto](../../1-teoria/05-pandas-en-un-proyecto.md) | **Ejercicio 01 · Series, índice y tipos** | [Ejercicio 02 · DataFrames: leer y mirar](../ejercicio-02-dataframes-leer-y-mirar/README.md) |
