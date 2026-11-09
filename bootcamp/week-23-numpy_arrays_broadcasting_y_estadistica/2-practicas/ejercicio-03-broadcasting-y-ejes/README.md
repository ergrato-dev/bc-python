# Ejercicio 03 — Broadcasting y ejes

⏱️ 1 h 30 min · Teoría previa: [03](../../1-teoria/03-operaciones-ejes-y-broadcasting.md)

## Objetivo

Trabajar con una tabla de medidas entera, sin bucles:

- operar elemento a elemento con operadores y *ufuncs*;
- resumir por estación y por día con `axis`;
- restar la media de cada columna y de cada fila con **broadcasting**, y arreglar su error;
- normalizar cada estación a media 0 y desviación 1;
- construir tablas de dos y tres ejes;
- medir broadcasting frente a bucles con 100 000 filas.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-23-numpy_arrays_broadcasting_y_estadistica/2-practicas/ejercicio-03-broadcasting-y-ejes/starter
uv run python main.py
```

```
Ejercicio 03 · Broadcasting y ejes
[[45.5 42.2 39.4 16.8]
 [44.3 18.7 49.1 46.1]
 [48.3 48.3 43.  34.6]
 [36.9 55.1 34.2 37.7]
 [32.8 34.8 36.9 42.6]
 [37.1 36.5 33.8 40.9]
 [26.6 40.5 53.1 32.3]]
```

`WEEK` es una semana de medidas: 7 días (filas) por 4 estaciones (columnas: Norte, Sur, Este y Oeste). Sale de un generador de NumPy con semilla 23 (teoría 04): en tu máquina son exactamente estos números.

## Pasos

### 1. Operaciones elemento a elemento

Descomenta el **PASO 1** y ejecuta:

```
en décimas: [455 422 394 168]
raíz:       [6.75 6.5  6.28 4.1 ]
día 1 - día 0: [ -1.2 -23.5   9.7  29.3]
máximo día a día de los dos primeros: [45.5 42.2 49.1 46.1]
```

Cada operación se aplica a cada elemento: multiplicar por 10, la raíz cuadrada, restar dos filas posición a posición. `np.maximum(a, b)` da el mayor de **cada pareja**; no lo confundas con `np.max(a)`, el mayor de todo el array.

### 2. Resumir por ejes

Descomenta el **PASO 2** y ejecuta:

```
media de todo: 38.86
por estación (axis=0): [38.79 39.44 41.36 35.86] (4,)
por día (axis=1):      [35.98 39.55 43.55 40.98 36.78 37.07 38.12] (7,)
la estación de media más alta: Este
```

`axis=0` hace desaparecer el eje 0, el de los 7 días: queda una media por estación, forma `(4,)`. `axis=1` hace desaparecer el de las estaciones: una media por día, `(7,)`. Si te lías, mira la `shape` del resultado y pregúntate qué eje falta.

### 3. Broadcasting por filas y por columnas

Descomenta el **PASO 3** y ejecuta:

```
menos la media de su estación, día 0: [  6.71   2.76  -1.96 -19.06]
ValueError: operands could not be broadcast together with shapes (7,4) (7,) 
keepdims: (7, 1) · [:, None]: (7, 1)
menos la media de su día, día 0:   [  9.52   6.23   3.42 -19.18]
```

- `WEEK - WEEK.mean(axis=0)`: `(7, 4)` menos `(4,)`. Alineadas por la derecha, 4 con 4 encaja, y la fila de medias se repite en los 7 días. El Norte del día 0 está 6.71 por encima de la media del Norte.
- `WEEK - WEEK.mean(axis=1)`: `(7, 4)` menos `(7,)`. Por la derecha, 4 frente a 7: ni iguales ni 1. Error.
- Con `keepdims=True` las medias por día tienen forma `(7, 1)`: una columna. 4 frente a 1 encaja (el 1 se estira), 7 con 7 encaja. `[:, None]` consigue lo mismo añadiendo un eje.

### 4. Normalizar cada estación

Descomenta el **PASO 4** y ejecuta:

```
medias: [0. 0. 0. 0.]
desviaciones: [1. 1. 1. 1.]
el día más alto de cada estación respecto a su media: [2 3 6 1]
```

Dos broadcastings en una línea: restar la media de cada columna y dividir por su desviación. Cada estación queda con media 0 y desviación 1. Así comparas estaciones con escalas distintas: el día 6 del Este (53.1) destaca más en su estación que el día 3 del Sur (55.1) en la suya, aunque el valor sea menor.

`.round(10) + 0.0` limpia los restos de la coma flotante: sin él verías `[ 3.17206578e-17 -4.75809868e-17  4.44089210e-16  4.12368552e-16]`, ceros que no son exactamente cero. El `+ 0.0` convierte un posible `-0.` en `0.`. Las z de los dos días que comparas son 1.70 y 1.47: añade `print(z[6, 2], z[3, 1])` si quieres verlas.

### 5. Tablas de dos ejes

Descomenta el **PASO 5** y ejecuta:

```
[[ 1  2  3  4  5]
 [ 2  4  6  8 10]
 [ 3  6  9 12 15]]
shape: (7, 4, 3)
días por encima de 30, 40 y 50 en cada estación:
[[6 3 0]
 [6 4 1]
 [7 3 1]
 [6 3 0]]
```

`(3, 1)` por `(5,)` da `(3, 5)`: una tabla de multiplicar. La misma idea con tres ejes compara **cada** valor con **cada** umbral: `WEEK[:, :, None]` tiene forma `(7, 4, 1)`, los umbrales `(3,)`, y el resultado `(7, 4, 3)`. Sumar sobre `axis=0` (los días) cuenta, para cada estación y cada umbral, cuántos días lo superan. El Este pasa de 30 los 7 días y de 50, uno.

### 6. Bucle o broadcasting

Descomenta el **PASO 6** y ejecuta:

```
bucles          83.1 ms
broadcasting     8.6 ms
iguales: True
```

Normalizar 100 000 filas de 4 columnas: diez veces más rápido con broadcasting, y una línea en lugar de una función de seis. `np.allclose` confirma que las dos dan lo mismo, con tolerancia. Tus tiempos serán otros: lo que debe coincidir es cuál gana.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| Tus números de `WEEK` son otros | Comprueba `default_rng(23)` y que no has añadido llamadas a `rng` antes de crear `WEEK`: cada llamada avanza el generador |
| `operands could not be broadcast together` en una línea que debía funcionar | Imprime las dos `shape`, alinéalas por la derecha y busca el eje que ni es igual ni es 1 |
| `NameError: name 'by_day' is not defined` en el paso 3 | Descomenta también el paso 2: el 3 usa `by_day` |
| `medias` salen con `e-16` | Te falta `.round(10)`: son ceros con error de redondeo |
| El paso 6 tarda mucho o se queda sin memoria | `100_000` por `10_000` en `big` |
| `iguales: False` | Comprueba que `normalize_loop` divide por `len(table)` (desviación de la población, como `std()` por defecto) y no por `len(table) - 1` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 02 · Índices, vistas y máscaras](../ejercicio-02-indices-vistas-y-mascaras/README.md) | **Ejercicio 03 · Broadcasting y ejes** | [Ejercicio 04 · NaN, estadística y aleatoriedad](../ejercicio-04-nan-estadistica-y-aleatoriedad/README.md) |
