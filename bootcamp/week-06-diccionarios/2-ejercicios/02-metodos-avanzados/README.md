# Ejercicio 02: Métodos Avanzados de Diccionarios

## 🎯 Objetivo

Dominar los métodos más útiles de diccionarios: `keys()`, `values()`, `items()`, `setdefault()`, `update()` y técnicas de copia.

---

## 📋 Descripción

En este ejercicio aprenderás a:

1. Obtener vistas de claves, valores e items
2. Usar `setdefault()` para valores por defecto
3. Combinar diccionarios con `update()` y el operador `|`
4. Diferenciar copia superficial de copia profunda
5. Aplicar `popitem()` para eliminar el último elemento

---

## 🔧 Instrucciones

1. Abre el archivo `starter/main.py`
2. Lee cada sección y la explicación del concepto
3. **Descomenta** el código de cada paso para ejecutarlo
4. Observa los resultados y experimenta modificando valores

---

## 📚 Conceptos Cubiertos

### Paso 1: Vistas - keys(), values(), items()

Las vistas son objetos dinámicos que reflejan el estado actual del diccionario:

```python
data = {"a": 1, "b": 2}

keys = data.keys()      # dict_keys(['a', 'b'])
values = data.values()  # dict_values([1, 2])
items = data.items()    # dict_items([('a', 1), ('b', 2)])

# Las vistas se actualizan automáticamente
data["c"] = 3
print(keys)  # dict_keys(['a', 'b', 'c'])
```

### Paso 2: setdefault()

Obtiene un valor si existe, o lo crea con un valor por defecto:

```python
data = {"name": "Alice"}

# Si existe, retorna el valor actual
name = data.setdefault("name", "Unknown")  # "Alice"

# Si no existe, lo crea y retorna el valor por defecto
age = data.setdefault("age", 0)  # 0
print(data)  # {"name": "Alice", "age": 0}
```

### Paso 3: Combinar Diccionarios

```python
dict1 = {"a": 1, "b": 2}
dict2 = {"b": 3, "c": 4}

# update() modifica el diccionario original
dict1.update(dict2)  # dict1 = {"a": 1, "b": 3, "c": 4}

# Operador | (Python 3.9+) crea nuevo diccionario
merged = dict1 | dict2  # {"a": 1, "b": 3, "c": 4}

# Operador |= actualiza in-place
dict1 |= dict2
```

### Paso 4: Copias de Diccionarios

```python
import copy

original = {"user": {"name": "Alice"}}

# Copia superficial (shallow) - objetos internos compartidos
shallow = original.copy()
shallow["user"]["name"] = "Bob"  # ¡Modifica también original!

# Copia profunda (deep) - totalmente independiente
deep = copy.deepcopy(original)
deep["user"]["name"] = "Carol"  # No afecta original
```

### Paso 5: popitem()

Elimina y retorna el último par clave-valor insertado:

```python
data = {"a": 1, "b": 2, "c": 3}

last = data.popitem()  # ("c", 3)
print(data)  # {"a": 1, "b": 2}
```

---

## ✅ Resultado Esperado

Al descomentar todo el código, deberías ver:

```
=== PASO 1: Vistas ===
Claves: dict_keys(['name', 'age', 'city'])
Valores: dict_values(['Alice', 30, 'Madrid'])
Items: dict_items([('name', 'Alice'), ('age', 30), ('city', 'Madrid')])
Lista de claves: ['name', 'age', 'city']
Después de agregar: dict_keys(['name', 'age', 'city', 'country'])

=== PASO 2: setdefault() ===
Nombre existente: Alice
Edad creada: 0
Diccionario actualizado: {'name': 'Alice', 'age': 0}
Conteo de palabras: {'hello': 2, 'world': 1, 'python': 1}

=== PASO 3: Combinar Diccionarios ===
Defaults: {'theme': 'dark', 'lang': 'en', 'font_size': 12}
User settings: {'theme': 'light', 'font_size': 14}
Merged (|): {'theme': 'light', 'lang': 'en', 'font_size': 14}
Después de |=: {'theme': 'light', 'lang': 'en', 'font_size': 14}

=== PASO 4: Copias ===
Original: {'config': {'debug': True}}
Shallow modificado debug: {'config': {'debug': False}}
¿Original afectado? {'config': {'debug': False}}
Después de deepcopy y modificar: Original={'config': {'debug': False}}, Deep={'config': {'debug': True}}

=== PASO 5: popitem() ===
Procesando: ('task3', 'Send email') - ✓
Procesando: ('task2', 'Review code') - ✓
Procesando: ('task1', 'Write tests') - ✓
Cola vacía: {}
```

---

## 🔗 Navegación

- ⬅️ **Anterior**: [CRUD de Diccionarios](../01-crud-diccionarios/README.md)
- ➡️ **Siguiente**: [Diccionarios Anidados](../03-diccionarios-anidados/README.md)
- 🏠 **Índice**: [README Semana 6](../../README.md)
