# Naming Conventions para Producción Audiovisual

## Objetivos

- Entender por qué la nomenclatura consistente es crítica en producción
- Definir y aplicar una convención con regex
- Construir un renombrador automático robusto
- Detectar y corregir nombres no conformes

---

## 1. Por qué importa la nomenclatura

En un estudio audiovisual, los archivos se procesan por múltiples personas y sistemas. Un nombre como `final_definitivo_v3_BUENO.mp4` provoca:
- Confusión sobre qué versión es la correcta
- Imposibilidad de ordenar cronológicamente
- Scripts que no pueden parsear metadata del nombre

---

## 2. La convención Studio BC

Formato: `{cliente}_{proyecto}_{tipo}_{fecha}_{version}.{ext}`

Ejemplos:
```
canal9_spot-verano_raw_20240315_v001.mp4
trademax_corto-institucional_edit_20240420_v003.mov
bcstudio_demo-reel_final_20240501_v001.prores
```

Reglas:
- `cliente`: slug en minúscula, sin espacios (`canal9`, `trademax`)
- `proyecto`: slug con guiones, sin underscores (`spot-verano`)
- `tipo`: `raw` | `edit` | `grade` | `final` | `export`
- `fecha`: `YYYYMMDD`
- `version`: `v` + 3 dígitos (`v001`, `v023`)
- extensión: siempre en minúscula

---

## 3. Regex para validar y parsear

```python
import re
from dataclasses import dataclass
from pathlib import Path

FILENAME_PATTERN = re.compile(
    r"^(?P<client>[a-z0-9]+)"
    r"_(?P<project>[a-z0-9][a-z0-9-]*)"
    r"_(?P<tipo>raw|edit|grade|final|export)"
    r"_(?P<date>\d{8})"
    r"_(?P<version>v\d{3})"
    r"\.(?P<ext>[a-z0-9]+)$"
)

@dataclass
class MediaFilename:
    client: str
    project: str
    tipo: str
    date: str
    version: str
    ext: str

    @classmethod
    def parse(cls, filename: str) -> "MediaFilename | None":
        m = FILENAME_PATTERN.match(filename)
        if not m:
            return None
        return cls(**m.groupdict())

    def canonical(self) -> str:
        return f"{self.client}_{self.project}_{self.tipo}_{self.date}_{self.version}.{self.ext}"

# Uso
name = MediaFilename.parse("canal9_spot-verano_raw_20240315_v001.mp4")
assert name is not None
print(name.canonical())  # canal9_spot-verano_raw_20240315_v001.mp4
```

---

## 4. Renombrador automático

Estrategia: intentar extraer componentes conocidos de nombres no conformes, aplicar defaults para lo desconocido.

```python
import re
from datetime import date
from pathlib import Path

def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")

def guess_tipo(stem: str) -> str:
    stem_lower = stem.lower()
    if any(k in stem_lower for k in ("raw", "bruto", "original")):
        return "raw"
    if any(k in stem_lower for k in ("edit", "edicion", "corte")):
        return "edit"
    if any(k in stem_lower for k in ("final", "master", "entrega")):
        return "final"
    return "edit"  # default

def auto_rename(path: Path, client: str, project: str) -> Path:
    # Renombra un archivo no conforme a la convención Studio BC
    today = date.today().strftime("%Y%m%d")
    tipo = guess_tipo(path.stem)
    ext = path.suffix.lower().lstrip(".")
    new_name = f"{client}_{project}_{tipo}_{today}_v001.{ext}"
    new_path = path.with_name(new_name)

    # Resolver colisiones
    counter = 1
    while new_path.exists():
        new_name = f"{client}_{project}_{tipo}_{today}_v{counter:03d}.{ext}"
        new_path = path.with_name(new_name)
        counter += 1

    path.rename(new_path)
    return new_path
```

---

## 5. Validar un lote de archivos

```python
from pathlib import Path

def audit_folder(folder: Path) -> tuple[list[Path], list[Path]]:
    # Retorna (conformes, no_conformes) para todos los archivos
    conformes: list[Path] = []
    no_conformes: list[Path] = []
    for f in folder.rglob("*"):
        if f.is_file():
            if MediaFilename.parse(f.name):
                conformes.append(f)
            else:
                no_conformes.append(f)
    return conformes, no_conformes
```

---

## ✅ Resumen

| Componente | Herramienta |
|------------|-------------|
| Validar nombre | `re.compile()` + named groups |
| Extraer metadata del nombre | `match.groupdict()` |
| Normalizar texto | `slugify()` custom |
| Resolver colisiones | sufijo numérico incremental |
| Renombrar | `Path.rename()` (mismo disco) |
