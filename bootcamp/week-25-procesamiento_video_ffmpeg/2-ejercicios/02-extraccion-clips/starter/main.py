"""
Ejercicio 02 — Extracción de clips, thumbnails y audio

Contexto: El editor necesita extraer segmentos específicos de un programa
largo y obtener thumbnails para la web.

Instrucciones:
1. Completá `extract_clip()` — extrae entre start y end por timecode
2. Completá `extract_thumbnail()` — guarda 1 frame como JPG
3. Completá `extract_audio()` — extrae audio a AAC
4. Completá `extract_thumbnails_at_intervals()` — 1 thumbnail cada N segundos
"""

from pathlib import Path
import ffmpeg


def extract_clip(src: Path, dest: Path, start: str, end: str) -> Path:
    """
    Extrae clip entre start y end (formato "HH:MM:SS" o segundos como float).
    Usa seek antes de -i para mayor velocidad.
    """
    # TODO: ffmpeg.input(str(src), ss=start, to=end)
    # .output(str(dest), vcodec="libx264", crf=18, acodec="aac")
    # .run(overwrite_output=True, quiet=True)
    raise NotImplementedError


def extract_thumbnail(src: Path, dest: Path, at_second: float = 5.0) -> Path:
    """Extrae 1 frame del video en at_second como imagen JPG."""
    # TODO: ffmpeg.input(str(src), ss=at_second)
    # .output(str(dest), vframes=1)
    # .run(overwrite_output=True, quiet=True)
    raise NotImplementedError


def extract_audio(src: Path, dest: Path) -> Path:
    """Extrae la pista de audio del video a un archivo separado."""
    # TODO: ffmpeg.input(str(src)).audio
    # .output(str(dest), acodec="aac", audio_bitrate="192k")
    # .run(overwrite_output=True, quiet=True)
    raise NotImplementedError


def extract_thumbnails_at_intervals(
    src: Path, dest_dir: Path, every_seconds: int = 10
) -> list[Path]:
    """Extrae 1 thumbnail cada every_seconds segundos."""
    # TODO: .filter("fps", fps=f"1/{every_seconds}")
    # .output(pattern, qscale_v=2)
    # retornar lista de paths generados
    raise NotImplementedError


# ── Crear video de muestra ────────────────────────────────────────────────────
def create_test_video(dest: Path, duration: int = 30) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    (
        ffmpeg
        .input("color=c=red:size=1280x720:rate=25", f="lavfi", t=duration)
        .output(str(dest), vcodec="libx264", crf=28, pix_fmt="yuv420p")
        .run(overwrite_output=True, quiet=True)
    )
    return dest


if __name__ == "__main__":
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        src = create_test_video(Path(tmp) / "programa.mp4", duration=30)
        print(f"Video de {30}s creado")

        clip = extract_clip(src, Path(tmp) / "clip.mp4", start="5", end="15")
        print(f"Clip extraído: {clip.exists()}")

        thumb = extract_thumbnail(src, Path(tmp) / "thumb.jpg", at_second=10.0)
        print(f"Thumbnail: {thumb.exists()}, {thumb.stat().st_size} bytes")

        audio = extract_audio(src, Path(tmp) / "audio.aac")
        print(f"Audio: {audio.exists()}, {audio.stat().st_size} bytes")

        thumbs = extract_thumbnails_at_intervals(src, Path(tmp) / "thumbs", every_seconds=10)
        print(f"Thumbnails cada 10s: {len(thumbs)} imágenes")
        print("✓ Extracciones completadas")
