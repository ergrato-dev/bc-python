# 🔮 Truthiness y Falsiness

## 🎯 Objetivos

- Comprender qué valores son "truthy" y "falsy" en Python
- Aplicar truthiness en condicionales de forma pythónica
- Usar evaluación de cortocircuito efectivamente
- Evitar errores comunes con valores falsy

---

## 📋 Contenido

### 1. ¿Qué es Truthiness y Falsiness?

En Python, **cualquier valor** puede ser evaluado como `True` o `False` en un contexto booleano.

- **Truthy**: Valores que se evalúan como `True`
- **Falsy**: Valores que se evalúan como `False`

```python
# Python convierte valores a booleanos implícitamente
if "hello":  # Un string no vacío es truthy
    print("Este string es truthy")

if [1, 2, 3]:  # Una lista no vacía es truthy
    print("Esta lista es truthy")

if 0:  # Cero es falsy
    print("Esto no se imprime")
else:
    print("Cero es falsy")
```

---

### 2. Valores Falsy en Python

Los siguientes valores se evalúan como `False`:

| Valor | Tipo | Descripción |
|-------|------|-------------|
| `False` | bool | El booleano False |
| `None` | NoneType | Ausencia de valor |
| `0` | int | Cero entero |
| `0.0` | float | Cero flotante |
| `0j` | complex | Cero complejo |
| `""` | str | String vacío |
| `[]` | list | Lista vacía |
| `()` | tuple | Tupla vacía |
| `{}` | dict | Diccionario vacío |
| `set()` | set | Set vacío |
| `range(0)` | range | Rango vacío |

```python
# Demostración de valores falsy
falsy_values = [False, None, 0, 0.0, "", [], (), {}, set()]

for value in falsy_values:
    if not value:
        print(f"{repr(value):12} es falsy")

# Output:
# False        es falsy
# None         es falsy
# 0            es falsy
# 0.0          es falsy
# ''           es falsy
# []           es falsy
# ()           es falsy
# {}           es falsy
# set()        es falsy
```

---

### 3. Valores Truthy

**Todo lo demás** es truthy:

```python
truthy_values = [
    True,           # bool
    1,              # int no-cero
    -1,             # negativos también
    3.14,           # float no-cero
    "hello",        # string no vacío
    " ",            # string con espacio (¡no está vacío!)
    [0],            # lista con elementos (aunque sea 0)
    {"a": 1},       # diccionario con elementos
    object(),       # cualquier objeto
]

for value in truthy_values:
    if value:
        print(f"{repr(value):20} es truthy")
```

> ⚠️ **Cuidado**: `" "` (string con espacio) es truthy, `""` es falsy.

---

### 4. La Función `bool()`

Puedes convertir explícitamente cualquier valor a booleano:

```python
# Conversión explícita
print(bool(0))        # False
print(bool(42))       # True
print(bool(""))       # False
print(bool("False"))  # True! El string "False" no está vacío
print(bool([]))       # False
print(bool([False]))  # True! La lista tiene un elemento
```

---

### 5. Uso Pythónico de Truthiness

#### Verificar si una lista tiene elementos

```python
items: list[str] = get_items()

# ❌ Forma no pythónica
if len(items) > 0:
    process(items)

# ✅ Forma pythónica
if items:
    process(items)
```

#### Verificar si un string tiene contenido

```python
name: str = get_name()

# ❌ Forma no pythónica
if name != "":
    print(f"Hola, {name}")

# ✅ Forma pythónica
if name:
    print(f"Hola, {name}")
```

#### Verificar None

```python
data: dict | None = get_data()

# ❌ No distingue entre None y otros falsy
if data:  # También es False si data = {}
    process(data)

# ✅ Explícito para None
if data is not None:
    process(data)
```

---

### 6. Evaluación de Cortocircuito con Truthiness

#### Operador `or` para Valores por Defecto

```python
# or retorna el primer valor truthy o el último
name: str = user_input or "Anonymous"

# Equivalente a:
# if user_input:
#     name = user_input
# else:
#     name = "Anonymous"

# Ejemplos
print("" or "default")        # "default"
print("Alice" or "default")   # "Alice"
print(None or "fallback")     # "fallback"
print(0 or 100)               # 100 - ¡cuidado!
```

> ⚠️ **Cuidado con `0` y `""`**: Son falsy pero pueden ser valores válidos.

```python
# Problema
count: int = 0  # 0 es un valor válido
result = count or 10  # result = 10, ¡pero queríamos 0!

# Solución: usar operador ternario o condicional explícito
result = count if count is not None else 10
```

#### Operador `and` para Validación

```python
# and retorna el primer valor falsy o el último
user = {"name": "Alice", "age": 25}

# Acceso seguro a propiedades anidadas
name = user and user.get("name")
print(name)  # "Alice"

# Si user es None
user = None
name = user and user.get("name")  # No falla
print(name)  # None (cortocircuito evita el error)
```

---

### 7. Asignación Condicional Moderna (Python 3.8+)

El operador walrus (`:=`) combinado con truthiness:

```python
# Antes de Python 3.8
line = file.readline()
while line:
    process(line)
    line = file.readline()

# Con walrus operator
while (line := file.readline()):
    process(line)

# En condicionales
if (result := expensive_function()) is not None:
    use(result)
```

---

### 8. Custom Truthiness en Clases

Puedes definir el comportamiento de truthiness en tus propias clases:

```python
class Inventory:
    def __init__(self, items: list[str] | None = None):
        self.items = items or []

    def __bool__(self) -> bool:
        """Define cuándo el inventario es truthy."""
        return len(self.items) > 0

    def __len__(self) -> int:
        """Permite usar len() y también afecta truthiness."""
        return len(self.items)

# Uso
empty_inventory = Inventory()
full_inventory = Inventory(["sword", "shield"])

if empty_inventory:
    print("Tienes items")
else:
    print("Inventario vacío")  # Se imprime

if full_inventory:
    print("Tienes items")  # Se imprime
```

---

### 9. Errores Comunes

```python
# ❌ Error 1: Comparar con True/False
if is_valid == True:   # Redundante
if is_valid == False:  # Redundante

# ✅ Correcto
if is_valid:
if not is_valid:

# ❌ Error 2: No considerar 0 como valor válido
score = user_score or 100  # Si user_score es 0, usará 100

# ✅ Correcto
score = user_score if user_score is not None else 100

# ❌ Error 3: Confundir falsiness con None
data = []
if data is None:  # False - data es [], no None
    print("No data")
if not data:      # True - [] es falsy
    print("Empty data")

# ❌ Error 4: El string "False" es truthy
config = "False"
if config:  # True! "False" es un string no vacío
    print("Esto se imprime")

# ✅ Correcto
config = False  # El booleano, no el string
if config:
    print("Esto NO se imprime")
```

---

## 🧪 Ejercicio Rápido

¿Qué imprime cada línea?

```python
# Predice antes de ejecutar
print(bool([0, 0, 0]))
print(bool([]))
print(bool("0"))
print(bool(0))
print("" or "a" or "b")
print("x" and "y" and "z")
print(0 and "hello")
print("" and "hello")
print(None or 0 or "" or [] or "finally!")
```

<details>
<summary>Ver respuestas</summary>

```python
print(bool([0, 0, 0]))  # True - lista NO vacía
print(bool([]))         # False - lista vacía
print(bool("0"))        # True - string NO vacío
print(bool(0))          # False - cero
print("" or "a" or "b") # "a" - primer truthy
print("x" and "y" and "z")  # "z" - último (todos truthy)
print(0 and "hello")    # 0 - primer falsy
print("" and "hello")   # "" - primer falsy
print(None or 0 or "" or [] or "finally!")  # "finally!" - primer truthy
```

</details>

---

## 📚 Recursos Adicionales

- [Truth Value Testing - Python Docs](https://docs.python.org/3/library/stdtypes.html#truth-value-testing)
- [Truthy and Falsy - Real Python](https://realpython.com/python-boolean/)

---

## ✅ Checklist de Verificación

- [ ] Conozco todos los valores falsy en Python
- [ ] Uso truthiness de forma pythónica (`if items:` en lugar de `if len(items) > 0:`)
- [ ] Sé distinguir entre `if data:` y `if data is not None:`
- [ ] Entiendo cómo `or` y `and` retornan valores (no solo booleanos)
- [ ] Evito el error de `"False"` (string) vs `False` (bool)
- [ ] Sé que `0` y `""` son falsy pero pueden ser valores válidos
