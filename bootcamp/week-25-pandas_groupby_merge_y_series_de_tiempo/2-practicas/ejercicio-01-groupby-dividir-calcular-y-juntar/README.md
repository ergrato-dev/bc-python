# Ejercicio 01 — groupby: dividir, calcular y juntar

⏱️ 1 h 30 min · Teoría previa: [01](../../1-teoria/01-groupby-dividir-calcular-y-juntar.md)

## Objetivo

Resumir una tabla por grupos sin escribir un bucle:

- una media por estación, con y sin orden alfabético;
- varias cuentas a la vez, con nombres elegidos por ti;
- ver qué pasa con la fila que no tiene estación;
- agrupar por dos columnas y leer el índice de dos niveles;
- devolver un valor por fila con `transform` y quitar grupos con `filter`;
- medir cuánto gana `groupby` frente a un diccionario de listas.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-25-pandas_groupby_merge_y_series_de_tiempo/2-practicas/ejercicio-01-groupby-dividir-calcular-y-juntar/starter
uv run python main.py
```

```
Ejercicio 01 · groupby
```

`readings` tiene ocho medidas de tres estaciones en dos días. La del Sur del día 2 no tiene valor (`None`), y la última no sabe de qué estación es.

## Pasos

### 1. Una media por estación

Descomenta el **PASO 1** y ejecuta:

```
station
Este     30.000000
Norte    27.133333
Sur       8.750000
Name: value, dtype: float64
en orden de aparición: {'Sur': 8.75, 'Norte': 27.133333333333336, 'Este': 30.0}
grupos: 3 · filas del Norte: [1, 4, 6]
```

- `groupby("station")` no calcula nada todavía: prepara los grupos. `["value"]` elige la columna y `mean()` calcula y junta.
- El resultado es una `Series` con la estación como índice, **ordenada** por defecto. Con `sort=False`, en el orden en que aparece cada estación.
- La media del Sur es 8,75: la medida sin valor no cuenta, como en todos los métodos de pandas.
- `get_group` da las filas de un grupo. Las del Norte son la 1, la 4 y la 6.

### 2. Varias cuentas a la vez

Descomenta el **PASO 2** y ejecuta:

```
         count  size       mean   max
station                              
Este         1     1  30.000000  30.0
Norte        3     3  27.133333  48.9
Sur          2     3   8.750000   9.5
         medidas      media  primer_dia
station                                
Este           1  30.000000           1
Norte          3  27.133333           1
Sur            2   8.750000           1
columnas: ['medidas', 'media', 'primer_dia']
```

- Con una lista, `agg` da una columna por función.
- `count` cuenta los **valores** y `size` las **filas**: el Sur tiene tres filas pero dos valores. La resta son los que faltan.
- La forma con nombre, `medidas=("value", "count")`, elige el nombre de cada columna y de qué columna sale: `primer_dia` sale de `day`. Es la que usarás en el proyecto.

### 3. La fila sin estación

Descomenta el **PASO 3** y ejecuta:

```
filas en grupos: 7 de 8
{'Este': 1, 'Norte': 3, 'Sur': 2, nan: 1}
```

`groupby` **quita** las filas cuya clave falta: la última medida no estaba en ningún grupo y nadie te avisó. Con `dropna=False` aparece un grupo `nan`. Cuando una clave puede faltar, cuenta las filas antes y después.

### 4. Dos claves

Descomenta el **PASO 4** y ejecuta:

```
station  day
Este     1      30.00
Norte    1      12.50
         2      34.45
Sur      1       8.75
         2        NaN
Name: value, dtype: float64
índice: ['station', 'day'] · Norte día 2: 34.45
day          1      2
station              
Este     30.00    NaN
Norte    12.50  34.45
Sur       8.75    NaN
  station  day  value
0    Este    1  30.00
1   Norte    1  12.50
2   Norte    2  34.45
```

- Con dos claves, el índice tiene dos niveles (`MultiIndex`) y se elige con una tupla: `loc[("Norte", 2)]`.
- El Sur del día 2 sale con NaN: el grupo existe, pero su único valor faltaba.
- `unstack("day")` pasa el nivel `day` a columnas: una tabla que se lee de un vistazo. Este no midió el día 2, y sale NaN.
- `as_index=False` deja las claves como columnas normales, útil para escribir un CSV.

### 5. transform y filter

Descomenta el **PASO 5** y ejecuta:

```
media de su estación: [8.75, 27.133333333333336, 8.75, 30.0, 27.133333333333336, 8.75, 27.133333333333336, nan]
diferencia: [-0.75, -14.63, 0.75, 0.0, 21.77, nan, -7.13, nan]
estaciones con 3 o más filas: ['Sur', 'Norte'] · 6 filas
```

- `transform` calcula por grupo pero devuelve **una fila por fila**, con el índice de `readings`: puedes restarla a la columna directamente. La fila sin estación recibe NaN.
- `filter` se queda con los grupos que cumplen la condición, con todas sus filas. Este, con una sola, desaparece.

### 6. ¿Cuánto se gana?

Descomenta el **PASO 6** y ejecuta. Los tiempos son los de la máquina del bootcamp; los tuyos serán otros:

```
¿las mismas medias? True
bucle      5.3 ms
groupby    4.3 ms
```

Con 100 000 filas y cinco estaciones, `groupby` gana poco a un diccionario de listas que recorre `pairs`, una lista de tuplas de Python. La diferencia de verdad está en todo lo demás: varias funciones a la vez, los NaN, el índice. Cambia `"mean"` por `.agg(["mean", "std", "max"])` y piensa cuántas líneas te costaría con el bucle.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ModuleNotFoundError: No module named 'pandas'` | Ejecuta con `uv run python main.py` dentro de `starter/` |
| `TypeError: 'DataFrameGroupBy' object is not callable` | Escribiste `groupby("station")("value")`: la columna se elige con corchetes, `["value"]` |
| `TypeError: Must provide 'func' or tuples of '(column, aggfunc).` | En la forma con nombre, cada valor es una tupla: `medidas=("value", "count")` |
| `KeyError: ('Este', 2)` | Pides un grupo que no existe: Este no midió el día 2. Mira `by_day.index.tolist()` |
| Los tiempos del paso 6 salen al revés | Tu máquina es otra: compara el orden de magnitud, no la cifra |
| `NameError: name 'groups' is not defined` | Descomenta los pasos en orden: el 2 usa lo del 1 |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [05 · pandas II en un proyecto](../../1-teoria/05-pandas-ii-en-un-proyecto.md) | **Ejercicio 01 · groupby: dividir, calcular y juntar** | [Ejercicio 02 · Combinar con concat, merge y join](../ejercicio-02-combinar-con-concat-merge-y-join/README.md) |
