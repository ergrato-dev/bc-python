# Ejercicio 02 — Combinar con concat, merge y join

⏱️ 1 h 30 min · Teoría previa: [02](../../1-teoria/02-combinar-tablas-concat-merge-y-join.md)

## Objetivo

Juntar tablas que vienen por separado:

- apilar las medidas de dos días con `concat`, y qué pasa con el índice;
- apilar tablas con columnas distintas, y ponerlas lado a lado;
- cruzar medidas con la tabla de estaciones usando los cuatro `how` de `merge`;
- ver cómo una clave repetida multiplica filas, y pararlo con `validate`;
- comparar dos días con `suffixes`, y cruzar con claves de nombre distinto;
- cruzar por el índice con `join` y con `map`.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-25-pandas_groupby_merge_y_series_de_tiempo/2-practicas/ejercicio-02-combinar-con-concat-merge-y-join/starter
uv run python main.py
```

```
Ejercicio 02 · Combinar tablas
```

Tres tablas: `monday` (Norte, Sur y Oeste), `tuesday` (Norte y Sur) y `stations`, con la región y la altitud de Norte, Sur y Centro. Oeste tiene medidas pero no está en `stations`; Centro está en `stations` pero no midió.

## Pasos

### 1. Apilar con concat

Descomenta el **PASO 1** y ejecuta:

```
  station  value
0   Norte   12.5
1     Sur    8.0
2   Oeste    3.1
0   Norte   48.9
1     Sur    9.5
índice repetido: [0, 1, 2, 0, 1]
ignore_index: [0, 1, 2, 3, 4]
    station  value
row               
0     Norte   48.9
1       Sur    9.5
```

- `concat` pone una tabla debajo de otra y **conserva** los índices: hay dos filas `0`. Un `loc[0]` daría dos filas.
- `ignore_index=True` numera de nuevo desde 0.
- Con un diccionario, cada tabla aporta su clave como primer nivel del índice: `by_day.loc["martes"]` recupera la del martes. Así no pierdes de qué día era cada fila.

### 2. Columnas que no coinciden

Descomenta el **PASO 2** y ejecuta:

```
  station  value unit
0   Norte   12.5  NaN
1     Sur    8.0  NaN
2   Oeste    3.1  NaN
3   Norte   48.9   mm
4     Sur    9.5   mm
   lunes  martes
0   12.5    48.9
1    8.0     9.5
2    3.1     NaN
```

- Apilar tablas con columnas distintas no da error: la que no tiene `unit` la rellena con NaN.
- `axis=1` pone las tablas **lado a lado**, alineadas por el índice (la teoría 01 de la semana 24). La fila 2 del martes no existe: NaN. Ojo: las alinea por el índice (0, 1, 2), **no por estación**: si el martes viniera en otro orden, mezclarías estaciones. Para eso está `merge`.

### 3. merge y sus cuatro how

Descomenta el **PASO 3** y ejecuta:

```
inner: ['Norte', 'Sur'] · región: ['montaña', 'costa']
 left: ['Norte', 'Sur', 'Oeste'] · región: ['montaña', 'costa', nan]
right: ['Norte', 'Sur', 'Centro'] · región: ['montaña', 'costa', 'valle']
outer: ['Centro', 'Norte', 'Oeste', 'Sur'] · región: ['valle', 'montaña', nan, 'costa']
  station      _merge
0  Centro  right_only
1   Norte        both
2   Oeste   left_only
3     Sur        both
```

- `inner` (el valor por defecto) solo deja las estaciones que están en las dos tablas: Oeste desaparece **sin aviso**.
- `left` deja todas las de la izquierda; Oeste sale con región NaN. Es el que más usarás: "a mis medidas, añádeles los datos de su estación".
- `right`, todas las de la derecha; `outer`, todas, ordenadas por la clave.
- `indicator=True` añade `_merge`, que dice de dónde salió cada fila. Úsalo para encontrar las que no cruzaron.

### 4. Una clave repetida

Descomenta el **PASO 4** y ejecuta:

```
left con medidas a la izquierda: 5 filas
con Norte dos veces en estaciones: 7 filas
MergeError: Merge keys are not unique in right dataset; not a many-to-one merge
```

- Cinco medidas cruzadas con `left` dan cinco filas: cada estación está una vez en `stations`.
- Si Norte está dos veces en `stations`, cada medida de Norte se cruza con las dos: 2 × 2 = 4 filas de Norte, y 7 en total. Las medias de después estarían mal, y nada falla.
- `validate="many_to_one"` dice lo que esperas (muchas medidas por estación, una fila por estación) y lanza `MergeError` si no se cumple. Ponlo siempre que sepas qué relación hay.

### 5. Columnas con el mismo nombre

Descomenta el **PASO 5** y ejecuta:

```
  station  value_lunes  value_martes
0   Norte         12.5          48.9
1     Sur          8.0           9.5
cambio: [36.4, 1.5]
['station', 'value', 'name', 'region', 'altitude']
```

- Las dos tablas tienen `value`: `suffixes` decide cómo se llama cada una. Sin él saldrían `value_x` y `value_y`.
- Con el cruce, restar el lunes al martes es una resta de columnas.
- Si la clave se llama distinto en cada tabla, `left_on` y `right_on`. Se quedan las dos columnas: `station` y `name`.

### 6. join por el índice

Descomenta el **PASO 6** y ejecuta:

```
          region  altitude   mean
station                          
Norte    montaña      2600  30.70
Sur        costa         5   8.75
Centro     valle      1500    NaN
map: ['montaña', 'costa', nan]
```

- `join` cruza por el índice: `stations` con la estación como índice y las medias de `groupby`, que ya la tienen. Es un `merge` con `left_index=True, right_index=True`, y por defecto `how="left"`.
- `map` con una `Series` busca cada valor en su índice: la forma corta de añadir **una** columna.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ModuleNotFoundError: No module named 'pandas'` | Ejecuta con `uv run python main.py` dentro de `starter/` |
| `KeyError: 'station'` en un `merge` | Una de las tablas no tiene esa columna: la clave tiene que estar en las dos, o usa `left_on` y `right_on` |
| `MergeError` en un paso que no es el 4 | Hay claves repetidas donde no las esperabas: búscalas con `df["station"].duplicated()` |
| Salen `value_x` y `value_y` | Falta `suffixes` |
| El paso 6 da `ValueError: columns overlap but no suffix specified` | Las dos tablas tienen una columna con el mismo nombre: renombra la `Series` con `.rename("mean")` |
| `NameError: name 'both' is not defined` | Descomenta los pasos en orden |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 01 · groupby: dividir, calcular y juntar](../ejercicio-01-groupby-dividir-calcular-y-juntar/README.md) | **Ejercicio 02 · Combinar con concat, merge y join** | [Ejercicio 03 · Dar forma con pivot y melt](../ejercicio-03-dar-forma-con-pivot-y-melt/README.md) |
