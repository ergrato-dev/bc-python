# Ejercicio 04 — De Python a pandas

⏱️ 1 h 30 min · Teoría previa: [04](../../1-teoria/04-ordenar-contar-y-copy-on-write.md) y [05](../../1-teoria/05-pandas-en-un-proyecto.md)

## Objetivo

El ensayo del proyecto: tienes medidas como objetos de Python y funciones que trabajan con ellas, y pasas a pandas sin cambiar los resultados.

- convertir una lista de objetos en tabla, también vacía;
- clasificar sin bucle con `pd.cut`, con los bordes bien puestos;
- contar como `Counter`;
- devolver tipos de Python;
- medir dónde gana pandas y dónde no;
- ver cuánta memoria ocupa el texto.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-24-pandas_series_dataframe_y_seleccion/2-practicas/ejercicio-04-de-python-a-pandas/starter
uv run python main.py
```

```
Ejercicio 04 · De Python a pandas
```

`main.py` trae una *dataclass* `Measurement`, la función `classify` de la semana 2 (umbrales 10 y 50) y `SERIES`, cinco medidas. Una vale justo 10 y otra justo 50: los bordes.

## Pasos

### 1. De objetos a una tabla

Descomenta el **PASO 1** y ejecuta:

```
           label  value
position
1          Norte   12.5
2            Sur    8.0
3         Centro    NaN
4          Norte   50.0
5            Sur   10.0
{'label': <StringDtype(storage='python', na_value=nan)>, 'value': dtype('float64')}
vacía, sin tipos: {'label': dtype('float64'), 'value': dtype('float64')}
vacía, con tipos: {'label': <StringDtype(storage='python', na_value=nan)>, 'value': dtype('float64')}
```

- Una columna por atributo, con una comprensión cada una; el `None` de Centro pasa a NaN.
- El índice empieza en 1 y se llama `position`: la posición de cada medida, como las líneas de un archivo.
- `StringDtype(...)` es el nombre largo del tipo `str` de pandas.
- Sin valores, pandas no sabe los tipos y pone `float64` en todo, también en `label`. Con `pd.Series([], dtype=...)` cada columna nace con el suyo.

### 2. Niveles sin bucle

Descomenta el **PASO 2** y ejecuta:

```
cut, right=True:  ['medio', 'bajo', nan, 'medio', 'bajo']
cut, right=False: ['medio', 'bajo', nan, 'alto', 'medio'] · category
con sin dato:     ['medio', 'bajo', 'sin dato', 'alto', 'medio']
¿igual que el bucle? True
```

Con `right=True` (por defecto), cada intervalo incluye su borde **derecho**: 50 cae en `(10, 50]`, "medio", y 10 en `(-inf, 10]`, "bajo". `classify` dice que 10 ya es "medio" y 50 ya es "alto": hace falta `right=False`.

El resultado es `category`, con NaN donde falta el valor. Pasado a texto y rellenado con `where`, coincide con el bucle.

Cambia `right=False` por `right=True` en la segunda línea de `cut` y mira la última línea: `False`. Ese es el error que tu proyecto busca con Hypothesis.

### 3. Contar, como Counter

Descomenta el **PASO 3** y ejecuta:

```
{'Norte': 2, 'Sur': 2, 'Centro': 1} · Counter: [('Norte', 2), ('Sur', 2), ('Centro', 1)]
tipo de un conteo: int64
TypeError: Object of type int64 is not JSON serializable
{"Norte": 2, "Sur": 2, "Centro": 1}
```

`value_counts` cuenta igual que `Counter.most_common`, y deja los empates (Norte y Sur) en el orden en que aparecen. Pero cada conteo es un `numpy.int64`, y `json` no lo sabe escribir. Con `str(...)` e `int(...)` en la frontera, todo es de Python.

### 4. Lo que sale de pandas

Descomenta el **PASO 4** y ejecuta:

```
max: 50.0 float64 · float(): float
tolist: [12.5, 8.0, nan, 50.0, 10.0] · float
sin dato: nan · isna: True
¿vuelta completa? True
```

- `max()` da un `numpy.float64`; `float(...)`, un `float` de Python.
- `tolist()` convierte la columna entera a tipos de Python.
- Para saber si falta un valor, `pd.isna`.
- `itertuples(index=False)` recorre las filas como tuplas `(label, value)`. Con `None` donde hay NaN, se recuperan exactamente las medidas de partida: es la comprobación del test `test_frame_of_keeps_every_measurement` de tu proyecto.

### 5. ¿Cuánto se gana?

Descomenta el **PASO 5** y ejecuta. Tarda unos segundos:

```
convertir a tabla    13.5 ms
niveles   bucle       6.4 ms · pandas   1.6 ms
filtrar   bucle       2.3 ms · pandas   4.2 ms
contar    Counter     4.1 ms · pandas   5.9 ms
```

Tus tiempos serán otros; compara las proporciones. 100 000 medidas con semilla 24:

- con **números** (niveles), pandas gana por 4;
- con **texto** (filtrar por etiqueta, contar), pierde: comparar cadenas es trabajo de Python también dentro de pandas;
- y convertir la lista en tabla cuesta más que todo lo demás junto.

pandas no se usa para ir más rápido con 100 000 filas que ya tienes en Python. Se usa por lo que deja escribir, y porque si los datos vienen de un archivo, `read_csv` no crea un objeto por medida (teoría 05, sección 5).

### 6. Memoria de texto

Descomenta el **PASO 6** y ejecuta:

```
str 5.36 MB · category 0.10 MB
categorías: ['Centro', 'Este', 'Norte', 'Oeste', 'Sur']
valores float64: 0.80 MB
```

100 000 etiquetas como `str` guardan 100 000 cadenas. Como `category`, cinco cadenas y un número pequeño por fila: 50 veces menos. Los valores, 100 000 `float64` de 8 bytes: 0,8 MB exactos.

`memory_usage(deep=True)` mide también el texto; sin `deep`, pandas solo cuenta las referencias.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `¿igual que el bucle? False` | Comprueba `right=False` en el segundo `cut`, y que el primero no ha cambiado de variable |
| `¿vuelta completa? False` | Falta `None if pd.isna(value) else value`: NaN no es igual a `None`, ni siquiera a sí mismo |
| `NameError: name 'frame' is not defined` | Descomenta también el paso 1 |
| `NameError: name 'table' is not defined` en el paso 6 | Descomenta también el paso 5 |
| Los tiempos del paso 5 varían mucho de una vez a otra | Normal: cierra otros programas y compara proporciones, no milisegundos |
| `vacía, sin tipos` con `str` en `label` | Tienes otra versión de pandas: debe ser `3.1.0` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 03 · Seleccionar con loc, iloc y máscaras](../ejercicio-03-seleccionar-con-loc-iloc-y-mascaras/README.md) | **Ejercicio 04 · De Python a pandas** | [Proyecto](../../3-proyecto/README.md) |
