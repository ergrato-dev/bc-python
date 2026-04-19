# Dict Comprehensions

## 🎯 Objetivos

- Dominar la sintaxis de dict comprehensions
- Aplicar condiciones y transformaciones en comprehensions
- Crear diccionarios eficientemente desde otras estructuras
- Conocer cuándo usar comprehensions vs bucles tradicionales

---

## 1. ¿Qué es una Dict Comprehension?

Una **dict comprehension** es una forma concisa y pythónica de crear diccionarios a partir de iterables, aplicando transformaciones y filtros en una sola línea.

### Sintaxis Básica

```python
# Sintaxis general
# {key_expr: value_expr for item in iterable}

# Ejemplo básico: cuadrados de números
squares: dict[int, int] = {x: x ** 2 for x in range(1, 6)}
print(squares)  # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# Comparación con bucle tradicional
squares_loop: dict[int, int] = {}
for x in range(1, 6):
    squares_loop[x] = x ** 2
```

### Anatomía de una Dict Comprehension

```python
#    clave : valor   for variable in iterable
#      ↓       ↓           ↓           ↓
result = {  x  :  x**2   for   x    in  range(5)}

# Componentes:
# 1. Expresión de clave (x)
# 2. Expresión de valor (x**2)
# 3. Variable de iteración (x)
# 4. Iterable (range(5))
```

---

## 2. Creación de Diccionarios desde Listas

### 2.1 Lista a Diccionario

```python
# Lista de frutas
fruits: list[str] = ["apple", "banana", "cherry"]

# Crear diccionario con longitud de cada palabra
fruit_lengths: dict[str, int] = {fruit: len(fruit) for fruit in fruits}
print(fruit_lengths)  # {'apple': 5, 'banana': 6, 'cherry': 6}

# Crear diccionario con índice como clave
indexed_fruits: dict[int, str] = {i: fruit for i, fruit in enumerate(fruits)}
print(indexed_fruits)  # {0: 'apple', 1: 'banana', 2: 'cherry'}
```

### 2.2 Dos Listas a Diccionario

```python
# Dos listas relacionadas
keys: list[str] = ["name", "age", "city"]
values: list[str | int] = ["Alice", 30, "Madrid"]

# Crear diccionario con zip()
person: dict[str, str | int] = {k: v for k, v in zip(keys, values)}
print(person)  # {'name': 'Alice', 'age': 30, 'city': 'Madrid'}

# Alternativa más simple (sin comprehension)
person_simple = dict(zip(keys, values))
```

### 2.3 Lista de Tuplas a Diccionario

```python
# Lista de pares (clave, valor)
pairs: list[tuple[str, int]] = [
    ("python", 1991),
    ("java", 1995),
    ("javascript", 1995),
    ("rust", 2010)
]

# Convertir a diccionario
languages: dict[str, int] = {name: year for name, year in pairs}
print(languages)
# {'python': 1991, 'java': 1995, 'javascript': 1995, 'rust': 2010}
```

---

## 3. Dict Comprehensions con Condiciones

### 3.1 Filtrar con `if`

```python
# Diccionario original
scores: dict[str, int] = {
    "alice": 95,
    "bob": 67,
    "carol": 82,
    "david": 45,
    "eve": 91
}

# Filtrar solo aprobados (>= 70)
passed: dict[str, int] = {name: score for name, score in scores.items() if score >= 70}
print(passed)  # {'alice': 95, 'carol': 82, 'eve': 91}

# Filtrar por clave
vowel_students = {name: score for name, score in scores.items() if name[0] in "aeiou"}
print(vowel_students)  # {'alice': 95, 'eve': 91}
```

### 3.2 Múltiples Condiciones

```python
products: dict[str, dict[str, float | int]] = {
    "laptop": {"price": 999.99, "stock": 50},
    "mouse": {"price": 29.99, "stock": 0},
    "keyboard": {"price": 79.99, "stock": 30},
    "monitor": {"price": 299.99, "stock": 5}
}

# Productos disponibles (stock > 0) y baratos (price < 100)
available_cheap: dict[str, dict[str, float | int]] = {
    name: info
    for name, info in products.items()
    if info["stock"] > 0 and info["price"] < 100
}
print(available_cheap)  # {'keyboard': {'price': 79.99, 'stock': 30}}
```

### 3.3 Condicional en Valor (`if-else`)

```python
scores: dict[str, int] = {"alice": 95, "bob": 67, "carol": 82}

# Asignar calificación basada en puntuación
# Nota: el if-else va en la expresión de valor, NO al final
grades: dict[str, str] = {
    name: ("A" if score >= 90 else "B" if score >= 80 else "C" if score >= 70 else "F")
    for name, score in scores.items()
}
print(grades)  # {'alice': 'A', 'bob': 'F', 'carol': 'B'}
```

---

## 4. Transformaciones en Dict Comprehensions

### 4.1 Transformar Claves

```python
# Diccionario con claves en diferentes formatos
data: dict[str, str] = {
    "First Name": "John",
    "Last Name": "Doe",
    "Email Address": "john@example.com"
}

# Convertir claves a snake_case
normalized: dict[str, str] = {
    key.lower().replace(" ", "_"): value
    for key, value in data.items()
}
print(normalized)
# {'first_name': 'John', 'last_name': 'Doe', 'email_address': 'john@example.com'}
```

### 4.2 Transformar Valores

```python
# Precios en dólares
prices_usd: dict[str, float] = {
    "laptop": 999.99,
    "mouse": 29.99,
    "keyboard": 79.99
}

# Convertir a euros
exchange_rate: float = 0.85
prices_eur: dict[str, float] = {
    product: round(price * exchange_rate, 2)
    for product, price in prices_usd.items()
}
print(prices_eur)  # {'laptop': 849.99, 'mouse': 25.49, 'keyboard': 67.99}
```

### 4.3 Transformar Ambos

```python
# Datos de usuarios
users: dict[int, str] = {
    1: "alice",
    2: "bob",
    3: "carol"
}

# Invertir y capitalizar
name_to_id: dict[str, int] = {
    name.capitalize(): user_id
    for user_id, name in users.items()
}
print(name_to_id)  # {'Alice': 1, 'Bob': 2, 'Carol': 3}
```

---

## 5. Invertir Diccionarios

### 5.1 Inversión Simple

```python
# Diccionario código -> país
country_codes: dict[str, str] = {
    "US": "United States",
    "GB": "United Kingdom",
    "ES": "Spain"
}

# Invertir: país -> código
code_lookup: dict[str, str] = {country: code for code, country in country_codes.items()}
print(code_lookup)
# {'United States': 'US', 'United Kingdom': 'GB', 'Spain': 'ES'}
```

### 5.2 Inversión con Valores Duplicados

⚠️ Si hay valores duplicados, algunos se pierden:

```python
# Diccionario con valores duplicados
grades: dict[str, str] = {
    "alice": "A",
    "bob": "B",
    "carol": "A",
    "david": "B"
}

# Inversión simple (pierde datos)
grade_to_student: dict[str, str] = {grade: name for name, grade in grades.items()}
print(grade_to_student)  # {'A': 'carol', 'B': 'david'} - ¡alice y bob perdidos!

# Solución: agrupar en listas
from collections import defaultdict

grade_groups: dict[str, list[str]] = {}
for name, grade in grades.items():
    if grade not in grade_groups:
        grade_groups[grade] = []
    grade_groups[grade].append(name)

print(grade_groups)  # {'A': ['alice', 'carol'], 'B': ['bob', 'david']}
```

---

## 6. Dict Comprehensions Anidadas

### 6.1 Crear Estructura Anidada

```python
# Crear tabla de multiplicar
multiplication_table: dict[int, dict[int, int]] = {
    x: {y: x * y for y in range(1, 6)}
    for x in range(1, 6)
}

# Acceder: multiplication_table[3][4] = 12
print(f"3 x 4 = {multiplication_table[3][4]}")

# Mostrar tabla
for x, row in multiplication_table.items():
    print(f"{x}: {row}")
# 1: {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}
# 2: {1: 2, 2: 4, 3: 6, 4: 8, 5: 10}
# ...
```

### 6.2 Aplanar Estructura Anidada

```python
# Estructura anidada
nested: dict[str, dict[str, int]] = {
    "group_a": {"alice": 95, "bob": 87},
    "group_b": {"carol": 92, "david": 78}
}

# Aplanar a diccionario simple
flattened: dict[str, int] = {
    name: score
    for group in nested.values()
    for name, score in group.items()
}
print(flattened)  # {'alice': 95, 'bob': 87, 'carol': 92, 'david': 78}

# Con información del grupo
flattened_with_group: dict[str, tuple[str, int]] = {
    name: (group_name, score)
    for group_name, members in nested.items()
    for name, score in members.items()
}
print(flattened_with_group)
# {'alice': ('group_a', 95), 'bob': ('group_a', 87), ...}
```

---

## 7. Casos de Uso Prácticos

### 7.1 Contar Ocurrencias

```python
# Contar caracteres en una palabra
text: str = "mississippi"

# Con dict comprehension y count()
char_count: dict[str, int] = {char: text.count(char) for char in set(text)}
print(char_count)  # {'m': 1, 'i': 4, 's': 4, 'p': 2}

# Más eficiente con bucle (evita múltiples pasadas)
char_count_efficient: dict[str, int] = {}
for char in text:
    char_count_efficient[char] = char_count_efficient.get(char, 0) + 1
```

### 7.2 Extraer Campos Específicos

```python
# Lista de usuarios con muchos campos
users: list[dict[str, str | int]] = [
    {"id": 1, "name": "Alice", "email": "alice@example.com", "age": 30},
    {"id": 2, "name": "Bob", "email": "bob@example.com", "age": 25},
    {"id": 3, "name": "Carol", "email": "carol@example.com", "age": 35}
]

# Crear diccionario id -> nombre
id_to_name: dict[int, str] = {user["id"]: user["name"] for user in users}
print(id_to_name)  # {1: 'Alice', 2: 'Bob', 3: 'Carol'}

# Crear diccionario email -> usuario completo
email_lookup: dict[str, dict[str, str | int]] = {
    user["email"]: user for user in users
}
```

### 7.3 Mapear Valores con Diccionario de Traducción

```python
# Traducción de códigos
status_codes: dict[int, str] = {
    200: "OK",
    404: "Not Found",
    500: "Server Error"
}

# Lista de respuestas
responses: list[int] = [200, 404, 200, 500, 200]

# Contar respuestas con nombres descriptivos
response_counts: dict[str, int] = {
    status_codes.get(code, "Unknown"): responses.count(code)
    for code in set(responses)
}
print(response_counts)  # {'OK': 3, 'Not Found': 1, 'Server Error': 1}
```

### 7.4 Crear Diccionario de Configuración

```python
# Variables de entorno simuladas
env_vars: list[str] = [
    "DATABASE_HOST=localhost",
    "DATABASE_PORT=5432",
    "DEBUG=true",
    "API_KEY=secret123"
]

# Parsear a diccionario
config: dict[str, str] = {
    line.split("=")[0]: line.split("=")[1]
    for line in env_vars
    if "=" in line
}
print(config)
# {'DATABASE_HOST': 'localhost', 'DATABASE_PORT': '5432', 'DEBUG': 'true', 'API_KEY': 'secret123'}

# Versión más robusta
def parse_env(lines: list[str]) -> dict[str, str]:
    """Parsea líneas de configuración a diccionario."""
    result: dict[str, str] = {}
    for line in lines:
        if "=" in line:
            key, _, value = line.partition("=")
            result[key.strip()] = value.strip()
    return result
```

---

## 8. Comparación: Comprehension vs Bucle

### 8.1 Cuándo Usar Comprehensions ✅

```python
# ✅ Transformación simple
prices = {name: price * 1.1 for name, price in original_prices.items()}

# ✅ Filtrado simple
adults = {name: age for name, age in people.items() if age >= 18}

# ✅ Crear diccionario desde otra estructura
lookup = {item.id: item for item in items_list}
```

### 8.2 Cuándo Usar Bucles ❌

```python
# ❌ NO usar comprehension si es muy compleja
# Difícil de leer:
result = {k: v1 if cond1 else v2 if cond2 else v3 for k, v in data.items() if filter_cond}

# ✅ Mejor con bucle:
result: dict[str, int] = {}
for k, v in data.items():
    if not filter_cond:
        continue
    if cond1:
        result[k] = v1
    elif cond2:
        result[k] = v2
    else:
        result[k] = v3

# ❌ NO usar comprehension con efectos secundarios
# Incorrecto (abusa de la comprehension):
{print(k): v for k, v in data.items()}

# ✅ Mejor con bucle:
for k, v in data.items():
    print(k)
```

### 8.3 Rendimiento

```python
# Las comprehensions suelen ser más rápidas que los bucles equivalentes
# debido a optimizaciones internas de Python

# Sin embargo, la diferencia es mínima en la mayoría de casos
# Prioriza LEGIBILIDAD sobre micro-optimizaciones
```

---

## 9. Errores Comunes

### 9.1 Olvidar los Dos Puntos

```python
# ❌ Error de sintaxis
# wrong = {x for x in range(5)}  # Esto es un SET, no un dict

# ✅ Correcto
correct: dict[int, int] = {x: x for x in range(5)}
```

### 9.2 Condición en Lugar Incorrecto

```python
scores = {"alice": 95, "bob": 67, "carol": 82}

# ❌ Filtro con if-else (no funciona así)
# wrong = {name: score for name, score in scores.items() if score >= 70 else 0}

# ✅ Filtro (al final, solo if)
filtered = {name: score for name, score in scores.items() if score >= 70}

# ✅ Transformación condicional (antes del for, usa if-else)
transformed = {name: (score if score >= 70 else 0) for name, score in scores.items()}
```

### 9.3 Claves Duplicadas

```python
# Las claves duplicadas se sobrescriben (la última gana)
items = [("a", 1), ("b", 2), ("a", 3)]

result = {k: v for k, v in items}
print(result)  # {'a': 3, 'b': 2} - El primer "a" se perdió
```

---

## 10. Resumen Visual

```
╔═══════════════════════════════════════════════════════════════════╗
║                    DICT COMPREHENSION                             ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  SINTAXIS BÁSICA:                                                 ║
║  {key_expr: value_expr for item in iterable}                      ║
║                                                                   ║
║  CON FILTRO:                                                      ║
║  {key: value for item in iterable if condition}                   ║
║                                                                   ║
║  CON TRANSFORMACIÓN CONDICIONAL:                                  ║
║  {key: (val1 if cond else val2) for item in iterable}             ║
║                                                                   ║
║  ANIDADA:                                                         ║
║  {k: {inner_k: inner_v for ...} for ...}                          ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
```

---

## ✅ Checklist de Verificación

Antes de continuar, asegúrate de poder:

- [ ] Escribir dict comprehensions básicas
- [ ] Crear diccionarios desde listas y tuplas
- [ ] Aplicar filtros con `if`
- [ ] Usar transformaciones condicionales con `if-else`
- [ ] Transformar claves y valores
- [ ] Invertir diccionarios
- [ ] Crear y aplanar estructuras anidadas
- [ ] Decidir cuándo usar comprehension vs bucle

---

## 🔗 Navegación

- ⬅️ **Anterior**: [Iteración sobre Diccionarios](03-iteracion-diccionarios.md)
- ➡️ **Siguiente**: [Ejercicios - CRUD de Diccionarios](../2-ejercicios/01-crud-diccionarios/README.md)
- 🏠 **Índice**: [README](../README.md)
