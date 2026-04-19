# Iteración sobre Diccionarios

## 🎯 Objetivos

- Dominar las diferentes formas de iterar sobre diccionarios
- Comprender cuándo usar `keys()`, `values()` o `items()`
- Aplicar técnicas avanzadas de iteración con `enumerate()` y `zip()`
- Filtrar y transformar diccionarios durante la iteración

---

## 1. Formas Básicas de Iteración

Python ofrece múltiples formas de recorrer un diccionario, cada una con su propósito específico.

### 1.1 Iteración por Defecto (Claves)

Por defecto, iterar sobre un diccionario recorre sus **claves**:

```python
# Diccionario de ejemplo
scores: dict[str, int] = {
    "alice": 95,
    "bob": 87,
    "carol": 92
}

# Iteración por defecto: recorre las claves
for name in scores:
    print(f"Estudiante: {name}")

# Output:
# Estudiante: alice
# Estudiante: bob
# Estudiante: carol

# Equivalente explícito con keys()
for name in scores.keys():
    print(f"Estudiante: {name}")
```

### 1.2 Iteración sobre Valores

Usa `values()` cuando solo necesites los valores:

```python
scores: dict[str, int] = {"alice": 95, "bob": 87, "carol": 92}

# Calcular promedio
total: int = 0
for score in scores.values():
    total += score

average: float = total / len(scores)
print(f"Promedio: {average:.2f}")  # Promedio: 91.33

# Forma más pythónica con sum()
average = sum(scores.values()) / len(scores)
```

### 1.3 Iteración sobre Pares Clave-Valor

Usa `items()` cuando necesites ambos (la forma más común):

```python
scores: dict[str, int] = {"alice": 95, "bob": 87, "carol": 92}

# Desempaquetado de tuplas en el for
for name, score in scores.items():
    status = "Aprobado" if score >= 90 else "Regular"
    print(f"{name}: {score} - {status}")

# Output:
# alice: 95 - Aprobado
# bob: 87 - Regular
# carol: 92 - Aprobado
```

---

## 2. Comparación de Métodos de Iteración

| Método | Retorna | Uso Principal |
|--------|---------|---------------|
| `for k in dict` | Claves | Solo necesitas las claves |
| `for k in dict.keys()` | Claves (explícito) | Claridad de código |
| `for v in dict.values()` | Valores | Solo necesitas los valores |
| `for k, v in dict.items()` | Tuplas (k, v) | Necesitas ambos |

```python
config: dict[str, str] = {
    "host": "localhost",
    "port": "8080",
    "debug": "true"
}

# ¿Cuándo usar cada uno?

# 1. Solo verificar si existe una clave
for key in config:
    if key.startswith("d"):
        print(f"Configuración encontrada: {key}")

# 2. Solo procesar valores
for value in config.values():
    print(f"Valor: {value.upper()}")

# 3. Procesar ambos (más común)
for key, value in config.items():
    print(f"{key}={value}")
```

---

## 3. Iteración con `enumerate()`

`enumerate()` añade un índice al iterar:

```python
products: dict[str, float] = {
    "laptop": 999.99,
    "mouse": 29.99,
    "keyboard": 79.99,
    "monitor": 299.99
}

# Enumerar items con índice
print("Lista de productos:")
for index, (name, price) in enumerate(products.items(), start=1):
    print(f"{index}. {name}: ${price:.2f}")

# Output:
# Lista de productos:
# 1. laptop: $999.99
# 2. mouse: $29.99
# 3. keyboard: $79.99
# 4. monitor: $299.99

# Útil para crear menús numerados
def show_menu(options: dict[str, str]) -> None:
    """Muestra un menú numerado."""
    print("\n--- Menú ---")
    for num, (code, description) in enumerate(options.items(), start=1):
        print(f"{num}. [{code}] {description}")

menu_options: dict[str, str] = {
    "N": "Nuevo archivo",
    "A": "Abrir archivo",
    "G": "Guardar",
    "S": "Salir"
}

show_menu(menu_options)
```

---

## 4. Iteración con `zip()`

`zip()` permite iterar sobre múltiples iterables en paralelo:

```python
# Crear diccionario desde dos listas
names: list[str] = ["alice", "bob", "carol"]
scores: list[int] = [95, 87, 92]

# Forma clásica con zip
student_scores: dict[str, int] = {}
for name, score in zip(names, scores):
    student_scores[name] = score

print(student_scores)  # {'alice': 95, 'bob': 87, 'carol': 92}

# Forma pythónica con dict()
student_scores = dict(zip(names, scores))

# zip con tres listas
names = ["alice", "bob"]
math_scores = [95, 87]
english_scores = [88, 92]

for name, math, english in zip(names, math_scores, english_scores):
    average = (math + english) / 2
    print(f"{name}: Math={math}, English={english}, Avg={average}")
```

### 4.1 `zip()` con `strict=True` (Python 3.10+)

```python
# zip() por defecto se detiene en el iterable más corto
names: list[str] = ["alice", "bob", "carol"]
scores: list[int] = [95, 87]  # Falta uno

# Esto NO da error, simplemente ignora "carol"
for name, score in zip(names, scores):
    print(f"{name}: {score}")
# Output: alice: 95, bob: 87 (carol ignorado)

# Con strict=True se detecta el error
try:
    for name, score in zip(names, scores, strict=True):
        print(f"{name}: {score}")
except ValueError as e:
    print(f"Error: {e}")  # Error: zip() argument 2 is shorter than argument 1
```

---

## 5. Filtrado Durante la Iteración

### 5.1 Filtrar con Condicionales

```python
products: dict[str, float] = {
    "laptop": 999.99,
    "mouse": 29.99,
    "keyboard": 79.99,
    "monitor": 299.99,
    "usb_cable": 9.99
}

# Filtrar productos caros (> $100)
expensive: dict[str, float] = {}
for name, price in products.items():
    if price > 100:
        expensive[name] = price

print(expensive)  # {'laptop': 999.99, 'monitor': 299.99}

# Forma pythónica con dict comprehension
expensive = {name: price for name, price in products.items() if price > 100}
```

### 5.2 Filtrar por Clave

```python
config: dict[str, str] = {
    "db_host": "localhost",
    "db_port": "5432",
    "db_name": "myapp",
    "cache_host": "redis",
    "cache_port": "6379"
}

# Extraer solo configuración de base de datos
db_config: dict[str, str] = {}
for key, value in config.items():
    if key.startswith("db_"):
        # Remover prefijo "db_" de la clave
        clean_key = key.replace("db_", "")
        db_config[clean_key] = value

print(db_config)  # {'host': 'localhost', 'port': '5432', 'name': 'myapp'}
```

### 5.3 Filtrar por Valor

```python
grades: dict[str, str] = {
    "alice": "A",
    "bob": "C",
    "carol": "A",
    "david": "B",
    "eve": "A"
}

# Encontrar estudiantes con A
top_students: list[str] = []
for student, grade in grades.items():
    if grade == "A":
        top_students.append(student)

print(f"Estudiantes con A: {top_students}")  # ['alice', 'carol', 'eve']

# Forma pythónica
top_students = [student for student, grade in grades.items() if grade == "A"]
```

---

## 6. Transformación Durante la Iteración

### 6.1 Transformar Valores

```python
prices_usd: dict[str, float] = {
    "laptop": 999.99,
    "mouse": 29.99,
    "keyboard": 79.99
}

# Convertir a euros (tasa: 0.85)
exchange_rate: float = 0.85
prices_eur: dict[str, float] = {}

for product, price_usd in prices_usd.items():
    prices_eur[product] = round(price_usd * exchange_rate, 2)

print(prices_eur)  # {'laptop': 849.99, 'mouse': 25.49, 'keyboard': 67.99}
```

### 6.2 Transformar Claves

```python
user_data: dict[str, str] = {
    "firstName": "John",
    "lastName": "Doe",
    "emailAddress": "john@example.com"
}

# Convertir camelCase a snake_case
def to_snake_case(name: str) -> str:
    """Convierte camelCase a snake_case."""
    result: list[str] = []
    for char in name:
        if char.isupper():
            result.append("_")
            result.append(char.lower())
        else:
            result.append(char)
    return "".join(result)

user_data_snake: dict[str, str] = {}
for key, value in user_data.items():
    new_key = to_snake_case(key)
    user_data_snake[new_key] = value

print(user_data_snake)
# {'first_name': 'John', 'last_name': 'Doe', 'email_address': 'john@example.com'}
```

### 6.3 Invertir Diccionario (Swap Keys-Values)

```python
country_codes: dict[str, str] = {
    "US": "United States",
    "GB": "United Kingdom",
    "ES": "Spain",
    "MX": "Mexico"
}

# Invertir: valores como claves, claves como valores
code_lookup: dict[str, str] = {}
for code, name in country_codes.items():
    code_lookup[name] = code

print(code_lookup)
# {'United States': 'US', 'United Kingdom': 'GB', 'Spain': 'ES', 'Mexico': 'MX'}

# Forma pythónica
code_lookup = {name: code for code, name in country_codes.items()}
```

---

## 7. Iteración Segura (Evitar Modificaciones)

⚠️ **Nunca modifiques un diccionario mientras lo iteras directamente**:

```python
scores: dict[str, int] = {"alice": 95, "bob": 45, "carol": 92, "david": 38}

# ❌ INCORRECTO - RuntimeError: dictionary changed size during iteration
# for name, score in scores.items():
#     if score < 50:
#         del scores[name]

# ✅ CORRECTO - Crear lista de claves a eliminar
to_remove: list[str] = []
for name, score in scores.items():
    if score < 50:
        to_remove.append(name)

for name in to_remove:
    del scores[name]

print(scores)  # {'alice': 95, 'carol': 92}

# ✅ ALTERNATIVA - Crear nuevo diccionario
scores = {"alice": 95, "bob": 45, "carol": 92, "david": 38}
passing_scores = {name: score for name, score in scores.items() if score >= 50}
print(passing_scores)  # {'alice': 95, 'carol': 92}

# ✅ ALTERNATIVA - Iterar sobre copia de keys()
scores = {"alice": 95, "bob": 45, "carol": 92, "david": 38}
for name in list(scores.keys()):  # list() crea una copia
    if scores[name] < 50:
        del scores[name]

print(scores)  # {'alice': 95, 'carol': 92}
```

---

## 8. Orden de Iteración

Desde Python 3.7+, los diccionarios **mantienen el orden de inserción**:

```python
# El orden de iteración es predecible
ordered: dict[str, int] = {}
ordered["first"] = 1
ordered["second"] = 2
ordered["third"] = 3

for key in ordered:
    print(key, end=" ")  # first second third

# Iterar en orden específico
scores: dict[str, int] = {"bob": 87, "alice": 95, "carol": 92}

# Orden alfabético por clave
print("\nOrden alfabético:")
for name in sorted(scores.keys()):
    print(f"{name}: {scores[name]}")

# Orden por valor (menor a mayor)
print("\nOrden por puntuación:")
for name, score in sorted(scores.items(), key=lambda x: x[1]):
    print(f"{name}: {score}")

# Orden por valor (mayor a menor)
print("\nTop scores:")
for name, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
    print(f"{name}: {score}")
```

---

## 9. Iteración sobre Diccionarios Anidados

```python
# Estructura anidada: departamento -> empleados -> datos
company: dict[str, dict[str, dict[str, str | int]]] = {
    "engineering": {
        "alice": {"role": "senior", "years": 5},
        "bob": {"role": "junior", "years": 1}
    },
    "marketing": {
        "carol": {"role": "manager", "years": 8},
        "david": {"role": "analyst", "years": 2}
    }
}

# Iterar sobre estructura anidada
for department, employees in company.items():
    print(f"\n📁 Departamento: {department.upper()}")
    for name, info in employees.items():
        print(f"  👤 {name}: {info['role']} ({info['years']} años)")

# Output:
# 📁 Departamento: ENGINEERING
#   👤 alice: senior (5 años)
#   👤 bob: junior (1 años)
# 📁 Departamento: MARKETING
#   👤 carol: manager (8 años)
#   👤 david: analyst (2 años)

# Buscar empleados con más de 3 años
experienced: list[str] = []
for department, employees in company.items():
    for name, info in employees.items():
        if info["years"] > 3:
            experienced.append(f"{name} ({department})")

print(f"\nExperimentados: {experienced}")  # ['alice (engineering)', 'carol (marketing)']
```

---

## 10. Ejemplo Práctico: Análisis de Datos

```python
# Ventas por producto y región
sales: dict[str, dict[str, int]] = {
    "laptop": {"north": 150, "south": 120, "east": 90, "west": 180},
    "mouse": {"north": 500, "south": 450, "east": 380, "west": 520},
    "keyboard": {"north": 200, "south": 180, "east": 150, "west": 220}
}

def analyze_sales(data: dict[str, dict[str, int]]) -> None:
    """Analiza datos de ventas por producto y región."""

    print("=" * 50)
    print("📊 ANÁLISIS DE VENTAS")
    print("=" * 50)

    # Total por producto
    print("\n📦 Ventas por Producto:")
    product_totals: dict[str, int] = {}
    for product, regions in data.items():
        total = sum(regions.values())
        product_totals[product] = total
        print(f"  {product}: {total} unidades")

    # Total por región
    print("\n🌍 Ventas por Región:")
    region_totals: dict[str, int] = {}
    for product, regions in data.items():
        for region, amount in regions.items():
            region_totals[region] = region_totals.get(region, 0) + amount

    for region, total in sorted(region_totals.items(), key=lambda x: x[1], reverse=True):
        print(f"  {region}: {total} unidades")

    # Mejor combinación producto-región
    print("\n🏆 Top 3 combinaciones:")
    combinations: list[tuple[str, str, int]] = []
    for product, regions in data.items():
        for region, amount in regions.items():
            combinations.append((product, region, amount))

    for product, region, amount in sorted(combinations, key=lambda x: x[2], reverse=True)[:3]:
        print(f"  {product} en {region}: {amount} unidades")

analyze_sales(sales)
```

---

## ✅ Checklist de Verificación

Antes de continuar, asegúrate de poder:

- [ ] Elegir el método de iteración correcto (`keys()`, `values()`, `items()`)
- [ ] Usar `enumerate()` para añadir índices
- [ ] Crear diccionarios desde listas con `zip()`
- [ ] Filtrar diccionarios durante la iteración
- [ ] Transformar claves y valores durante la iteración
- [ ] Evitar errores al modificar durante la iteración
- [ ] Ordenar la iteración por clave o valor
- [ ] Iterar sobre estructuras anidadas

---

## 🔗 Navegación

- ⬅️ **Anterior**: [Métodos de Diccionarios](02-metodos-diccionarios.md)
- ➡️ **Siguiente**: [Dict Comprehensions](04-dict-comprehensions.md)
- 🏠 **Índice**: [README](../README.md)
