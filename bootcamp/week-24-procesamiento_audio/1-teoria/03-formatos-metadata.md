# Formatos de Audio y Metadata

## Objetivos

- Conocer las características de MP3, WAV, FLAC, OGG, AAC
- Convertir entre formatos preservando calidad
- Leer y escribir etiquetas ID3 con `mutagen`
- Extraer BPM básico con librosa

---

## 1. Comparativa de formatos

| Formato | Compresión | Calidad | Tamaño (3 min) | Uso |
|---------|-----------|---------|----------------|-----|
| WAV | Sin pérdida | Lossless | ~30 MB | Edición, master |
| FLAC | Sin pérdida | Lossless | ~15 MB | Archivo, distribución |
| MP3 | Con pérdida | 320k ≈ transparente | ~7 MB | Distribución, streaming |
| OGG | Con pérdida | Alta | ~5 MB | Juegos, web |
| AAC | Con pérdida | Alta (mejor que MP3) | ~5 MB | iOS, YouTube |

---

## 2. Conversión entre formatos

```python
from pydub import AudioSegment
from pathlib import Path

def convert_audio(src: Path, dest: Path, **export_kwargs: object) -> Path:
    audio = AudioSegment.from_file(str(src))
    fmt = dest.suffix.lstrip(".")
    audio.export(str(dest), format=fmt, **export_kwargs)
    return dest

# WAV → MP3 320k
convert_audio(Path("master.wav"), Path("dist.mp3"), bitrate="320k")

# WAV → FLAC (sin pérdida)
convert_audio(Path("master.wav"), Path("archivo.flac"))

# MP3 → WAV (para edición posterior)
convert_audio(Path("recibido.mp3"), Path("para_editar.wav"))

# Normalizar + convertir en una pasada
def normalized_export(src: Path, dest: Path, target_dbfs: float = -14.0) -> Path:
    from pydub.effects import normalize
    audio = AudioSegment.from_file(str(src))
    delta = target_dbfs - audio.dBFS
    normalized = audio.apply_gain(delta)
    normalized.export(str(dest), format=dest.suffix.lstrip("."))
    return dest
```

---

## 3. Metadatos ID3 con mutagen

ID3 es el sistema de etiquetas estándar para MP3. mutagen soporta también Vorbis comments (FLAC/OGG) y MP4 tags (AAC/M4A).

```python
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TDRC, TBPM, TCON

# Leer tags de un MP3
audio = MP3("track.mp3")
print(f"Duración: {audio.info.length:.1f}s")
print(f"Bitrate: {audio.info.bitrate} bps")
print(f"Canales: {audio.info.channels}")

tags = audio.tags
if tags:
    title  = str(tags.get("TIT2", ""))
    artist = str(tags.get("TPE1", ""))
    album  = str(tags.get("TALB", ""))
    year   = str(tags.get("TDRC", ""))
    bpm    = str(tags.get("TBPM", ""))
    print(f"{title} — {artist} ({year})")

# Escribir tags
tags = ID3()
tags["TIT2"] = TIT2(encoding=3, text="Spot Verano Canal 9")
tags["TPE1"] = TPE1(encoding=3, text="Studio BC")
tags["TALB"] = TALB(encoding=3, text="Producción 2024")
tags["TDRC"] = TDRC(encoding=3, text="2024")
tags["TBPM"] = TBPM(encoding=3, text="120")
tags["TCON"] = TCON(encoding=3, text="Jingle")
tags.save("track_tagged.mp3")
```

---

## 4. Metadatos para FLAC y OGG

```python
from mutagen.flac import FLAC
from mutagen.oggvorbis import OggVorbis

# FLAC (Vorbis Comments)
flac = FLAC("master.flac")
flac["title"] = ["Spot Verano"]
flac["artist"] = ["Studio BC"]
flac["bpm"] = ["120"]
flac.save()

# OGG Vorbis
ogg = OggVorbis("track.ogg")
ogg["title"] = ["Spot Verano"]
ogg["tracknumber"] = ["1"]
ogg.save()
```

---

## 5. Detección de BPM con librosa

```python
import librosa
import numpy as np

def detect_bpm(audio_path: str) -> float:
    # Cargar en mono con sample rate 22050 Hz (estándar librosa)
    y, sr = librosa.load(audio_path, sr=22050, mono=True)
    # tempo: BPM estimado (array con un elemento)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    return float(np.asarray(tempo).item())

bpm = detect_bpm("musica_fondo.mp3")
print(f"BPM estimado: {bpm:.1f}")
```

---

## ✅ Resumen

| Necesidad | Herramienta |
|-----------|-------------|
| Edición sin pérdida | WAV o FLAC |
| Distribución web | MP3 192k o AAC |
| Streaming | MP3 320k o FLAC |
| Tags MP3 | `mutagen.id3.ID3` |
| Tags FLAC | `mutagen.flac.FLAC` |
| Detectar BPM | `librosa.beat.beat_track()` |
