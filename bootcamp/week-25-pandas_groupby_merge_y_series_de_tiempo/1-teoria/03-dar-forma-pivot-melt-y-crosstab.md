# 03 · Dar forma: pivot, melt y crosstab

⏱️ 45 min

## 🎯 Objetivos

- Distinguir el formato largo (una fila por medida) del ancho (una columna por categoría), y saber para qué sirve cada uno.
- Pasar de largo a ancho con `pivot`, y entender por qué falla con datos repetidos.
- Resumir y dar forma a la vez con `pivot_table`.
- Volver de ancho a largo con `melt`.
- Mover niveles entre el índice y las columnas con `stack` y `unstack`.
- Contar combinaciones con `crosstab`, y aplanar columnas de dos niveles.

---

## 1. Largo y ancho

Las mismas seis medidas, de dos formas:

```
formato largo                     formato ancho
   day station  value             station  Este  Norte  Sur
0  lun   Norte   12.5             day
1  lun     Sur    8.0             lun      61.0   12.5  8.0
2  lun    Este   61.0             mar       NaN   48.9  9.5
3  mar   Norte   48.9             mié       NaN   20.0  NaN
4  mar     Sur    9.5
5  mié   Norte   20.0
```

- En formato **largo** cada fila es una medida, y cada columna, una variable: el día, la estación, el valor. Es la forma de `medidas.csv`, de una tabla de PostgreSQL y de lo que espera `groupby`. Añadir una estación nueva es añadir filas.
- En formato **ancho** cada estación es una columna, y cada celda, una medida. Es la forma de una hoja de cálculo, fácil de leer y de comparar: el martes contra el lunes es una resta de filas. Las combinaciones que no existen son NaN.

Regla práctica: **largo para guardar y calcular, ancho para mostrar y comparar**. pandas pasa de una a otra en una línea.

---

## 2. pivot: de largo a ancho

```python
wide = long.pivot(index="day", columns="station", values="value")
```

Tres columnas de la tabla larga: la que forma el índice (`day`), la que forma las columnas (`station`) y la que rellena las celdas (`value`). Índice y columnas salen **ordenados**; sus nombres (`day`, `station`) se guardan en `wide.index.name` y `wide.columns.name`.

En formato ancho, las cuentas por columna son cuentas por estación:

```python
wide.mean()                   # Este 61.0 · Norte 27.13 · Sur 8.75
wide.mean(axis="columns")     # lun 27.17 · mar 29.2 · mié 20.0
wide.loc["mar"] - wide.loc["lun"]   # cuánto cambió cada estación
```

`pivot` tiene una condición: cada pareja (índice, columna) puede aparecer **una sola vez**. Si Norte midió dos veces el lunes, no sabe cuál poner:

```
ValueError: Index contains duplicate entries, cannot reshape
```

En tu proyecto, `evolution` llama a `pivot` sobre una tabla cuyo índice es el instante de cada medida, y todos son distintos: nunca falla.

---

## 3. pivot_table: resumir y dar forma

`pivot_table` junta los repetidos con una función, `aggfunc`, la media si no dices otra:

```python
repeated.pivot_table(index="day", columns="station", values="value", aggfunc="mean")
```

Con las dos medidas de Norte del lunes (12,5 y 14,5), la celda vale 13,5. Es exactamente un `groupby` de dos claves seguido de `unstack`:

```python
long.groupby(["day", "station"])["value"].mean().unstack()   # igual que el pivot
```

Opciones útiles:

- `aggfunc="count"` cuenta las medidas de cada celda; con `fill_value=0`, las vacías salen 0 en lugar de NaN.
- `margins=True` añade una fila y una columna de totales (con la misma función: la media de todas, no la media de las medias).
- Con una lista, `aggfunc=["mean", "count"]`, salen columnas de **dos niveles**:

```
         mean             count          
day       lun   mar   mié   lun  mar  mié
station                                  
Este     61.0   NaN   NaN   1.0  NaN  NaN
Norte    12.5  48.9  20.0   1.0  1.0  1.0
Sur       8.0   9.5   NaN   1.0  1.0  NaN
```

Cada columna es una tupla, `("mean", "lun")`. Para escribirla en un CSV o leerla con comodidad, aplánala:

```python
table.columns = [f"{function}_{day}" for function, day in table.columns]
# ['mean_lun', 'mean_mar', 'mean_mié', 'count_lun', 'count_mar', 'count_mié']
```

---

## 4. melt: de ancho a largo

`melt` hace lo contrario: cada celda vuelve a ser una fila.

```python
wide.reset_index().melt(id_vars="day", var_name="station", value_name="value")
```

```
   day station  value
0  lun    Este   61.0
1  mar    Este    NaN
2  mié    Este    NaN
3  lun   Norte   12.5
...
```

- `melt` trabaja con columnas: primero `reset_index()` para que `day` sea una columna.
- `id_vars` son las columnas que se quedan como están; las demás se "derriten" en dos: el nombre de la columna (`var_name`) y su valor (`value_name`). Con `value_vars` eliges cuáles.
- Salen 3 días × 3 estaciones = 9 filas: las celdas vacías también, con NaN. `dropna()` las quita.

Tras `dropna`, ordenar y renumerar, la tabla es **exactamente** la del principio (ejercicio 03, paso 3). `pivot` y `melt` no pierden información, salvo que haya repetidos.

¿Cuándo lo necesitas? Cuando los datos llegan anchos (una hoja de cálculo con una columna por mes) y quieres usar `groupby`, `merge` o guardarlos en una tabla de PostgreSQL.

---

## 5. stack y unstack

`stack` y `unstack` mueven un **nivel** entre las columnas y el índice:

- `unstack(nivel)` pasa un nivel del índice a las columnas. Lo usaste en la teoría 01: `groupby(["station", "day"])` y después `unstack("day")`.
- `stack()` pasa las columnas al índice: una tabla ancha se convierte en una `Series` con índice de dos niveles.

```python
wide.stack()
```

```
day  station
lun  Este       61.0
     Norte      12.5
     Sur         8.0
mar  Este        NaN
...
```

En pandas 3, `stack` **conserva** las celdas NaN: salen 9 filas, no 6. Muchos tutoriales, escritos para pandas 1 o 2, dicen que las quita.

`wide.stack().unstack("day")` da la tabla traspuesta, con las estaciones en filas: lo mismo que `wide.T`.

---

## 6. crosstab: contar combinaciones

`crosstab` cuenta cuántas filas hay de cada combinación de dos columnas. Con los niveles de `pd.cut` (semana 24):

```python
pd.crosstab(long["station"], long["level"])
```

```
level    bajo  medio  alto
station                   
Este        0      0     1
Norte       0      3     0
Sur         2      0     0
```

- Es un `pivot_table` con `aggfunc="count"` y `fill_value=0`, más corto de escribir.
- Las columnas siguen el orden de las categorías (bajo, medio, alto), no el alfabético. Una categoría que no aparece en ninguna fila no sale.
- `margins=True` añade totales; `normalize="index"` reparte cada fila en proporciones que suman 1.

---

## 7. Qué forma para qué

| Quieres... | Forma | Con |
|---|---|---|
| Guardar en CSV o en PostgreSQL | Larga | `melt` si llega ancha |
| Agrupar, filtrar, cruzar | Larga | `groupby`, máscaras, `merge` |
| Comparar categorías en el mismo instante | Ancha | `pivot`, y restas de filas |
| Agrupar por periodos de tiempo todas las estaciones a la vez | Ancha, índice de tiempo | `pivot` y `resample` (teoría 04) |
| Mostrar una tabla a una persona | Ancha | `pivot`, `to_string` |
| Contar combinaciones | Ancha | `crosstab` |

`evolucion`, el comando nuevo de tu Observatorio, hace exactamente la cuarta fila: tabla larga, `pivot` para tener una columna por etiqueta y `resample` para agrupar por periodos.

---

## 8. Errores frecuentes

| Error | Por qué está mal | Qué hacer |
|---|---|---|
| `pivot` con datos repetidos | No sabe qué valor poner: `ValueError` | `pivot_table` con un `aggfunc` |
| `melt` sobre una tabla con el índice importante | `melt` ignora el índice | `reset_index()` antes |
| Esperar que `stack` quite los NaN | En pandas 3 los conserva | `dropna()` después |
| Columnas de dos niveles en un CSV | Se escriben en dos filas de cabecera | Aplánalas antes de guardar |
| Calcular sobre la tabla ancha con `groupby` | Ya está agrupada: cada columna es un grupo | Cuentas por columna (`mean()`) o vuelve a larga |
| `margins=True` y esperar la media de las medias | El total usa todas las filas | Calcúlala aparte si es lo que quieres |

---

## ✅ Qué debes saber al terminar

- [ ] Reconocer una tabla larga y una ancha, y para qué sirve cada una.
- [ ] Usar `pivot`, y saber cuándo falla y por qué.
- [ ] Usar `pivot_table` con `aggfunc`, `fill_value` y `margins`, y aplanar columnas de dos niveles.
- [ ] Volver a formato largo con `melt`.
- [ ] Mover niveles con `stack` y `unstack`.
- [ ] Contar combinaciones con `crosstab`.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [02 · Combinar tablas: concat, merge y join](02-combinar-tablas-concat-merge-y-join.md) | **03 · Dar forma: pivot, melt y crosstab** | [04 · Series de tiempo](04-series-de-tiempo.md) |
