# 03 · Ordenar

⏱️ 40 min

## 🎯 Objetivos

- Explicar por qué ordenar cuesta O(n log n) y qué hace Python por dentro.
- Aprovechar que `sorted` es estable para ordenar por varios criterios.
- Calcular la mediana ordenando una copia.
- Sacar los k mayores con `heapq` y saber cuándo basta `max` o `min`.

---

## 1. Ordenar a mano, una vez

Hay muchos algoritmos de ordenación. El más fácil de entender es la **ordenación por selección**: busca el menor, ponlo el primero; busca el menor de los que quedan, ponlo el segundo; y así.

```python
def selection_sort(values: list[float]) -> list[float]:
    result = values.copy()
    for i in range(len(result)):
        smallest = min(range(i, len(result)), key=lambda j: result[j])
        result[i], result[smallest] = result[smallest], result[i]
    return result
```

Por cada posición recorre lo que queda para encontrar el menor: un bucle dentro de otro, **O(n²)**. Con un millón de datos, horas. Es útil para entender qué significa ordenar, y nunca se usa en la práctica.

Los buenos algoritmos de ordenación son **O(n log n)**: parten los datos por la mitad, ordenan cada mitad y las mezclan. Hay `log n` niveles de partir, y en cada nivel se mueven los `n` datos. Ningún algoritmo que ordene comparando parejas puede hacerlo mejor en el peor caso.

## 2. `sorted` y `list.sort`

Python usa **Timsort** (desde la 3.11, con la regla de mezcla de Powersort): O(n log n) en el peor caso y muy rápido con datos que ya vienen casi ordenados, como unas medidas que llegan en orden de fecha. Lo usan `sorted` y `list.sort`:

| | `sorted(iterable)` | `lista.sort()` |
|---|---|---|
| Qué recibe | Cualquier iterable | Solo una lista |
| Qué devuelve | Una lista **nueva** | `None`: cambia la lista misma |
| El original | No cambia | Cambia |

Lo viste en la semana 5. Esta semana importa por una razón nueva: una función que recibe una lista no debe desordenársela a quien llama. Por eso `median` del proyecto usa `sorted(values)` y no `values.sort()`, y `test_median_does_not_change_values` lo vigila.

## 3. Ordenar es estable

Una ordenación es **estable** si, cuando dos elementos tienen la misma clave, los deja en el orden en que llegaron. La de Python lo es siempre:

```python
records = [("Sur", 8.0), ("Norte", 48.9), ("Este", 8.0)]
sorted(records, key=lambda record: record[1])
# [('Sur', 8.0), ('Este', 8.0), ('Norte', 48.9)]  Sur sigue antes que Este
```

Eso permite ordenar por varios criterios en varias pasadas, **del menos importante al más importante**:

```python
by_label = sorted(records, key=lambda record: record[0])         # 1.º el desempate
by_value_then_label = sorted(by_label, key=lambda record: record[1])  # 2.º el criterio principal
# [('Este', 8.0), ('Sur', 8.0), ('Norte', 48.9)]
```

La `key` con una tupla de la semana 5 hace lo mismo en una sola pasada, y suele leerse mejor:

```python
sorted(records, key=lambda record: (record[1], record[0]))
```

`most_common` de `Counter` también es estable: con conteos iguales, deja primero la etiqueta que apareció antes. Lo comprueba `test_most_common_labels_ties_keep_first_seen_order`.

## 4. La mediana

La **mediana** es el valor que queda en el centro cuando los ordenas: la mitad de los datos está por debajo y la otra mitad por encima.

```python
values = [12.5, 8.0, 55.1, 61.0, 48.9, 9.5]
ordered = sorted(values)       # [8.0, 9.5, 12.5, 48.9, 55.1, 61.0]
# 6 valores, número par: la media de los dos del centro
(ordered[2] + ordered[3]) / 2  # 30.7
```

| Número de valores | Mediana |
|---|---|
| Impar (5) | `ordered[2]`, el del centro: `ordered[len(ordered) // 2]` |
| Par (6) | La media de `ordered[2]` y `ordered[3]`: `len(ordered) // 2` y el anterior |
| 0 | No existe: mejor lanzar `ValueError` que inventar un número |

La mediana importa en datos porque **un valor extremo no la arrastra**. Con `[10, 11, 12, 13, 500]`, la media es 109,2 y no describe a nadie; la mediana es 12. Un sensor que falla y da un pico, un sueldo enorme en una empresa pequeña: la mediana los aguanta.

Cuesta O(n log n) por ordenar. Existen algoritmos que la encuentran en O(n) sin ordenarlo todo, y la biblioteca estándar trae `statistics.median`, que ordena igual que tú. En la fase 4, pandas y NumPy la calculan sobre millones de datos.

## 5. Los k mayores sin ordenar todo

Para el máximo o el mínimo no hace falta ordenar: `max` y `min` recorren una vez, O(n). Para los **k** mayores:

```python
import heapq

heapq.nlargest(3, readings)                              # [61.0, 55.1, 48.9]
heapq.nsmallest(2, records, key=lambda record: record[1])
sorted(readings, reverse=True)[:3]                       # lo mismo, ordenándolo todo
```

`heapq` usa un **montículo** (*heap*): una estructura que mantiene a mano el menor de los k mejores sin ordenar el resto. Cuesta O(n log k): con un millón de datos y k = 3, mucho menos que ordenar.

| Quieres | Usa | Coste |
|---|---|---|
| El mayor o el menor | `max`, `min` | O(n) |
| Los k mayores, k pequeño | `heapq.nlargest(k, ...)` | O(n log k) |
| Los k mayores, k parecido a n | `sorted(...)[:k]` | O(n log n) |
| Todo ordenado | `sorted` | O(n log n) |

Tu `top` de la semana 5 usa `sorted(...)[:n]`, y con unas pocas etiquetas está bien: no lo cambies sin una razón medida.

---

## ⚠️ Errores frecuentes

| Error | Causa | Arreglo |
|---|---|---|
| La lista de quien llama aparece ordenada | La función usó `.sort()` sobre su argumento | `sorted(values)` crea una copia ordenada |
| `TypeError: '<' not supported between instances of 'float' and 'NoneType'` | Hay `None` entre los valores | Quítalos antes de ordenar |
| La mediana con un número par sale mal | Tomas solo `ordered[len // 2]` | Con par, la media de ese y el anterior |
| Ordenar para sacar el máximo | O(n log n) para algo O(n) | `max` |
| El desempate sale al revés en varias pasadas | Ordenaste primero por el criterio principal | Del menos importante al más importante, o una `key` con tupla |

## ✅ Qué debes saber al terminar

- [ ] Por qué la ordenación por selección es O(n²) y la de Python O(n log n).
- [ ] La diferencia entre `sorted` y `.sort()`, y por qué una función no debe usar `.sort()` sobre su argumento.
- [ ] Qué significa que una ordenación sea estable y cómo se aprovecha.
- [ ] Cómo calcular la mediana con un número par e impar de valores, y por qué resiste los valores extremos.
- [ ] Cuándo usar `max`, `heapq.nlargest` o `sorted`.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [02 · Buscar](02-buscar.md) | **03 · Ordenar** | [04 · collections](04-collections.md) |
