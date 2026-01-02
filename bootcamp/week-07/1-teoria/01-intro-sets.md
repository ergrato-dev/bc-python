# Introducción a Sets

## 🎯 Objetivos

- Comprender qué son los sets y sus características
- Aprender las diferentes formas de crear sets
- Dominar los métodos básicos de manipulación
- Entender cuándo usar sets vs otras estructuras

---

## 1. ¿Qué es un Set?

Un **set** (conjunto) es una colección **no ordenada** de elementos **únicos** y **hashables**. Está basado en el concepto matemático de conjuntos.

### Características Principales

| Característica | Descripción |
|----------------|-------------|
| **No ordenado** | Los elementos no tienen índice ni posición fija |
| **Sin duplicados** | Cada elemento aparece una sola vez |
| **Mutable** | Se pueden agregar/eliminar elementos |
| **Elementos hashables** | Solo acepta tipos inmutables (str, int, tuple) |
| **Acceso O(1)** | Verificar pertenencia es muy rápido |

```python
# Crear un set básico
fruits: set[str] = {"apple", "banana", "cherry"}
print(fruits)  # {'cherry', 'apple', 'banana'} - orden puede variar

# Los duplicados se eliminan automáticamente
numbers: set[int] = {1, 2, 2, 3, 3, 3}
print(numbers)  # {1, 2, 3}
```

---

## 2. Crear Sets

### 2.1 Con Llaves `{}`

```python
# Set literal (no vacío)
colors: set[str] = {"red", "green", "blue"}

# ⚠️ CUIDADO: {} crea un diccionario vacío, NO un set
empty_dict = {}  # tipo: dict
print(type(empty_dict))  # <class 'dict'>
```

### 2.2 Con el Constructor `set()`

```python
# Set vacío
empty_set: set[int] = set()
print(empty_set)  # set()

# Desde una lista (elimina duplicados)
numbers_list: list[int] = [1, 2, 2, 3, 4, 4, 5]
unique_numbers: set[int] = set(numbers_list)
print(unique_numbers)  # {1, 2, 3, 4, 5}

# Desde una cadena (cada carácter es un elemento)
letters: set[str] = set("hello")
print(letters)  # {'h', 'e', 'l', 'o'} - 'l' aparece una vez

# Desde un rango
digits: set[int] = set(range(10))
print(digits)  # {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}

# Desde una tupla
from_tuple: set[int] = set((1, 2, 3))
print(from_tuple)  # {1, 2, 3}
```

### 2.3 Con Set Comprehension

```python
# Cuadrados de números del 0 al 4
squares: set[int] = {x ** 2 for x in range(5)}
print(squares)  # {0, 1, 4, 9, 16}

# Solo números pares
evens: set[int] = {x for x in range(10) if x % 2 == 0}
print(evens)  # {0, 2, 4, 6, 8}

# Primeras letras de palabras
words: list[str] = ["apple", "banana", "avocado", "cherry"]
first_letters: set[str] = {word[0] for word in words}
print(first_letters)  # {'a', 'b', 'c'}
```

---

## 3. Acceso y Pertenencia

A diferencia de listas y diccionarios, **no puedes acceder por índice** a elementos de un set.

### 3.1 Verificar Pertenencia con `in`

```python
fruits: set[str] = {"apple", "banana", "cherry"}

# Verificar si existe (O(1) - muy rápido)
print("apple" in fruits)      # True
print("mango" in fruits)      # False
print("mango" not in fruits)  # True

# Comparación con listas (O(n) - más lento)
fruits_list: list[str] = ["apple", "banana", "cherry"]
print("apple" in fruits_list)  # True, pero más lento en listas grandes
```

### 3.2 Iterar sobre un Set

```python
colors: set[str] = {"red", "green", "blue"}

# Iterar (orden no garantizado)
for color in colors:
    print(color)

# Convertir a lista si necesitas orden
sorted_colors: list[str] = sorted(colors)
print(sorted_colors)  # ['blue', 'green', 'red']
```

---

## 4. Métodos para Agregar Elementos

### 4.1 `add()` - Agregar un Elemento

```python
fruits: set[str] = {"apple", "banana"}

# Agregar un elemento
fruits.add("cherry")
print(fruits)  # {'apple', 'banana', 'cherry'}

# Agregar elemento existente (no hace nada, sin error)
fruits.add("apple")
print(fruits)  # {'apple', 'banana', 'cherry'} - sin cambios
```

### 4.2 `update()` - Agregar Múltiples Elementos

```python
fruits: set[str] = {"apple", "banana"}

# Desde otra colección (lista, set, tupla, etc.)
fruits.update(["cherry", "mango"])
print(fruits)  # {'apple', 'banana', 'cherry', 'mango'}

# Desde múltiples colecciones
fruits.update(["kiwi"], {"grape"}, ("melon",))
print(fruits)  # Incluye todos los nuevos elementos

# Desde un string (agrega cada carácter)
letters: set[str] = {"a", "b"}
letters.update("cd")
print(letters)  # {'a', 'b', 'c', 'd'}
```

---

## 5. Métodos para Eliminar Elementos

### 5.1 `remove()` - Eliminar (Error si no existe)

```python
fruits: set[str] = {"apple", "banana", "cherry"}

# Eliminar elemento existente
fruits.remove("banana")
print(fruits)  # {'apple', 'cherry'}

# Error si no existe
try:
    fruits.remove("mango")
except KeyError as e:
    print(f"Error: {e}")  # Error: 'mango'
```

### 5.2 `discard()` - Eliminar (Sin error si no existe)

```python
fruits: set[str] = {"apple", "banana", "cherry"}

# Eliminar elemento existente
fruits.discard("banana")
print(fruits)  # {'apple', 'cherry'}

# No hace nada si no existe (sin error)
fruits.discard("mango")
print(fruits)  # {'apple', 'cherry'} - sin cambios, sin error
```

### 5.3 `pop()` - Eliminar y Retornar un Elemento Arbitrario

```python
fruits: set[str] = {"apple", "banana", "cherry"}

# Elimina y retorna un elemento (no sabes cuál)
removed = fruits.pop()
print(f"Eliminado: {removed}")
print(f"Restantes: {fruits}")

# Error si el set está vacío
empty_set: set[int] = set()
try:
    empty_set.pop()
except KeyError:
    print("No se puede hacer pop de un set vacío")
```

### 5.4 `clear()` - Vaciar el Set

```python
fruits: set[str] = {"apple", "banana", "cherry"}

fruits.clear()
print(fruits)  # set()
print(len(fruits))  # 0
```

---

## 6. Otros Métodos Útiles

### 6.1 `copy()` - Crear Copia Superficial

```python
original: set[str] = {"apple", "banana"}
copy_set: set[str] = original.copy()

copy_set.add("cherry")
print(original)  # {'apple', 'banana'} - no afectado
print(copy_set)  # {'apple', 'banana', 'cherry'}
```

### 6.2 `len()` - Cantidad de Elementos

```python
fruits: set[str] = {"apple", "banana", "cherry"}
print(len(fruits))  # 3
```

---

## 7. Elementos Válidos (Hashables)

Solo tipos **inmutables** pueden ser elementos de un set:

```python
# ✅ Válidos: tipos inmutables
valid_set: set = {
    42,                    # int
    3.14,                  # float
    "hello",               # str
    True,                  # bool
    (1, 2, 3),             # tuple (de elementos inmutables)
    frozenset({1, 2})      # frozenset
}

# ❌ Inválidos: tipos mutables
try:
    invalid = {[1, 2, 3]}  # list - TypeError
except TypeError as e:
    print(f"Error: {e}")  # unhashable type: 'list'

try:
    invalid = {{"a": 1}}  # dict - TypeError
except TypeError as e:
    print(f"Error: {e}")  # unhashable type: 'dict'

try:
    invalid = {{1, 2}}    # set - TypeError
except TypeError as e:
    print(f"Error: {e}")  # unhashable type: 'set'
```

---

## 8. Comparación: Set vs Lista vs Diccionario

| Operación | Set | Lista | Diccionario |
|-----------|-----|-------|-------------|
| Duplicados | ❌ No permite | ✅ Permite | ❌ Claves únicas |
| Orden | ❌ No ordenado | ✅ Ordenado | ✅ Orden inserción |
| Acceso por índice | ❌ No | ✅ `list[0]` | ❌ No |
| Acceso por clave | ❌ No | ❌ No | ✅ `dict["key"]` |
| Pertenencia (`in`) | O(1) ⚡ | O(n) 🐢 | O(1) ⚡ (claves) |
| Uso de memoria | Medio | Bajo | Alto |

### ¿Cuándo Usar Sets?

```python
# ✅ Eliminar duplicados
emails: list[str] = ["a@test.com", "b@test.com", "a@test.com"]
unique_emails: set[str] = set(emails)

# ✅ Verificar pertenencia rápidamente
allowed_users: set[str] = {"alice", "bob", "carol"}
if user in allowed_users:
    grant_access()

# ✅ Operaciones de conjuntos
set_a = {1, 2, 3}
set_b = {2, 3, 4}
common = set_a & set_b  # {2, 3}

# ❌ NO usar cuando necesitas orden
# ❌ NO usar cuando necesitas acceso por índice
# ❌ NO usar cuando necesitas valores duplicados
```

---

## 9. Ejemplo Práctico: Análisis de Palabras

```python
def analyze_text(text: str) -> dict[str, int | set[str]]:
    """Analiza un texto y retorna estadísticas usando sets."""
    words: list[str] = text.lower().split()

    # Palabras únicas
    unique_words: set[str] = set(words)

    # Palabras que aparecen más de una vez
    seen: set[str] = set()
    duplicates: set[str] = set()
    for word in words:
        if word in seen:
            duplicates.add(word)
        seen.add(word)

    return {
        "total_words": len(words),
        "unique_count": len(unique_words),
        "unique_words": unique_words,
        "duplicates": duplicates
    }

# Uso
text = "the quick brown fox jumps over the lazy dog the fox"
result = analyze_text(text)

print(f"Total palabras: {result['total_words']}")      # 12
print(f"Palabras únicas: {result['unique_count']}")    # 9
print(f"Duplicadas: {result['duplicates']}")           # {'the', 'fox'}
```

---

## 10. Resumen Visual

```
╔═══════════════════════════════════════════════════════════════╗
║                           SET                                 ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  CREAR:                                                       ║
║  {1, 2, 3}           → Set literal                            ║
║  set()               → Set vacío                              ║
║  set([1,2,2,3])      → Desde iterable (sin duplicados)        ║
║  {x for x in range}  → Set comprehension                      ║
║                                                               ║
║  AGREGAR:                                                     ║
║  s.add(x)            → Agregar un elemento                    ║
║  s.update(iterable)  → Agregar múltiples                      ║
║                                                               ║
║  ELIMINAR:                                                    ║
║  s.remove(x)         → Elimina (KeyError si no existe)        ║
║  s.discard(x)        → Elimina (sin error si no existe)       ║
║  s.pop()             → Elimina y retorna arbitrario           ║
║  s.clear()           → Vacía todo                             ║
║                                                               ║
║  VERIFICAR:                                                   ║
║  x in s              → Pertenencia O(1)                       ║
║  len(s)              → Cantidad de elementos                  ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## ✅ Checklist de Verificación

Antes de continuar, asegúrate de poder:

- [ ] Crear sets con `{}`, `set()` y comprehensions
- [ ] Agregar elementos con `add()` y `update()`
- [ ] Eliminar elementos con `remove()`, `discard()` y `pop()`
- [ ] Verificar pertenencia con `in`
- [ ] Entender qué tipos pueden ser elementos de un set
- [ ] Decidir cuándo usar set vs lista vs diccionario

---

## 🔗 Navegación

- ➡️ **Siguiente**: [Operaciones de Conjuntos](02-operaciones-conjuntos.md)
- 🏠 **Índice**: [README](../README.md)
