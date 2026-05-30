"""
Ejercicio 01 — Transcodificación básica

Contexto: Studio BC recibe videos en distintos formatos y necesita
estandarizarlos a H.264 para distribución web y H.265 para archivo.

Instrucciones:
1. Completá `transcode_h264()` — H.264 CRF 23, preset slow, AAC 128k
2. Completá `transcode_h265()` — H.265 CRF 28, preset medium, AAC 128k
3. Completá `to_prores()` — ProRes 422 HQ con audio PCM
4. Completá `get_file_size_mb()` — tamaño del archivo en MB

Prerequisito: ffmpeg instalado en el sistema (sudo apt install ffmpeg)
Instalar: pip install ffmpeg-python
"""

from pathlib import Path
import ffmpeg


def transcode_h264(src: Path, dest: Path, crf: int = 23) -> Path:
    """Transcodifica a H.264 con CRF dado, preset slow, AAC 128k."""
    # TODO:
    # ffmpeg.input(str(src))
    # .output(str(dest), vcodec="libx264", crf=crf, preset="slow",
    #         acodec="aac", audio_bitrate="128k", movflags="+faststart")
    # .run(overwrite_output=True, quiet=True)
    raise NotImplementedError


def transcode_h265(src: Path, dest: Path, crf: int = 28) -> Path:
    """Transcodifica a H.265/HEVC con CRF dado."""
    # TODO: similar a h264 pero vcodec="libx265"
    # Agregar **{"x265-params": "log-level=error"} para suprimir logs
    raise NotImplementedError


def to_prores(src: Path, dest: Path, profile: int = 3) -> Path:
    """
    Transcodifica a ProRes.
    profile: 0=proxy, 1=lt, 2=standard, 3=hq, 4=4444
    """
    # TODO: vcodec="prores_ks", profile_v=profile, acodec="pcm_s16le"
    raise NotImplementedError


def get_file_size_mb(path: Path) -> float:
    """Retorna el tamaño del archivo en MB."""
    # TODO: path.stat().st_size / (1024 * 1024)
    raise NotImplementedError


# ── Crear video de muestra ────────────────────────────────────────────────────
def create_test_video(dest: Path, duration: int = 5) -> Path:
    """Crea un video de prueba con tono de color sólido."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    (
        ffmpeg
        .input("color=c=blue:size=1280x720:rate=25", f="lavfi", t=duration)
        .output(str(dest), vcodec="libx264", crf=18, pix_fmt="yuv420p")
        .run(overwrite_output=True, quiet=True)
    )
    return dest


if __name__ == "__main__":
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        src = create_test_video(Path(tmp) / "test.mp4")
        print(f"Fuente: {get_file_size_mb(src):.2f} MB")

        h264 = transcode_h264(src, Path(tmp) / "h264.mp4")
        print(f"H.264: {get_file_size_mb(h264):.2f} MB")

        h265 = transcode_h265(src, Path(tmp) / "h265.mp4")
        print(f"H.265: {get_file_size_mb(h265):.2f} MB (esperado: < H.264)")

        print("✓ Transcodificación completada")
