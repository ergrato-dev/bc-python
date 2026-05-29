# pathlib Avanzado

## Objetivos

- Dominar `Path.glob()` y `Path.rglob()` para búsquedas de archivos
- Realizar operaciones masivas: renombrar, mover, eliminar con seguridad
- Comparar árboles de directorios para detectar cambios
- Construir rutas de destino complejas de forma segura

---

## 1. Recordatorio: pathlib básico

```python
from pathlib import Path

p = Path("/media/studio/entregables/spot_verano.mp4")

p.name        # "spot_verano.mp4"
p.stem        # "spot_verano"
p.suffix      # ".mp4"
p.parent      # Path("/media/studio/entregables")
p.exists()    # True / False
p.is_file()   # True
p.is_dir()    # False
p.stat().st_size   # tamaño en bytes
```

---

## 2. glob() vs rglob()

`glob(pattern)` — busca en el directorio actual:
```python
root = Path("/media/studio/entregables")

# Todos los .mp4 directamente en la carpeta
for f in root.glob("*.mp4"):
    print(f)

# Patrón con un nivel de profundidad
for f in root.glob("*/raw/*.mp4"):
    print(f)
```

`rglob(pattern)` — búsqueda recursiva (equivale a `**/pattern`):
```python
# Todos los .mp4 en cualquier subdirectorio
for f in root.rglob("*.mp4"):
    print(f)

# Todos los archivos de imagen
MEDIA_IMAGES = {"*.jpg", "*.jpeg", "*.png", "*.tiff", "*.webp"}
images = [f for ext in MEDIA_IMAGES for f in root.rglob(ext)]
```

Diferencia clave:

| Método | Búsqueda | Uso típico |
|--------|----------|------------|
| `glob("*.mp4")` | Solo directorio actual | Carpeta plana de entregables |
| `glob("**/*.mp4")` | Recursiva (explícita) | Equivalente a rglob |
| `rglob("*.mp4")` | Recursiva (implícita) | Árbol de proyectos |

---

## 3. Operaciones masivas

### Rename por lote

```python
from pathlib import Path

def batch_rename(folder: Path, old_suffix: str, new_suffix: str) -> list[Path]:
    renamed = []
    for f in folder.glob(f"*{old_suffix}"):
        new_name = f.with_suffix(new_suffix)
        f.rename(new_name)
        renamed.append(new_name)
    return renamed

# .jpeg → .jpg
batch_rename(Path("entregables/fotos"), ".jpeg", ".jpg")
```

### Mover con shutil (cross-device seguro)

`Path.rename()` falla en movimientos entre dispositivos distintos (ej: disco → NAS). Usar `shutil.move()` para moverlos de forma segura:

```python
import shutil
from pathlib import Path

def move_file(src: Path, dst_dir: Path) -> Path:
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / src.name
    if dst.exists():
        stem, suffix = src.stem, src.suffix
        counter = 1
        while dst.exists():
            dst = dst_dir / f"{stem}_{counter:03d}{suffix}"
            counter += 1
    shutil.move(str(src), dst)
    return dst
```

### Copiar preservando metadatos

```python
import shutil

shutil.copy2(src, dst)    # copia contenido + metadatos (mtime, atime)
shutil.copyfile(src, dst) # solo contenido
```

---

## 4. Walk de árbol de directorios

```python
from pathlib import Path
from collections import defaultdict

def tree_summary(root: Path) -> dict[str, list[Path]]:
    # Agrupa archivos por extensión en todo el árbol
    by_ext: dict[str, list[Path]] = defaultdict(list)
    for f in root.rglob("*"):
        if f.is_file():
            by_ext[f.suffix.lower()].append(f)
    return dict(by_ext)

summary = tree_summary(Path("/media/studio"))
for ext, files in sorted(summary.items()):
    print(f"{ext:10} {len(files):4d} archivos")
```

---

## 5. Comparar dos árboles

```python
from pathlib import Path

def find_new_files(source: Path, reference: Path) -> list[Path]:
    # Retorna archivos en source que NO están en reference
    source_files = {f.relative_to(source) for f in source.rglob("*") if f.is_file()}
    ref_files = {f.relative_to(reference) for f in reference.rglob("*") if f.is_file()}
    return [source / rel for rel in source_files - ref_files]
```

---

## 6. Operaciones atómicas

Un renombrado dentro del mismo filesystem es **atómico** en Linux/macOS:

```python
# Escritura atómica: escribe en .tmp, luego renombra
tmp = Path("output.json.tmp")
tmp.write_text(json_data)
tmp.rename("output.json")  # atómico — nunca hay un archivo a medias
```

---

## ✅ Resumen

| Operación | API recomendada |
|-----------|-----------------|
| Buscar archivos | `Path.rglob(pattern)` |
| Renombrar en mismo disco | `Path.rename()` |
| Mover entre discos | `shutil.move()` |
| Copiar con metadatos | `shutil.copy2()` |
| Crear directorios anidados | `Path.mkdir(parents=True, exist_ok=True)` |
| Escritura atómica | escribe a `.tmp`, luego `rename()` |
