# Algoritmos de Búsqueda y Ordenamiento

## 🎯 Objetivos

- Comprender la búsqueda lineal y binaria
- Dominar `sorted()` y `sort()` con sus parámetros
- Entender conceptos básicos de complejidad algorítmica (Big O)
- Aplicar algoritmos de búsqueda y ordenamiento en Python

---

## 1. Introducción a Algoritmos

Un **algoritmo** es una secuencia de pasos para resolver un problema. La **eficiencia** de un algoritmo determina qué tan rápido resuelve el problema cuando los datos crecen.

### Notación Big O (Simplificada)

| Notación | Nombre | Ejemplo | Descripción |
|----------|--------|---------|-------------|
| O(1) | Constante | `dict[key]` | Mismo tiempo sin importar el tamaño |
| O(log n) | Logarítmica | Búsqueda binaria | Muy eficiente, divide el problema |
| O(n) | Lineal | Búsqueda lineal | Tiempo crece con el tamaño |
| O(n log n) | Linearítmica | `sorted()` | Ordenamiento eficiente |
| O(n²) | Cuadrática | Bubble sort | Lento para datos grandes |

```python
# O(1) - Constante: acceso a diccionario
data = {"a": 1, "b": 2, "c": 3}
value = data["b"]  # Siempre igual de rápido

# O(n) - Lineal: buscar en lista
numbers = [1, 2, 3, 4, 5]
found = 3 in numbers  # Peor caso: revisar todos

# O(n log n) - Ordenar
sorted_numbers = sorted(numbers)  # Muy eficiente
```

---

## 2. Búsqueda Lineal

La **búsqueda lineal** revisa cada elemento secuencialmente hasta encontrar el objetivo o llegar al final.

### Complejidad: O(n)

- **Mejor caso**: O(1) - elemento al inicio
- **Peor caso**: O(n) - elemento al final o no existe
- **Caso promedio**: O(n/2) ≈ O(n)

### Implementación Básica

```python
def linear_search(items: list[int], target: int) -> int:
    """
    Busca un elemento en una lista.

    Args:
        items: Lista donde buscar
        target: Elemento a encontrar

    Returns:
        Índice del elemento o -1 si no existe
    """
    for index, item in enumerate(items):
        if item == target:
            return index
    return -1

# Uso
numbers = [64, 34, 25, 12, 22, 11, 90]
result = linear_search(numbers, 22)
print(f"Encontrado en índice: {result}")  # 4
```

### Con Información de Búsqueda

```python
def linear_search_verbose(
    items: list[int],
    target: int
) -> dict[str, int | bool]:
    """Búsqueda lineal con estadísticas."""
    comparisons = 0

    for index, item in enumerate(items):
        comparisons += 1
        if item == target:
            return {
                "found": True,
                "index": index,
                "comparisons": comparisons
            }

    return {
        "found": False,
        "index": -1,
        "comparisons": comparisons
    }

# Demostración
numbers = list(range(1, 101))  # 1 a 100
result = linear_search_verbose(numbers, 73)
print(f"Comparaciones: {result['comparisons']}")  # 73
```

### Búsqueda de Todos los Índices

```python
def find_all_indices(items: list[str], target: str) -> list[int]:
    """Encuentra todos los índices donde aparece el elemento."""
    return [i for i, item in enumerate(items) if item == target]

# Uso
words = ["apple", "banana", "apple", "cherry", "apple"]
indices = find_all_indices(words, "apple")
print(f"'apple' en índices: {indices}")  # [0, 2, 4]
```

---

## 3. Búsqueda Binaria

La **búsqueda binaria** divide repetidamente el espacio de búsqueda a la mitad. **Requiere datos ordenados**.

### Complejidad: O(log n)

- Para 1,000 elementos: ~10 comparaciones
- Para 1,000,000 elementos: ~20 comparaciones

### Implementación Iterativa

```python
def binary_search(items: list[int], target: int) -> int:
    """
    Búsqueda binaria en lista ordenada.

    Args:
        items: Lista ORDENADA donde buscar
        target: Elemento a encontrar

    Returns:
        Índice del elemento o -1 si no existe
    """
    left = 0
    right = len(items) - 1

    while left <= right:
        mid = (left + right) // 2
        mid_value = items[mid]

        if mid_value == target:
            return mid
        elif mid_value < target:
            left = mid + 1  # Buscar en mitad derecha
        else:
            right = mid - 1  # Buscar en mitad izquierda

    return -1

# Uso (¡lista debe estar ordenada!)
numbers = [11, 12, 22, 25, 34, 64, 90]
result = binary_search(numbers, 22)
print(f"Encontrado en índice: {result}")  # 2
```

### Implementación Recursiva

```python
def binary_search_recursive(
    items: list[int],
    target: int,
    left: int = 0,
    right: int | None = None
) -> int:
    """Búsqueda binaria recursiva."""
    if right is None:
        right = len(items) - 1

    if left > right:
        return -1

    mid = (left + right) // 2

    if items[mid] == target:
        return mid
    elif items[mid] < target:
        return binary_search_recursive(items, target, mid + 1, right)
    else:
        return binary_search_recursive(items, target, left, mid - 1)

# Uso
numbers = [11, 12, 22, 25, 34, 64, 90]
result = binary_search_recursive(numbers, 64)
print(f"Encontrado en índice: {result}")  # 5
```

### Usando el Módulo `bisect`

Python incluye búsqueda binaria optimizada:

```python
import bisect

numbers = [11, 12, 22, 25, 34, 64, 90]

# Encontrar posición de inserción (izquierda)
pos = bisect.bisect_left(numbers, 22)
print(f"Posición: {pos}")  # 2

# Verificar si el elemento existe
def binary_search_bisect(items: list[int], target: int) -> int:
    """Búsqueda binaria usando bisect."""
    pos = bisect.bisect_left(items, target)
    if pos < len(items) and items[pos] == target:
        return pos
    return -1

result = binary_search_bisect(numbers, 22)
print(f"Índice: {result}")  # 2

# Insertar manteniendo orden
bisect.insort(numbers, 30)
print(numbers)  # [11, 12, 22, 25, 30, 34, 64, 90]
```

---

## 4. Comparación: Lineal vs Binaria

```python
def compare_searches(size: int, target: int) -> None:
    """Compara búsqueda lineal vs binaria."""
    items = list(range(size))

    # Búsqueda lineal
    linear_steps = 0
    for i, item in enumerate(items):
        linear_steps += 1
        if item == target:
            break

    # Búsqueda binaria
    binary_steps = 0
    left, right = 0, len(items) - 1
    while left <= right:
        binary_steps += 1
        mid = (left + right) // 2
        if items[mid] == target:
            break
        elif items[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    print(f"Buscando {target} en {size:,} elementos:")
    print(f"  Lineal: {linear_steps:,} pasos")
    print(f"  Binaria: {binary_steps} pasos")

compare_searches(1_000_000, 750_000)
# Lineal: 750,001 pasos
# Binaria: 20 pasos
```

---

## 5. Ordenamiento con `sorted()`

La función `sorted()` retorna una **nueva lista ordenada** sin modificar la original.

### Uso Básico

```python
numbers = [64, 34, 25, 12, 22, 11, 90]

# Orden ascendente (por defecto)
sorted_asc = sorted(numbers)
print(sorted_asc)  # [11, 12, 22, 25, 34, 64, 90]
print(numbers)     # [64, 34, 25, 12, 22, 11, 90] - sin cambios

# Orden descendente
sorted_desc = sorted(numbers, reverse=True)
print(sorted_desc)  # [90, 64, 34, 25, 22, 12, 11]

# Funciona con cualquier iterable
word = "python"
sorted_chars = sorted(word)
print(sorted_chars)  # ['h', 'n', 'o', 'p', 't', 'y']

# Strings se ordenan alfabéticamente
words = ["banana", "apple", "cherry", "date"]
print(sorted(words))  # ['apple', 'banana', 'cherry', 'date']
```

### Ordenar con `key`

El parámetro `key` permite especificar una función de ordenamiento:

```python
# Ordenar por longitud
words = ["python", "is", "awesome", "and", "fun"]
by_length = sorted(words, key=len)
print(by_length)  # ['is', 'and', 'fun', 'python', 'awesome']

# Ordenar sin distinguir mayúsculas
names = ["Alice", "bob", "Carol", "david"]
by_name = sorted(names, key=str.lower)
print(by_name)  # ['Alice', 'bob', 'Carol', 'david']

# Ordenar por valor absoluto
numbers = [-5, 2, -8, 1, -3, 7]
by_abs = sorted(numbers, key=abs)
print(by_abs)  # [1, 2, -3, -5, 7, -8]

# Ordenar por último carácter
words = ["apple", "banana", "cherry", "date"]
by_last = sorted(words, key=lambda w: w[-1])
print(by_last)  # ['banana', 'apple', 'date', 'cherry']
```

### Ordenar Diccionarios y Objetos

```python
# Lista de diccionarios
students = [
    {"name": "Alice", "grade": 85, "age": 22},
    {"name": "Bob", "grade": 92, "age": 20},
    {"name": "Carol", "grade": 78, "age": 23},
    {"name": "David", "grade": 92, "age": 21},
]

# Por calificación (descendente)
by_grade = sorted(students, key=lambda s: s["grade"], reverse=True)
for s in by_grade:
    print(f"{s['name']}: {s['grade']}")
# Bob: 92, David: 92, Alice: 85, Carol: 78

# Por múltiples criterios: primero grade desc, luego age asc
by_grade_age = sorted(
    students,
    key=lambda s: (-s["grade"], s["age"])
)
for s in by_grade_age:
    print(f"{s['name']}: {s['grade']}, {s['age']}")
# Bob: 92, 20 (grade 92, younger)
# David: 92, 21 (grade 92, older)
# Alice: 85, 22
# Carol: 78, 23
```

### Usando `operator.itemgetter` y `attrgetter`

```python
from operator import itemgetter, attrgetter

students = [
    {"name": "Alice", "grade": 85},
    {"name": "Bob", "grade": 92},
    {"name": "Carol", "grade": 78},
]

# itemgetter para diccionarios (más eficiente que lambda)
by_grade = sorted(students, key=itemgetter("grade"))
by_name = sorted(students, key=itemgetter("name"))

# Múltiples claves
by_grade_name = sorted(students, key=itemgetter("grade", "name"))

# Para objetos con atributos
class Student:
    def __init__(self, name: str, grade: int):
        self.name = name
        self.grade = grade

students_obj = [Student("Alice", 85), Student("Bob", 92)]
by_grade_obj = sorted(students_obj, key=attrgetter("grade"))
```

---

## 6. Ordenamiento In-Place con `sort()`

El método `sort()` modifica la lista original (solo para listas):

```python
numbers = [64, 34, 25, 12, 22, 11, 90]

# sort() modifica la lista original
numbers.sort()
print(numbers)  # [11, 12, 22, 25, 34, 64, 90]

# Retorna None, no la lista ordenada
result = numbers.sort(reverse=True)
print(result)   # None
print(numbers)  # [90, 64, 34, 25, 22, 12, 11]

# También acepta key
words = ["Python", "java", "JavaScript", "go"]
words.sort(key=str.lower)
print(words)  # ['go', 'java', 'JavaScript', 'Python']
```

### ¿Cuándo usar `sort()` vs `sorted()`?

```python
# ✅ Usa sort() cuando:
# - Quieres modificar la lista original
# - No necesitas la versión sin ordenar
# - Quieres ahorrar memoria (no crea copia)
my_list = [3, 1, 2]
my_list.sort()

# ✅ Usa sorted() cuando:
# - Necesitas mantener el original intacto
# - Trabajas con iterables que no son listas
# - Necesitas el resultado en una expresión
original = [3, 1, 2]
new_list = sorted(original)  # original sin cambios

# Ejemplo: ordenar y usar inmediatamente
for item in sorted(my_data, key=get_priority):
    process(item)
```

---

## 7. Algoritmos de Ordenamiento Básicos

Aunque Python usa Timsort (muy eficiente), es educativo conocer algoritmos básicos.

### Bubble Sort - O(n²)

```python
def bubble_sort(items: list[int]) -> list[int]:
    """
    Ordenamiento burbuja.
    Compara elementos adyacentes e intercambia si están desordenados.
    """
    arr = items.copy()
    n = len(arr)

    for i in range(n):
        # Flag para optimizar si ya está ordenado
        swapped = False

        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True

        if not swapped:
            break

    return arr

# Uso
numbers = [64, 34, 25, 12, 22, 11, 90]
sorted_nums = bubble_sort(numbers)
print(sorted_nums)  # [11, 12, 22, 25, 34, 64, 90]
```

### Selection Sort - O(n²)

```python
def selection_sort(items: list[int]) -> list[int]:
    """
    Ordenamiento por selección.
    Encuentra el mínimo y lo coloca en su posición.
    """
    arr = items.copy()
    n = len(arr)

    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j

        arr[i], arr[min_idx] = arr[min_idx], arr[i]

    return arr

# Uso
numbers = [64, 34, 25, 12, 22, 11, 90]
sorted_nums = selection_sort(numbers)
print(sorted_nums)  # [11, 12, 22, 25, 34, 64, 90]
```

### Insertion Sort - O(n²)

```python
def insertion_sort(items: list[int]) -> list[int]:
    """
    Ordenamiento por inserción.
    Construye la lista ordenada elemento por elemento.
    """
    arr = items.copy()

    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1

        arr[j + 1] = key

    return arr

# Uso
numbers = [64, 34, 25, 12, 22, 11, 90]
sorted_nums = insertion_sort(numbers)
print(sorted_nums)  # [11, 12, 22, 25, 34, 64, 90]
```

---

## 8. Comparación de Algoritmos

| Algoritmo | Mejor | Promedio | Peor | Memoria | Estable |
|-----------|-------|----------|------|---------|---------|
| Bubble Sort | O(n) | O(n²) | O(n²) | O(1) | ✅ |
| Selection Sort | O(n²) | O(n²) | O(n²) | O(1) | ❌ |
| Insertion Sort | O(n) | O(n²) | O(n²) | O(1) | ✅ |
| Timsort (Python) | O(n) | O(n log n) | O(n log n) | O(n) | ✅ |

> **Nota**: Python usa **Timsort**, un algoritmo híbrido muy optimizado. ¡Siempre usa `sorted()` o `sort()` en código real!

---

## 9. Ejemplo Práctico: Sistema de Ranking

```python
from dataclasses import dataclass
from operator import attrgetter

@dataclass
class Player:
    name: str
    score: int
    games_played: int

    @property
    def average(self) -> float:
        return self.score / max(1, self.games_played)


def create_leaderboard(
    players: list[Player],
    min_games: int = 5,
    top_n: int = 10
) -> list[dict[str, str | int | float]]:
    """
    Crea un leaderboard ordenado por promedio.

    Args:
        players: Lista de jugadores
        min_games: Mínimo de partidas para calificar
        top_n: Cantidad de posiciones a mostrar
    """
    # Filtrar jugadores que califican
    qualified = [p for p in players if p.games_played >= min_games]

    # Ordenar por promedio descendente, luego por nombre
    ranked = sorted(
        qualified,
        key=lambda p: (-p.average, p.name)
    )

    # Crear leaderboard
    leaderboard = []
    for rank, player in enumerate(ranked[:top_n], start=1):
        leaderboard.append({
            "rank": rank,
            "name": player.name,
            "score": player.score,
            "games": player.games_played,
            "average": round(player.average, 2)
        })

    return leaderboard


# Uso
players = [
    Player("Alice", 450, 10),
    Player("Bob", 380, 8),
    Player("Carol", 520, 12),
    Player("David", 200, 3),  # No califica
    Player("Eve", 410, 9),
]

leaderboard = create_leaderboard(players, min_games=5, top_n=3)

print("🏆 LEADERBOARD")
print("-" * 50)
for entry in leaderboard:
    print(f"{entry['rank']}. {entry['name']}: {entry['average']} avg")
# 1. Alice: 45.0 avg
# 2. Eve: 45.56 avg (mismo promedio que Alice, pero 'E' > 'A')
# 3. Carol: 43.33 avg
```

---

## 10. Resumen

```
╔═══════════════════════════════════════════════════════════════╗
║              BÚSQUEDA Y ORDENAMIENTO                          ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  BÚSQUEDA:                                                    ║
║  ├─ Lineal: O(n) - cualquier lista                            ║
║  ├─ Binaria: O(log n) - REQUIERE lista ordenada               ║
║  └─ bisect: módulo Python para búsqueda binaria               ║
║                                                               ║
║  ORDENAMIENTO:                                                ║
║  ├─ sorted(iterable) → nueva lista ordenada                   ║
║  ├─ list.sort() → ordena in-place                             ║
║  ├─ key=función → criterio de ordenamiento                    ║
║  └─ reverse=True → orden descendente                          ║
║                                                               ║
║  COMPLEJIDAD:                                                 ║
║  ├─ O(1): constante (acceso dict/set)                         ║
║  ├─ O(log n): logarítmica (búsqueda binaria)                  ║
║  ├─ O(n): lineal (búsqueda lineal)                            ║
║  ├─ O(n log n): linearítmica (sorted, sort)                   ║
║  └─ O(n²): cuadrática (bubble sort)                           ║
║                                                               ║
║  REGLA: Siempre usa sorted()/sort() de Python                 ║
║         Son altamente optimizados (Timsort)                   ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## ✅ Checklist de Verificación

Antes de continuar, asegúrate de poder:

- [ ] Implementar búsqueda lineal
- [ ] Implementar búsqueda binaria (lista ordenada)
- [ ] Usar `sorted()` con `key` y `reverse`
- [ ] Usar `sort()` para ordenar in-place
- [ ] Ordenar por múltiples criterios
- [ ] Entender la diferencia entre O(n), O(log n), O(n log n)
- [ ] Saber cuándo usar búsqueda lineal vs binaria

---

## 🔗 Navegación

- ⬅️ **Anterior**: [Frozenset y Aplicaciones](03-frozenset-aplicaciones.md)
- ➡️ **Siguiente**: [Ejercicios](../2-ejercicios/)
- 🏠 **Índice**: [README](../README.md)
