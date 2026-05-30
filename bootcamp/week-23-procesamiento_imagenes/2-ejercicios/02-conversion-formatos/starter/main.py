"""
Ejercicio 02 — Conversión de Formatos y EXIF

Contexto: El estudio recibe fotos en distintos formatos y necesita:
- Convertir todo a WebP para reducir peso en web
- Extraer metadatos EXIF (fecha, ISO) para registrarlos
- Eliminar EXIF de imágenes públicas para proteger privacidad

Instrucciones:
1. Completá `to_webp()` — convierte cualquier imagen a WebP con calidad dada
2. Completá `extract_exif_info()` — retorna dict con fecha y ISO si están disponibles
3. Completá `strip_exif()` — guarda imagen sin metadatos EXIF
4. Completá `batch_convert()` — convierte un directorio entero a WebP
"""

from pathlib import Path
from PIL import Image


def to_webp(src: Path, dest: Path, quality: int = 85) -> Path:
    """Convierte src a WebP con la calidad dada. Retorna dest."""
    # TODO: Image.open(src), convert("RGB"), save(dest, "WEBP", quality=quality)
    raise NotImplementedError


def extract_exif_info(src: Path) -> dict[str, str]:
    """
    Retorna dict con claves disponibles: "date", "iso", "make", "model".
    Retorna {} si no hay EXIF o no está disponible piexif.
    """
    try:
        import piexif
    except ImportError:
        return {}

    # TODO:
    # piexif.load(str(src)) → exif_dict
    # exif_dict["Exif"].get(piexif.ExifIFD.DateTimeOriginal) → bytes → decode
    # exif_dict["Exif"].get(piexif.ExifIFD.ISOSpeedRatings) → int
    # exif_dict["0th"].get(piexif.ImageIFD.Make) → bytes → decode
    raise NotImplementedError


def strip_exif(src: Path, dest: Path) -> Path:
    """Guarda una copia de src en dest sin datos EXIF."""
    # TODO: abrir imagen, reconstruir con putdata(), guardar sin exif
    # img = Image.open(src)
    # data = list(img.getdata())
    # clean = Image.new(img.mode, img.size)
    # clean.putdata(data)
    raise NotImplementedError


def batch_convert(folder: Path, dest_dir: Path, quality: int = 85) -> list[Path]:
    """Convierte todos los JPG/PNG de folder a WebP en dest_dir."""
    # TODO: rglob para .jpg, .jpeg, .png; llamar to_webp para cada uno
    raise NotImplementedError


# ── Muestra ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import tempfile

    # Crear imagen de muestra
    src_img = Image.new("RGB", (800, 600), color=(100, 150, 200))
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        src = tmp_path / "test.jpg"
        src_img.save(src, quality=90)

        # to_webp
        webp = to_webp(src, tmp_path / "test.webp")
        print(f"WebP: {webp.stat().st_size} bytes (vs JPG: {src.stat().st_size} bytes)")

        # extract_exif_info
        info = extract_exif_info(src)
        print(f"EXIF: {info or 'sin metadatos'}")

        # strip_exif
        clean = strip_exif(src, tmp_path / "clean.jpg")
        print(f"Sin EXIF guardado: {clean.exists()}")

        print("✓ Conversiones completadas")
