"""
Ejercicio 03 — Renombrador Automático con Naming Convention

Contexto: Studio BC recibió archivos con nombres inconsistentes.
Hay que aplicar la convención: {cliente}_{proyecto}_{tipo}_{fecha}_{version}.{ext}

Instrucciones:
1. Completá `MediaFilename.parse()` usando el regex provisto
2. Completá `slugify()` — convierte texto libre a slug (minúscula, guiones)
3. Completá `auto_rename()` — renombra archivos no conformes con defaults
4. Completá `audit_and_rename()` — aplica auto_rename a todos los no conformes

Los archivos YA conformes no deben modificarse.
"""

import re
from dataclasses import dataclass
from datetime import date
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
        # TODO: aplicar FILENAME_PATTERN.match(filename)
        # Si no hay match, retornar None
        # Si hay match, retornar cls(**m.groupdict())
        raise NotImplementedError

    def canonical(self) -> str:
        return f"{self.client}_{self.project}_{self.tipo}_{self.date}_{self.version}.{self.ext}"


def slugify(text: str) -> str:
    """Convierte texto libre a slug: minúscula, solo alfanumérico y guiones."""
    # TODO: text.lower(), re.sub para reemplazar [^a-z0-9]+ por "-", strip("-")
    raise NotImplementedError


def guess_tipo(stem: str) -> str:
    """Intenta inferir el tipo desde el nombre del archivo."""
    stem_lower = stem.lower()
    if any(k in stem_lower for k in ("raw", "bruto", "original")):
        return "raw"
    if any(k in stem_lower for k in ("final", "master", "entrega")):
        return "final"
    return "edit"


def auto_rename(path: Path, client: str, project: str) -> Path:
    """Renombra un archivo no conforme. Retorna el nuevo path."""
    # TODO:
    # 1. Si ya es conforme (MediaFilename.parse no es None), retornar path sin cambios
    # 2. Calcular today = date.today().strftime("%Y%m%d")
    # 3. tipo = guess_tipo(path.stem)
    # 4. ext = path.suffix.lower().lstrip(".")
    # 5. Construir new_name = f"{client}_{project}_{tipo}_{today}_v001.{ext}"
    # 6. Resolver colisiones con contador
    # 7. path.rename(new_path), retornar new_path
    raise NotImplementedError


def audit_and_rename(folder: Path, client: str, project: str) -> tuple[list[Path], list[Path]]:
    """
    Retorna (renamed, skipped):
    - renamed: archivos que fueron renombrados
    - skipped: archivos ya conformes
    """
    # TODO: iterar folder.glob("*"), aplicar auto_rename a no conformes
    raise NotImplementedError


# ── Muestra ───────────────────────────────────────────────────────────────────
def create_sample(folder: Path) -> None:
    folder.mkdir(exist_ok=True)
    names = [
        "canal9_spot-verano_raw_20240315_v001.mp4",  # conforme
        "FINAL_spot verano OK.mp4",
        "entrega_master_v2.mov",
        "raw bruto original canal9.wav",
        "brief_cliente.pdf",
    ]
    for n in names:
        (folder / n).write_bytes(b"\x00")


if __name__ == "__main__":
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp) / "entregables"
        create_sample(folder)

        renamed, skipped = audit_and_rename(folder, "canal9", "spot-verano")
        print(f"Renombrados: {len(renamed)}, Sin cambios: {len(skipped)}")
        for p in renamed:
            print(f"  → {p.name}")
