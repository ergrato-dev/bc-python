# Ejercicio 03 — Comprehensions

⏱️ 1 h 30 min · Teoría previa: [05](../../1-teoria/05-comprehensions.md)

## Objetivo

Escribir en una línea los bucles que crean listas, diccionarios y conjuntos; distinguir el `if` que filtra del que elige, y usar expresiones generadoras con `sum`, `any` y `all`. Ejercicio **guiado**: descomentas cada paso de `comprehensions_lab.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-05-colecciones_y_comprehensions/2-practicas/ejercicio-03-comprehensions/starter
uv run python comprehensions_lab.py
```

```
Ejercicio 03 · Comprehensions
```

## Pasos

### 1. El mismo filtro, dos formas

Descomenta el **PASO 1** y ejecuta:

```
Con bucle:         [12.5, 8.0, 55.1, 61.0]
Con comprehension: [12.5, 8.0, 55.1, 61.0]
```

Pon las dos versiones una encima de otra y busca cada pieza: la expresión que se añade (`float(...)`), el `for` y el `if`. La comprehension las ordena así: **qué** se añade, **de dónde** sale y **cuáles** pasan.

### 2. Transformar todos o elegir entre dos

Descomenta el **PASO 2**:

```
Cuadrados: [1, 4, 9, 16, 25]
Niveles: ['normal', 'normal', 'alto', 'alto']
```

En `Niveles` salen 4 elementos, tantos como en `same`: el `if ... else` del principio no quita ninguno, solo decide qué texto poner. Prueba a mover el `if` al final sin el `else`: `["alto" for value in same if value >= 50]` da `['alto', 'alto']`, porque ahora filtra. Prueba también `["alto" for value in same if value >= 50 else "normal"]`: `SyntaxError`, el `else` no vale al final. Deshaz los cambios.

### 3. Diccionarios

Descomenta el **PASO 3**:

```
Longitudes: {'Norte': 5, 'Sur': 3, 'Este': 4}
Altas: {'Este': 55.1}
```

Con `clave: valor` delante del `for` sale un diccionario. Recorrer `.items()` y filtrar construye un diccionario más pequeño a partir de otro. Así es `label_means` en el proyecto: `{label: media de values for label, values in groups.items()}`.

### 4. Conjuntos

Descomenta el **PASO 4**:

```
Palabras: 9 | distintas: ['aire', 'del', 'el', 'norte', 'sur', 'y']
Iniciales: ['a', 'd', 'e', 'n', 's', 'y']
```

Llaves sin dos puntos: un conjunto. De 9 palabras quedan 6 distintas. En el proyecto, `distinct_labels` es una set comprehension de una línea.

### 5. Expresiones generadoras

Descomenta el **PASO 5**:

```
Cuántas altas: 2
¿Alguna > 60? True | ¿todas > 5? True
Generador: <generator object <genexpr> at 0x7f...>
Primera vuelta: [0, 1, 4] | segunda: []
```

Dentro de `sum(...)`, `any(...)` o `all(...)` no hace falta construir una lista entera: la expresión entre paréntesis da los valores de uno en uno. `sum(1 for ... if ...)` cuenta cuántos cumplen la condición. La dirección `0x7f...` cambia en cada ejecución. La segunda vuelta sale vacía: un generador se **agota**, igual que `sys.stdin` en la semana 3. Por eso el `main` del proyecto convierte las líneas en lista antes de recorrerlas dos veces.

### 6. Anidadas

Descomenta el **PASO 6**:

```
Aplanada: [1, 2, 3, 4, 5, 6]
Columnas: [[1, 4], [2, 5], [3, 6]]
```

`[n for row in grid for n in row]` se lee como dos bucles en ese orden: primero cada fila, y dentro cada número. `columns` tiene una comprehension dentro de otra. Si para entender una comprehension necesitas releerla tres veces, escribe el bucle: es igual de correcto y se lee mejor.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `NameError: name 'same' is not defined` | Los pasos 2 y 5 usan `same` del PASO 1: descomenta en orden |
| `SyntaxError` con `if ... else` | El `if` con `else` va delante del `for`; el `if` solo, al final |
| Sale `<generator object ...>` en lugar de una lista | Usaste paréntesis: con corchetes es una lista, o pásalo a `list(...)` |
| Sale `{...}` con dos puntos cuando querías un set | Con `clave: valor` es un diccionario; un set no lleva dos puntos |
| `ValueError: could not convert string to float: 'NA'` | Falta el `if text != "NA"`, o está mal escrito |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 02 · Diccionarios y conjuntos](../ejercicio-02-diccionarios-y-conjuntos/README.md) | **Ejercicio 03 · Comprehensions** | [Ejercicio 04 · Estructuras anidadas](../ejercicio-04-estructuras-anidadas/README.md) |
