# Ejercicio 03 — Dar forma con pivot y melt

⏱️ 1 h 30 min · Teoría previa: [03](../../1-teoria/03-dar-forma-pivot-melt-y-crosstab.md)

## Objetivo

La misma información en dos formas, y pasar de una a otra:

- de formato largo (una fila por medida) a ancho (una columna por estación) con `pivot`;
- qué hacer cuando dos medidas caen en la misma celda: `pivot_table`;
- volver a formato largo con `melt`, sin perder nada;
- `stack` y `unstack`, que mueven niveles entre el índice y las columnas;
- contar con `crosstab`;
- elegir la forma según lo que vayas a hacer.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-25-pandas_groupby_merge_y_series_de_tiempo/2-practicas/ejercicio-03-dar-forma-con-pivot-y-melt/starter
uv run python main.py
```

```
Ejercicio 03 · Dar forma
```

`long` tiene seis medidas en formato largo: una fila por medida, con su día (`lun`, `mar`, `mié`), su estación y su valor.

## Pasos

### 1. pivot, de largo a ancho

Descomenta el **PASO 1** y ejecuta:

```
station  Este  Norte  Sur
day                      
lun      61.0   12.5  8.0
mar       NaN   48.9  9.5
mié       NaN   20.0  NaN
forma: larga (6, 3) · ancha (3, 3)
media de cada estación: {'Este': 61.0, 'Norte': 27.13, 'Sur': 8.75}
media de cada día: {'lun': 27.17, 'mar': 29.2, 'mié': 20.0}
```

- `pivot` usa una columna como índice (`day`), otra como columnas (`station`) y una tercera para rellenar las celdas (`value`). Índice y columnas salen ordenados.
- Las celdas sin medida son NaN: Este solo midió el lunes.
- En formato ancho, la media de cada estación es la de cada **columna** (`mean()`), y la de cada día, la de cada **fila** (`mean(axis="columns")`).

### 2. Dos valores en la misma celda

Descomenta el **PASO 2** y ejecuta:

```
ValueError: Index contains duplicate entries, cannot reshape
{'Este': 61.0, 'Norte': 13.5, 'Sur': 8.0}
station  Este  Norte  Sur
day                      
lun         1      2    1
mar         0      1    1
mié         0      1    0
```

- Con dos medidas de Norte el lunes, `pivot` no sabe cuál poner en la celda y lanza `ValueError`.
- `pivot_table` las junta con `aggfunc`: la media de 12,5 y 14,5 es 13,5. Es un `groupby` de dos claves seguido de `unstack`.
- Con `aggfunc="count"` y `fill_value=0` cuenta las medidas de cada celda.

### 3. melt, de ancho a largo

Descomenta el **PASO 3** y ejecuta:

```
   day station  value
0  lun    Este   61.0
1  mar    Este    NaN
2  mié    Este    NaN
3  lun   Norte   12.5
filas: 9 · con valor: 6
¿vuelta completa? True
```

- `melt` hace lo contrario de `pivot`: cada celda vuelve a ser una fila. `id_vars` son las columnas que se quedan como están.
- Salen 9 filas (3 días × 3 estaciones), tres con NaN: las celdas vacías también se convierten en fila.
- Tras `dropna`, ordenar y renumerar, es **exactamente** la tabla del principio: `equals` compara valores, tipos e índice.

### 4. stack y unstack

Descomenta el **PASO 4** y ejecuta:

```
day  station
lun  Este       61.0
     Norte      12.5
     Sur         8.0
mar  Este        NaN
dtype: float64
índice: ['day', 'station'] · filas: 9 · con valor: 6
day       lun   mar   mié
station                  
Este     61.0   NaN   NaN
Norte    12.5  48.9  20.0
Sur       8.0   9.5   NaN
```

- `stack` pasa las columnas al índice: una `Series` con índice de dos niveles. En pandas 3 **conserva** los NaN; en tutoriales antiguos los quitaba.
- `unstack("day")` pasa el nivel `day` a columnas: la tabla traspuesta, con las estaciones en filas.

### 5. Tablas de conteo con crosstab

Descomenta el **PASO 5** y ejecuta:

```
level    bajo  medio  alto
station                   
Este        0      0     1
Norte       0      3     0
Sur         2      0     0
{'bajo': 2, 'medio': 3, 'alto': 1, 'total': 6}
{'bajo': 0.0, 'medio': 1.0, 'alto': 0.0}
```

- `crosstab` cuenta cuántas filas hay de cada combinación: estación por nivel.
- Las columnas salen en el orden de las categorías de `pd.cut` (bajo, medio, alto), no por orden alfabético.
- `margins=True` añade los totales; `normalize="index"` reparte cada fila en proporciones: todas las medidas de Norte son de nivel medio.

### 6. Ancho para leer, largo para calcular

Descomenta el **PASO 6** y ejecuta:

```
largo, groupby: {'Este': 61.0, 'Norte': 48.9, 'Sur': 9.5}
ancho, max:     {'Este': 61.0, 'Norte': 48.9, 'Sur': 9.5}
de lunes a martes: {'Este': nan, 'Norte': 36.4, 'Sur': 1.5}
station  Este  Norte  Sur
day                      
lun      61.0   12.5  8.0
mar         —   48.9  9.5
mié         —   20.0    —
```

- El máximo por estación sale igual en las dos formas: en largo con `groupby`, en ancho con `max()` por columna.
- Comparar dos días es una resta de filas en formato ancho. En largo necesitarías un `merge` (ejercicio 02, paso 5).
- Para mostrar, la ancha: `to_string` con `na_rep` y `float_format`, como en tu Observatorio.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ModuleNotFoundError: No module named 'pandas'` | Ejecuta con `uv run python main.py` dentro de `starter/` |
| `ValueError: Index contains duplicate entries, cannot reshape` fuera del `try` | Hay dos valores para la misma celda: usa `pivot_table` con un `aggfunc` |
| `KeyError: "The following id_vars or value_vars are not present in the DataFrame: ['day']"` | Falta `reset_index()`: en la tabla ancha, `day` es el índice, no una columna |
| `¿vuelta completa? False` | Comprueba que ordenas por las mismas columnas y que usas `reset_index(drop=True)` en las dos |
| `crosstab` no tiene la columna `alto` | Cambiaste un valor: `crosstab` solo muestra las categorías que aparecen |
| `NameError: name 'wide' is not defined` | Descomenta los pasos en orden |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 02 · Combinar con concat, merge y join](../ejercicio-02-combinar-con-concat-merge-y-join/README.md) | **Ejercicio 03 · Dar forma con pivot y melt** | [Ejercicio 04 · Series de tiempo](../ejercicio-04-series-de-tiempo/README.md) |
