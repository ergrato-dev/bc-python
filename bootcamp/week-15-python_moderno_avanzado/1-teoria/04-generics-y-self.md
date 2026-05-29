# 🔧 Generics Nativos y Self Type

## 🎯 Objetivos

- Escribir funciones y clases genéricas con `TypeVar` y la sintaxis nativa de Python 3.12+
- Usar `Generic[T]` para colecciones y repositorios tipados
- Aplicar `Self` para métodos que retornan la misma instancia (builder pattern, fluent API)
- Entender covarianza y contravarianza en contextos prácticos

---

## 1. TypeVar — Variables de tipo

`TypeVar` define un tipo que puede ser cualquier cosa, pero que se mantiene consistente dentro de un contexto:

```python
from typing import TypeVar

T = TypeVar("T")

def first(items: list[T]) -> T:
    return items[0]

first([1, 2, 3])          # retorna int ✅
first(["a", "b", "c"])    # retorna str ✅
first([1, "mixed"])       # retorna int | str — OK, pero no ideal
```

### TypeVar con bounds

```python
from typing import TypeVar, Protocol

class Nameable(Protocol):
    @property
    def name(self) -> str: ...

N = TypeVar("N", bound=Nameable)

def get_by_name(items: list[N], name: str) -> N | None:
    return next((item for item in items if item.name == name), None)
```

`bound=Nameable` garantiza que `N` siempre implementa el protocolo `Nameable`.

---

## 2. Clases genéricas con `Generic[T]`

```python
from typing import Generic, TypeVar

T = TypeVar("T")

class Repository(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []

    def add(self, item: T) -> None:
        self._items.append(item)

    def get_all(self) -> list[T]:
        return self._items.copy()

    def find(self, predicate: "Callable[[T], bool]") -> T | None:
        return next((item for item in self._items if predicate(item)), None)
```

```python
from dataclasses import dataclass

@dataclass
class Client:
    id: int
    name: str

@dataclass
class Project:
    id: int
    name: str
    client_id: int

# Repositorios completamente tipados
client_repo: Repository[Client] = Repository()
project_repo: Repository[Project] = Repository()

client_repo.add(Client(1, "Acme Corp"))
project_repo.add(Project(1, "Campaña Q4", client_id=1))

# mypy sabe exactamente qué tipo retorna
client = client_repo.find(lambda c: c.name == "Acme Corp")
# client es Client | None ✅
```

---

## 3. Sintaxis nativa de generics (Python 3.12+)

Python 3.12 introduce una sintaxis más limpia:

```python
# Antes (3.11 y anteriores)
from typing import TypeVar, Generic

T = TypeVar("T")

class Stack(Generic[T]):
    def push(self, item: T) -> None: ...
    def pop(self) -> T: ...

# Ahora (3.12+) — más conciso
class Stack[T]:
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        if not self._items:
            raise IndexError("stack is empty")
        return self._items.pop()

# Funciones genéricas también
def first[T](items: list[T]) -> T:
    return items[0]

# Con bounds
def get_name[N: Nameable](items: list[N]) -> list[str]:
    return [item.name for item in items]
```

> La sintaxis `class Foo[T]:` es Python 3.12+. Usa `Generic[T]` si necesitas compatibilidad con 3.10/3.11.

---

## 4. `Self` — métodos que retornan la misma clase

`Self` es un tipo especial que representa "la clase en la que estoy definido", incluyendo subclases.

### Sin Self — el problema

```python
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class QueryBuilder:
    _table: str
    _conditions: list[str]

    def where(self, condition: str) -> "QueryBuilder":   # siempre QueryBuilder
        self._conditions.append(condition)
        return self
```

Si heredas de `QueryBuilder`, el tipo de retorno sigue siendo `QueryBuilder`, no la subclase.

### Con Self — solución

```python
from typing import Self
from dataclasses import dataclass, field

@dataclass
class QueryBuilder:
    _table: str
    _conditions: list[str] = field(default_factory=list)
    _limit: int | None = None

    def where(self, condition: str) -> Self:    # retorna la clase exacta
        self._conditions.append(condition)
        return self

    def limit(self, n: int) -> Self:
        self._limit = n
        return self

    def build(self) -> str:
        where = " AND ".join(self._conditions)
        base = f"SELECT * FROM {self._table}"
        if where:
            base += f" WHERE {where}"
        if self._limit:
            base += f" LIMIT {self._limit}"
        return base

class ProjectQueryBuilder(QueryBuilder):
    def active_only(self) -> Self:              # ✅ retorna ProjectQueryBuilder
        return self.where("active = true")

# Fluent API completamente tipada
query = (
    ProjectQueryBuilder(_table="projects")
    .active_only()          # retorna ProjectQueryBuilder ✅
    .where("budget > 10000")
    .limit(50)
    .build()
)
```

### `Self` en classmethods y factories

```python
from typing import Self
from dataclasses import dataclass

@dataclass
class Asset:
    name: str
    file_path: str
    asset_type: str

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> Self:    # retorna la subclase correcta
        return cls(
            name=data["name"],
            file_path=data["file_path"],
            asset_type=data["type"],
        )

class VideoAsset(Asset):
    pass

# from_dict en VideoAsset retorna VideoAsset, no Asset ✅
video = VideoAsset.from_dict({"name": "video.mp4", "file_path": "/media/v.mp4", "type": "video"})
```

---

## 5. Covarianza y contravarianza (introducción)

Estos conceptos definen en qué dirección se puede "sustituir" un tipo genérico.

### Covariante — "produce" el tipo (out)

```python
from typing import TypeVar

T_co = TypeVar("T_co", covariant=True)

class Producer(Generic[T_co]):
    def produce(self) -> T_co: ...   # solo retorna T, no recibe
```

Si `Dog` es subclase de `Animal`, entonces `Producer[Dog]` es subclase de `Producer[Animal]` ✅

### Contravariante — "consume" el tipo (in)

```python
T_contra = TypeVar("T_contra", contravariant=True)

class Consumer(Generic[T_contra]):
    def consume(self, item: T_contra) -> None: ...   # solo recibe T, no retorna
```

Si `Dog` es subclase de `Animal`, entonces `Consumer[Animal]` es subclase de `Consumer[Dog]` ✅

### Regla práctica

| Uso del tipo | Varianza |
|-------------|----------|
| Solo retornar (leer) | `covariant=True` |
| Solo recibir (escribir) | `contravariant=True` |
| Ambos | Invariante (default) |

Para el 90% del trabajo diario, no necesitas covarianza/contravarianza. Se usa principalmente en librerías y frameworks.

---

## ✅ Resumen

| Feature | Versión | Para qué |
|---------|---------|---------|
| `TypeVar` | 3.5+ | Variable de tipo para funciones/clases genéricas |
| `Generic[T]` | 3.5+ | Clase genérica explícita |
| `class Foo[T]:` | 3.12+ | Clase genérica con sintaxis moderna |
| `def f[T]():` | 3.12+ | Función genérica con sintaxis moderna |
| `Self` | 3.11+ | Retorno de la misma clase (fluent API, factories) |
| `covariant` | 3.5+ | Varianza para tipos de solo lectura |

---

## 📚 Recursos Adicionales

- [PEP 673 — Self Type](https://peps.python.org/pep-0673/)
- [PEP 695 — Type Parameter Syntax](https://peps.python.org/pep-0695/)
- [mypy — Generics](https://mypy.readthedocs.io/en/stable/generics.html)
