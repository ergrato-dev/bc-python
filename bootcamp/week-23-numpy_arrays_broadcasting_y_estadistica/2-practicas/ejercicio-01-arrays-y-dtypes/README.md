# Ejercicio 01 — Arrays y dtypes

⏱️ 1 h 30 min · Teoría previa: [01](../../1-teoria/01-arrays-forma-tipo-y-memoria.md)

## Objetivo

Mirar por dentro un array de NumPy:

- crearlo de seis formas distintas;
- leer su forma, su tamaño, su tipo y sus `strides`;
- ver qué `dtype` sale al mezclar tipos, y convertir con `astype`;
- ver cómo un entero **da la vuelta** sin avisar y cómo redondea la coma flotante;
- comprobar que `reshape` da una **vista** que comparte memoria con el original.

Ejercicio **guiado**: descomentas cada paso de `main.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-23-numpy_arrays_broadcasting_y_estadistica/2-practicas/ejercicio-01-arrays-y-dtypes/starter
uv run python main.py
```

```
Ejercicio 01 · Arrays y dtypes
```

La primera vez, uv crea el entorno y descarga `numpy==2.5.4`. Los cuatro ejercicios de la semana usan la misma versión, así que en los siguientes sale de la caché de uv.

## Pasos

### 1. Crear arrays

Descomenta el **PASO 1** y ejecuta:

```
de una lista: [12.5  8.  55.1 61. ]
ceros:        [0. 0. 0.]
lleno de 7:   [7. 7. 7.]
arange:       [0 3 6 9]
linspace:     [0.   0.25 0.5  0.75 1.  ]
fromiter:     [ 0  1  4  9 16]
```

Fíjate en los puntos: `[0. 0. 0.]` son `float64` (el `0.` es `0.0`), y `[0 3 6 9]` son enteros. `np.zeros` da `float64` salvo que pidas otro tipo, y `np.arange` con enteros da enteros.

`linspace(0, 1, 5)` da **5 puntos** con los dos extremos; `arange(0, 10, 3)` va de 3 en 3 **sin** llegar al 10, como `range`. `fromiter` llena el array desde un generador sin crear una lista intermedia: es la que usa tu Observatorio en el proyecto.

### 2. Forma, tamaño y memoria

Descomenta el **PASO 2** y ejecuta:

```
[[ 0  1  2  3]
 [ 4  5  6  7]
 [ 8  9 10 11]]
ndim 2 · shape (3, 4) · size 12
dtype int64 · itemsize 8 · nbytes 96
strides (32, 8)
```

`reshape(3, 4)` convierte los 12 números en 3 filas de 4. En memoria siguen siendo 96 bytes seguidos (12 × 8). Los `strides` dicen cómo leerlos como tabla: para bajar una fila, salta 32 bytes; para pasar a la columna siguiente, 8. Prueba `np.arange(12).reshape(4, 3).strides` en un `uv run python` interactivo: ¿qué cambia, y por qué?

### 3. Un solo tipo para todos

Descomenta el **PASO 3** y ejecuta:

```
int64 float64 bool
<U5 ['Norte' '1']
object
[ 1 -1]
[25. 16.]
```

- `[1, 2.5]` da `float64`: el 1 se convierte en 1.0 para que quepan los dos.
- `["Norte", 1]` da texto: el 1 se convierte en `'1'`. Ya no es un número.
- `[1, None]` da `object`: NumPy guarda referencias a objetos de Python, como una lista. Es lo que **no** quieres para los datos que faltan; para eso está NaN (ejercicio 04).
- `astype(np.int64)` **corta** los decimales hacia el cero: `1.7` da 1 y `-1.7`, -1. No redondea.
- `astype(np.float64)` convierte texto en números, como `float()` con cada elemento.

### 4. Enteros que dan la vuelta

Descomenta el **PASO 4** y ejecuta:

```
int8 + 10: [ 110 -126]
límites de int8: -128 a 127
límites de int64: 9 223 372 036 854 775 807
OverflowError: Python integer 200 out of bounds for int8
```

`120 + 10 = 130` no cabe en un `int8`, que llega a 127: da la vuelta y sale -126. Sin error ni aviso. Con `int64` el límite es enorme, pero existe: los enteros de Python no tienen límite y los de NumPy, sí.

NumPy sí protesta al **crear** el array con un número de Python que no cabe: `OverflowError`. Lo peligroso es el resultado de una operación.

### 5. Coma flotante

Descomenta el **PASO 5** y ejecuta:

```
main.py:69: RuntimeWarning: divide by zero encountered in divide
  print(np.array([1.0, -1.0, 0.0]) / 0)
main.py:69: RuntimeWarning: invalid value encountered in divide
  print(np.array([1.0, -1.0, 0.0]) / 0)
...
False True
float32: 0.10000000149011612
float64: 0.10000000000000001
épsilon de float64: 2.220446049250313e-16
[ inf -inf  nan]
```

Los dos avisos salen por stderr y tu terminal puede mostrarlos **antes** que el resto, aunque se producen al final; delante de `main.py` verás la ruta completa.

- `0.1 + 0.2 == 0.3` es `False`, como en la semana 1; `np.isclose` compara con tolerancia y da `True`.
- Ni `float32` ni `float64` pueden guardar 0.1 exacto. `float32` se aleja a partir del octavo decimal; `float64`, a partir del decimosexto.
- El épsilon es la distancia entre 1.0 y el siguiente `float64`: unos 16 dígitos de precisión.
- Dividir por cero no lanza una excepción: da `inf`, `-inf` y `nan` (0 / 0), y **avisa**. Lo ves a fondo en el ejercicio 04.

### 6. Vistas y copias

Descomenta el **PASO 6** y ejecuta:

```
flat tras cambiar la vista: [99  1  2  3  4  5]
¿comparten memoria? True True
flat tras cambiar la copia: [99  1  2  3  4  5]
¿comparten memoria? False
traspuesta: shape (3, 2) · strides (8, 24) · False
```

Cambiaste `view[0, 0]` y cambió `flat[0]`: `reshape` no copió nada, solo creó otro array que mira el mismo bloque con otra forma. `view.base is flat` lo confirma: `view` no tiene memoria propia. La copia, en cambio, es independiente.

La traspuesta tampoco copia: intercambia los `strides`. Por eso deja de ser **contigua** (`c_contiguous` es `False`): sus filas ya no están seguidas en memoria. Funciona igual, pero algunas operaciones son más lentas sobre ella, y `reshape` de una traspuesta sí tiene que copiar.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ModuleNotFoundError: No module named 'numpy'` | Ejecuta con `uv run python main.py`, no con `python main.py`: el entorno es el de uv |
| `IndentationError` al descomentar | Quita solo `# ` (almohadilla y espacio) del principio de cada línea, no los espacios de dentro |
| `int8 + 10` te da `[110 130]` | Has creado `small` sin `dtype=np.int8`: por defecto es `int64` |
| No ves los `RuntimeWarning` del paso 5 | Python muestra cada aviso una vez por línea; si los silenciaste con `-W ignore`, quítalo |
| `flat tras cambiar la vista` no cambia | Has escrito `view = flat.reshape(2, 3).copy()`, o `view = 99` en lugar de `view[0, 0] = 99` |
| `strides` distintos de `(32, 8)` | Tu `dtype` no es `int64`: en Windows con NumPy antiguo, `arange` daba `int32`. Con 2.5.4 es `int64` en todas partes |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [05 · NumPy en un proyecto](../../1-teoria/05-numpy-en-un-proyecto.md) | **Ejercicio 01 · Arrays y dtypes** | [Ejercicio 02 · Índices, vistas y máscaras](../ejercicio-02-indices-vistas-y-mascaras/README.md) |
