# 🎬 Proyecto Semana 15: Modelado de Entidades Studio BC

## 📋 Descripción

Construir el modelo de dominio completo de **Studio BC** usando todo lo aprendido esta semana: Protocols, dataclasses avanzadas, Generics y TypeGuard. Este modelo será la base sobre la que se construirán todas las semanas siguientes de la Fase 2.

---

## 🎯 Objetivos

- Definir los Protocols que describen los contratos de cada entidad
- Implementar todas las entidades como dataclasses tipadas y optimizadas
- Crear funciones TypeGuard para clasificación en runtime
- Garantizar que el código pasa `mypy --strict` sin errores

---

## 🗂️ Estructura del Proyecto

```
3-proyecto/starter/
├── src/
│   ├── __init__.py
│   ├── models.py          # Protocols + Dataclasses (implementar)
│   └── validators.py      # TypeGuard + funciones de validación (implementar)
├── main.py                # Script de demostración (no modificar)
└── pyproject.toml
```

---

## 📐 Especificación

### Protocols a definir en `src/models.py`

```python
# Protocols base del dominio
class Nameable(Protocol): ...        # tiene .name: str
class Describable(Protocol): ...     # tiene .description: str
class Timestamped(Protocol): ...     # tiene .created_at: datetime
class Identifiable(Protocol): ...    # tiene .id: int
```

### Entidades a implementar en `src/models.py`

#### `Client`
```
Atributos:
  id: int                      — keyword-only
  name: str
  email: str                   — validar con __post_init__
  phone: str                   — default ""
  active: bool                 — default True
  created_at: datetime         — auto, no en repr
Requisitos:
  - __post_init__ valida email (debe tener @ y .)
  - __post_init__ normaliza email a lowercase
  - slots=True
```

#### `Project`
```
Atributos:
  id: int                      — keyword-only
  name: str
  client_id: int               — keyword-only
  description: str             — default ""
  start_date: date
  end_date: date
  budget: float
  tags: list[str]              — default_factory
  created_at: datetime         — auto, no en repr
Requisitos:
  - __post_init__ valida que end_date > start_date
  - __post_init__ valida que budget > 0
  - __post_init__ calcula slug (name lowercase, espacios → guiones)
  - slug: str — campo calculado (init=False)
  - slots=True
```

#### `Phase`
```
Atributos:
  id: int                      — keyword-only
  name: str
  project_id: int              — keyword-only
  order: int                   — posición en el proyecto (1-based)
  description: str             — default ""
  completed: bool              — default False
Requisitos:
  - frozen=True (las fases no se modifican, se reemplazan)
  - slots=True
```

#### `Deliverable`
```
Atributos:
  id: int                      — keyword-only
  name: str
  phase_id: int                — keyword-only
  description: str             — default ""
  due_date: date
  approved: bool               — default False
  created_at: datetime         — auto, no en repr
Requisitos:
  - slots=True
```

#### `Asset`
```
Atributos:
  id: int                      — keyword-only
  name: str
  file_path: str               — keyword-only
  asset_type: str              — "video" | "image" | "audio" | "document"
  size_mb: float               — default 0.0
  project_id: int | None       — default None, keyword-only
  metadata: dict[str, str]     — default_factory
  created_at: datetime         — auto, no en repr
Requisitos:
  - __post_init__ valida que asset_type esté en {"video","image","audio","document"}
  - slots=True
```

### Funciones TypeGuard en `src/validators.py`

```python
def is_video_asset(asset: Asset) -> TypeGuard[Asset]:
    """True si asset_type == 'video'"""

def is_image_asset(asset: Asset) -> TypeGuard[Asset]:
    """True si asset_type == 'image'"""

def is_uploadable(obj: object) -> TypeGuard[Asset]:
    """True si obj es Asset con file_path no vacío"""

def is_active_project(obj: object) -> TypeGuard[Project]:
    """True si obj es Project con end_date >= hoy"""
```

---

## 📊 Criterios de Evaluación

| Criterio | Puntos |
|----------|--------|
| Protocols correctamente definidos (Nameable, Describable, Timestamped, Identifiable) | 6 |
| Las 5 entidades implementadas con todos sus requisitos | 8 |
| `Asset` y `Phase` con `slots=True`, `Phase` con `frozen=True` | 4 |
| `__post_init__` con validación real que lanza excepciones | 4 |
| 4 funciones TypeGuard implementadas y funcionando | 4 |
| `mypy --strict src/` pasa sin errores | 4 |

**Total: 30 puntos**

---

## 🚀 Cómo ejecutar

```bash
cd starter/

# Instalar dependencias
uv sync

# Ejecutar la demo
uv run python main.py

# Verificar tipos
uv run mypy --strict src/
```

---

## 💡 Pistas

- Para `slug`, usa `self.name.lower().replace(" ", "-")` en `__post_init__`
- `field(init=False)` para atributos calculados en `__post_init__`
- `field(default_factory=datetime.now, repr=False, compare=False)` para timestamps
- Recuerda importar `KW_ONLY` de `dataclasses`
