# 📖 Métodos de Diccionarios

## 🎯 Objetivos

- Dominar los métodos principales de diccionarios
- Usar `keys()`, `values()`, `items()` correctamente
- Aplicar `get()`, `setdefault()`, `update()`
- Entender la diferencia entre `copy()` y asignación

---

## 1. Métodos de Acceso

### `get(key, default=None)`

Retorna el valor de una clave, o un valor por defecto si no existe:

```python
user = {"name": "Alice", "age": 25}

# Sin valor por defecto (retorna None)
email = user.get("email")
print(email)  # None

# Con valor por defecto
email = user.get("email", "not-set")
print(email)  # "not-set"

# La clave NO se agrega al diccionario
print("email" in user)  # False
```

### `setdefault(key, default=None)`

Similar a `get()`, pero **SÍ agrega** la clave si no existe:

```python
user = {"name": "Alice", "age": 25}

# Si existe, retorna el valor actual
name = user.setdefault("name", "Unknown")
print(name)  # "Alice"

# Si no existe, agrega y retorna el default
email = user.setdefault("email", "default@email.com")
print(email)  # "default@email.com"
print(user)   # {'name': 'Alice', 'age': 25, 'email': 'default@email.com'}
```

### Comparación `get()` vs `setdefault()`

| Método | Si clave existe | Si clave no existe | Modifica dict |
|--------|-----------------|-------------------|---------------|
| `get()` | Retorna valor | Retorna default | ❌ No |
| `setdefault()` | Retorna valor | Agrega y retorna | ✅ Sí |

```python
# Caso de uso: agrupar elementos
words = ["apple", "banana", "apricot", "blueberry", "avocado"]
by_letter: dict[str, list[str]] = {}

for word in words:
    letter = word[0]
    # setdefault crea la lista si no existe
    by_letter.setdefault(letter, []).append(word)

print(by_letter)
# {'a': ['apple', 'apricot', 'avocado'], 'b': ['banana', 'blueberry']}
```

---

## 2. Vistas: keys(), values(), items()

Estos métodos retornan **vistas** (views) del diccionario, no copias.

### `keys()` - Obtener Claves

```python
person = {"name": "Alice", "age": 25, "city": "NYC"}

# Obtener todas las claves
keys = person.keys()
print(keys)       # dict_keys(['name', 'age', 'city'])
print(type(keys)) # <class 'dict_keys'>

# Convertir a lista
keys_list = list(person.keys())
print(keys_list)  # ['name', 'age', 'city']

# Iterar directamente
for key in person.keys():
    print(key)
# name
# age
# city

# Nota: iterar sobre dict es equivalente
for key in person:  # Implícitamente usa keys()
    print(key)
```

### `values()` - Obtener Valores

```python
person = {"name": "Alice", "age": 25, "city": "NYC"}

# Obtener todos los valores
values = person.values()
print(values)  # dict_values(['Alice', 25, 'NYC'])

# Convertir a lista
values_list = list(person.values())
print(values_list)  # ['Alice', 25, 'NYC']

# Operaciones sobre valores
prices = {"apple": 1.50, "banana": 0.75, "cherry": 2.00}
total = sum(prices.values())
print(f"Total: ${total}")  # Total: $4.25
```

### `items()` - Obtener Pares Clave-Valor

```python
person = {"name": "Alice", "age": 25, "city": "NYC"}

# Obtener pares como tuplas
items = person.items()
print(items)  # dict_items([('name', 'Alice'), ('age', 25), ('city', 'NYC')])

# Iterar con unpacking (MUY COMÚN)
for key, value in person.items():
    print(f"{key}: {value}")
# name: Alice
# age: 25
# city: NYC

# Convertir a lista de tuplas
items_list = list(person.items())
print(items_list)  # [('name', 'Alice'), ('age', 25), ('city', 'NYC')]
```

### Las Vistas son Dinámicas

```python
data = {"a": 1, "b": 2}
keys_view = data.keys()

print(keys_view)  # dict_keys(['a', 'b'])

# Modificar el diccionario
data["c"] = 3
data.pop("a")

# La vista refleja los cambios
print(keys_view)  # dict_keys(['b', 'c'])
```

---

## 3. Métodos de Modificación

### `update()`

Actualiza el diccionario con pares de otro diccionario o iterable:

```python
config = {"host": "localhost", "port": 8080}

# Actualizar con otro diccionario
config.update({"port": 9000, "debug": True})
print(config)  # {'host': 'localhost', 'port': 9000, 'debug': True}

# Actualizar con argumentos con nombre
config.update(timeout=30, retries=3)
print(config)  # {..., 'timeout': 30, 'retries': 3}

# Actualizar con lista de tuplas
config.update([("ssl", True), ("version", "1.0")])
print(config)  # {..., 'ssl': True, 'version': '1.0'}
```

### `pop(key, default)`

Elimina y retorna el valor de una clave:

```python
inventory = {"apples": 50, "bananas": 30, "oranges": 25}

# Eliminar y obtener valor
apples = inventory.pop("apples")
print(apples)     # 50
print(inventory)  # {'bananas': 30, 'oranges': 25}

# Con valor por defecto (evita KeyError)
mangos = inventory.pop("mangos", 0)
print(mangos)  # 0

# Sin default, KeyError si no existe
# inventory.pop("grapes")  # KeyError: 'grapes'
```

### `popitem()`

Elimina y retorna el último par insertado (LIFO):

```python
data = {"a": 1, "b": 2, "c": 3}

# Eliminar último par
last = data.popitem()
print(last)  # ('c', 3)
print(data)  # {'a': 1, 'b': 2}

# Útil para procesar y vaciar
while data:
    key, value = data.popitem()
    print(f"Processing: {key}={value}")
# Processing: b=2
# Processing: a=1
```

### `clear()`

Elimina todos los elementos:

```python
cache = {"user1": "data1", "user2": "data2"}

cache.clear()
print(cache)  # {}
print(len(cache))  # 0
```

---

## 4. Métodos de Copia

### `copy()` - Copia Superficial

```python
original = {"name": "Alice", "scores": [85, 90, 78]}

# Copia superficial
shallow = original.copy()

# Modificar copia no afecta original (primer nivel)
shallow["name"] = "Bob"
print(original["name"])  # "Alice" ✓

# ⚠️ Pero objetos anidados SÍ se comparten
shallow["scores"].append(95)
print(original["scores"])  # [85, 90, 78, 95] ← ¡También cambió!
```

### Copia Profunda con `copy.deepcopy()`

```python
import copy

original = {"name": "Alice", "scores": [85, 90, 78]}

# Copia profunda
deep = copy.deepcopy(original)

# Modificar anidados NO afecta original
deep["scores"].append(95)
print(original["scores"])  # [85, 90, 78] ✓
print(deep["scores"])      # [85, 90, 78, 95]
```

### Asignación vs Copia

```python
original = {"a": 1, "b": 2}

# ❌ Asignación: ambas variables apuntan al mismo objeto
reference = original
reference["c"] = 3
print(original)  # {'a': 1, 'b': 2, 'c': 3} ← ¡Modificado!

# ✅ Copia: objetos independientes
original = {"a": 1, "b": 2}
copy_dict = original.copy()
copy_dict["c"] = 3
print(original)  # {'a': 1, 'b': 2} ← Sin cambios
```

---

## 5. Combinar Diccionarios

### Operador `|` (Python 3.9+)

```python
defaults = {"theme": "light", "language": "en", "font_size": 14}
user_prefs = {"theme": "dark", "notifications": True}

# Combinar (user_prefs sobreescribe defaults)
config = defaults | user_prefs
print(config)
# {'theme': 'dark', 'language': 'en', 'font_size': 14, 'notifications': True}

# El original no cambia
print(defaults)  # {'theme': 'light', 'language': 'en', 'font_size': 14}
```

### Operador `|=` (Update in-place)

```python
config = {"debug": False, "port": 8080}
config |= {"debug": True, "host": "localhost"}
print(config)  # {'debug': True, 'port': 8080, 'host': 'localhost'}
```

### Usando `**` (Unpacking)

```python
dict1 = {"a": 1, "b": 2}
dict2 = {"c": 3, "d": 4}
dict3 = {"b": 99, "e": 5}  # 'b' se sobreescribirá

# Combinar múltiples diccionarios
combined = {**dict1, **dict2, **dict3}
print(combined)  # {'a': 1, 'b': 99, 'c': 3, 'd': 4, 'e': 5}
```

---

## 6. Tabla Resumen de Métodos

### Métodos de Acceso

| Método | Descripción | Retorna |
|--------|-------------|---------|
| `d.get(k)` | Valor de k o None | Valor o None |
| `d.get(k, v)` | Valor de k o v | Valor o default |
| `d.setdefault(k, v)` | Valor de k, agrega si no existe | Valor |
| `d.keys()` | Vista de claves | dict_keys |
| `d.values()` | Vista de valores | dict_values |
| `d.items()` | Vista de pares | dict_items |

### Métodos de Modificación

| Método | Descripción | Retorna |
|--------|-------------|---------|
| `d.update(other)` | Actualiza con otro dict | None |
| `d.pop(k)` | Elimina k, retorna valor | Valor |
| `d.pop(k, v)` | Elimina k o retorna v | Valor o default |
| `d.popitem()` | Elimina último par | Tupla (k, v) |
| `d.clear()` | Elimina todos | None |

### Métodos de Copia

| Método | Descripción | Tipo |
|--------|-------------|------|
| `d.copy()` | Copia superficial | dict |
| `copy.deepcopy(d)` | Copia profunda | dict |

---

## 7. Ejemplos Prácticos

### Contador de Frecuencias

```python
def count_frequency(items: list) -> dict[str, int]:
    """Cuenta la frecuencia de cada elemento."""
    freq: dict[str, int] = {}
    for item in items:
        freq[item] = freq.get(item, 0) + 1
    return freq

words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
print(count_frequency(words))
# {'apple': 3, 'banana': 2, 'cherry': 1}
```

### Invertir Diccionario

```python
def invert_dict(d: dict) -> dict:
    """Invierte claves y valores (asume valores únicos)."""
    return {v: k for k, v in d.items()}

original = {"a": 1, "b": 2, "c": 3}
inverted = invert_dict(original)
print(inverted)  # {1: 'a', 2: 'b', 3: 'c'}
```

### Merge con Prioridad

```python
def merge_configs(*configs: dict) -> dict:
    """Combina múltiples configs, últimos tienen prioridad."""
    result: dict = {}
    for config in configs:
        result.update(config)
    return result

defaults = {"debug": False, "port": 8080, "host": "localhost"}
env_config = {"port": 9000}
user_config = {"debug": True}

final = merge_configs(defaults, env_config, user_config)
print(final)  # {'debug': True, 'port': 9000, 'host': 'localhost'}
```

### Agrupar por Atributo

```python
from typing import NamedTuple

class Student(NamedTuple):
    name: str
    grade: str

students = [
    Student("Alice", "A"),
    Student("Bob", "B"),
    Student("Charlie", "A"),
    Student("Diana", "B"),
    Student("Eve", "A"),
]

# Agrupar por calificación
by_grade: dict[str, list[str]] = {}
for student in students:
    by_grade.setdefault(student.grade, []).append(student.name)

print(by_grade)
# {'A': ['Alice', 'Charlie', 'Eve'], 'B': ['Bob', 'Diana']}
```

---

## ✅ Resumen

| Tarea | Método Recomendado |
|-------|-------------------|
| Acceso seguro | `get(key, default)` |
| Agregar si no existe | `setdefault(key, default)` |
| Iterar pares | `for k, v in d.items()` |
| Combinar dicts | `d1 \| d2` o `update()` |
| Eliminar y obtener | `pop(key)` |
| Copia independiente | `copy()` o `deepcopy()` |

---

## 🔗 Navegación

← [Introducción](01-intro-diccionarios.md) | [Iteración](03-iteracion-diccionarios.md) →
