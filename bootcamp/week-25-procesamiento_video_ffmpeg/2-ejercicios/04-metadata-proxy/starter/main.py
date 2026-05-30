"""
Ejercicio 04 — Metadata con ffprobe y generación de Proxy

Contexto: Antes de procesar cada video, el estudio necesita saber
qué codec usa, su resolución y duración. Luego genera un proxy liviano.

Instrucciones:
1. Completá `ffprobe_json()` — ejecuta ffprobe y retorna el JSON parseado
2. Completá `get_video_info()` — extrae campos clave del JSON de ffprobe
3. Completá `generate_proxy()` — genera proxy al 25% de la resolución original
4. Completá `save_metadata_json()` — guarda el dict de info como .json

Prerequisito: ffmpeg/ffprobe instalados
"""

import json
import subprocess
from pathlib import Path
import ffmpeg


def ffprobe_json(path: Path) -> dict:
    """Ejecuta ffprobe -show_streams -show_format y retorna el JSON."""
    # TODO: subprocess.run(["ffprobe", "-v", "quiet", "-print_format", "json",
    #                        "-show_streams", "-show_format", str(path)],
    #                       capture_output=True, text=True, check=True)
    # return json.loads(result.stdout)
    raise NotImplementedError


def get_video_info(path: Path) -> dict[str, object]:
    """
    Retorna dict con: path, duration_s, size_bytes, bitrate_bps,
    video_codec, width, height, fps, audio_codec, sample_rate.
    """
    # TODO: usar ffprobe_json(), buscar stream con codec_type == "video"
    # y stream con codec_type == "audio"
    # fps: parsear avg_frame_rate como "num/den"
    raise NotImplementedError


def generate_proxy(src: Path, dest_dir: Path, scale: float = 0.25) -> Path:
    """Genera proxy escalado al factor dado (default 25% de la resolución)."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / f"{src.stem}_proxy.mp4"
    # TODO:
    # inp = ffmpeg.input(str(src))
    # v = inp.video.filter("scale", f"iw*{scale}", -2)
    # ffmpeg.output(v, inp.audio, str(dest), vcodec="libx264", crf=23,
    #               preset="veryfast", acodec="aac", audio_bitrate="96k")
    # .run(overwrite_output=True, quiet=True)
    raise NotImplementedError


def save_metadata_json(info: dict[str, object], dest: Path) -> Path:
    """Guarda el dict como JSON en dest."""
    # TODO: dest.write_text(json.dumps(info, indent=2, ensure_ascii=False))
    raise NotImplementedError


# ── Crear video de muestra ────────────────────────────────────────────────────
def create_test_video(dest: Path, width: int = 1920, height: int = 1080) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    (
        ffmpeg
        .input(f"color=c=purple:size={width}x{height}:rate=25", f="lavfi", t=5)
        .output(str(dest), vcodec="libx264", crf=23, pix_fmt="yuv420p")
        .run(overwrite_output=True, quiet=True)
    )
    return dest


if __name__ == "__main__":
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        src = create_test_video(Path(tmp) / "raw.mp4")

        info = get_video_info(src)
        print("=== Metadata ===")
        for k, v in info.items():
            print(f"  {k}: {v}")

        assert info["video_codec"] == "h264"
        assert info["width"] == 1920
        assert info["height"] == 1080
        assert info["fps"] == 25.0

        json_path = save_metadata_json(info, Path(tmp) / "meta" )
        print(f"\nMetadata guardada: {json_path}")

        proxy = generate_proxy(src, Path(tmp) / "proxy")
        proxy_info = get_video_info(proxy)
        print(f"\nProxy: {proxy_info['width']}×{proxy_info['height']}")
        assert proxy_info["width"] == 480  # 1920 * 0.25
        print("✓ Metadata y proxy OK")
