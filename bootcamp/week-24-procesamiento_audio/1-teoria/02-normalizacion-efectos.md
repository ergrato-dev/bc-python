# Normalización y Efectos

## Objetivos

- Normalizar loudness a un target dBFS estándar
- Aplicar fade in y fade out
- Detectar y eliminar segmentos de silencio
- Ajustar ganancia por secciones

---

## 1. dBFS y normalización

**dBFS** (decibeles relativos al Full Scale) es la unidad de amplitud en audio digital.
- 0 dBFS = nivel máximo sin clipping
- -14 dBFS = estándar de streaming (Spotify, YouTube)
- Valores más negativos = más silencioso

```python
from pydub import AudioSegment
from pydub.effects import normalize

audio = AudioSegment.from_file("entrevista.mp3")
print(f"Loudness original: {audio.dBFS:.1f} dBFS")

# Normalizar al nivel máximo (0 dBFS - headroom)
normalizado = normalize(audio, headroom=1.0)  # deja 1 dB de margen
print(f"Loudness normalizado: {normalizado.dBFS:.1f} dBFS")

# Normalizar a target específico (-14 dBFS para streaming)
def normalize_to_target(audio: AudioSegment, target_dbfs: float = -14.0) -> AudioSegment:
    delta = target_dbfs - audio.dBFS
    return audio.apply_gain(delta)

streaming_ready = normalize_to_target(audio, -14.0)
print(f"Para streaming: {streaming_ready.dBFS:.1f} dBFS")
```

---

## 2. Fade in y fade out

```python
from pydub import AudioSegment

audio = AudioSegment.from_file("spot.mp3")

# Fade in: primer segundo
con_fade_in = audio.fade_in(1000)  # 1000 ms = 1 segundo

# Fade out: último segundo
con_fade_out = audio.fade_out(2000)  # 2 segundos

# Ambos
con_fades = audio.fade_in(1000).fade_out(2000)

# Fade personalizado en una sección
# Bajar volumen gradualmente entre ms 10000 y 12000
sección = audio[10_000:12_000].fade(from_gain=0, to_gain=-20, start=0, end=2000)
```

---

## 3. Detección de silencio

```python
from pydub import AudioSegment
from pydub.silence import detect_silence, split_on_silence

audio = AudioSegment.from_file("entrevista.mp3")

# Detectar intervalos de silencio
# min_silence_len: duración mínima en ms para considerar silencio
# silence_thresh: umbral de dBFS por debajo del cual es "silencio"
silencios = detect_silence(
    audio,
    min_silence_len=500,    # 0.5 segundos de silencio mínimo
    silence_thresh=-40,     # -40 dBFS como umbral
)
# Retorna [(inicio_ms, fin_ms), ...]
for inicio, fin in silencios:
    print(f"Silencio: {inicio/1000:.1f}s → {fin/1000:.1f}s")

# Dividir en chunks removiendo silencios
chunks = split_on_silence(
    audio,
    min_silence_len=700,
    silence_thresh=-40,
    keep_silence=200,       # mantener 200 ms de silencio en los extremos
)
print(f"Segmentos detectados: {len(chunks)}")
for i, chunk in enumerate(chunks):
    chunk.export(f"segmento_{i:03d}.mp3", format="mp3")
```

---

## 4. Ajuste de ganancia por secciones

Para un audio con partes demasiado bajas o altas:

```python
from pydub import AudioSegment

def boost_quiet_sections(
    audio: AudioSegment,
    threshold_dbfs: float = -30.0,
    boost_db: float = 6.0,
    chunk_ms: int = 500,
) -> AudioSegment:
    result = AudioSegment.empty()
    for i in range(0, len(audio), chunk_ms):
        chunk = audio[i:i + chunk_ms]
        if chunk.dBFS < threshold_dbfs:
            chunk = chunk + boost_db
        result += chunk
    return result
```

---

## 5. Análisis de loudness por sección

```python
from pydub import AudioSegment

def loudness_profile(audio: AudioSegment, chunk_ms: int = 1000) -> list[float]:
    return [
        audio[i:i + chunk_ms].dBFS
        for i in range(0, len(audio), chunk_ms)
    ]

audio = AudioSegment.from_file("programa.mp3")
profile = loudness_profile(audio)
avg = sum(v for v in profile if v != float("-inf")) / len(profile)
print(f"Loudness promedio: {avg:.1f} dBFS")
print(f"Sección más baja: {min(profile):.1f} dBFS")
print(f"Sección más alta: {max(profile):.1f} dBFS")
```

---

## ✅ Resumen

| Efecto | API pydub |
|--------|-----------|
| Normalizar (máximo) | `pydub.effects.normalize(audio)` |
| Normalizar (target) | `audio.apply_gain(target - audio.dBFS)` |
| Fade in | `audio.fade_in(ms)` |
| Fade out | `audio.fade_out(ms)` |
| Detectar silencios | `detect_silence(audio, min_silence_len, silence_thresh)` |
| Dividir por silencios | `split_on_silence(audio, ...)` |
| Ajustar ganancia | `audio + N_dB` / `audio.apply_gain(N)` |
