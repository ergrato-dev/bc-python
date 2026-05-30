# Metadata de Video con ffprobe y pymediainfo

## Objetivos

- Extraer metadata técnica de video con ffprobe (JSON)
- Usar pymediainfo como alternativa más estructurada
- Construir una función `get_video_info()` reutilizable
- Detectar codec, resolución, framerate, duración y bitrate

---

## 1. ffprobe desde Python

ffprobe es la herramienta de inspección de ffmpeg. Retorna JSON con información detallada:

```python
import subprocess
import json
from pathlib import Path

def ffprobe(path: Path) -> dict:
    result = subprocess.run(
        [
            "ffprobe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_streams",
            "-show_format",
            str(path),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)

data = ffprobe(Path("video.mp4"))
```

---

## 2. Extraer campos relevantes

```python
from pathlib import Path

def get_video_info(path: Path) -> dict[str, object]:
    data = ffprobe(path)

    # Buscar el stream de video
    video_stream = next(
        (s for s in data["streams"] if s["codec_type"] == "video"),
        None,
    )
    audio_stream = next(
        (s for s in data["streams"] if s["codec_type"] == "audio"),
        None,
    )
    fmt = data.get("format", {})

    info: dict[str, object] = {
        "path":       str(path),
        "duration_s": float(fmt.get("duration", 0)),
        "size_bytes":  int(fmt.get("size", 0)),
        "bitrate_bps": int(fmt.get("bit_rate", 0)),
    }

    if video_stream:
        # framerate como fracción "25/1" o "30000/1001"
        fps_str = video_stream.get("avg_frame_rate", "0/1")
        num, den = map(int, fps_str.split("/"))
        fps = num / den if den else 0

        info.update({
            "video_codec":  video_stream.get("codec_name"),
            "width":        video_stream.get("width"),
            "height":       video_stream.get("height"),
            "fps":          round(fps, 3),
            "pixel_format": video_stream.get("pix_fmt"),
        })

    if audio_stream:
        info.update({
            "audio_codec":   audio_stream.get("codec_name"),
            "sample_rate":   int(audio_stream.get("sample_rate", 0)),
            "audio_channels": audio_stream.get("channels"),
        })

    return info
```

---

## 3. pymediainfo — alternativa más amigable

```python
from pymediainfo import MediaInfo
from pathlib import Path

def get_info_pymediainfo(path: Path) -> dict[str, object]:
    media_info = MediaInfo.parse(str(path))
    info: dict[str, object] = {}

    for track in media_info.tracks:
        if track.track_type == "General":
            info["duration_s"]  = (track.duration or 0) / 1000
            info["file_size"]   = track.file_size
            info["format"]      = track.format

        elif track.track_type == "Video":
            info["video_codec"] = track.codec_id or track.format
            info["width"]       = track.width
            info["height"]      = track.height
            info["fps"]         = track.frame_rate
            info["bit_depth"]   = track.bit_depth

        elif track.track_type == "Audio":
            info["audio_codec"]    = track.format
            info["sample_rate"]    = track.sampling_rate
            info["audio_channels"] = track.channel_s

    return info
```

---

## 4. Validar un video antes de procesar

```python
from pathlib import Path

def validate_video(path: Path) -> tuple[bool, str]:
    """Retorna (is_valid, reason). Usa ffprobe para verificar."""
    try:
        info = get_video_info(path)
        if not info.get("video_codec"):
            return False, "No tiene stream de video"
        if (info.get("duration_s") or 0) < 0.5:
            return False, "Duración demasiado corta"
        return True, "OK"
    except (subprocess.CalledProcessError, KeyError, ValueError) as e:
        return False, f"No se pudo leer: {e}"
```

---

## 5. Guardar metadata como JSON

```python
import json
from pathlib import Path

def save_metadata(video_path: Path, dest_dir: Path) -> Path:
    info = get_video_info(video_path)
    dest_dir.mkdir(parents=True, exist_ok=True)
    json_path = dest_dir / f"{video_path.stem}_meta.json"
    json_path.write_text(json.dumps(info, indent=2, ensure_ascii=False))
    return json_path
```

---

## ✅ Resumen

| Necesidad | Herramienta |
|-----------|-------------|
| Metadata completa desde Python | `ffprobe` + `subprocess` + JSON |
| API más amigable | `pymediainfo` |
| Framerate (fracción) | `avg_frame_rate` → `num/den` |
| Duración | `format.duration` (segundos) |
| Validar video antes de procesar | `ffprobe` con try/except |
| Persistir metadata | `json.dumps()` → archivo `.json` |
