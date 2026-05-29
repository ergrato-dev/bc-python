# 🔬 Ejercicio 01: Protocols en Studio BC

## 🎯 Objetivo

Definir Protocols para modelar contratos de tipo sin herencia y aplicarlos a entidades del estudio audiovisual.

---

## Paso 1: Definir los Protocols base

Los Protocols definen *qué debe tener* un objeto, sin importar de dónde venga.

```python
from typing import Protocol
from datetime import datetime

class Nameable(Protocol):
    @property
    def name(self) -> str: ...

class Timestamped(Protocol):
    @property
    def created_at(self) -> datetime: ...

class Describable(Protocol):
    @property
    def description(self) -> str: ...
```

**Abre `starter/main.py`** y descomenta la sección **PASO 1**.

---

## Paso 2: Crear clases que implementen los Protocols (sin herencia)

Las clases satisfacen los Protocols simplemente teniendo los atributos correctos:

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Client:
    name: str
    email: str
    created_at: datetime = field(default_factory=datetime.now)

# Client satisface Nameable y Timestamped automáticamente ✅
```

**Descomenta la sección PASO 2.**

---

## Paso 3: Funciones que aceptan Protocols

Una función que acepta `Nameable` funciona con *cualquier* objeto que tenga `name`:

```python
def display_name(item: Nameable) -> str:
    return f"[{item.name}]"

# Funciona con Client, Project, Asset — sin herencia común ✅
```

**Descomenta la sección PASO 3** y observa que `display_name` acepta todos los tipos.

---

## Paso 4: `@runtime_checkable` y `isinstance`

```python
from typing import runtime_checkable, Protocol

@runtime_checkable
class Nameable(Protocol):
    @property
    def name(self) -> str: ...

# Ahora puedes usar isinstance en runtime
print(isinstance(Client("Acme", "acme@example.com"), Nameable))  # True
```

**Descomenta la sección PASO 4** y verifica el resultado.

---

## ✅ Resultado esperado

```
=== PASO 1: Protocols definidos ✅ ===
=== PASO 2: Entidades creadas ✅ ===
[Acme Corp]
[Campaña Navidad]
[video_hero.mp4]
=== PASO 3: display_name funciona con Client, Project y Asset ✅ ===
Client es Nameable en runtime: True
Asset es Nameable en runtime: True
str no es Nameable en runtime: False
=== PASO 4: @runtime_checkable ✅ ===
```
