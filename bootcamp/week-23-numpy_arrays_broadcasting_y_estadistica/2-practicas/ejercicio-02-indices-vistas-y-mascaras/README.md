# Ejercicio 02 — Índices, vistas y máscaras

⏱️ 1 h 30 min · Teoría previa: [02](../../1-teoria/02-indices-vistas-y-mascaras.md)

## Objetivo

Elegir partes de una tabla de medidas sin un solo bucle:

- filas, columnas y bloques con índices y cortes;
- comprobar que un corte es una **vista** y cambiarlo cambia el original;
- elegir con listas de posiciones, que dan una **copia**;
- filtrar con máscaras y combinarlas;
- cambiar solo lo que cumple una condición, y decidir con `np.where`;
- ordenar sin perder qué estación tenía cada valor.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-23-numpy_arrays_broadcasting_y_estadistica/2-practicas/ejercicio-02-indices-vistas-y-mascaras/starter
uv run python main.py
```

```
Ejercicio 02 · Índices, vistas y máscaras
```

`WEEK` son las medidas de tres días (filas) en cuatro estaciones (columnas, en el orden de `STATIONS`: Norte, Sur, Este y Oeste):

```
[[12.5  8.  55.1 61. ]
 [48.9  9.5 40.2 33.3]
 [20.  71.4  5.5 18.8]]
```

## Pasos

### 1. Índices y cortes

Descomenta el **PASO 1** y ejecuta:

```
primer día:    [12.5  8.  55.1 61. ]
último valor:  61.0 · del 1 al 2: [ 8.  55.1] · salteados: [12.5 55.1]
día 1, Este:   40.2
columna Sur:   [ 8.   9.5 71.4]
bloque:
 [[48.9  9.5]
 [20.  71.4]]
```

Con dos ejes, un índice por eje separados por comas: `WEEK[1, 2]` es "fila 1, columna 2". `:` sola significa "todo ese eje": `WEEK[:, 1]` es la columna entera. `WEEK[1:, :2]` combina dos cortes: desde la fila 1 y hasta la columna 2 (sin incluirla).

### 2. Un corte es una vista

Descomenta el **PASO 2** y ejecuta:

```
tras poner a 0 la vista:
 [[ 0.   8.  55.1 61. ]
 [ 0.   9.5 40.2 33.3]
 [ 0.  71.4  5.5 18.8]]
WEEK sigue igual: [12.5 48.9 20. ]
```

`north` es la columna Norte de `week`, y al ponerla a 0 cambió `week`. Un corte no copia: mira el mismo bloque de memoria. Por eso el paso empieza con `week = WEEK.copy()`: sin ella, habrías estropeado `WEEK` para los pasos siguientes.

`safe` es una copia (`.copy()`): cambiarla no toca `WEEK`.

Prueba a cambiar `north[:] = 0` por `north = 0`. ¿Cambia `week`? No: `north = 0` solo hace que el nombre `north` apunte al número 0. Para escribir **dentro** de un array, siempre con corchetes.

### 3. Índices con una lista: una copia

Descomenta el **PASO 3** y ejecuta:

```
elegidos: [61.  12.5 12.5]
WEEK[0] sigue igual: [12.5  8.  55.1 61. ]
filas 2 y 0:
 [[20.  71.4  5.5 18.8]
 [12.5  8.  55.1 61. ]]
una por día: [61.  48.9 71.4]
```

Con una lista de posiciones, los elementos salen en el orden pedido y se pueden repetir: el 12.5 aparece dos veces. Eso no se puede expresar como "mismo bloque con otros saltos", así que NumPy **copia**: poner `chosen` a 0 no toca `WEEK`.

Con dos listas, una por eje, se eligen **parejas**: `(0, 3)`, `(1, 0)` y `(2, 1)`. No es un bloque de 3 × 3, sino 3 elementos sueltos.

### 4. Máscaras

Descomenta el **PASO 4** y ejecuta:

```
[[False False  True  True]
 [False False False False]
 [False  True False False]]
altos: [55.1 61.  71.4] · cuántos: 3
medios: [12.5 48.9 40.2 33.3 20.  18.8]
ni altos ni medios: [8.  9.5 5.5]
ValueError: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()
```

`WEEK > 50` da una tabla de `bool` de la misma forma. Indexar con ella da los valores donde es `True`, en orden de lectura, en una sola fila: la forma de tabla se pierde.

Las condiciones se combinan con `&` (y), `|` (o) y `~` (no), siempre con paréntesis. Con `and`, Python intenta convertir cada máscara en **un** `True` o `False`, y NumPy se niega: ese es el `ValueError`.

Con los umbrales de tu dominio (semana 2), cambia 10 y 50 por tus valores `LOW` y `HIGH`. ¿Cuántas medidas quedan en cada nivel?

### 5. Cambiar lo que cumple una condición

Descomenta el **PASO 5** y ejecuta:

```
con tope 60:
 [[12.5  8.  55.1 60. ]
 [48.9  9.5 40.2 33.3]
 [20.  60.   5.5 18.8]]
['no alto' 'no alto' 'alto' 'alto']
posiciones de los altos del día 0: [2 3]
días con algún alto: [ True False  True]
```

`capped[capped > 60] = 60` escribe 60 solo donde la máscara es `True`, en el mismo array. Leer con una máscara copia; **escribir** con ella modifica.

`np.where(condición, a, b)` elige elemento a elemento: `a` donde se cumple, `b` donde no. `np.flatnonzero` da las posiciones de los `True`; tu Observatorio la usa para saber qué medidas son atípicas. `.any(axis=1)` responde por cada fila "¿alguno?".

### 6. Ordenar y elegir los mayores

Descomenta el **PASO 6** y ejecuta:

```
ordenados: [ 9.5 33.3 40.2 48.9] · posiciones: [1 3 2 0]
de mayor a menor: ['Norte' 'Este' 'Oeste' 'Sur'] [48.9 40.2 33.3  9.5]
el mayor: 71.4 el día 2 en Sur
la estación más alta de cada día: ['Oeste' 'Norte' 'Sur']
```

`np.sort` da los valores ordenados y pierde de dónde venían. `np.argsort` da las **posiciones** en orden: el menor está en la 1, luego la 3... Con esas posiciones ordenas `STATIONS` y `day` a la vez, y cada valor sigue con su estación. `[::-1]` le da la vuelta: de mayor a menor.

`WEEK.argmax()` sin eje da la posición en el bloque aplanado (la 9); `np.unravel_index` la convierte en fila y columna. Con `axis=1`, una posición por fila: la estación más alta de cada día.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| En el paso 3, `WEEK` aparece con ceros | En el paso 2 quitaste `.copy()` de `week = WEEK.copy()`: has cambiado `WEEK` a través de una vista |
| `TypeError: ufunc 'bitwise_and' not supported for the input types` | Faltan los paréntesis: `(WEEK >= 10) & (WEEK <= 50)` |
| `IndexError: too many indices for array` | Usas dos índices con un array de una dimensión, como `WEEK[0][1, 2]` |
| `IndexError: index 4 is out of bounds for axis 1 with size 4` | Las columnas van de 0 a 3 |
| `de mayor a menor` sale de menor a mayor | Falta `[::-1]` detrás de `np.argsort(day)` |
| Las estaciones no se corresponden con los valores | Ordenaste `STATIONS` con `np.sort` en lugar de con las posiciones de `argsort` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 01 · Arrays y dtypes](../ejercicio-01-arrays-y-dtypes/README.md) | **Ejercicio 02 · Índices, vistas y máscaras** | [Ejercicio 03 · Broadcasting y ejes](../ejercicio-03-broadcasting-y-ejes/README.md) |
