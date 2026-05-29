# 📋 Rúbrica de Evaluación — Semana 15: Python Moderno Avanzado

> **Puntaje total: 100 puntos** · Mínimo para aprobar: **70 puntos**

---

## 1. Conocimiento 🧠 — 30 puntos

### 1.1 Protocol y subtipado estructural (10 pts)

| Indicador | Puntos |
|-----------|--------|
| Explica la diferencia entre subtipado nominal (herencia) y estructural (Protocol) | 4 |
| Puede identificar cuándo usar `Protocol` vs `ABC` | 3 |
| Comprende por qué `Protocol` no requiere herencia explícita en las clases que lo implementan | 3 |

### 1.2 Structural Pattern Matching (10 pts)

| Indicador | Puntos |
|-----------|--------|
| Explica qué es un guard (`if`) dentro de un `case` | 3 |
| Diferencia entre captura de variable y comparación de valor en `match` | 4 |
| Identifica cuándo `match` es mejor opción que `if/elif` encadenados | 3 |

### 1.3 Dataclasses y type system (10 pts)

| Indicador | Puntos |
|-----------|--------|
| Explica el beneficio de `__slots__` en dataclasses | 3 |
| Describe para qué sirve `__post_init__` | 3 |
| Comprende la diferencia entre `TypeGuard` y un `isinstance` regular | 4 |

---

## 2. Desempeño 💪 — 40 puntos

### 2.1 Ejercicios completados (20 pts)

| Ejercicio | Puntos | Criterio |
|-----------|--------|---------|
| 01-protocols | 5 | Protocol definido correctamente, clases sin herencia explícita |
| 02-pattern-matching | 5 | Todos los `case` con tipos correctos, al menos un guard |
| 03-dataclasses | 5 | `__slots__`, `__post_init__` y `field()` usados correctamente |
| 04-typeguard | 5 | `TypeGuard` retorna `bool`, narrowing funciona en el bloque `if` |

### 2.2 Calidad del código (20 pts)

| Indicador | Puntos |
|-----------|--------|
| Todos los tipos anotados (sin `Any` implícito) | 5 |
| Sin errores de mypy con `--strict` | 5 |
| Nombres de variables y funciones en inglés, snake_case | 5 |
| Código ejecuta sin errores ni warnings | 5 |

---

## 3. Producto 📦 — 30 puntos

### 3.1 Proyecto: Modelado Studio BC (30 pts)

| Indicador | Puntos |
|-----------|--------|
| `Nameable`, `Describable` y `Timestamped` definidos como Protocols | 6 |
| Entidades `Client`, `Project`, `Phase`, `Deliverable`, `Asset` implementadas como dataclasses | 8 |
| `Asset` usa `__slots__` y `frozen=True` | 4 |
| `Project.__post_init__` valida que la fecha de inicio sea anterior a la de fin | 4 |
| `TypeGuard` para al menos una función de validación de tipo (`is_video_asset`, etc.) | 4 |
| Sin errores de mypy `--strict` en `src/models.py` | 4 |

---

## Criterios de Aprobación

- ✅ Mínimo **21/30** en Conocimiento
- ✅ Mínimo **28/40** en Desempeño
- ✅ Mínimo **21/30** en Producto
- ✅ Todos los ejercicios ejecutan sin errores en Python 3.13+
- ✅ El archivo `src/models.py` del proyecto pasa `mypy --strict`
