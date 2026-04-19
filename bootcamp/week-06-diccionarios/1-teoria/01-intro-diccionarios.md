# 📖 Introducción a Diccionarios

## 🎯 Objetivos

- Entender qué es un diccionario y cuándo usarlo
- Crear diccionarios con diferentes sintaxis
- Acceder, agregar y modificar elementos
- Comprender claves válidas (hashability)

---

## 1. ¿Qué es un Diccionario?

Un **diccionario** es una estructura de datos que almacena pares **clave-valor**. A diferencia de las listas (que usan índices numéricos), los diccionarios usan **claves únicas** para acceder a los valores.

```python
# Lista: acceso por índice numérico
fruits: list[str] = ["apple", "banana", "cherry"]
print(fruits[0])  # "apple"

# Diccionario: acceso por clave
prices: dict[str, float] = {"apple": 1.50, "banana": 0.75, "cherry": 2.00}
print(prices["apple"])  # 1.50
```

### Analogía del Mundo Real

Piensa en un diccionario como:
- 📞 **Agenda telefónica**: nombre → número
- 📚 **Diccionario real**: palabra → definición
- 🏷️ **Etiquetas**: identificador → valor

---

## 2. Crear Diccionarios

### Sintaxis con Llaves `{}`

```python
# Diccionario vacío
empty: dict = {}

# Con datos iniciales
person: dict[str, str | int] = {
    "name": "Alice",
    "age": 30,
    "city": "New York"
}

# En una línea
colors: dict[str, str] = {"red": "#FF0000", "green": "#00FF00", "blue": "#0000FF"}
```

### Constructor `dict()`

```python
# Desde argumentos con nombre (solo claves string)
config = dict(host="localhost", port=8080, debug=True)
print(config)  # {'host': 'localhost', 'port': 8080, 'debug': True}

# Desde lista de tuplas
items = dict([("a", 1), ("b", 2), ("c", 3)])
print(items)  # {'a': 1, 'b': 2, 'c': 3}

# Desde dos listas con zip
keys = ["name", "age", "city"]
values = ["Bob", 25, "London"]
person = dict(zip(keys, values))
print(person)  # {'name': 'Bob', 'age': 25, 'city': 'London'}
```

### Método `fromkeys()`

Crea un diccionario con claves predefinidas y un valor común:

```python
# Todas las claves con el mismo valor
defaults = dict.fromkeys(["a", "b", "c"], 0)
print(defaults)  # {'a': 0, 'b': 0, 'c': 0}

# Sin valor = None
nulls = dict.fromkeys(["x", "y", "z"])
print(nulls)  # {'x': None, 'y': None, 'z': None}
```

---

## 3. Acceder a Valores

### Operador `[]`

```python
student: dict[str, str | int] = {"name": "Alice", "age": 25, "grade": "A"}

# Acceso directo
print(student["name"])   # "Alice"
print(student["age"])    # 25

# ⚠️ KeyError si la clave no existe
# print(student["email"])  # KeyError: 'email'
```

### Método `get()` (Recomendado)

```python
student: dict[str, str | int] = {"name": "Alice", "age": 25}

# get() retorna None si no existe
email = student.get("email")
print(email)  # None

# get() con valor por defecto
email = student.get("email", "no-email@example.com")
print(email)  # "no-email@example.com"

# La clave original NO se modifica
print("email" in student)  # False
```

### ¿Cuándo usar `[]` vs `get()`?

| Situación | Usar | Razón |
|-----------|------|-------|
| Clave debe existir | `[]` | Error explícito si falta |
| Clave puede no existir | `get()` | Evita KeyError |
| Valor por defecto | `get(key, default)` | Código más limpio |

```python
# Ejemplo práctico: contador de palabras
text = "hello world hello python"
word_count: dict[str, int] = {}

for word in text.split():
    # Sin get(): necesita verificar primero
    # if word in word_count:
    #     word_count[word] += 1
    # else:
    #     word_count[word] = 1

    # Con get(): más elegante
    word_count[word] = word_count.get(word, 0) + 1

print(word_count)  # {'hello': 2, 'world': 1, 'python': 1}
```

---

## 4. Agregar y Modificar Elementos

### Asignación Directa

```python
student: dict[str, str | int] = {"name": "Alice"}

# Agregar nueva clave
student["age"] = 25
student["email"] = "alice@example.com"

# Modificar valor existente
student["age"] = 26

print(student)
# {'name': 'Alice', 'age': 26, 'email': 'alice@example.com'}
```

### Actualizar Múltiples Valores

```python
student: dict[str, str | int] = {"name": "Alice", "age": 25}

# update() con diccionario
student.update({"age": 26, "city": "NYC"})
print(student)  # {'name': 'Alice', 'age': 26, 'city': 'NYC'}

# update() con argumentos con nombre
student.update(grade="A", year=2024)
print(student)  # {..., 'grade': 'A', 'year': 2024}
```

### Operador `|` (Python 3.9+)

```python
dict1 = {"a": 1, "b": 2}
dict2 = {"b": 3, "c": 4}

# Combinar diccionarios (dict2 sobreescribe dict1)
combined = dict1 | dict2
print(combined)  # {'a': 1, 'b': 3, 'c': 4}

# Actualizar in-place
dict1 |= dict2
print(dict1)  # {'a': 1, 'b': 3, 'c': 4}
```

---

## 5. Eliminar Elementos

### `del` Statement

```python
person = {"name": "Alice", "age": 25, "city": "NYC"}

# Eliminar una clave
del person["city"]
print(person)  # {'name': 'Alice', 'age': 25}

# ⚠️ KeyError si no existe
# del person["email"]  # KeyError
```

### Método `pop()`

```python
person = {"name": "Alice", "age": 25, "city": "NYC"}

# Elimina y retorna el valor
city = person.pop("city")
print(city)    # "NYC"
print(person)  # {'name': 'Alice', 'age': 25}

# Con valor por defecto (evita KeyError)
email = person.pop("email", "not found")
print(email)  # "not found"
```

### Método `popitem()`

```python
person = {"name": "Alice", "age": 25, "city": "NYC"}

# Elimina y retorna el último par insertado (LIFO)
last = person.popitem()
print(last)    # ('city', 'NYC')
print(person)  # {'name': 'Alice', 'age': 25}
```

### Método `clear()`

```python
data = {"a": 1, "b": 2, "c": 3}

# Elimina todos los elementos
data.clear()
print(data)  # {}
```

---

## 6. Verificar Existencia

### Operador `in`

```python
config = {"host": "localhost", "port": 8080}

# Verificar si existe la clave
print("host" in config)     # True
print("timeout" in config)  # False

# NOT in
print("debug" not in config)  # True
```

### Uso en Condicionales

```python
settings: dict[str, str | int] = {"theme": "dark", "language": "en"}

# Patrón común: verificar antes de acceder
if "font_size" in settings:
    size = settings["font_size"]
else:
    size = 14  # valor por defecto

# Equivalente más simple con get()
size = settings.get("font_size", 14)
```

---

## 7. Claves Válidas (Hashability)

Las claves de un diccionario **deben ser hashables** (inmutables):

### ✅ Claves Válidas

```python
# Strings
d1: dict[str, int] = {"name": 1}

# Números
d2: dict[int, str] = {1: "one", 2: "two"}

# Tuplas (si contienen solo inmutables)
d3: dict[tuple[int, int], str] = {(0, 0): "origin", (1, 1): "point"}

# Booleanos
d4: dict[bool, str] = {True: "yes", False: "no"}

# Mezcla de tipos hashables
d5 = {"name": "Alice", 1: "first", (0, 0): "origin"}
```

### ❌ Claves Inválidas

```python
# Listas NO son hashables
# bad = {[1, 2]: "value"}  # TypeError: unhashable type: 'list'

# Diccionarios NO son hashables
# bad = {{"a": 1}: "value"}  # TypeError: unhashable type: 'dict'

# Sets NO son hashables
# bad = {{1, 2}: "value"}  # TypeError: unhashable type: 'set'
```

### ¿Por qué esta restricción?

Los diccionarios usan una **tabla hash** internamente para búsquedas O(1). Las claves deben tener un hash estable que no cambie.

```python
# Los objetos mutables pueden cambiar su contenido
my_list = [1, 2, 3]
my_list.append(4)  # El "contenido" cambió

# Si se usara como clave, ¿cómo encontrarla después?
# Por eso solo se permiten inmutables como claves
```

---

## 8. Longitud y Propiedades

```python
inventory = {"apples": 50, "bananas": 30, "oranges": 25}

# Número de pares clave-valor
print(len(inventory))  # 3

# Verificar si está vacío
empty_dict: dict = {}
print(len(empty_dict) == 0)  # True
print(not empty_dict)        # True (dict vacío es falsy)

# Verificar si tiene elementos
print(bool(inventory))  # True
```

---

## 9. Type Hints para Diccionarios

```python
from typing import Any

# Diccionario simple
ages: dict[str, int] = {"Alice": 25, "Bob": 30}

# Valores de múltiples tipos
config: dict[str, str | int | bool] = {
    "host": "localhost",
    "port": 8080,
    "debug": True
}

# Diccionario anidado
users: dict[str, dict[str, str | int]] = {
    "user1": {"name": "Alice", "age": 25},
    "user2": {"name": "Bob", "age": 30}
}

# Cuando los valores pueden ser cualquier cosa
flexible: dict[str, Any] = {"data": [1, 2, 3], "count": 3}
```

---

## 10. Comparación: Dict vs Otras Estructuras

| Característica | `dict` | `list` | `tuple` |
|----------------|--------|--------|---------|
| Acceso | Por clave O(1) | Por índice O(1) | Por índice O(1) |
| Búsqueda | O(1) | O(n) | O(n) |
| Mutable | ✅ | ✅ | ❌ |
| Ordenado | ✅ (3.7+) | ✅ | ✅ |
| Duplicados | Claves: ❌ | ✅ | ✅ |
| Uso memoria | Alto | Medio | Bajo |

### ¿Cuándo usar cada uno?

```python
# Lista: colección ordenada de elementos similares
scores = [85, 92, 78, 95]

# Tupla: colección inmutable de elementos relacionados
point = (10, 20)
rgb = (255, 128, 0)

# Diccionario: mapeo clave-valor, búsqueda rápida
student = {"name": "Alice", "age": 25, "grade": "A"}
phone_book = {"Alice": "555-1234", "Bob": "555-5678"}
```

---

## ✅ Resumen

| Operación | Sintaxis | Ejemplo |
|-----------|----------|---------|
| Crear vacío | `{}` o `dict()` | `d = {}` |
| Crear con datos | `{k: v, ...}` | `d = {"a": 1}` |
| Acceder | `d[key]` o `d.get(key)` | `d["a"]` |
| Agregar/Modificar | `d[key] = value` | `d["b"] = 2` |
| Eliminar | `del d[key]` o `d.pop(key)` | `del d["a"]` |
| Verificar | `key in d` | `"a" in d` |
| Longitud | `len(d)` | `len(d)` |

---

## 🔗 Navegación

← [Semana 06](../README.md) | [Métodos de Diccionarios](02-metodos-diccionarios.md) →
