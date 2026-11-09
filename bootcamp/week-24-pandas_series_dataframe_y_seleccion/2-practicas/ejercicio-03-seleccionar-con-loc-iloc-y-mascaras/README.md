# Ejercicio 03 — Seleccionar con loc, iloc y máscaras

⏱️ 1 h 30 min · Teoría previa: [03](../../1-teoria/03-seleccionar-loc-iloc-y-mascaras.md) y [04](../../1-teoria/04-ordenar-contar-y-copy-on-write.md)

## Objetivo

Elegir exactamente las filas y columnas que quieres:

- por etiqueta con `.loc` y por posición con `.iloc`;
- con máscaras, `isin`, `between` y los NaN en medio;
- con `query`;
- con otro índice;
- ordenando, con empates;
- y cambiar una selección sin caer en la asignación encadenada.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-24-pandas_series_dataframe_y_seleccion/2-practicas/ejercicio-03-seleccionar-con-loc-iloc-y-mascaras/starter
uv run python main.py
```

```
Ejercicio 03 · Seleccionar con loc, iloc y máscaras
```

`main.py` define `READINGS`: 8 medidas de tres estaciones en tres días, con un dato que falta (la 5). Su índice, `posicion`, va de **1** a 8, como las líneas de un archivo: la etiqueta 1 está en la posición 0.

## Pasos

### 1. loc por etiqueta, iloc por posición

Descomenta el **PASO 1** y ejecuta:

```
         estacion  dia  valor
posicion
1           Norte    1   12.5
2             Sur    1    8.0
3            Este    1   48.9
4           Norte    2   15.0
5             Sur    2    NaN
6            Este    2   52.3
7           Norte    3    9.5
8             Sur    3   30.1
loc[1, 'valor']: 12.5 · iloc[1, 2]: 8.0
         estacion  valor
posicion
2             Sur    8.0
3            Este   48.9
4           Norte   15.0
         estacion  valor
posicion
2             Sur    8.0
3            Este   48.9
KeyError: 0
```

- `loc[1, "valor"]` es la fila de **etiqueta** 1; `iloc[1, 2]` es la fila en la **posición** 1 (la segunda) y la tercera columna.
- `loc[2:4]` incluye la 4; `iloc[1:3]` excluye la posición 3. Las dos selecciones conservan sus etiquetas.
- `loc[0]` no existe: `KeyError`.

### 2. Máscaras

Descomenta el **PASO 2** y ejecuta:

```
máscara: [False, False, True, False, False, True, False, True]
         estacion  dia  valor
posicion
3            Este    1   48.9
6            Este    2   52.3
8             Sur    3   30.1
Norte o Sur y más de 10: [1, 4, 8]
entre 10 y 30: [1, 4]
no mayor que 20: [1, 2, 4, 5, 7] · menor o igual que 20: [1, 2, 4, 7]
ValueError: The truth value of a Series is ambiguous. Use a.empty, a.item(), a.any() or a.all().
```

- `isin` y `&` combinan dos condiciones, cada una entre paréntesis.
- `between(10, 30)` incluye los dos bordes. La 8 (30.1) se queda fuera por poco.
- La 5 no tiene valor: `~high` ("no mayor que 20") la incluye; `<= 20` no. No son lo mismo.
- `and` entre dos máscaras da `ValueError`: usa `&`.

### 3. query y loc con máscara

Descomenta el **PASO 3** y ejecuta:

```
         estacion  dia  valor
posicion
6            Este    2   52.3
con @limit: [3, 6, 8]
posicion
7     9.5
8    30.1
Name: valor, dtype: float64
```

En `query` se escribe `and` y los nombres de las columnas sin comillas; `@limit` usa la variable de Python. `loc[máscara, "valor"]` elige filas con una máscara y una columna por su nombre a la vez: el resultado es una `Series`.

### 4. Otro índice

Descomenta el **PASO 4** y ejecuta:

```
          dia  valor
estacion
Este        1   48.9
Este        2   52.3
índice único: False
          dia  valor
estacion
Este        1   48.9
Este        2   52.3
Norte       1   12.5
Norte       2   15.0
['estacion', 'dia', 'valor']
```

Con `set_index("estacion")`, las estaciones son las etiquetas. Como se repiten, `loc["Este"]` da **dos** filas, una tabla. `sort_index` ordena por la etiqueta y `reset_index` devuelve el índice a una columna.

Prueba `by_station.loc["Oeste"]`: `KeyError: 'Oeste'`.

### 5. Ordenar

Descomenta el **PASO 5** y ejecuta:

```
[6, 3, 8, 4, 1, 7, 2, 5]
[5, 2, 7, 1, 4, 8, 3, 6]
[6, 3, 4, 1, 7, 8, 2, 5]
         estacion  dia  valor
posicion
6            Este    2   52.3
3            Este    1   48.9
quicksort: [0, 2, 3, 5, 6, 11]
stable:    [0, 2, 3, 5, 6, 8]
```

1. De mayor a menor: la 5 (NaN) al final.
2. De menor a mayor con `na_position="first"`: la 5 delante.
3. Por estación A-Z y, dentro de cada estación, de mayor a menor valor.
4. `nlargest(2, "valor")`: las dos más altas.
5. 60 filas con valores 1, 2, 1, 1, 2, 1... Ordenadas con el algoritmo por defecto, la fila 11 aparece antes que la 8, aunque las dos valen 1.0: `quicksort` no conserva el orden de los empates. Con `kind="stable"`, sí.

### 6. Cambiar una selección

Descomenta el **PASO 6** y ejecuta:

```
north: [0.0, 0.0, 0.0] · readings: [12.5, 15.0, 9.5]
encadenado: [12.5, 15.0, 9.5]
con loc: [0.0, 0.0, 0.0]
```

Y, antes de todo lo demás o mezclado con ello (sale por stderr):

```
main.py:93: ChainedAssignmentError: A value is being set on a copy of a DataFrame or Series through chained assignment.
Such chained assignment never works to update the original DataFrame or Series, because the intermediate object on which we are setting values always behaves as a copy (due to Copy-on-Write).
...
```

1. `north` es una selección: cambiarla no toca `readings` (*copy-on-write*).
2. `readings[máscara]["valor"] = 0.0` cambia una tabla intermedia que nadie guarda. pandas avisa y `readings` sigue igual.
3. `readings.loc[máscara, "valor"] = 0.0`, en un solo paso, sí cambia `readings`.

`READINGS.copy()` al principio del paso evita que el cambio afecte a la tabla de los pasos anteriores.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `KeyError: 0` fuera del `try` del paso 1 | Has usado `.loc[0]`: la primera fila tiene la etiqueta 1, o usa `.iloc[0]` |
| `ValueError: The truth value of a Series is ambiguous` con `&`, o una selección vacía | Faltan paréntesis alrededor de cada condición: `&` se calcula antes que `>` y `==` |
| `no mayor que 20` sin la 5 | Has escrito `<= 20` en lugar de `~high` |
| `pandas.errors.UndefinedVariableError: local variable 'limit' is not defined` | Falta la línea `limit = 30` antes de `query` |
| `quicksort` y `stable` dan lo mismo | Has cambiado el tamaño de `ties`: con pocas filas el algoritmo no se nota |
| No ves el `ChainedAssignmentError` | Sale por stderr, a veces antes que el resto: sube en la terminal |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 02 · DataFrames: leer y mirar](../ejercicio-02-dataframes-leer-y-mirar/README.md) | **Ejercicio 03 · Seleccionar con loc, iloc y máscaras** | [Ejercicio 04 · De Python a pandas](../ejercicio-04-de-python-a-pandas/README.md) |
