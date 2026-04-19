# 📖 Glosario - Semana 05: Listas y Tuplas

## A

### Append
Método de lista que agrega un elemento al final.
```python
numbers = [1, 2, 3]
numbers.append(4)  # [1, 2, 3, 4]
```

---

## C

### Copy (Shallow)
Copia superficial de una lista donde los elementos de primer nivel son copiados, pero los objetos anidados comparten referencia.
```python
original = [1, [2, 3]]
shallow = original.copy()  # o original[:]
```

### Count
Método que cuenta las ocurrencias de un elemento en una secuencia.
```python
numbers = [1, 2, 2, 3, 2]
count = numbers.count(2)  # 3
```

---

## E

### Extend
Método de lista que agrega todos los elementos de un iterable al final.
```python
a = [1, 2]
a.extend([3, 4])  # [1, 2, 3, 4]
```

### Extended Unpacking
Uso del operador `*` para capturar múltiples elementos en unpacking.
```python
first, *rest = [1, 2, 3, 4]  # first=1, rest=[2, 3, 4]
```

---

## I

### Immutable (Inmutable)
Objeto que no puede ser modificado después de su creación. Las tuplas son inmutables.
```python
t = (1, 2, 3)
# t[0] = 5  # TypeError: 'tuple' object does not support item assignment
```

### Index
1. Posición de un elemento en una secuencia (base 0)
2. Método que retorna la posición de la primera ocurrencia de un elemento
```python
fruits = ["apple", "banana", "cherry"]
pos = fruits.index("banana")  # 1
```

### Insert
Método de lista que inserta un elemento en una posición específica.
```python
numbers = [1, 3, 4]
numbers.insert(1, 2)  # [1, 2, 3, 4]
```

### In-place
Operación que modifica el objeto original en lugar de crear uno nuevo.
```python
numbers = [3, 1, 2]
numbers.sort()  # Modifica numbers directamente
```

### Iterable
Objeto que puede ser recorrido en un bucle (listas, tuplas, strings, etc.).

---

## L

### List (Lista)
Secuencia mutable y ordenada de elementos.
```python
numbers: list[int] = [1, 2, 3, 4, 5]
```

### List Comprehension
Sintaxis concisa para crear listas basadas en iterables existentes.
```python
squares = [x**2 for x in range(5)]  # [0, 1, 4, 9, 16]
```

---

## M

### Matrix (Matriz)
Estructura de datos bidimensional representada como lista de listas.
```python
matrix: list[list[int]] = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
```

### Mutable
Objeto que puede ser modificado después de su creación. Las listas son mutables.

---

## N

### Named Tuple
Subclase de tupla que permite acceso por nombre además de por índice.
```python
from typing import NamedTuple

class Point(NamedTuple):
    x: float
    y: float

p = Point(10, 20)
print(p.x)  # 10
```

### Negative Index
Índice negativo que cuenta desde el final de la secuencia.
```python
items = [1, 2, 3, 4, 5]
last = items[-1]  # 5
second_last = items[-2]  # 4
```

### Nested (Anidado)
Estructura que contiene otras estructuras del mismo o diferente tipo.
```python
nested = [[1, 2], [3, 4], [5, 6]]
```

---

## P

### Pop
Método que elimina y retorna un elemento de una posición específica (por defecto el último).
```python
stack = [1, 2, 3]
last = stack.pop()  # 3, stack = [1, 2]
first = stack.pop(0)  # 1, stack = [2]
```

### Packing
Proceso de combinar múltiples valores en una tupla.
```python
coordinates = 10, 20, 30  # Tupla (10, 20, 30)
```

---

## R

### Remove
Método de lista que elimina la primera ocurrencia de un valor.
```python
colors = ["red", "green", "red", "blue"]
colors.remove("red")  # ["green", "red", "blue"]
```

### Reverse
1. Método que invierte una lista in-place
2. Función `reversed()` que retorna un iterador invertido
```python
numbers = [1, 2, 3]
numbers.reverse()  # [3, 2, 1]
# O usando slicing:
reversed_copy = numbers[::-1]
```

---

## S

### Sequence (Secuencia)
Tipo de dato ordenado que soporta indexación, slicing e iteración. Incluye listas, tuplas y strings.

### Slice (Rebanada)
Porción de una secuencia extraída usando la notación `[start:stop:step]`.
```python
numbers = [0, 1, 2, 3, 4, 5]
subset = numbers[1:4]    # [1, 2, 3]
every_other = numbers[::2]  # [0, 2, 4]
```

### Slicing
Técnica para extraer una porción de una secuencia.
```python
text = "Python"
text[0:2]   # "Py"
text[::2]   # "Pto"
text[::-1]  # "nohtyP"
```

### Sort
1. Método `sort()` que ordena una lista in-place
2. Función `sorted()` que retorna una nueva lista ordenada
```python
numbers = [3, 1, 4, 1, 5]
numbers.sort()  # Modifica: [1, 1, 3, 4, 5]

original = [3, 1, 4]
new = sorted(original)  # original sin cambios
```

### Step
Tercer parámetro del slicing que define el incremento entre índices.
```python
numbers = [0, 1, 2, 3, 4, 5]
every_second = numbers[::2]   # [0, 2, 4]
reversed = numbers[::-1]      # [5, 4, 3, 2, 1, 0]
```

---

## T

### Tuple (Tupla)
Secuencia inmutable y ordenada de elementos.
```python
point: tuple[int, int] = (10, 20)
rgb: tuple[int, int, int] = (255, 128, 0)
```

### Tuple Unpacking
Proceso de extraer elementos de una tupla en variables individuales.
```python
coordinates = (10, 20, 30)
x, y, z = coordinates  # x=10, y=20, z=30
```

---

## U

### Unpacking
Extracción de elementos de una secuencia en variables separadas.
```python
a, b, c = [1, 2, 3]
first, *rest = (1, 2, 3, 4)  # first=1, rest=[2, 3, 4]
```

---

## Z

### Zero-based Index
Sistema de indexación donde el primer elemento tiene índice 0.
```python
items = ["a", "b", "c"]
items[0]  # "a" (primer elemento)
items[1]  # "b" (segundo elemento)
```

---

## 🔗 Navegación

← [Recursos](../4-recursos/) | [Semana 05](../README.md) | [Semana 06](../../week-06/) →
