# Proxies y Extracción de Contenido

## Objetivos

- Generar proxies de baja resolución para edición no destructiva
- Extraer clips por timecode
- Extraer thumbnails/stills en frames específicos
- Separar audio de un video

---

## 1. ¿Qué es un proxy?

Un **proxy** es una versión de menor calidad y resolución del video original, usada para edición en tiempo real. El editor trabaja sobre el proxy (fluido) y al exportar se sustituye por el original (alta calidad).

Resoluciones proxy estándar:
- `1/4` de la original (4K → 1080p, 1080p → 270p)
- Codificado en H.264 rápido para decodificación fluida
- Mismo timecode y duración que el original

---

## 2. Generar proxy

```python
import ffmpeg
from pathlib import Path

def generate_proxy(src: Path, dest_dir: Path, scale_factor: float = 0.25) -> Path:
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / f"{src.stem}_proxy.mp4"

    inp = ffmpeg.input(str(src))

    # Escalar al factor indicado preservando aspect ratio
    # -2 en el alto: ffmpeg calcula el valor par más cercano
    scaled = inp.video.filter("scale", f"iw*{scale_factor}", -2)

    out = ffmpeg.output(
        scaled,
        inp.audio,
        str(dest),
        vcodec="libx264",
        crf=23,
        preset="veryfast",   # velocidad > calidad para proxy
        acodec="aac",
        audio_bitrate="96k",
    )
    out.run(overwrite_output=True, quiet=True)
    return dest
```

---

## 3. Extraer clip por timecode

```python
import ffmpeg
from pathlib import Path

def extract_clip(
    src: Path,
    dest: Path,
    start: str,
    end: str,
) -> Path:
    """
    Extrae un clip entre start y end (formato "HH:MM:SS" o "HH:MM:SS.mmm").
    Usa -ss antes de -i (seek rápido) y -to para el punto de fin.
    """
    dest.parent.mkdir(parents=True, exist_ok=True)
    (
        ffmpeg
        .input(str(src), ss=start, to=end)
        .output(
            str(dest),
            vcodec="libx264",
            crf=18,
            acodec="aac",
            audio_bitrate="128k",
        )
        .run(overwrite_output=True, quiet=True)
    )
    return dest

# Uso
extract_clip(
    Path("programa.mp4"),
    Path("clips/entrevista.mp4"),
    start="00:05:30",
    end="00:12:45",
)
```

---

## 4. Extraer thumbnail (still frame)

```python
import ffmpeg
from pathlib import Path

def extract_thumbnail(src: Path, dest: Path, at_second: float = 5.0) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    (
        ffmpeg
        .input(str(src), ss=at_second)
        .output(str(dest), vframes=1)   # solo 1 frame
        .run(overwrite_output=True, quiet=True)
    )
    return dest

def extract_thumbnails_grid(
    src: Path,
    dest_dir: Path,
    every_seconds: int = 60,
) -> list[Path]:
    """Extrae un thumbnail cada N segundos."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    pattern = str(dest_dir / "thumb_%04d.jpg")
    (
        ffmpeg
        .input(str(src))
        .filter("fps", fps=f"1/{every_seconds}")
        .output(pattern, qscale_v=2)
        .run(overwrite_output=True, quiet=True)
    )
    return sorted(dest_dir.glob("thumb_*.jpg"))
```

---

## 5. Separar audio de video

```python
import ffmpeg
from pathlib import Path

def extract_audio(src: Path, dest: Path, codec: str = "aac") -> Path:
    """Extrae la pista de audio del video."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    (
        ffmpeg
        .input(str(src))
        .audio
        .output(str(dest), acodec=codec, audio_bitrate="192k")
        .run(overwrite_output=True, quiet=True)
    )
    return dest

def split_video_audio(src: Path, dest_dir: Path) -> tuple[Path, Path]:
    """Separa video (sin audio) y audio (sin video) en archivos distintos."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    video_dest = dest_dir / f"{src.stem}_noaudio.mp4"
    audio_dest = dest_dir / f"{src.stem}.aac"

    inp = ffmpeg.input(str(src))
    v_out = ffmpeg.output(inp.video, str(video_dest), vcodec="copy", an=None)
    a_out = ffmpeg.output(inp.audio, str(audio_dest), acodec="aac", vn=None)
    ffmpeg.run([v_out, a_out], overwrite_output=True, quiet=True)

    return video_dest, audio_dest
```

---

## ✅ Resumen

| Operación | ffmpeg-python |
|-----------|--------------|
| Proxy (25% resolución) | `filter("scale", "iw*0.25", -2)` |
| Clip por timecode | `input(src, ss=start, to=end)` |
| Thumbnail en segundo N | `input(src, ss=N)` + `output(..., vframes=1)` |
| Thumbnails cada N seg | `filter("fps", fps="1/N")` |
| Extraer audio | `.audio.output(dest, acodec="aac")` |
