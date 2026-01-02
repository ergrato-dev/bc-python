# 📚 Métodos de Listas en Python

![Métodos de Listas](../0-assets/01-list-methods.svg)

## 🎯 Objetivos

- Dominar los métodos de modificación de listas
- Comprender la diferencia entre métodos in-place y funciones que retornan
- Aplicar métodos de búsqueda y conteo
- Conocer métodos de ordenamiento y copia

---

## 1. Introducción a los Métodos de Listas

Las listas en Python son **mutables**, lo que significa que podemos modificarlas después de crearlas. Python proporciona numerosos métodos para manipular listas de forma eficiente.

```python
# Las listas son objetos con métodos
numbers: list[int] = [1, 2, 3]

# Los métodos se llaman con la sintaxis: objeto.metodo()
numbers.append(4)
print(numbers)  # [1, 2, 3, 4]
```

### Categorías de Métodos

| Categoría | Métodos | Descripción |
|-----------|---------|-------------|
| **Agregar** | `append`, `extend`, `insert` | Añadir elementos |
| **Eliminar** | `remove`, `pop`, `clear` | Quitar elementos |
| **Buscar** | `index`, `count` | Encontrar elementos |
| **Ordenar** | `sort`, `reverse` | Reordenar elementos |
| **Copiar** | `copy` | Duplicar lista |

---

## 2. Métodos para Agregar Elementos

### `append(item)` - Agregar al Final

Añade **un** elemento al final de la lista.

```python
fruits: list[str] = ["apple", "banana"]

# Agregar un elemento
fruits.append("orange")
print(fruits)  # ['apple', 'banana', 'orange']

# append() siempre agrega al final
fruits.append("mango")
print(fruits)  # ['apple', 'banana', 'orange', 'mango']

# ⚠️ Cuidado: append agrega el elemento como un todo
fruits.append(["kiwi", "grape"])
print(fruits)  # ['apple', 'banana', 'orange', 'mango', ['kiwi', 'grape']]
#                                                       ↑ Lista anidada!
```

### `extend(iterable)` - Agregar Múltiples Elementos

Añade **todos los elementos** de un iterable al final.

```python
colors: list[str] = ["red", "blue"]

# Extender con otra lista
colors.extend(["green", "yellow"])
print(colors)  # ['red', 'blue', 'green', 'yellow']

# Funciona con cualquier iterable
colors.extend("RGB")  # String es iterable
print(colors)  # ['red', 'blue', 'green', 'yellow', 'R', 'G', 'B']

# Extender con tupla
colors.extend(("black", "white"))
print(colors)  # [..., 'black', 'white']
```

### `insert(index, item)` - Insertar en Posición

Inserta un elemento en una posición específica.

```python
numbers: list[int] = [1, 2, 4, 5]

# Insertar 3 en el índice 2
numbers.insert(2, 3)
print(numbers)  # [1, 2, 3, 4, 5]

# Insertar al inicio (índice 0)
numbers.insert(0, 0)
print(numbers)  # [0, 1, 2, 3, 4, 5]

# Índices negativos también funcionan
numbers.insert(-1, 99)  # Antes del último
print(numbers)  # [0, 1, 2, 3, 4, 99, 5]
```

### Comparación: append vs extend vs insert

```python
# Diferencias clave
base: list[int] = [1, 2, 3]

# append: agrega UN elemento (puede ser lista)
list1 = base.copy()
list1.append([4, 5])
print(list1)  # [1, 2, 3, [4, 5]]

# extend: agrega CADA elemento del iterable
list2 = base.copy()
list2.extend([4, 5])
print(list2)  # [1, 2, 3, 4, 5]

# insert: agrega en posición específica
list3 = base.copy()
list3.insert(1, 99)
print(list3)  # [1, 99, 2, 3]
```

---

## 3. Métodos para Eliminar Elementos

### `remove(item)` - Eliminar por Valor

Elimina la **primera** ocurrencia de un valor.

```python
letters: list[str] = ["a", "b", "c", "b", "d"]

# Eliminar primera 'b'
letters.remove("b")
print(letters)  # ['a', 'c', 'b', 'd']

# Eliminar la otra 'b'
letters.remove("b")
print(letters)  # ['a', 'c', 'd']

# ⚠️ Error si el elemento no existe
# letters.remove("z")  # ValueError: list.remove(x): x not in list

# Verificar antes de eliminar
if "z" in letters:
    letters.remove("z")
```

### `pop([index])` - Eliminar y Retornar

Elimina y **retorna** el elemento en una posición (por defecto el último).

```python
stack: list[str] = ["first", "second", "third"]

# Pop sin índice: elimina el último
last = stack.pop()
print(last)    # 'third'
print(stack)   # ['first', 'second']

# Pop con índice: elimina en posición
first = stack.pop(0)
print(first)   # 'first'
print(stack)   # ['second']

# ⚠️ Error si índice fuera de rango
# stack.pop(100)  # IndexError: pop index out of range

# ⚠️ Error si lista vacía
empty: list[int] = []
# empty.pop()  # IndexError: pop from empty list
```

### `clear()` - Vaciar Lista

Elimina **todos** los elementos de la lista.

```python
data: list[int] = [1, 2, 3, 4, 5]

data.clear()
print(data)  # []

# Equivalente a:
# data[:] = []
# del data[:]
```

### Comparación: remove vs pop vs del

```python
items: list[str] = ["a", "b", "c", "d", "e"]

# remove: por valor, no retorna nada
items.remove("b")      # Elimina "b"
print(items)           # ['a', 'c', 'd', 'e']

# pop: por índice, retorna el elemento
removed = items.pop(1) # Elimina índice 1, retorna 'c'
print(removed)         # 'c'
print(items)           # ['a', 'd', 'e']

# del: por índice o slice, no retorna
del items[0]           # Elimina índice 0
print(items)           # ['d', 'e']

del items[:]           # Elimina todo (como clear)
print(items)           # []
```

---

## 4. Métodos de Búsqueda

### `index(item, [start, [end]])` - Encontrar Posición

Retorna el índice de la **primera** ocurrencia.

```python
colors: list[str] = ["red", "green", "blue", "green", "yellow"]

# Encontrar 'green'
idx = colors.index("green")
print(idx)  # 1 (primera ocurrencia)

# Buscar desde una posición específica
idx = colors.index("green", 2)  # Buscar desde índice 2
print(idx)  # 3 (segunda ocurrencia)

# Buscar en un rango
idx = colors.index("blue", 0, 4)  # Entre índices 0 y 4
print(idx)  # 2

# ⚠️ Error si no existe
# colors.index("purple")  # ValueError: 'purple' is not in list

# Verificar existencia primero
if "purple" in colors:
    idx = colors.index("purple")
```

### `count(item)` - Contar Ocurrencias

Retorna el número de veces que aparece un elemento.

```python
numbers: list[int] = [1, 2, 2, 3, 2, 4, 2, 5]

# Contar cuántas veces aparece 2
count = numbers.count(2)
print(count)  # 4

# Contar elemento que no existe
count = numbers.count(99)
print(count)  # 0 (no genera error)

# Útil para verificar existencia
if numbers.count(3) > 0:
    print("3 está en la lista")
```

---

## 5. Métodos de Ordenamiento

### `sort(*, key=None, reverse=False)` - Ordenar In-Place

Ordena la lista **modificándola** (no retorna nada).

```python
numbers: list[int] = [3, 1, 4, 1, 5, 9, 2, 6]

# Ordenar ascendente (por defecto)
numbers.sort()
print(numbers)  # [1, 1, 2, 3, 4, 5, 6, 9]

# Ordenar descendente
numbers.sort(reverse=True)
print(numbers)  # [9, 6, 5, 4, 3, 2, 1, 1]

# Ordenar strings
words: list[str] = ["banana", "Apple", "cherry"]
words.sort()
print(words)  # ['Apple', 'banana', 'cherry'] (mayúsculas primero)

# Ordenar ignorando mayúsculas
words.sort(key=str.lower)
print(words)  # ['Apple', 'banana', 'cherry']
```

### Ordenar con `key`

El parámetro `key` permite ordenar por criterios personalizados.

```python
# Ordenar por longitud
words: list[str] = ["python", "is", "awesome", "!"]
words.sort(key=len)
print(words)  # ['!', 'is', 'python', 'awesome']

# Ordenar por valor absoluto
numbers: list[int] = [-5, 2, -1, 8, -3]
numbers.sort(key=abs)
print(numbers)  # [-1, 2, -3, -5, 8]

# Ordenar tuplas por segundo elemento
students: list[tuple[str, int]] = [
    ("Alice", 85),
    ("Bob", 92),
    ("Charlie", 78)
]
students.sort(key=lambda x: x[1])
print(students)  # [('Charlie', 78), ('Alice', 85), ('Bob', 92)]
```

### `reverse()` - Invertir In-Place

Invierte el orden de los elementos.

```python
numbers: list[int] = [1, 2, 3, 4, 5]

numbers.reverse()
print(numbers)  # [5, 4, 3, 2, 1]

# ⚠️ No es lo mismo que ordenar descendente
mixed: list[int] = [3, 1, 4, 1, 5]
mixed.reverse()
print(mixed)  # [5, 1, 4, 1, 3] (no ordenado, solo invertido)
```

### `sort()` vs `sorted()`

```python
original: list[int] = [3, 1, 4, 1, 5]

# sort() modifica la lista original, retorna None
result1 = original.sort()
print(result1)   # None
print(original)  # [1, 1, 3, 4, 5] (modificada)

# sorted() retorna nueva lista, original intacta
original = [3, 1, 4, 1, 5]
result2 = sorted(original)
print(result2)   # [1, 1, 3, 4, 5]
print(original)  # [3, 1, 4, 1, 5] (sin cambios)
```

---

## 6. Método de Copia

### `copy()` - Copia Superficial

Crea una **copia superficial** (shallow copy) de la lista.

```python
original: list[int] = [1, 2, 3]

# Crear copia
copied = original.copy()

# Modificar copia no afecta original
copied.append(4)
print(original)  # [1, 2, 3]
print(copied)    # [1, 2, 3, 4]
```

### ⚠️ Cuidado con Listas Anidadas

```python
# Con listas anidadas, copy() solo copia la referencia
matrix: list[list[int]] = [[1, 2], [3, 4]]
shallow = matrix.copy()

# Modificar elemento anidado afecta ambas!
shallow[0][0] = 99
print(matrix)   # [[99, 2], [3, 4]] ← También cambió!
print(shallow)  # [[99, 2], [3, 4]]

# Para copia profunda, usar copy.deepcopy()
import copy
matrix = [[1, 2], [3, 4]]
deep = copy.deepcopy(matrix)

deep[0][0] = 99
print(matrix)  # [[1, 2], [3, 4]] ← Sin cambios
print(deep)    # [[99, 2], [3, 4]]
```

### Formas de Copiar Listas

```python
original: list[int] = [1, 2, 3]

# Método 1: copy()
copy1 = original.copy()

# Método 2: slicing
copy2 = original[:]

# Método 3: constructor list()
copy3 = list(original)

# Método 4: list comprehension
copy4 = [x for x in original]

# Todas crean copias superficiales independientes
```

---

## 7. Resumen de Métodos

| Método | Acción | Retorna | Modifica Lista |
|--------|--------|---------|----------------|
| `append(x)` | Agrega x al final | `None` | ✅ Sí |
| `extend(iter)` | Agrega elementos de iter | `None` | ✅ Sí |
| `insert(i, x)` | Inserta x en posición i | `None` | ✅ Sí |
| `remove(x)` | Elimina primera x | `None` | ✅ Sí |
| `pop([i])` | Elimina y retorna [i] | Elemento | ✅ Sí |
| `clear()` | Elimina todos | `None` | ✅ Sí |
| `index(x)` | Encuentra posición de x | `int` | ❌ No |
| `count(x)` | Cuenta ocurrencias de x | `int` | ❌ No |
| `sort()` | Ordena elementos | `None` | ✅ Sí |
| `reverse()` | Invierte orden | `None` | ✅ Sí |
| `copy()` | Copia superficial | Nueva lista | ❌ No |

---

## 8. Ejercicio Rápido

```python
# Practica cada método
tasks: list[str] = ["email", "meeting", "code"]

# 1. Agregar "review" al final
tasks.append("review")

# 2. Insertar "breakfast" al inicio
tasks.insert(0, "breakfast")

# 3. Eliminar "meeting"
tasks.remove("meeting")

# 4. ¿Cuántas veces aparece "code"?
count = tasks.count("code")

# 5. Ordenar alfabéticamente
tasks.sort()

print(tasks)  # ['breakfast', 'code', 'email', 'review']
```

---

## 📚 Recursos

- [Documentación oficial - Listas](https://docs.python.org/3/tutorial/datastructures.html#more-on-lists)
- [Python List Methods](https://www.w3schools.com/python/python_ref_list.asp)

---

[← Volver a Semana 05](../README.md) | [Siguiente: Slicing →](02-listas-slicing.md)
