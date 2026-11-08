# Ejercicio 04 — Vectorizar con NumPy

⏱️ 1 h 30 min · Teoría previa: [05](../../1-teoria/05-vectorizar-con-numpy.md)

## Objetivo

Comparar con números un bucle de Python, las funciones de Python y NumPy:

- sumar un millón de valores de tres formas;
- hacer una operación por elemento sin bucle;
- medir lo que cuesta **convertir** una lista en array y volver;
- contar y filtrar con una **máscara**;
- escribir la media móvil de tu Observatorio con sumas acumuladas;
- ver que con pocos datos NumPy **pierde**.

NumPy es el tema de la semana 23: aquí solo lo justo para medir. Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-22-rendimiento_profiling_cprofile_py_spy_y_vectorizacion/2-practicas/ejercicio-04-vectorizar-con-numpy/starter
uv run python main.py
```

```
Ejercicio 04 · Vectorizar
```

La primera vez uv descarga `numpy==2.5.4` (17 MB en Linux, 6 MB en un Mac con Apple Silicon). `VALUES` es una lista de un millón de `float` de Python, siempre los mismos. `best` devuelve los milisegundos por llamada con el método del ejercicio 01: el mínimo de varias repeticiones.

## Pasos

### 1. Sumar un millón de valores

Descomenta el **PASO 1** y ejecuta:

```
dtype float64 · shape (1000000,) · 8 MB
bucle     17.2 ms
sum()      5.0 ms
np.sum     0.1 ms
```

`np.array(VALUES)` crea un **array**: un bloque de memoria con un millón de números de 8 bytes (`float64`) seguidos, sin nada más. Una lista guarda un millón de **referencias** a objetos `float` repartidos por la memoria, cada uno con su tipo y su contador.

Tres formas de sumar, tres velocidades:

- el **bucle** ejecuta en el intérprete, un millón de veces, "lee `value`, súmalo a `total`, guarda `total`";
- `sum()` hace el mismo bucle, pero en C: se ahorra el intérprete, no los objetos;
- `np.sum` recorre la memoria seguida en C, sin objetos, y usa instrucciones que suman varios números a la vez.

Eso es **vectorizar**: escribir la operación sobre el array entero y dejar el bucle a código compilado.

### 2. Una operación por elemento

Descomenta el **PASO 2** y ejecuta:

```
lista     59.7 ms
array      2.2 ms
primera puntuación: 1.5860 · 1.5860
```

La **puntuación z** de cada valor: cuántas desviaciones típicas está de la media. `array - array.mean()` resta un número a **cada** elemento y da un array nuevo; dividir por `array.std()`, igual. Sin `for`, unas 27 veces más rápido que la comprensión. Las dos formas dan lo mismo.

### 3. El precio de entrar y salir

Descomenta el **PASO 3** y ejecuta:

```
np.array(lista)   15.6 ms
array.tolist()    33.6 ms
sum() de lista     4.8 ms
convertir y np.sum   17.0 ms
```

Convertir la lista en array obliga a leer un millón de objetos `float` (16 ms), y volver a lista, a crear un millón (34 ms). Si tus datos llegan en una lista y solo los sumas una vez, `sum()` (5 ms) gana a "convertir y `np.sum`" (17 ms).

NumPy compensa cuando los datos **ya** están en un array o cuando haces **muchas** operaciones sobre ellos: conviertes una vez y vectorizas todo lo demás. Es lo que hace pandas (semana 24): lee el archivo directamente a arrays.

### 4. Contar y filtrar sin bucle

Descomenta el **PASO 4** y ejecuta:

```
bucle     32.3 ms
máscara    0.1 ms
altos: 375447 · el primero 76.66 · [ True False False  True]
```

`array > 50` no da un `bool`: da un **array de booleanos**, uno por valor, la **máscara**. `np.count_nonzero` cuenta los `True`, y `array[máscara]` se queda con los valores donde la máscara es `True`. Es el "filtrar filas" de pandas.

### 5. La media móvil

Descomenta el **PASO 5** y ejecuta:

```
deque   127.4 ms
cumsum    3.5 ms
iguales: True · 3 medias de 5 valores
```

`moving_average` es la de `trends.py` de tu Observatorio: una vuelta del bucle por valor. `moving_average_np` usa un truco: con las **sumas acumuladas** `sums` (`sums[i]` es la suma de los `i` primeros valores), la suma de un tramo es `sums[fin] - sums[inicio]`. Restar dos arrays desplazados calcula todos los tramos a la vez: 36 veces más rápido.

`np.allclose` compara con tolerancia: los dos métodos suman en distinto orden y pueden diferir en el último decimal. Comparar dos `float` con `==` es un error que ya conoces de la semana 4.

### 6. Con pocos datos

Descomenta el **PASO 6** y ejecuta:

```
10 valores · sum()  0.10 µs
10 valores · np.sum  1.06 µs
10 valores · convertir y np.sum  1.48 µs
```

Con 10 valores, `np.sum` es **10 veces más lento** que `sum()`. Cada llamada a NumPy tiene un coste fijo (comprobar tipos, preparar el resultado) de alrededor de un microsegundo, que solo se amortiza con muchos datos.

Y hay otro coste fijo, el de importar NumPy:

```bash
uv run python -X importtime -c "import numpy" 2>&1 | tail -1
```

```
import time:      1579 |     258503 | numpy
```

La segunda columna son microsegundos: 0,26 s la primera vez (Python compila y guarda los `.pyc`), alrededor de 0,1 s las siguientes. En una CLI que tarda un segundo, importar NumPy para ahorrar 30 ms en la media móvil la haría **más lenta**. Lo mides en el paso 11 del proyecto.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ModuleNotFoundError: No module named 'numpy'` | Ejecuta con `uv run python main.py`, no con `python main.py`: el entorno es el de uv |
| `MemoryError` o el equipo va muy lento | Un millón de `float` ocupan unos 32 MB en lista; cierra programas o cambia `1_000_000` por `200_000` |
| `iguales: False` | Revisa `sums[window:] - sums[:-window]`: los dos lados deben tener la misma longitud |
| `ValueError: The truth value of an array with more than one element is ambiguous` | Has escrito `if array > 50:`: una máscara no es un `bool`. Usa `np.count_nonzero(...)`, `.any()` o `.all()` |
| `np.sum` sale `0.0 ms` | Es más rápido que la precisión del formato: cambia `6.1f` por `6.3f` |
| Tus proporciones no se parecen a las del README | Cambian con la CPU, pero el orden debe ser el mismo: bucle > `sum()` > NumPy con un millón, y al revés con 10 |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 03 · Muestrear con py-spy](../ejercicio-03-muestrear-con-py-spy/README.md) | **Ejercicio 04 · Vectorizar con NumPy** | [Proyecto](../../3-proyecto/README.md) |
