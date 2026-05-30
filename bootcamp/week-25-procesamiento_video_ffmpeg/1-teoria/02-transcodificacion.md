# Transcodificación de Video

## Objetivos

- Entender los codecs más usados en producción: H.264, H.265, AV1, ProRes
- Controlar calidad con CRF vs bitrate fijo
- Elegir el preset correcto para velocidad/calidad
- Construir perfiles de transcodificación reutilizables

---

## 1. Comparativa de codecs

| Codec | Nombre | Eficiencia | Compatibilidad | Uso |
|-------|--------|-----------|----------------|-----|
| H.264 / AVC | `libx264` | Media | Universal | Web, streaming, distribución |
| H.265 / HEVC | `libx265` | Alta (50% menos) | Buena (no IE) | Archivo, 4K, OTT |
| AV1 | `libaom-av1` | Muy alta | Creciente | YouTube, web moderno |
| ProRes | `prores_ks` | Baja (grande) | Profesional | Edición, masterizado |
| DNxHD | `dnxhd` | Baja (grande) | Avid | Post-producción |

---

## 2. CRF — Calidad Constante

CRF (Constant Rate Factor) controla la calidad sin fijar el bitrate. El codificador ajusta el bitrate según la complejidad de cada frame.

```python
import ffmpeg

def transcode_h264(src: str, dest: str, crf: int = 23) -> None:
    # CRF 0=lossless, 23=default, 51=peor calidad
    # Para streaming web: CRF 18-28
    # Para archivo: CRF 15-20
    (
        ffmpeg
        .input(src)
        .output(
            dest,
            vcodec="libx264",
            crf=crf,
            preset="slow",       # slow: mejor compresión, más tiempo
            acodec="aac",
            audio_bitrate="128k",
            movflags="+faststart",
        )
        .run(overwrite_output=True, quiet=True)
    )

def transcode_h265(src: str, dest: str, crf: int = 28) -> None:
    # H.265: mismo CRF = menor tamaño que H.264
    # CRF equivalente H.264/H.265: 23 ≈ 28
    (
        ffmpeg
        .input(src)
        .output(
            dest,
            vcodec="libx265",
            crf=crf,
            preset="medium",
            acodec="aac",
            audio_bitrate="128k",
            **{"x265-params": "log-level=error"},
        )
        .run(overwrite_output=True, quiet=True)
    )
```

---

## 3. Bitrate fijo (CBR/VBR)

Útil cuando hay un límite de tamaño de archivo o ancho de banda:

```python
import ffmpeg

def transcode_fixed_bitrate(src: str, dest: str, video_kbps: int = 2000) -> None:
    (
        ffmpeg
        .input(src)
        .output(
            dest,
            vcodec="libx264",
            video_bitrate=f"{video_kbps}k",
            maxrate=f"{video_kbps * 2}k",
            bufsize=f"{video_kbps * 4}k",
            acodec="aac",
            audio_bitrate="128k",
        )
        .run(overwrite_output=True, quiet=True)
    )
```

---

## 4. ProRes para post-producción

ProRes es el formato de archivo estándar en producción audiovisual profesional:

```python
import ffmpeg

PRORES_PROFILES = {
    "proxy":    0,   # ProRes 422 Proxy — edición offline
    "lt":       1,   # ProRes 422 LT
    "standard": 2,   # ProRes 422 — estándar producción
    "hq":       3,   # ProRes 422 HQ
    "4444":     4,   # ProRes 4444 — con alpha
}

def to_prores(src: str, dest: str, profile: str = "standard") -> None:
    (
        ffmpeg
        .input(src)
        .output(
            dest,
            vcodec="prores_ks",
            profile_v=PRORES_PROFILES[profile],
            acodec="pcm_s16le",   # audio PCM sin comprimir
        )
        .run(overwrite_output=True, quiet=True)
    )
```

---

## 5. Perfiles reutilizables

```python
from dataclasses import dataclass
from pathlib import Path
import ffmpeg

@dataclass(frozen=True)
class EncodeProfile:
    name: str
    vcodec: str
    crf: int
    preset: str
    acodec: str
    audio_bitrate: str
    ext: str

PROFILES: dict[str, EncodeProfile] = {
    "web":     EncodeProfile("web",     "libx264", 23, "fast",  "aac", "128k", ".mp4"),
    "archive": EncodeProfile("archive", "libx265", 22, "slow",  "aac", "192k", ".mp4"),
    "preview": EncodeProfile("preview", "libx264", 28, "veryfast", "aac", "96k",  ".mp4"),
}

def encode(src: Path, dest_dir: Path, profile: EncodeProfile) -> Path:
    dest = dest_dir / (src.stem + profile.ext)
    dest_dir.mkdir(parents=True, exist_ok=True)
    (
        ffmpeg
        .input(str(src))
        .output(
            str(dest),
            vcodec=profile.vcodec,
            crf=profile.crf,
            preset=profile.preset,
            acodec=profile.acodec,
            audio_bitrate=profile.audio_bitrate,
            movflags="+faststart",
        )
        .run(overwrite_output=True, quiet=True)
    )
    return dest
```

---

## ✅ Resumen

| Codec | Cuándo | CRF típico |
|-------|--------|------------|
| H.264 (libx264) | Web, distribución general | 18-28 |
| H.265 (libx265) | Archivo, 4K, tamaño reducido | 22-32 |
| AV1 | Web moderno, YouTube | 30-40 |
| ProRes | Post-producción, edición | Sin CRF |

Preset: `ultrafast` → `veryfast` → `fast` → `medium` → `slow` → `veryslow`
Más lento = mejor compresión al mismo CRF.
