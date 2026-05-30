"""
Ejercicio 03 — Filtros: escala, recorte y watermark de texto

Contexto: Studio BC necesita preparar videos en múltiples formatos:
vertical para Instagram Reels, cuadrado para feed, y web con watermark.

Instrucciones:
1. Completá `scale_video()` — escala preservando aspect ratio
2. Completá `crop_center_square()` — recorta un cuadrado central
3. Completá `add_text_watermark()` — texto en esquina inferior derecha
4. Completá `prepare_for_social()` — genera las 3 variantes de una sola vez
"""

from pathlib import Path
import ffmpeg


def scale_video(src: Path, dest: Path, width: int, height: int = -2) -> Path:
    """
    Escala el video a width×height.
    height=-2: calcula el alto preservando aspect ratio (valor par).
    """
    # TODO: inp.video.filter("scale", width, height)
    raise NotImplementedError


def crop_center_square(src: Path, dest: Path) -> Path:
    """
    Recorta el menor lado para obtener un video cuadrado centrado.
    Usa crop con min(iw,ih) para ambos lados.
    """
    # TODO: filter("crop", "min(iw,ih)", "min(iw,ih)",
    #              "(iw-min(iw,ih))/2", "(ih-min(iw,ih))/2")
    raise NotImplementedError


def add_text_watermark(
    src: Path,
    dest: Path,
    text: str = "© Studio BC",
    opacity: float = 0.7,
) -> Path:
    """Agrega texto en la esquina inferior derecha con opacidad dada."""
    # TODO: filter("drawtext", text=text,
    #              fontsize=24, fontcolor=f"white@{opacity}",
    #              x="w-text_w-15", y="h-text_h-15",
    #              shadowx=2, shadowy=2)
    raise NotImplementedError


def prepare_for_social(src: Path, dest_dir: Path) -> dict[str, Path]:
    """
    Genera 3 variantes:
    - "web": 1280×720, con watermark
    - "square": cuadrado 1080×1080, sin watermark
    - "vertical": 608×1080 (recortado desde landscape), sin watermark
    Retorna dict {nombre: path}
    """
    # TODO: llamar las funciones anteriores para cada variante
    raise NotImplementedError


# ── Crear video de muestra ────────────────────────────────────────────────────
def create_test_video(dest: Path, duration: int = 5) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    (
        ffmpeg
        .input("color=c=green:size=1920x1080:rate=25", f="lavfi", t=duration)
        .output(str(dest), vcodec="libx264", crf=28, pix_fmt="yuv420p")
        .run(overwrite_output=True, quiet=True)
    )
    return dest


if __name__ == "__main__":
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        src = create_test_video(Path(tmp) / "source_1080p.mp4")
        out = Path(tmp) / "output"
        out.mkdir()

        scaled = scale_video(src, out / "720p.mp4", width=1280)
        print(f"Escalado 720p: {scaled.exists()}")

        square = crop_center_square(src, out / "square.mp4")
        print(f"Cuadrado: {square.exists()}")

        watermarked = add_text_watermark(src, out / "watermark.mp4")
        print(f"Watermark: {watermarked.exists()}")

        variants = prepare_for_social(src, out / "social")
        print(f"Variantes generadas: {list(variants.keys())}")
        print("✓ Filtros aplicados correctamente")
