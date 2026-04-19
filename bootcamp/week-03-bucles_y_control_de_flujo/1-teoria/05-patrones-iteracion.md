# 🎨 Patrones de Iteración

## 🎯 Objetivos

- Dominar patrones comunes de iteración
- Reconocer cuándo aplicar cada patrón
- Escribir código más idiomático y eficiente
- Combinar patrones para resolver problemas complejos

---

## 📋 Contenido

### 1. Patrón: Contador

Contar elementos que cumplen una condición:

```python
def count_even(numbers: list[int]) -> int:
    """Cuenta números pares."""
    count: int = 0

    for num in numbers:
        if num % 2 == 0:
            count += 1

    return count

print(count_even([1, 2, 3, 4, 5, 6]))  # 3
```

#### Variación: Múltiples Contadores

```python
def count_types(text: str) -> dict[str, int]:
    """Cuenta letras, dígitos y otros."""
    letters: int = 0
    digits: int = 0
    others: int = 0

    for char in text:
        if char.isalpha():
            letters += 1
        elif char.isdigit():
            digits += 1
        else:
            others += 1

    return {"letters": letters, "digits": digits, "others": others}

print(count_types("Hello 123!"))
# {'letters': 5, 'digits': 3, 'others': 2}
```

---

### 2. Patrón: Acumulador

Acumular un valor a través de las iteraciones:

```python
def sum_list(numbers: list[int]) -> int:
    """Suma todos los números."""
    total: int = 0

    for num in numbers:
        total += num

    return total

print(sum_list([1, 2, 3, 4, 5]))  # 15
```

#### Variación: Producto

```python
def factorial(n: int) -> int:
    """Calcula el factorial de n."""
    result: int = 1

    for i in range(1, n + 1):
        result *= i

    return result

print(factorial(5))  # 120 (5! = 5*4*3*2*1)
```

#### Variación: Concatenación de Strings

```python
def join_words(words: list[str], separator: str = " ") -> str:
    """Une palabras con un separador."""
    if not words:
        return ""

    result: str = words[0]

    for word in words[1:]:
        result += separator + word

    return result

print(join_words(["Hola", "Mundo", "Python"]))  # "Hola Mundo Python"
```

---

### 3. Patrón: Búsqueda

Encontrar un elemento o verificar si existe:

#### Búsqueda Lineal

```python
def find_index(items: list[str], target: str) -> int:
    """Encuentra el índice de target, -1 si no existe."""
    for i, item in enumerate(items):
        if item == target:
            return i
    return -1

colors = ["rojo", "verde", "azul"]
print(find_index(colors, "verde"))  # 1
print(find_index(colors, "negro"))  # -1
```

#### Verificar Existencia

```python
def contains_negative(numbers: list[int]) -> bool:
    """Verifica si hay algún número negativo."""
    for num in numbers:
        if num < 0:
            return True
    return False

print(contains_negative([1, 2, 3, -4, 5]))  # True
print(contains_negative([1, 2, 3, 4, 5]))   # False
```

#### Búsqueda con Condición Compleja

```python
def find_first_adult(people: list[dict]) -> dict | None:
    """Encuentra la primera persona mayor de 18."""
    for person in people:
        if person.get("age", 0) >= 18:
            return person
    return None

people = [
    {"name": "Ana", "age": 15},
    {"name": "Bob", "age": 22},
    {"name": "Carlos", "age": 17},
]
print(find_first_adult(people))  # {'name': 'Bob', 'age': 22}
```

---

### 4. Patrón: Filtrado

Seleccionar elementos que cumplen una condición:

```python
def filter_positive(numbers: list[int]) -> list[int]:
    """Filtra solo números positivos."""
    result: list[int] = []

    for num in numbers:
        if num > 0:
            result.append(num)

    return result

print(filter_positive([-2, 3, -5, 8, 0, 1]))  # [3, 8, 1]
```

#### Variación: Filtrar con Transformación

```python
def get_adult_names(people: list[dict]) -> list[str]:
    """Obtiene nombres de personas mayores de 18."""
    names: list[str] = []

    for person in people:
        if person["age"] >= 18:
            names.append(person["name"])

    return names

people = [
    {"name": "Ana", "age": 15},
    {"name": "Bob", "age": 22},
    {"name": "Carlos", "age": 30},
]
print(get_adult_names(people))  # ['Bob', 'Carlos']
```

---

### 5. Patrón: Transformación (Mapping)

Aplicar una operación a cada elemento:

```python
def square_all(numbers: list[int]) -> list[int]:
    """Eleva al cuadrado cada número."""
    result: list[int] = []

    for num in numbers:
        result.append(num ** 2)

    return result

print(square_all([1, 2, 3, 4]))  # [1, 4, 9, 16]
```

#### Variación: Normalizar Strings

```python
def normalize_names(names: list[str]) -> list[str]:
    """Normaliza nombres: primera letra mayúscula, resto minúscula."""
    result: list[str] = []

    for name in names:
        result.append(name.strip().title())

    return result

print(normalize_names(["  ANA  ", "bob", "CARLOS"]))
# ['Ana', 'Bob', 'Carlos']
```

---

### 6. Patrón: Máximo/Mínimo

Encontrar el valor extremo:

```python
def find_max(numbers: list[int]) -> int | None:
    """Encuentra el valor máximo."""
    if not numbers:
        return None

    max_value: int = numbers[0]

    for num in numbers[1:]:
        if num > max_value:
            max_value = num

    return max_value

print(find_max([3, 7, 2, 9, 1]))  # 9
```

#### Variación: Elemento con Máximo Atributo

```python
def oldest_person(people: list[dict]) -> dict | None:
    """Encuentra la persona de mayor edad."""
    if not people:
        return None

    oldest: dict = people[0]

    for person in people[1:]:
        if person["age"] > oldest["age"]:
            oldest = person

    return oldest

people = [
    {"name": "Ana", "age": 25},
    {"name": "Bob", "age": 35},
    {"name": "Carlos", "age": 30},
]
print(oldest_person(people))  # {'name': 'Bob', 'age': 35}
```

---

### 7. Patrón: Verificación Universal

Comprobar si TODOS los elementos cumplen una condición:

```python
def all_positive(numbers: list[int]) -> bool:
    """Verifica si todos son positivos."""
    for num in numbers:
        if num <= 0:
            return False  # Encontró uno que no cumple
    return True

print(all_positive([1, 2, 3, 4]))   # True
print(all_positive([1, 2, -3, 4]))  # False
```

#### Variación: Verificación Existencial

```python
def any_even(numbers: list[int]) -> bool:
    """Verifica si hay al menos un número par."""
    for num in numbers:
        if num % 2 == 0:
            return True  # Encontró uno que cumple
    return False

print(any_even([1, 3, 5, 7]))  # False
print(any_even([1, 3, 4, 7]))  # True
```

---

### 8. Patrón: Agrupación

Agrupar elementos por categoría:

```python
def group_by_length(words: list[str]) -> dict[int, list[str]]:
    """Agrupa palabras por longitud."""
    groups: dict[int, list[str]] = {}

    for word in words:
        length = len(word)
        if length not in groups:
            groups[length] = []
        groups[length].append(word)

    return groups

words = ["sol", "luna", "mar", "cielo", "rio"]
print(group_by_length(words))
# {3: ['sol', 'mar', 'rio'], 4: ['luna'], 5: ['cielo']}
```

#### Variación: Contar por Categoría

```python
def count_by_initial(names: list[str]) -> dict[str, int]:
    """Cuenta nombres por letra inicial."""
    counts: dict[str, int] = {}

    for name in names:
        initial = name[0].upper()
        if initial in counts:
            counts[initial] += 1
        else:
            counts[initial] = 1

    return counts

names = ["Ana", "Alberto", "Bob", "Andrea", "Carlos"]
print(count_by_initial(names))
# {'A': 3, 'B': 1, 'C': 1}
```

---

### 9. Patrón: Zip (Iteración Paralela)

Iterar sobre múltiples secuencias simultáneamente:

```python
names: list[str] = ["Ana", "Bob", "Carlos"]
ages: list[int] = [25, 30, 35]

# zip combina elemento a elemento
for name, age in zip(names, ages):
    print(f"{name} tiene {age} años")

# Salida:
# Ana tiene 25 años
# Bob tiene 30 años
# Carlos tiene 35 años
```

#### Ejemplo: Calcular Diferencias

```python
def calculate_changes(before: list[int], after: list[int]) -> list[int]:
    """Calcula diferencias entre dos listas."""
    changes: list[int] = []

    for b, a in zip(before, after):
        changes.append(a - b)

    return changes

before = [100, 200, 300]
after = [150, 180, 350]
print(calculate_changes(before, after))  # [50, -20, 50]
```

---

### 10. Combinando Patrones

Ejemplo complejo que combina varios patrones:

```python
def analyze_scores(students: list[dict]) -> dict:
    """Analiza calificaciones de estudiantes."""
    # Filtrado + Acumulador + Contador
    passing_names: list[str] = []
    total_score: int = 0
    count: int = 0
    highest: dict | None = None

    for student in students:
        score = student["score"]
        total_score += score
        count += 1

        # Filtrado: solo aprobados
        if score >= 60:
            passing_names.append(student["name"])

        # Máximo
        if highest is None or score > highest["score"]:
            highest = student

    return {
        "average": total_score / count if count > 0 else 0,
        "passing_students": passing_names,
        "top_student": highest["name"] if highest else None,
        "pass_rate": len(passing_names) / count if count > 0 else 0,
    }

students = [
    {"name": "Ana", "score": 85},
    {"name": "Bob", "score": 55},
    {"name": "Carlos", "score": 92},
    {"name": "Diana", "score": 78},
]

result = analyze_scores(students)
print(result)
# {
#   'average': 77.5,
#   'passing_students': ['Ana', 'Carlos', 'Diana'],
#   'top_student': 'Carlos',
#   'pass_rate': 0.75
# }
```

---

### 11. Resumen de Patrones

| Patrón | Uso | Inicialización |
|--------|-----|----------------|
| Contador | Contar elementos | `count = 0` |
| Acumulador | Sumar/multiplicar valores | `total = 0` o `product = 1` |
| Búsqueda | Encontrar elemento | `return` cuando encuentre |
| Filtrado | Seleccionar elementos | `result = []` |
| Transformación | Modificar elementos | `result = []` |
| Max/Min | Encontrar extremo | `best = items[0]` |
| Verificación | Comprobar condición | `return True/False` |
| Agrupación | Organizar por categoría | `groups = {}` |

---

## 🧪 Ejercicio Rápido

Implementa una función que combine varios patrones:

```python
def analyze_numbers(numbers: list[int]) -> dict:
    """
    Analiza una lista de números y retorna estadísticas.

    >>> analyze_numbers([1, -2, 3, -4, 5, 6])
    {
        'sum': 9,
        'count_positive': 4,
        'count_negative': 2,
        'max': 6,
        'min': -4,
        'positives': [1, 3, 5, 6]
    }
    """
    # Tu código aquí
    pass
```

<details>
<summary>Ver solución</summary>

```python
def analyze_numbers(numbers: list[int]) -> dict:
    total: int = 0
    count_pos: int = 0
    count_neg: int = 0
    max_val: int = numbers[0]
    min_val: int = numbers[0]
    positives: list[int] = []

    for num in numbers:
        total += num

        if num > 0:
            count_pos += 1
            positives.append(num)
        elif num < 0:
            count_neg += 1

        if num > max_val:
            max_val = num
        if num < min_val:
            min_val = num

    return {
        "sum": total,
        "count_positive": count_pos,
        "count_negative": count_neg,
        "max": max_val,
        "min": min_val,
        "positives": positives,
    }
```

</details>

---

## 📚 Recursos Adicionales

- [Python Docs - Functional Programming](https://docs.python.org/3/howto/functional.html)
- [Real Python - Python Iterators](https://realpython.com/introduction-to-python-generators/)

---

## ✅ Checklist de Verificación

- [ ] Reconozco los patrones de contador y acumulador
- [ ] Puedo implementar búsqueda y filtrado
- [ ] Sé aplicar transformación a listas
- [ ] Puedo encontrar máximos/mínimos manualmente
- [ ] Sé combinar múltiples patrones en una solución
