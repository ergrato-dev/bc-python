# 01 · Arrays: forma, tipo y memoria

⏱️ 45 min

## 🎯 Objetivos

- Crear arrays de varias formas y elegir la adecuada para cada caso.
- Leer la forma (`shape`), el número de ejes (`ndim`) y el tipo (`dtype`) de un array, y cambiar su forma con `reshape`.
- Saber qué pasa cuando mezclas tipos, y por qué un array de `object` pierde lo que gana NumPy.
- Reconocer los dos límites de los números de NumPy: los enteros dan la vuelta y la coma flotante redondea.
- Explicar con los `strides` cómo un bloque de memoria se convierte en una tabla.

---

## 1. De la semana 22 a NumPy de verdad

En la semana 22 viste lo justo para medir: un array es un bloque de números seguidos, todos del mismo tipo, y una operación sobre el array entero recorre ese bloque en C. Con un millón de valores, entre 25 y 100 veces más rápido que un bucle.

Esta semana lo usas en serio, en tu Observatorio. Para eso necesitas saber **qué** es un array por dentro (este archivo), cómo se eligen partes (02), cómo se opera con tablas (03), qué pasa con los datos que faltan y cómo se resume una columna (04), y cómo se lleva todo a un proyecto con tipos y tests (05). Es la base de todo lo que viene en la fase 4: pandas, Polars, scikit-learn y PyTorch guardan sus datos en arrays o en algo muy parecido.

---

## 2. Crear arrays

```python
import numpy as np

np.array([12.5, 8.0, 55.1, 61.0])   # de una lista: [12.5  8.  55.1 61. ]
np.zeros(3)                          # [0. 0. 0.]
np.full(3, 7.0)                      # [7. 7. 7.]
np.arange(0, 10, 3)                  # como range: [0 3 6 9]
np.linspace(0, 1, 5)                 # 5 puntos, extremos incluidos: [0.   0.25 0.5  0.75 1.  ]
np.fromiter((n * n for n in range(5)), dtype=np.int64, count=5)  # [ 0  1  4  9 16]
```

| Función | Cuándo |
|---|---|
| `np.array(lista)` | Ya tienes los datos en una lista |
| `np.zeros`, `np.ones`, `np.full` | Vas a rellenar un array de un tamaño conocido |
| `np.arange(inicio, fin, paso)` | Una secuencia de enteros, como `range` |
| `np.linspace(inicio, fin, n)` | `n` puntos repartidos, con decimales: `arange` con paso `0.1` acumula errores de redondeo y puede dar un elemento de más |
| `np.fromiter(generador, dtype, count)` | Los datos salen de un generador: no crea la lista intermedia, y con `count` reserva la memoria de una vez |

`np.fromiter` es la que usa tu Observatorio para convertir una `Series` en un array (proyecto, paso 5): recorre las medidas una vez y escribe cada valor directamente en el bloque.

`print` de un array no pone comas, y alinea los números: `[12.5  8.  55.1 61. ]`. Es el mismo formato que vas a ver en todos los ejercicios.

---

## 3. Forma y ejes

```python
grid = np.arange(12).reshape(3, 4)
```

```
[[ 0  1  2  3]
 [ 4  5  6  7]
 [ 8  9 10 11]]
```

| Atributo | Valor | Qué dice |
|---|---|---|
| `grid.ndim` | `2` | Cuántos ejes (dimensiones) tiene: 1 es una fila de números, 2 una tabla |
| `grid.shape` | `(3, 4)` | El tamaño de cada eje: 3 filas de 4 columnas |
| `grid.size` | `12` | Cuántos elementos hay en total |
| `grid.dtype` | `int64` | El tipo de **todos** los elementos |
| `grid.itemsize` | `8` | Bytes de cada elemento |
| `grid.nbytes` | `96` | Bytes de todo el array: `size × itemsize` |

El **eje 0** son las filas y el **eje 1**, las columnas. Lo vas a usar en cuanto resumas una tabla: `grid.sum(axis=0)` suma bajando por las filas y da un total por columna (teoría 03).

`reshape` cambia la forma sin cambiar los datos. El número de elementos tiene que cuadrar, y un `-1` le pide a NumPy que calcule ese eje:

```python
np.arange(6).reshape(-1, 2).shape   # (3, 2)
np.arange(6).reshape(4, 2)          # ValueError: cannot reshape array of size 6 into shape (4,2)
```

Un array de una dimensión tiene `shape` `(6,)`, con la coma: es una tupla de un elemento. No es lo mismo que `(1, 6)` (una tabla de una fila) ni que `(6, 1)` (una de una columna). La diferencia importa en la teoría 03.

---

## 4. Un solo tipo para todos

Un array tiene **un** `dtype`. Si le das valores de varios tipos, NumPy busca uno en el que quepan todos:

```python
np.array([1, 2, 3]).dtype        # int64
np.array([1, 2.5]).dtype         # float64: el 1 pasa a 1.0
np.array([True, False]).dtype    # bool
np.array(["Norte", "Sur"]).dtype # <U5: texto de hasta 5 caracteres
np.array(["Norte", 1])           # ['Norte' '1']: el 1 se convierte en texto
np.array([1, None]).dtype        # object
```

| `dtype` | Qué guarda | Bytes |
|---|---|---|
| `int64` | Enteros entre unos ±9,2 × 10¹⁸ | 8 |
| `float64` | Decimales, el `float` de Python | 8 |
| `bool` | `True` o `False` | 1 |
| `<U5` | Texto Unicode de hasta 5 caracteres | 20 (4 por carácter) |
| `object` | Referencias a objetos de Python | 8, más cada objeto |

El último es la trampa. `None` no cabe en ningún tipo numérico, así que NumPy guarda **referencias** a objetos de Python: vuelves a la lista de la semana 22, con toda su lentitud, y muchas funciones dejan de funcionar. Por eso tu Observatorio no convierte las medidas que faltan en `None`, sino en **NaN** (teoría 04), que es un `float64`.

`astype` convierte un array a otro tipo y da uno nuevo:

```python
np.array([1.7, -1.7]).astype(np.int64)          # [ 1 -1]: corta los decimales, no redondea
np.array(["12.5", "8"]).astype(np.float64) * 2  # [25. 16.]
```

---

## 5. Los límites de los números

### Los enteros dan la vuelta

Un entero de Python crece lo que haga falta. Uno de NumPy tiene un tamaño fijo y, si el resultado no cabe, **da la vuelta** sin avisar:

```python
small = np.array([100, 120], dtype=np.int8)   # int8: de -128 a 127
small + 10                                    # [ 110 -126]
```

`120 + 10 = 130` no cabe en un `int8`, y sale `-126`. Ni error ni aviso. Con `int64` el límite está en 9 223 372 036 854 775 807 y casi nunca lo tocas, pero un `int8` o un `int16` elegido para ahorrar memoria te puede dar un total imposible. NumPy sí protesta si **creas** el array con un número que no cabe:

```python
np.array([200], dtype=np.int8)
# OverflowError: Python integer 200 out of bounds for int8
```

`np.iinfo(np.int8)` te dice los límites de un tipo entero.

### La coma flotante redondea

`float64` es el mismo número que el `float` de Python (semana 1), con los mismos redondeos:

```python
0.1 + 0.2 == 0.3              # False
np.isclose(0.1 + 0.2, 0.3)    # True
```

Dos cálculos que hacen lo mismo en distinto orden pueden diferir en el último decimal. Los resultados de NumPy se comparan con **tolerancia**: `np.isclose` para un número, `np.allclose` para arrays enteros, y en los tests, `np.testing.assert_allclose` (teoría 05). `float32` ahorra la mitad de memoria a cambio de unos 7 dígitos de precisión en lugar de 16: `np.float32(0.1)` es `0.10000000149011612`. Es el tipo de las GPU y de muchos modelos de IA (semanas 34 a 36); para analizar datos, `float64`.

Y dividir por cero no es un error, sino un **aviso** (teoría 04):

```python
np.array([1.0, -1.0, 0.0]) / 0
# RuntimeWarning: divide by zero encountered in divide
# RuntimeWarning: invalid value encountered in divide
# [ inf -inf  nan]
```

---

## 6. Cómo un bloque se convierte en tabla

![El array grid de forma (3, 4) se ve como una tabla, pero en memoria es un bloque de 12 enteros de 8 bytes; con strides (32, 8), el elemento [1, 2] está en el byte 48](../0-assets/01-anatomia-de-un-array.svg)

En memoria no hay filas ni columnas: hay un bloque de 96 bytes con los 12 números seguidos. Lo que lo convierte en tabla son tres datos que el array guarda aparte: el `dtype`, la `shape` y los **`strides`**, los bytes que hay que saltar para avanzar uno en cada eje.

```python
grid.strides   # (32, 8)
```

Para bajar una fila se saltan 32 bytes (4 números de 8 bytes); para pasar a la columna siguiente, 8. El elemento `grid[1, 2]` está en el byte `1 × 32 + 2 × 8 = 48`: el séptimo número del bloque, el 6.

Esto explica por qué muchas operaciones son gratis. `reshape` y la traspuesta `grid.T` no mueven ni un byte: crean otro array que **mira el mismo bloque** con otra `shape` y otros `strides`. Es una **vista**:

```python
flat = np.arange(6)
view = flat.reshape(2, 3)
view[0, 0] = 99
flat                          # [99  1  2  3  4  5]: ¡cambió el original!
np.shares_memory(flat, view)  # True
view.base is flat             # True: view no tiene memoria propia
```

Cambiar la vista cambia el original. Cuando necesitas un array independiente, `.copy()`. La teoría 02 te enseña qué operaciones dan vistas y cuáles copias, que es la fuente de errores más típica de NumPy.

---

## 7. Errores frecuentes

| Error | Por qué está mal | Qué hacer |
|---|---|---|
| `None` en un array de números | El array pasa a `object`: lento y sin la mayoría de funciones | NaN para los datos que faltan (teoría 04) |
| Elegir `int8` o `int16` para ahorrar | Los resultados que no caben dan la vuelta sin aviso | `int64` y `float64`, salvo que midas que la memoria importa |
| `astype(np.int64)` para redondear | Corta los decimales: `1.7` da `1` | `np.round(a).astype(np.int64)` |
| `np.arange(1, 1.3, 0.1)` | Los redondeos dan `[1.  1.1 1.2 1.3]`: el 1.3 no debía estar | `np.linspace(1, 1.2, 3)` |
| Comparar resultados con `==` | El último decimal depende del orden de las sumas | `np.isclose`, `np.allclose`, `assert_allclose` |
| Confundir `(6,)` con `(1, 6)` o `(6, 1)` | Son formas distintas, y el broadcasting las trata distinto | Mira `shape` siempre que dudes |
| Cambiar un `reshape` y esperar que el original no cambie | `reshape` da una vista del mismo bloque | `.copy()` si lo necesitas independiente |

---

## ✅ Qué debes saber al terminar

- [ ] Crear arrays con `np.array`, `zeros`, `full`, `arange`, `linspace` y `fromiter`, y cuándo usar cada una.
- [ ] Qué dicen `ndim`, `shape`, `size`, `dtype` e `itemsize`, y cómo cambiar la forma con `reshape`.
- [ ] Qué `dtype` sale al mezclar tipos, y por qué `object` es una trampa.
- [ ] Que los enteros de NumPy dan la vuelta y que los `float64` se comparan con tolerancia.
- [ ] Qué son los `strides`, y por qué `reshape` y `.T` no copian.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 23](../README.md) | **01 · Arrays: forma, tipo y memoria** | [02 · Índices, vistas y máscaras](02-indices-vistas-y-mascaras.md) |
