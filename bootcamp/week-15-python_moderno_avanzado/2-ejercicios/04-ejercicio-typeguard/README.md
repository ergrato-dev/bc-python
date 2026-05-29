# 🔍 Ejercicio 04: TypeGuard y Narrowing

## 🎯 Objetivo

Usar `TypeGuard` para crear funciones de validación que informan al type checker del tipo exacto de un objeto, habilitando narrowing en el bloque `if`.

---

## Paso 1: El problema sin TypeGuard

```python
def process_items(items: list[object]) -> None:
    for item in items:
        if hasattr(item, "name") and hasattr(item, "file_path"):
            print(item.name)      # ❌ mypy error: object has no attribute 'name'
```

mypy no puede saber que `hasattr` garantiza el tipo. **Descomenta la sección PASO 1** y observa el comentario de error.

---

## Paso 2: TypeGuard — solución

```python
from typing import TypeGuard

def is_asset(obj: object) -> TypeGuard[Asset]:
    return (
        isinstance(obj, dict) is False
        and hasattr(obj, "name")
        and hasattr(obj, "file_path")
        and hasattr(obj, "asset_type")
    )
```

Ahora el type checker sabe que si `is_asset(item)` es `True`, entonces `item` es `Asset`:

```python
def process_items(items: list[object]) -> None:
    for item in items:
        if is_asset(item):
            print(item.name)       # ✅ mypy OK — item es Asset aquí
            print(item.file_path)  # ✅
```

**Descomenta la sección PASO 2.**

---

## Paso 3: TypeGuard para discriminar tipos

```python
def is_video(asset: Asset) -> TypeGuard[VideoAsset]:
    return isinstance(asset, VideoAsset)

def is_image(asset: Asset) -> TypeGuard[ImageAsset]:
    return isinstance(asset, ImageAsset)

def route_to_pipeline(asset: Asset) -> str:
    if is_video(asset):
        return f"video pipeline: {asset.codec}"   # ✅ asset es VideoAsset
    if is_image(asset):
        return f"image pipeline: {asset.width}x{asset.height}"  # ✅ asset es ImageAsset
    return "default pipeline"
```

**Descomenta la sección PASO 3.**

---

## Paso 4: TypeGuard vs isinstance

Cuando las condiciones son más complejas que un `isinstance` simple, `TypeGuard` es la solución:

```python
def is_uploadable_asset(obj: object) -> TypeGuard[Asset]:
    if not hasattr(obj, "asset_type") or not hasattr(obj, "file_path"):
        return False
    file_path = getattr(obj, "file_path")
    return isinstance(file_path, str) and len(file_path) > 0
```

**Descomenta la sección PASO 4.**

---

## ✅ Resultado esperado

```
=== PASO 1: Sin TypeGuard — narrowing manual ===
sin TypeGuard, mypy no puede verificar el tipo dentro del if

=== PASO 2: Con TypeGuard ===
Procesando 3 assets válidos de 5 objetos
name: video_hero.mp4 | path: /media/hero.mp4
name: banner.png     | path: /media/banner.png
name: jingle.mp3     | path: /media/jingle.mp3

=== PASO 3: TypeGuard para discriminar tipos ===
video pipeline: h264
image pipeline: 1920x1080

=== PASO 4: TypeGuard con validación compleja ===
2 de 3 objetos son uploadables ✅
```
