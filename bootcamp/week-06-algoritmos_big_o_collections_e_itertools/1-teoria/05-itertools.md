# 05 · itertools

⏱️ 50 min

## 🎯 Objetivos

- Explicar qué es un iterador y por qué `itertools` no crea listas.
- Mirar vecinos con `pairwise` y acumular con `accumulate`.
- Encontrar rachas con `groupby` y no confundirlo con un "group by".
- Cortar con `islice` y `batched`, encadenar con `chain` y combinar con `combinations`.
- Usar `max` y `min` con `key` y `default`.

---

## 1. Iteradores: un valor cada vez

En la semana 5 viste que una expresión generadora da los valores de uno en uno y se agota. Es un **iterador**: un objeto al que se le pide "el siguiente" hasta que no quedan. `sys.stdin`, un archivo abierto, `enumerate`, `zip` y `range` (cuando lo recorres) funcionan así.

El módulo `itertools` trae funciones que reciben iterables y **devuelven iteradores**. No crean listas: producen cada valor cuando se le pide. Eso tiene dos consecuencias:

| Consecuencia | Ejemplo |
|---|---|
| Gastan poca memoria aunque los datos sean enormes o infinitos | `islice(count(), 5)` |
| Se agotan: solo se recorren una vez | Si necesitas el resultado dos veces, guárdalo con `list(...)` |

Para ver lo que da un iterador en el REPL, envuélvelo en `list(...)`. Las funciones de esta teoría se importan así:

```python
from itertools import accumulate, batched, chain, combinations, count, groupby, islice, pairwise
```

## 2. `pairwise`: vecinos

`pairwise` da cada pareja de elementos seguidos:

```python
values = [10.0, 15.0, 12.0, 30.0]
list(pairwise(values))     # [(10.0, 15.0), (15.0, 12.0), (12.0, 30.0)]
```

Con `n` valores, `n − 1` parejas. Es la forma de comparar cada medida con la anterior sin pelearte con índices (`values[i]` y `values[i + 1]`, con cuidado de no pasarte del final). `jumps` del proyecto:

```python
[after - before for before, after in pairwise(values)]   # [5.0, -3.0, 18.0]
```

En pandas es `diff()`.

## 3. `accumulate`: resultados parciales

`accumulate` va aplicando una operación y da cada resultado parcial:

```python
list(accumulate([10.0, 15.0, 12.0, 30.0]))        # [10.0, 25.0, 37.0, 67.0]: suma acumulada
list(accumulate([10.0, 15.0, 12.0, 30.0], max))   # [10.0, 15.0, 15.0, 30.0]: máximo hasta aquí
```

La suma acumulada responde "¿cuánto llevamos?" en cada momento: la lluvia caída en el mes, las ventas del año.

## 4. `groupby`: rachas de vecinos iguales

`groupby` junta los elementos **seguidos** que tienen la misma clave. Da parejas `(clave, grupo)`, donde `grupo` es un iterador:

```python
levels = ["alto", "alto", "bajo", "alto", "alto", "alto"]
[(level, len(list(group))) for level, group in groupby(levels)]
# [('alto', 2), ('bajo', 1), ('alto', 3)]
```

`alto` sale dos veces: hay un `bajo` en medio. `groupby` **no** reúne todos los elementos de una clave, como el `GROUP BY` de SQL o `groupby` de pandas: solo los que van seguidos. Si quieres un grupo por clave, ordena antes por esa clave, o usa un diccionario (`values_by_label`).

Precisamente por eso es la herramienta perfecta para **rachas**. Con `key=`, la clave sale de una función, como en `sorted`:

```python
max(
    (len(list(group)) for key, group in groupby(rows, key=level_of) if key == "alto"),
    default=0,
)
```

Es la refactorización de `longest_streak` del proyecto: sin `best`, sin `current`, sin reiniciar el contador a mano.

Cada `group` se agota y, además, deja de servir en cuanto `groupby` avanza al siguiente grupo. Consúmelo dentro de la misma vuelta: `len(list(group))`, `sum(...)`, o `list(group)` si lo necesitas después.

## 5. Cortar, encadenar y combinar

| Función | Qué da | Ejemplo | Resultado |
|---|---|---|---|
| `chain(a, b)` | Los de `a` y después los de `b` | `list(chain([1, 2], [3]))` | `[1, 2, 3]` |
| `islice(it, n)` | Los `n` primeros de un iterador | `list(islice(count(1), 3))` | `[1, 2, 3]` |
| `count(start)` | `start`, `start + 1`, ... sin fin | Numerar o generar ids | — |
| `batched(it, n)` | Tuplas de `n` en `n`; la última puede ser más corta | `list(batched([1, 2, 3, 4, 5], 2))` | `[(1, 2), (3, 4), (5,)]` |
| `combinations(it, 2)` | Cada pareja una vez, sin importar el orden | `list(combinations("ABC", 2))` | `[('A', 'B'), ('A', 'C'), ('B', 'C')]` |

`islice` es el slicing de los iteradores: `sys.stdin[:5]` no existe, `islice(sys.stdin, 5)` sí. `batched` (desde Python 3.12) sirve para mandar datos por lotes, por ejemplo de 500 en 500 a PostgreSQL en la semana 19. `combinations(it, 2)` da `n · (n − 1) / 2` parejas: si lo usas para comparar todo con todo, es O(n²), con o sin bucles anidados.

## 6. `max` y `min` con `key` y `default`

No son de `itertools`, pero se usan con ellos todo el rato:

```python
jumps = [5.0, -8.0, 3.0]
max(jumps)                      # 5.0: el mayor
max(jumps, key=abs)             # -8.0: el mayor en valor absoluto, con su signo
max(abs(j) for j in jumps)      # 8.0: el tamaño, sin signo
max([], default=0.0)            # 0.0 en lugar de error
```

`key` dice **por qué** comparar, pero devuelve el elemento original. Sin `default`, `max([])` lanza `ValueError: max() iterable argument is empty`. `largest_jump` del proyecto combina las dos cosas: `max(jumps(values), key=abs, default=0.0)`. Con empates, `max` devuelve el primero.

## 7. ¿Bucle o `itertools`?

Las dos opciones son O(n). `itertools` no hace el programa más rápido en orden; lo hace más **corto** y con menos sitios donde equivocarse (índices, contadores que reiniciar). Como con las comprehensions: si la versión con `itertools` se lee peor que el bucle, quédate con el bucle. Escribe primero el bucle, comprueba que funciona y, si encaja con una de estas funciones, refactoriza con los tests en verde.

---

## ⚠️ Errores frecuentes

| Error | Causa | Arreglo |
|---|---|---|
| `groupby` da la misma clave dos veces | Solo junta los seguidos | Ordena antes, o usa un diccionario |
| `len(list(group))` da 0 | Leíste el grupo después de avanzar `groupby` | Consúmelo en la misma vuelta |
| El segundo recorrido no da nada | Un iterador se agota | Guárdalo con `list(...)` |
| El programa no termina | `list(count())`: `count` es infinito | Córtalo con `islice` |
| `ValueError: max() iterable argument is empty` | `max` o `min` sobre nada | `default=` |
| `max(abs(j) for j in jumps)` pierde el signo | Comparas y devuelves el valor absoluto | `max(jumps, key=abs)` |
| `ValueError: n must be at least one` | `batched(datos, 0)` | El tamaño del lote es 1 o más |

## ✅ Qué debes saber al terminar

- [ ] Qué es un iterador y qué significa que `itertools` devuelva iteradores.
- [ ] Qué dan `pairwise` y `accumulate` con una lista de cinco valores.
- [ ] Por qué `groupby` sirve para rachas y no para agrupar por clave.
- [ ] Para qué sirven `islice`, `batched`, `chain` y `combinations`.
- [ ] Qué hacen `key` y `default` en `max`.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [04 · collections](04-collections.md) | **05 · itertools** | [Ejercicio 01 · Contar pasos y medir](../2-practicas/ejercicio-01-contar-pasos-y-medir/README.md) |
