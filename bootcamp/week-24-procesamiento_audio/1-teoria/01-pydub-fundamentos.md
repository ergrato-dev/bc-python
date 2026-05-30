# pydub — Fundamentos

## Objetivos

- Cargar y guardar audio en distintos formatos con `AudioSegment`
- Cortar y concatenar segmentos de audio
- Inspeccionar propiedades: duración, canales, sample rate, loudness
- Entender el modelo de datos de pydub (muestras en dBFS)

---

## 1. Prerequisito: ffmpeg

pydub usa ffmpeg como backend para codecs. Instalar antes de usar:

```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Verificar
ffmpeg -version
```

---

## 2. Cargar y guardar

```python
from pydub import AudioSegment
from pathlib import Path

# Cargar
audio = AudioSegment.from_file("entrevista.mp3")
audio_wav = AudioSegment.from_wav("musica.wav")
audio_flac = AudioSegment.from_file("master.flac", format="flac")

# Propiedades
print(audio.duration_seconds)      # 183.5
print(audio.frame_rate)            # 44100 (Hz)
print(audio.channels)              # 2 (stereo) / 1 (mono)
print(audio.sample_width)          # 2 (bytes por muestra = 16 bit)
print(audio.dBFS)                  # -14.3 (loudness media en dBFS)
print(len(audio))                  # 183500 (duración en ms)

# Guardar
audio.export("salida.mp3", format="mp3", bitrate="192k")
audio.export("salida.wav", format="wav")
audio.export("salida.flac", format="flac")
audio.export("salida.ogg", format="ogg", codec="libvorbis")
audio.export(
    "salida.mp3",
    format="mp3",
    bitrate="320k",
    tags={"title": "Spot Verano", "artist": "Studio BC"},
)
```

---

## 3. Cortar y concatenar

pydub usa milisegundos para los índices:

```python
# Cortar: [inicio_ms:fin_ms]
primer_minuto = audio[:60_000]       # primeros 60 segundos
segundo_minuto = audio[60_000:120_000]
ultimos_30s = audio[-30_000:]         # últimos 30 segundos

# Concatenar con +
intro = AudioSegment.from_file("intro.wav")
musica = AudioSegment.from_file("musica.mp3")
final = intro + musica

# Repetir
loop = musica * 3  # repetir 3 veces

# Silencio
silencio = AudioSegment.silent(duration=1000)  # 1 segundo de silencio
with_pause = primer_minuto + silencio + segundo_minuto
```

---

## 4. Overlay (mezcla)

```python
from pydub import AudioSegment

voz = AudioSegment.from_file("voz.wav")
musica = AudioSegment.from_file("musica.mp3")

# Bajar volumen de la música para fondo
musica_fondo = musica - 20  # -20 dB

# Superponer: musica_fondo como fondo durante toda la voz
# position=0: la música empieza al inicio
mezcla = voz.overlay(musica_fondo, position=0)

# Si la música es más corta, loop=True la repite automáticamente
mezcla = voz.overlay(musica_fondo, loop=True)

mezcla.export("entrega_final.mp3", bitrate="192k")
```

---

## 5. Mono y stereo

```python
# Convertir a mono
mono = audio.set_channels(1)

# Convertir a stereo
stereo = audio.set_channels(2)

# Cambiar sample rate
resampled = audio.set_frame_rate(44100)

# Cambiar profundidad de bits
audio_16bit = audio.set_sample_width(2)   # 16 bit
audio_24bit = audio.set_sample_width(3)   # 24 bit
```

---

## 6. Trabajar con numpy

Para análisis numérico, convertir a numpy array:

```python
import numpy as np
from pydub import AudioSegment

audio = AudioSegment.from_file("audio.wav")

# Convertir a numpy array (valores -32768 a 32767 para 16 bit)
samples = np.array(audio.get_array_of_samples())

# Para stereo: reshape
if audio.channels == 2:
    samples = samples.reshape((-1, 2))

print(samples.shape)  # (n_samples, 2) para stereo
print(samples.dtype)  # int16

# Convertir de vuelta a AudioSegment
audio_back = AudioSegment(
    samples.tobytes(),
    frame_rate=audio.frame_rate,
    sample_width=audio.sample_width,
    channels=audio.channels,
)
```

---

## ✅ Resumen

| Operación | API |
|-----------|-----|
| Cargar | `AudioSegment.from_file(path)` |
| Guardar | `.export(path, format="mp3", bitrate="192k")` |
| Cortar | `audio[inicio_ms:fin_ms]` |
| Concatenar | `seg1 + seg2` |
| Silencio | `AudioSegment.silent(duration_ms)` |
| Mezclar | `base.overlay(other, position=ms)` |
| Volumen | `audio + N_dB` / `audio - N_dB` |
| Duración | `len(audio)` (ms) / `.duration_seconds` |
