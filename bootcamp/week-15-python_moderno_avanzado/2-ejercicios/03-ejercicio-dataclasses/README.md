# 🏗️ Ejercicio 03: Dataclasses Avanzadas

## 🎯 Objetivo

Construir las entidades `Client` y `Asset` de Studio BC usando las características avanzadas de dataclasses: `field()`, `__post_init__`, `KW_ONLY` y `slots`.

---

## Paso 1: `field()` — defaults seguros y metadatos

```python
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Client:
    name: str
    email: str
    tags: list[str] = field(default_factory=list)      # ✅ nunca compartido
    created_at: datetime = field(default_factory=datetime.now, repr=False)
```

**Abre `starter/main.py`** y descomenta la sección **PASO 1**.  
Ejecuta el código y verifica que dos clientes con tags diferentes no comparten la lista.

---

## Paso 2: `__post_init__` — validación

```python
def __post_init__(self) -> None:
    if "@" not in self.email:
        raise ValueError(f"invalid email: {self.email!r}")
    self.email = self.email.lower().strip()
```

**Descomenta la sección PASO 2** y prueba con un email inválido.

---

## Paso 3: `KW_ONLY` — argumentos keyword obligatorios

```python
from dataclasses import KW_ONLY

@dataclass
class Asset:
    name: str
    _: KW_ONLY
    file_path: str
    asset_type: str
    size_mb: float = 0.0
```

Con `KW_ONLY`, `file_path` y `asset_type` deben pasarse con su nombre:

```python
# ✅
Asset("video.mp4", file_path="/media/v.mp4", asset_type="video")
# ❌ TypeError
Asset("video.mp4", "/media/v.mp4", "video")
```

**Descomenta la sección PASO 3.**

---

## Paso 4: `slots=True` — comparar uso de memoria

```python
import sys

@dataclass
class AssetNormal:
    name: str
    file_path: str

@dataclass(slots=True)
class AssetSlots:
    name: str
    file_path: str

n = AssetNormal("v.mp4", "/media/v.mp4")
s = AssetSlots("v.mp4", "/media/v.mp4")
print(sys.getsizeof(n.__dict__))   # mayor
# s no tiene __dict__
```

**Descomenta la sección PASO 4** y observa la diferencia de tamaño.

---

## ✅ Resultado esperado

```
=== PASO 1: field() ===
Client 1 tags: ['vip', 'activo']
Client 2 tags: []     ← listas independientes ✅

=== PASO 2: __post_init__ ===
Email normalizado: contact@acme.com
ValueError capturado: invalid email: 'no-es-email'  ✅

=== PASO 3: KW_ONLY ===
Asset: video_hero.mp4 → /media/hero.mp4 (video, 245.0 MB)
TypeError capturado: Asset no acepta posicionales después de KW_ONLY ✅

=== PASO 4: slots ===
__dict__ de AssetNormal: ~232 bytes
AssetSlots no tiene __dict__ ✅
```
