# Ejercicio 02 — Buscar y ordenar

⏱️ 1 h 30 min · Teoría previa: [02](../../1-teoria/02-buscar.md) y [03](../../1-teoria/03-ordenar.md)

## Objetivo

Comparar la búsqueda lineal con la binaria, usar `bisect` para buscar y clasificar en una lista ordenada, comprobar que `sorted` es estable y sacar los k mayores con `heapq`. Ejercicio **guiado**: descomentas cada paso de `search_lab.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-06-algoritmos_big_o_collections_e_itertools/2-practicas/ejercicio-02-buscar-y-ordenar/starter
uv run python search_lab.py
```

```
Ejercicio 02 · Buscar y ordenar
```

## Pasos

### 1. Búsqueda lineal

Descomenta el **PASO 1** y ejecuta:

```
¿Está 48.9? True | posición: 4
¿Está 99.0? False
```

`in` e `.index` miran los elementos uno a uno: O(n). Funcionan con cualquier lista, ordenada o no. Prueba `readings.index(99.0)`:

```
ValueError: list.index(x): x not in list
```

Por eso se pregunta antes con `in`. Deshaz el cambio.

### 2. Búsqueda binaria a mano

Descomenta el **PASO 2**:

```
Busco 22:
  miro [0..15] -> centro 7: 14
  miro [8..15] -> centro 11: 22
Posición: 11
Busco 7:
  miro [0..15] -> centro 7: 14
  miro [0..6] -> centro 3: 6
  miro [4..6] -> centro 5: 10
  miro [4..4] -> centro 4: 8
Posición: -1
```

Cada vuelta mira el centro del tramo que queda y descarta la mitad donde el número no puede estar: 16, 8, 4, 2, 1. Con 16 elementos bastan 4 o 5 miradas; con un millón, 20. Eso es **O(log n)**. Solo funciona porque la lista está ordenada: cambia `ordered` por `[30, 2, 14, 22, 0]` y busca 30: dice `-1` aunque está. Deshaz el cambio.

### 3. `bisect`

Descomenta el **PASO 3**:

```
Ordenadas: [8.0, 9.5, 12.5, 22.4, 30.1, 48.9, 55.1, 61.0]
¿Cuántas por debajo de 30? 4
bisect_left(48.9): 5 | bisect_right(48.9): 6
Tras insort(40.0): [8.0, 9.5, 12.5, 22.4, 30.1, 40.0, 48.9, 55.1, 61.0]
    8.0 -> bajo
   10.0 -> medio
   49.9 -> medio
   50.0 -> alto
   61.0 -> alto
```

`bisect_left(lista, x)` es la posición donde iría `x` para no romper el orden; también es **cuántos elementos son menores que `x`**. Con un valor que ya está, `bisect_left` da la posición de antes y `bisect_right` la de después. `insort` inserta en su sitio: encuentra la posición en O(log n), aunque mover los de detrás sigue siendo O(n).

El final es el ejemplo clásico de la documentación: con los umbrales ordenados, `bisect_right` dice en qué tramo cae cada valor. `10.0` va a `medio` porque `bisect_right` deja los iguales a la izquierda; es la misma regla que tu `classify` de la semana 2 (`value < low` es `bajo`).

### 4. Ordenar es estable

Descomenta el **PASO 4**:

```
Por valor:          [('Sur', 8.0), ('Este', 8.0), ('Norte', 12.5), ('Norte', 48.9), ('Oeste', 48.9)]
Por etiqueta:       [('Este', 8.0), ('Norte', 48.9), ('Norte', 12.5), ('Oeste', 48.9), ('Sur', 8.0)]
Etiqueta y valor:   [('Este', 8.0), ('Sur', 8.0), ('Norte', 12.5), ('Norte', 48.9), ('Oeste', 48.9)]
```

En la primera, `Sur` y `Este` valen lo mismo y salen en el orden en que llegaron: `sorted` es **estable**. La tercera ordena por valor una lista que ya estaba por etiqueta, y los empates conservan el orden alfabético. Es otra forma de ordenar por dos criterios: primero por el secundario y después por el principal. La `key` con una tupla de la semana 5 hace lo mismo en una pasada.

### 5. Los k mayores

Descomenta el **PASO 5**:

```
3 mayores: [61.0, 55.1, 48.9]
Con sorted: [61.0, 55.1, 48.9]
2 menores por valor: [('Sur', 8.0), ('Este', 8.0)]
Máximo: 61.0 | mínimo: 8.0
```

`heapq.nlargest(k, datos)` da lo mismo que ordenar y cortar, pero sin ordenarlo todo: con millones de datos y `k` pequeño, se nota. Para uno solo, `max` y `min` (O(n)). Prueba `heapq.nlargest(2, [3, "a"])`:

```
TypeError: '<' not supported between instances of 'int' and 'str'
```

Para ordenar o elegir los mayores, Python compara con `<`, y un número y un texto no se comparan. Deshaz el cambio.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `NameError: name 'readings' is not defined` en el PASO 3 o 5 | Los pasos van en orden: `readings` viene del PASO 1 y `records` del PASO 4 |
| La búsqueda binaria dice `-1` y el número está | La lista no está ordenada: ordénala primero |
| El programa no termina en el PASO 2 | Cambiaste `low = middle + 1` o `high = middle - 1` y el tramo ya no se encoge: `Ctrl+C` y revísalo |
| `bisect` da posiciones raras | La lista no está ordenada: `bisect` no lo comprueba |
| `TypeError: '<' not supported between instances of 'float' and 'NoneType'` | Ordenas registros con valores `None`: quítalos antes, como hace `values_by_label` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 01 · Contar pasos y medir](../ejercicio-01-contar-pasos-y-medir/README.md) | **Ejercicio 02 · Buscar y ordenar** | [Ejercicio 03 · collections](../ejercicio-03-collections/README.md) |
