# Ejercicio 03 — collections

⏱️ 1 h 30 min · Teoría previa: [04](../../1-teoria/04-collections.md)

## Objetivo

Usar las cuatro herramientas de `collections` que más vas a ver: `Counter` para contar, `defaultdict` para agrupar, `deque` para colas y ventanas, y `namedtuple` para registros con nombres. La ventana del paso 4 es la media móvil del proyecto. Ejercicio **guiado**: descomentas cada paso de `collections_lab.py`, ejecutas y comparas. No se entrega.

## Antes de empezar

```bash
cd bootcamp/week-06-algoritmos_big_o_collections_e_itertools/2-practicas/ejercicio-03-collections/starter
uv run python collections_lab.py
```

```
Ejercicio 03 · collections
```

## Pasos

### 1. `Counter`

Descomenta el **PASO 1** y ejecuta:

```
Conteo: Counter({'alto': 3, 'bajo': 2, 'medio': 1})
Los 2 más comunes: [('alto', 3), ('bajo', 2)]
¿Cuántos 'sin dato'? 0
Tras update: Counter({'alto': 3, 'bajo': 3, 'medio': 1, 'sin dato': 1})
Total: 8
```

Es el contador con `get(level, 0) + 1` del ejercicio 02 de la semana 5, en una línea. Un `Counter` es un diccionario: `counts["alto"]` da 3, pero una clave que no está da **0** en lugar de `KeyError`. `most_common(n)` da las `n` parejas más frecuentes; con empates, primero la que apareció antes. Es `most_common_labels` del proyecto.

### 2. `defaultdict`

Descomenta el **PASO 2**:

```
Grupos: {'Norte': [12.5, 48.9], 'Sur': [8.0, 9.5], 'Este': [30.0]}
¿Oeste? False
groups['Oeste']: []
¿Oeste ahora? True
```

`defaultdict(list)` llama a `list()` la primera vez que pides una clave que no está, guarda esa lista vacía y te la devuelve. Así `groups[label].append(value)` sustituye a `setdefault(label, []).append(value)`.

Las tres últimas líneas son la trampa: **solo leer** `groups["Oeste"]` crea la clave. Por eso el proyecto devuelve `dict(groups)` y no el `defaultdict`: quien reciba los grupos y pregunte por una etiqueta que no existe debe ver un `KeyError`, no una lista vacía que aparece sola. Con `"Oeste" in groups` o `groups.get("Oeste")` no se crea nada.

### 3. `deque`

Descomenta el **PASO 3**:

```
Cola: ['Oeste', 'Norte', 'Sur', 'Este']
Sale: Oeste | queda: ['Norte', 'Sur', 'Este']
Vaciar 100,000 por la izquierda | lista: 376 ms | deque: 2.2 ms
```

Un `deque` (se pronuncia "dec") añade y quita por los dos extremos en O(1). Una lista también es rápida por la derecha, pero `pop(0)` tiene que correr una posición todos los elementos que quedan: O(n) cada vez, O(n²) para vaciarla entera. Tus milisegundos serán otros; la diferencia, parecida.

### 4. Los últimos N con `maxlen`

Descomenta el **PASO 4**:

```
  entra 10.0 -> [10.0] media 10.0
  entra 20.0 -> [10.0, 20.0] media 15.0
  entra 30.0 -> [10.0, 20.0, 30.0] media 20.0
  entra 40.0 -> [20.0, 30.0, 40.0] media 30.0
  entra 50.0 -> [30.0, 40.0, 50.0] media 40.0
```

Con `maxlen=3`, cuando el deque está lleno y entra uno nuevo, el más antiguo sale solo por el otro lado. Es una **ventana deslizante**: siempre los tres últimos. Las tres últimas medias son la media móvil de ventana 3 de `[10, 20, 30, 40, 50]`, y son lo que espera `test_moving_average_window_three` del proyecto.

Fíjate en `sum(last_three)`: suma la ventana entera en cada vuelta. Con ventana `k` y `n` valores son `n × k` sumas. En el proyecto lo haces mejor: guardas el total, sumas el que entra y restas el que sale (teoría 04, sección 3).

### 5. `namedtuple`

Descomenta el **PASO 5**:

```
Reading(label='Norte', value=12.5) | etiqueta: Norte | valor: 12.5
Desempaquetada: Norte 12.5 | ¿es tupla? True
Cambiada: Reading(label='Norte', value=13.0) | original: Reading(label='Norte', value=12.5)
```

Una `namedtuple` es una tupla cuyas partes también tienen nombre: `reading.value` se lee mejor que `reading[1]`. Sigue siendo una tupla: se desempaqueta y no cambia. Prueba `reading.value = 13.0`:

```
AttributeError: can't set attribute
```

`_replace` crea una tupla **nueva** con un campo cambiado. Deshaz el cambio. En la semana 9 verás `dataclasses`, que dan lo mismo con tipos y algo más.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `TypeError: first argument must be callable or None` | Escribiste `defaultdict([])`: se le pasa la función que crea el valor, `list`, sin paréntesis |
| Aparecen claves vacías en un `defaultdict` | Leíste con `groups[clave]` una que no estaba: usa `in` o `.get` para preguntar |
| `IndexError: deque index out of range` | Pediste una posición que el deque aún no tiene: mira `len()` antes |
| `AttributeError: can't set attribute` | Las `namedtuple` no cambian: usa `_replace` |
| `most_common` da otro orden en los empates | Con conteos iguales manda el orden de aparición; cambia el orden de la lista y lo verás |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 02 · Buscar y ordenar](../ejercicio-02-buscar-y-ordenar/README.md) | **Ejercicio 03 · collections** | [Ejercicio 04 · itertools](../ejercicio-04-itertools/README.md) |
