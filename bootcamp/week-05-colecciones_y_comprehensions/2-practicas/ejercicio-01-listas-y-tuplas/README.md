# Ejercicio 01 — Listas y tuplas

⏱️ 1 h 30 min · Teoría previa: [01](../../1-teoria/01-listas.md) y [02](../../1-teoria/02-tuplas-y-desempaquetado.md)

## Objetivo

Crear, leer, cambiar y ordenar una lista; ver con tus ojos qué pasa cuando dos nombres apuntan a la misma lista, y usar tuplas como registros que se desempaquetan. Ejercicio **guiado**: descomentas cada paso de `lists_lab.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-05-colecciones_y_comprehensions/2-practicas/ejercicio-01-listas-y-tuplas/starter
uv run python lists_lab.py
```

```
Ejercicio 01 · Listas y tuplas
```

Cada paso usa la lista tal como la dejó el anterior: descoméntalos en orden.

## Pasos

### 1. Crear, medir y leer por posición

Descomenta el **PASO 1** y ejecuta:

```
Lecturas: [12.5, 8.0, 55.1, 61.0] | cuántas: 4
Primera: 12.5 | última: 61.0 | del medio: [8.0, 55.1]
```

`readings[0]` es el primer elemento y `readings[-1]`, el último. El trozo `[1:3]` incluye la posición 1 y no la 3, igual que con los textos de la semana 2. Prueba `print(readings[4])`: `IndexError: list index out of range`, porque con 4 elementos la última posición es 3. Deshaz el cambio.

### 2. Cambiar la lista en su sitio

Descomenta el **PASO 2**:

```
Tras cambiar: [3.2, 12.5, 9.5, 61.0] | pop sacó: 48.9
```

Sigue cada línea sobre papel: `[1] = 9.5` sustituye el `8.0`; `append` añade al final; `insert(0, ...)` añade al principio; `pop()` saca el último y lo devuelve; `remove(55.1)` quita el primer elemento que vale `55.1`. Prueba `readings.remove(100.0)`: `ValueError: list.remove(x): x not in list`. Deshaz el cambio.

### 3. `sorted` frente a `sort`

Descomenta el **PASO 3**:

```
sorted: [3.2, 9.5, 12.5, 61.0] | original: [3.2, 12.5, 9.5, 61.0]
sort: [61.0, 12.5, 9.5, 3.2] | sort devolvió: None
```

`sorted` deja la original como estaba y devuelve una lista nueva. `sort` ordena la lista misma y devuelve `None`: escribir `readings = readings.sort()` te deja con `None` y sin lista. Es un error muy frecuente.

### 4. Alias y copia

Descomenta el **PASO 4**:

```
readings: [61.0, 12.5, 9.5, 3.2, 0.0]
snapshot: [61.0, 12.5, 9.5, 3.2]
alias is readings: True | snapshot is readings: False
```

Añadiste `0.0` a `alias` y apareció en `readings`: son dos nombres para **la misma** lista (`is` da `True`). `snapshot` es otra lista, copiada antes del cambio, y no se enteró.

### 5. Tuplas y desempaquetado

Descomenta el **PASO 5**:

```
Norte: 12.5 µg/m³ | campos: 3
first: 3 | rest: [1, 4, 1, 5]
intercambio: 50.0 10.0
```

`label, value, unit = station` reparte las tres partes en tres nombres. `*rest` recoge lo que sobra, en una lista. `low, high = high, low` intercambia sin variable auxiliar: primero se construye la tupla de la derecha y después se reparte. Prueba:

| Cambio | Resultado |
|---|---|
| `station[1] = 13.0` | `TypeError: 'tuple' object does not support item assignment` |
| `label, value = station` | `ValueError: too many values to unpack (expected 2, got 3)` |

Deshaz los cambios.

### 6. Una lista de tuplas, ordenada por el valor

Descomenta el **PASO 6**:

```
  Oriente   55.1
  Norte     12.5
  Sur        8.0
Máximo: ('Oriente', 55.1)
```

Sin `key`, `sorted` compararía las tuplas por su primera parte, la etiqueta, y saldrían en orden alfabético. `key=lambda record: record[1]` ordena por el valor. `max` acepta el mismo `key` y devuelve la tupla entera, no solo el número. Así es `top` en el proyecto.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `NameError: name 'readings' is not defined` | Descomentaste un paso sin el PASO 1: descomenta en orden |
| Las listas salen distintas a las de este README | Ejecutaste un paso dos veces o cambiaste el orden: vuelve a comentar y descomenta en orden |
| `sort: None` | Escribiste `readings = readings.sort(...)`: `sort` no devuelve la lista |
| `IndentationError` en el PASO 6 | El `print` de dentro del `for` necesita 4 espacios más que el `for` |
| `ValueError: too many values to unpack` | Hay más partes que nombres a la izquierda: cuenta las dos cosas |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [05 · Comprehensions](../../1-teoria/05-comprehensions.md) | **Ejercicio 01 · Listas y tuplas** | [Ejercicio 02 · Diccionarios y conjuntos](../ejercicio-02-diccionarios-y-conjuntos/README.md) |
