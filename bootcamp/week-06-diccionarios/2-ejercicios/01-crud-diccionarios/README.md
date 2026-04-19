# Ejercicio 01: CRUD de Diccionarios

## 🎯 Objetivo

Practicar las operaciones fundamentales de diccionarios: **C**reate (Crear), **R**ead (Leer), **U**pdate (Actualizar) y **D**elete (Eliminar).

---

## 📋 Descripción

En este ejercicio aprenderás a:

1. Crear diccionarios de diferentes formas
2. Acceder a valores con `[]` y `.get()`
3. Agregar y actualizar elementos
4. Eliminar elementos con `del`, `pop()` y `clear()`
5. Verificar existencia de claves con `in`

---

## 🔧 Instrucciones

1. Abre el archivo `starter/main.py`
2. Lee cada sección y la explicación del concepto
3. **Descomenta** el código de cada paso para ejecutarlo
4. Observa los resultados y experimenta modificando valores

---

## 📚 Conceptos Cubiertos

### Paso 1: Crear Diccionarios

Existen múltiples formas de crear diccionarios:

```python
# Forma literal (más común)
person = {"name": "Alice", "age": 30}

# Constructor dict()
person = dict(name="Alice", age=30)

# Desde lista de tuplas
person = dict([("name", "Alice"), ("age", 30)])

# Diccionario vacío
empty = {}
empty = dict()
```

### Paso 2: Leer/Acceder Valores

```python
person = {"name": "Alice", "age": 30}

# Con corchetes (lanza KeyError si no existe)
name = person["name"]  # "Alice"

# Con get() (retorna None o valor por defecto)
city = person.get("city")  # None
city = person.get("city", "Unknown")  # "Unknown"
```

### Paso 3: Agregar y Actualizar

```python
person = {"name": "Alice"}

# Agregar nueva clave
person["age"] = 30

# Actualizar valor existente
person["name"] = "Alicia"

# Agregar múltiples con update()
person.update({"city": "Madrid", "country": "Spain"})
```

### Paso 4: Eliminar Elementos

```python
person = {"name": "Alice", "age": 30, "city": "Madrid"}

# del - elimina por clave
del person["city"]

# pop() - elimina y retorna valor
age = person.pop("age")

# pop() con valor por defecto
country = person.pop("country", "N/A")

# clear() - vacía todo el diccionario
person.clear()
```

### Paso 5: Verificar Existencia

```python
person = {"name": "Alice", "age": 30}

# Verificar si clave existe
if "name" in person:
    print("Tiene nombre")

# Verificar si clave NO existe
if "email" not in person:
    print("No tiene email")
```

---

## ✅ Resultado Esperado

Al descomentar todo el código, deberías ver:

```
=== PASO 1: Crear Diccionarios ===
Literal: {'name': 'Alice', 'age': 30, 'city': 'Madrid'}
Constructor: {'name': 'Bob', 'age': 25}
Desde tuplas: {'a': 1, 'b': 2, 'c': 3}
fromkeys: {'x': 0, 'y': 0, 'z': 0}

=== PASO 2: Leer/Acceder ===
Nombre: Alice
Edad: 30
País (corchetes fallaría): Unknown
Email: None

=== PASO 3: Agregar y Actualizar ===
Después de agregar email: {'name': 'Alice', 'age': 30, 'email': 'alice@example.com'}
Después de actualizar edad: {'name': 'Alice', 'age': 31, 'email': 'alice@example.com'}
Después de update(): {'name': 'Alice', 'age': 31, 'email': 'alice@example.com', 'city': 'Madrid', 'country': 'Spain'}

=== PASO 4: Eliminar ===
Después de del: {'name': 'Alice', 'age': 31, 'email': 'alice@example.com', 'country': 'Spain'}
Valor eliminado con pop: alice@example.com
Pop con default: N/A
Después de clear: {}

=== PASO 5: Verificar Existencia ===
✓ El producto tiene nombre
✗ El producto NO tiene descuento
Stock: 50
```

---

## 🔗 Navegación

- ⬅️ **Anterior**: [Dict Comprehensions](../../1-teoria/04-dict-comprehensions.md)
- ➡️ **Siguiente**: [Métodos Avanzados](../02-metodos-avanzados/README.md)
- 🏠 **Índice**: [README Semana 6](../../README.md)
