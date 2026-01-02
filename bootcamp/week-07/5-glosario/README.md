# Glosario Semana 07: Sets y Algoritmos

## A

### Add (método)
Método de set que agrega un elemento. Si el elemento ya existe, no hace nada.
```python
s = {1, 2}
s.add(3)  # {1, 2, 3}
s.add(1)  # {1, 2, 3} - sin cambios
```

### Algoritmo
Secuencia finita de pasos bien definidos para resolver un problema. Ejemplos: búsqueda lineal, búsqueda binaria, bubble sort.

---

## B

### Big O Notation
Notación matemática que describe el rendimiento de un algoritmo en el peor caso. Ejemplos: O(1), O(log n), O(n), O(n log n), O(n²).

### Binary Search (Búsqueda Binaria)
Algoritmo de búsqueda que divide repetidamente el espacio de búsqueda a la mitad. Requiere datos ordenados. Complejidad: O(log n).
```python
# Buscar 25 en [11, 12, 22, 25, 34]
# Paso 1: mid=22, 25>22 → buscar derecha
# Paso 2: mid=25, encontrado!
```

### bisect (módulo)
Módulo de Python que implementa búsqueda binaria optimizada.
```python
import bisect
bisect.bisect_left([1, 2, 4, 5], 3)  # 2 (posición para insertar)
```

### Bubble Sort
Algoritmo de ordenamiento que compara e intercambia elementos adyacentes. Simple pero ineficiente. Complejidad: O(n²).

---

## C

### Clear (método)
Método que vacía completamente un set o diccionario.
```python
s = {1, 2, 3}
s.clear()  # set()
```

### Complejidad Algorítmica
Medida de los recursos (tiempo/espacio) que requiere un algoritmo. Se expresa con notación Big O.

### Conjunto
Ver **Set**.

---

## D

### Difference (Diferencia)
Operación de conjuntos que retorna elementos en A pero no en B. Operador: `-`.
```python
{1, 2, 3} - {2, 3, 4}  # {1}
```

### Discard (método)
Elimina un elemento del set sin lanzar error si no existe.
```python
s = {1, 2, 3}
s.discard(2)  # {1, 3}
s.discard(5)  # {1, 3} - sin error
```

### Disjoint (Disjuntos)
Dos conjuntos son disjuntos si no tienen elementos en común.
```python
{1, 2}.isdisjoint({3, 4})  # True
```

---

## F

### Frozenset
Versión inmutable de un set. Es hashable, por lo que puede ser clave de diccionario o elemento de otro set.
```python
fs = frozenset([1, 2, 3])
# fs.add(4)  # Error! Es inmutable
d = {fs: "valor"}  # Válido como clave
```

---

## H

### Hashable
Objeto que tiene un valor hash que nunca cambia durante su vida. Requisito para ser elemento de set o clave de dict. Tipos hashables: int, str, tuple (de hashables), frozenset.

---

## I

### In-Place
Operación que modifica la estructura original en lugar de crear una nueva.
```python
# sorted() NO es in-place (crea nueva lista)
# list.sort() SÍ es in-place (modifica original)
```

### Insertion Sort
Algoritmo que construye la lista ordenada elemento por elemento. Eficiente para listas pequeñas o casi ordenadas. Complejidad: O(n²).

### Intersection (Intersección)
Operación de conjuntos que retorna elementos comunes a ambos. Operador: `&`.
```python
{1, 2, 3} & {2, 3, 4}  # {2, 3}
```

### isdisjoint()
Método que verifica si dos conjuntos no tienen elementos en común.

### issubset()
Método que verifica si un conjunto es subconjunto de otro. Equivalente a `<=`.

### issuperset()
Método que verifica si un conjunto es superconjunto de otro. Equivalente a `>=`.

---

## J

### Jaccard Index (Índice de Jaccard)
Medida de similitud entre dos conjuntos: |A ∩ B| / |A ∪ B|. Valor entre 0 (sin similitud) y 1 (idénticos).

---

## K

### Key (parámetro)
Parámetro de `sorted()` y `sort()` que especifica una función para extraer el valor de comparación.
```python
sorted(["bb", "aaa", "c"], key=len)  # ['c', 'bb', 'aaa']
```

---

## L

### Linear Search (Búsqueda Lineal)
Algoritmo que revisa cada elemento secuencialmente hasta encontrar el objetivo. Funciona con datos no ordenados. Complejidad: O(n).

---

## M

### Mutable
Objeto que puede ser modificado después de su creación. `set` es mutable, `frozenset` es inmutable.

---

## O

### O(1)
Complejidad constante. El tiempo no depende del tamaño de entrada. Ejemplo: acceso a diccionario por clave.

### O(log n)
Complejidad logarítmica. El tiempo crece lentamente. Ejemplo: búsqueda binaria.

### O(n)
Complejidad lineal. El tiempo crece proporcionalmente al tamaño. Ejemplo: búsqueda lineal.

### O(n log n)
Complejidad linearítmica. Típica de algoritmos de ordenamiento eficientes como Timsort.

### O(n²)
Complejidad cuadrática. Típica de algoritmos con bucles anidados como bubble sort.

---

## P

### Pop (método)
En sets, elimina y retorna un elemento arbitrario. Lanza `KeyError` si está vacío.
```python
s = {1, 2, 3}
x = s.pop()  # Retorna algún elemento
```

---

## R

### Remove (método)
Elimina un elemento del set. Lanza `KeyError` si no existe.
```python
s = {1, 2, 3}
s.remove(2)  # {1, 3}
# s.remove(5)  # KeyError!
```

### Reverse (parámetro)
Parámetro de `sorted()` y `sort()` que indica orden descendente.
```python
sorted([3, 1, 2], reverse=True)  # [3, 2, 1]
```

---

## S

### Selection Sort
Algoritmo que encuentra el mínimo y lo coloca en su posición. Complejidad: O(n²).

### Set (Conjunto)
Colección no ordenada de elementos únicos y hashables.
```python
s = {1, 2, 3}  # Set literal
s = set([1, 2, 2, 3])  # {1, 2, 3}
```

### sort() (método)
Método de listas que ordena in-place. Retorna `None`.
```python
nums = [3, 1, 2]
nums.sort()  # nums es ahora [1, 2, 3]
```

### sorted() (función)
Función que retorna una nueva lista ordenada sin modificar el original.
```python
sorted([3, 1, 2])  # [1, 2, 3]
```

### Stable Sort
Ordenamiento que mantiene el orden relativo de elementos iguales. Timsort (usado por Python) es estable.

### Subset (Subconjunto)
Conjunto A es subconjunto de B si todos los elementos de A están en B. Operador: `<=`.
```python
{1, 2} <= {1, 2, 3}  # True
```

### Superset (Superconjunto)
Conjunto A es superconjunto de B si A contiene todos los elementos de B. Operador: `>=`.

### Symmetric Difference (Diferencia Simétrica)
Elementos que están en uno u otro conjunto, pero no en ambos. Operador: `^`.
```python
{1, 2, 3} ^ {2, 3, 4}  # {1, 4}
```

---

## T

### Timsort
Algoritmo híbrido usado por Python para `sorted()` y `sort()`. Combina merge sort e insertion sort. Complejidad: O(n log n).

---

## U

### Union (Unión)
Operación de conjuntos que combina todos los elementos de ambos. Operador: `|`.
```python
{1, 2} | {2, 3}  # {1, 2, 3}
```

### Update (método)
Agrega múltiples elementos a un set desde un iterable.
```python
s = {1, 2}
s.update([3, 4])  # {1, 2, 3, 4}
```

---

## V

### Venn Diagram (Diagrama de Venn)
Representación gráfica de conjuntos y sus relaciones usando círculos superpuestos.

---

## 🔗 Navegación

- ⬅️ **Recursos**: [4-recursos](../4-recursos/)
- 🏠 **Volver al índice**: [README](../README.md)
