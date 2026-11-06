# Glosario — Semana 06

| Término | Definición |
|---|---|
| **Algoritmo** | Lista finita de pasos que, a partir de una entrada, da una salida |
| **Big-O** (notación O grande) | Forma de decir cómo crece el trabajo de un algoritmo cuando crece la entrada, sin constantes ni términos pequeños: O(n), O(n²) |
| **`bisect`** | Módulo con búsquedas binarias sobre listas ordenadas: `bisect_left`, `bisect_right`, `insort` |
| **Búsqueda binaria** | Buscar en una lista ordenada mirando el centro y descartando la mitad donde no puede estar; O(log n) |
| **Búsqueda lineal** | Mirar los elementos uno a uno hasta encontrarlo; O(n) y sirve con cualquier lista |
| **`Counter`** | Diccionario que cuenta los elementos de un iterable; una clave que no está vale 0 |
| **`defaultdict`** | Diccionario que crea el valor de una clave que no está llamando a una función, como `list` o `int` |
| **`deque`** | Cola de dos extremos: añade y quita por los dos lados en O(1); con `maxlen` guarda solo los últimos |
| **Estable** (ordenación) | Que, con claves iguales, conserva el orden en que llegaron los elementos; `sorted` lo es |
| **`groupby`** | Función de `itertools` que junta los elementos seguidos con la misma clave; sirve para rachas |
| **`heapq`** | Módulo de montículos: `nlargest` y `nsmallest` dan los k mayores o menores sin ordenarlo todo |
| **Iterador** | Objeto que da sus valores de uno en uno cuando se le piden y se agota |
| **Mediana** | El valor del centro de los datos ordenados; con un número par, la media de los dos del centro |
| **Media móvil** | La media de cada tramo de k valores seguidos; suaviza el ruido y deja ver la tendencia |
| **`namedtuple`** | Tupla cuyas partes también se leen por nombre: `reading.value` |
| **O(1)** (constante) | El trabajo no depende del tamaño: `d[clave]`, `x in conjunto` |
| **O(log n)** (logarítmico) | El trabajo crece como las veces que se puede partir n por la mitad: 20 pasos con un millón |
| **O(n)** (lineal) | El trabajo crece igual que n: un recorrido |
| **O(n log n)** | El orden de ordenar bien: `sorted` |
| **O(n²)** (cuadrático) | El trabajo crece como n por n: dos bucles anidados sobre los mismos datos |
| **`pairwise`** | Función de `itertools` que da cada pareja de elementos seguidos |
| **Peor caso** | La entrada que obliga al algoritmo a hacer más trabajo; Big-O suele describir este caso |
| **`perf_counter`** | Reloj de alta precisión de `time`; solo tiene sentido restar dos lecturas |
| **Refactorizar** | Cambiar cómo está escrito el código sin cambiar lo que hace; los tests no cambian y siguen en verde |
| **`timeit`** | Módulo que mide una instrucción repitiéndola muchas veces |
| **Ventana deslizante** | Los últimos k elementos de una secuencia, que avanzan de uno en uno |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Videografía](../4-recursos/videografia/README.md) | **Glosario** | [Rúbrica de evaluación](../rubrica-evaluacion.md) |
