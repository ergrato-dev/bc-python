# Frozenset y Aplicaciones Prácticas

## 🎯 Objetivos

- Comprender qué es un frozenset y sus diferencias con set
- Aprender cuándo usar frozenset sobre set
- Aplicar sets y frozensets en casos de uso reales
- Dominar patrones comunes con conjuntos

---

## 1. ¿Qué es un Frozenset?

Un **frozenset** es una versión **inmutable** de un set. Una vez creado, no se puede modificar.

### Características

| Característica | Set | Frozenset |
|----------------|-----|-----------|
| Mutable | ✅ Sí | ❌ No |
| Métodos de modificación | ✅ add, remove, etc. | ❌ No disponibles |
| Hashable | ❌ No | ✅ Sí |
| Puede ser clave de dict | ❌ No | ✅ Sí |
| Puede ser elemento de set | ❌ No | ✅ Sí |
| Operaciones de conjunto | ✅ Sí | ✅ Sí |

```python
# Crear un frozenset
fs: frozenset[int] = frozenset([1, 2, 3, 4, 5])
print(fs)  # frozenset({1, 2, 3, 4, 5})

# Desde un set
regular_set: set[str] = {"apple", "banana", "cherry"}
frozen: frozenset[str] = frozenset(regular_set)

# Desde cualquier iterable
from_string: frozenset[str] = frozenset("hello")
print(from_string)  # frozenset({'h', 'e', 'l', 'o'})
```

---

## 2. Inmutabilidad del Frozenset

```python
fs: frozenset[int] = frozenset([1, 2, 3])

# ❌ No se puede agregar
try:
    fs.add(4)  # AttributeError
except AttributeError as e:
    print(f"Error: 'frozenset' object has no attribute 'add'")

# ❌ No se puede eliminar
try:
    fs.remove(1)  # AttributeError
except AttributeError as e:
    print(f"Error: 'frozenset' object has no attribute 'remove'")

# ❌ No se puede vaciar
try:
    fs.clear()  # AttributeError
except AttributeError as e:
    print(f"Error: 'frozenset' object has no attribute 'clear'")
```

---

## 3. Operaciones Disponibles en Frozenset

Aunque inmutable, soporta todas las operaciones de consulta y operaciones que **retornan nuevos conjuntos**:

```python
a: frozenset[int] = frozenset([1, 2, 3, 4])
b: frozenset[int] = frozenset([3, 4, 5, 6])

# ✅ Operaciones que retornan nuevo frozenset
union = a | b
print(union)  # frozenset({1, 2, 3, 4, 5, 6})
print(type(union))  # <class 'frozenset'>

intersection = a & b
print(intersection)  # frozenset({3, 4})

difference = a - b
print(difference)  # frozenset({1, 2})

symmetric = a ^ b
print(symmetric)  # frozenset({1, 2, 5, 6})

# ✅ Métodos de consulta
print(len(a))              # 4
print(3 in a)              # True
print(a.issubset(b))       # False
print(a.isdisjoint(b))     # False

# ✅ Iteración
for item in a:
    print(item)

# ✅ Copia (retorna el mismo objeto, es inmutable)
copy_fs = a.copy()
print(copy_fs is a)  # True (misma referencia, es seguro)
```

---

## 4. Frozenset como Clave de Diccionario

Una ventaja clave: **frozenset es hashable**, así que puede ser clave de diccionario.

```python
# Usar frozenset como clave
permissions: dict[frozenset[str], str] = {
    frozenset(["read"]): "Viewer",
    frozenset(["read", "write"]): "Editor",
    frozenset(["read", "write", "delete"]): "Admin",
}

# Buscar por permisos
user_perms: frozenset[str] = frozenset(["read", "write"])
role = permissions.get(user_perms, "Unknown")
print(f"Role: {role}")  # Role: Editor

# ❌ Un set normal NO puede ser clave
try:
    bad_dict = {{"read", "write"}: "Editor"}  # TypeError
except TypeError as e:
    print(f"Error: unhashable type: 'set'")
```

### Caso de Uso: Cache con Argumentos de Conjunto

```python
def expensive_calculation(items: frozenset[int]) -> int:
    """Cálculo costoso cacheado por frozenset."""
    print(f"  Calculando para {items}...")
    return sum(x ** 2 for x in items)

# Cache usando frozenset como clave
cache: dict[frozenset[int], int] = {}

def cached_calculation(items: set[int]) -> int:
    """Versión cacheada que acepta sets normales."""
    key = frozenset(items)
    if key not in cache:
        cache[key] = expensive_calculation(key)
    return cache[key]

# Uso
print(cached_calculation({1, 2, 3}))  # Calcula
print(cached_calculation({3, 2, 1}))  # Usa cache (mismo frozenset)
print(cached_calculation({1, 2, 3}))  # Usa cache
```

---

## 5. Frozenset como Elemento de Set

```python
# Set de frozensets (conjuntos de conjuntos)
groups: set[frozenset[str]] = {
    frozenset(["alice", "bob"]),
    frozenset(["carol", "david"]),
    frozenset(["alice", "carol"]),
}

# Verificar si un grupo existe
team = frozenset(["alice", "bob"])
print(team in groups)  # True

# Agregar nuevo grupo
groups.add(frozenset(["eve", "frank"]))
print(len(groups))  # 4

# ❌ No se puede hacer con sets normales
try:
    bad_groups: set[set[str]] = {{"alice", "bob"}}  # TypeError
except TypeError:
    print("Error: sets no pueden ser elementos de sets")
```

---

## 6. Conversión entre Set y Frozenset

```python
# Set a frozenset
regular: set[int] = {1, 2, 3}
frozen: frozenset[int] = frozenset(regular)

# Frozenset a set
frozen2: frozenset[int] = frozenset([4, 5, 6])
regular2: set[int] = set(frozen2)

# Ahora regular2 es mutable
regular2.add(7)
print(regular2)  # {4, 5, 6, 7}
```

---

## 7. Aplicaciones Prácticas de Sets

### 7.1 Eliminar Duplicados Preservando Orden

```python
def remove_duplicates_ordered(items: list[str]) -> list[str]:
    """Elimina duplicados manteniendo el orden de primera aparición."""
    seen: set[str] = set()
    result: list[str] = []

    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)

    return result

# Uso
data = ["apple", "banana", "apple", "cherry", "banana", "date"]
unique = remove_duplicates_ordered(data)
print(unique)  # ['apple', 'banana', 'cherry', 'date']

# Alternativa con dict (Python 3.7+, preserva orden)
unique_alt = list(dict.fromkeys(data))
print(unique_alt)  # ['apple', 'banana', 'cherry', 'date']
```

### 7.2 Encontrar Elementos Duplicados

```python
def find_duplicates(items: list[str]) -> set[str]:
    """Encuentra elementos que aparecen más de una vez."""
    seen: set[str] = set()
    duplicates: set[str] = set()

    for item in items:
        if item in seen:
            duplicates.add(item)
        seen.add(item)

    return duplicates

# Uso
emails = [
    "user1@test.com",
    "user2@test.com",
    "user1@test.com",
    "user3@test.com",
    "user2@test.com"
]
dups = find_duplicates(emails)
print(f"Duplicados: {dups}")  # {'user1@test.com', 'user2@test.com'}
```

### 7.3 Validación de Datos

```python
VALID_STATUSES: frozenset[str] = frozenset([
    "pending", "approved", "rejected", "cancelled"
])

VALID_PRIORITIES: frozenset[str] = frozenset([
    "low", "medium", "high", "critical"
])

def validate_task(status: str, priority: str) -> list[str]:
    """Valida campos de una tarea."""
    errors: list[str] = []

    if status not in VALID_STATUSES:
        valid = ", ".join(sorted(VALID_STATUSES))
        errors.append(f"Invalid status '{status}'. Valid: {valid}")

    if priority not in VALID_PRIORITIES:
        valid = ", ".join(sorted(VALID_PRIORITIES))
        errors.append(f"Invalid priority '{priority}'. Valid: {valid}")

    return errors

# Uso
errors = validate_task("active", "urgent")
for error in errors:
    print(f"❌ {error}")
# ❌ Invalid status 'active'. Valid: approved, cancelled, pending, rejected
# ❌ Invalid priority 'urgent'. Valid: critical, high, low, medium
```

### 7.4 Comparar Versiones de Datos

```python
def compare_configs(
    old_config: dict[str, str],
    new_config: dict[str, str]
) -> dict[str, set[str]]:
    """Compara dos configuraciones y encuentra diferencias."""
    old_keys: set[str] = set(old_config.keys())
    new_keys: set[str] = set(new_config.keys())

    return {
        "added": new_keys - old_keys,
        "removed": old_keys - new_keys,
        "common": old_keys & new_keys,
        "changed": {
            key for key in old_keys & new_keys
            if old_config[key] != new_config[key]
        }
    }

# Uso
old = {"host": "localhost", "port": "8080", "debug": "true"}
new = {"host": "localhost", "port": "3000", "timeout": "30"}

diff = compare_configs(old, new)
print(f"Agregadas: {diff['added']}")     # {'timeout'}
print(f"Eliminadas: {diff['removed']}")  # {'debug'}
print(f"Cambiadas: {diff['changed']}")   # {'port'}
```

### 7.5 Sistema de Tags/Etiquetas

```python
from typing import TypeAlias

Tags: TypeAlias = frozenset[str]

class Article:
    def __init__(self, title: str, tags: set[str]):
        self.title = title
        self.tags: Tags = frozenset(tags)  # Inmutable

    def has_tag(self, tag: str) -> bool:
        return tag in self.tags

    def has_all_tags(self, required: set[str]) -> bool:
        return frozenset(required) <= self.tags

    def has_any_tag(self, tags: set[str]) -> bool:
        return not self.tags.isdisjoint(tags)


def find_articles_by_tags(
    articles: list[Article],
    required_tags: set[str],
    excluded_tags: set[str] | None = None
) -> list[Article]:
    """Encuentra artículos que tienen todos los tags requeridos."""
    excluded = excluded_tags or set()

    return [
        article for article in articles
        if article.has_all_tags(required_tags)
        and article.tags.isdisjoint(excluded)
    ]


# Uso
articles = [
    Article("Python Basics", {"python", "beginner", "tutorial"}),
    Article("Advanced Python", {"python", "advanced", "tips"}),
    Article("Web Development", {"javascript", "web", "beginner"}),
    Article("Python Web", {"python", "web", "flask"}),
]

# Buscar artículos de Python para principiantes
results = find_articles_by_tags(
    articles,
    required_tags={"python", "beginner"},
    excluded_tags={"advanced"}
)

for article in results:
    print(f"📄 {article.title}")  # Python Basics
```

---

## 8. Rendimiento: Set vs Lista para Búsqueda

```python
import time

def benchmark_membership(size: int, iterations: int) -> None:
    """Compara rendimiento de búsqueda en list vs set."""
    # Crear estructuras
    data_list: list[int] = list(range(size))
    data_set: set[int] = set(range(size))

    # Elementos a buscar (mitad existentes, mitad no)
    search_items = list(range(0, size * 2, 2))

    # Benchmark lista
    start = time.perf_counter()
    for _ in range(iterations):
        for item in search_items:
            _ = item in data_list
    list_time = time.perf_counter() - start

    # Benchmark set
    start = time.perf_counter()
    for _ in range(iterations):
        for item in search_items:
            _ = item in data_set
    set_time = time.perf_counter() - start

    print(f"Tamaño: {size:,}")
    print(f"  Lista: {list_time:.4f}s")
    print(f"  Set:   {set_time:.4f}s")
    print(f"  Set es {list_time / set_time:.1f}x más rápido")

# benchmark_membership(10_000, 100)
# Resultado típico: Set es 100-1000x más rápido
```

---

## 9. Resumen: Cuándo Usar Cada Tipo

```
╔═══════════════════════════════════════════════════════════════╗
║                 ¿CUÁNDO USAR CADA TIPO?                       ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  USA SET cuando:                                              ║
║  ├─ Necesitas agregar/eliminar elementos                      ║
║  ├─ Colección de trabajo que cambia                           ║
║  └─ Operaciones in-place (|=, &=, -=)                         ║
║                                                               ║
║  USA FROZENSET cuando:                                        ║
║  ├─ Necesitas clave de diccionario                            ║
║  ├─ Necesitas elemento de otro set                            ║
║  ├─ Constantes/configuración inmutable                        ║
║  ├─ Garantizar que no se modifique                            ║
║  └─ Pasar a funciones sin riesgo de modificación              ║
║                                                               ║
║  USA LISTA cuando:                                            ║
║  ├─ Necesitas orden                                           ║
║  ├─ Necesitas duplicados                                      ║
║  ├─ Necesitas acceso por índice                               ║
║  └─ Pocos elementos (< 10) con búsquedas infrecuentes         ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## ✅ Checklist de Verificación

Antes de continuar, asegúrate de poder:

- [ ] Crear frozensets desde diferentes iterables
- [ ] Entender por qué frozenset es hashable y set no
- [ ] Usar frozenset como clave de diccionario
- [ ] Usar frozenset como elemento de set
- [ ] Convertir entre set y frozenset
- [ ] Elegir entre set y frozenset según el caso de uso
- [ ] Aplicar sets para eliminar duplicados y validar datos

---

## 🔗 Navegación

- ⬅️ **Anterior**: [Operaciones de Conjuntos](02-operaciones-conjuntos.md)
- ➡️ **Siguiente**: [Algoritmos de Búsqueda y Ordenamiento](04-algoritmos-busqueda-ordenamiento.md)
- 🏠 **Índice**: [README](../README.md)
