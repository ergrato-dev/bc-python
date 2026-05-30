# Transcripción con Whisper

## Objetivos

- Entender qué es Whisper y cómo funciona localmente
- Transcribir audio con timestamps por segmento
- Elegir el modelo según velocidad/accuracy
- Pre-procesar audio para mejorar la transcripción

---

## 1. Qué es Whisper

Whisper es un modelo de reconocimiento de voz automático (ASR) de OpenAI entrenado en 680.000 horas de audio multilingüe. Funciona completamente **local** — no requiere API key ni conexión a internet.

Instalación:
```bash
pip install openai-whisper
# Requiere ffmpeg instalado en el sistema
```

---

## 2. Modelos disponibles

| Modelo | Parámetros | VRAM | Velocidad | Accuracy |
|--------|-----------|------|-----------|----------|
| `tiny` | 39M | ~1 GB | Muy rápida | Básica |
| `base` | 74M | ~1 GB | Rápida | Buena |
| `small` | 244M | ~2 GB | Media | Muy buena |
| `medium` | 769M | ~5 GB | Lenta | Excelente |
| `large` | 1550M | ~10 GB | Muy lenta | Máxima |

Para producción con CPU: `base` o `small`. Con GPU: `medium` o `large`.

---

## 3. Transcripción básica

```python
import whisper

# Cargar modelo (se descarga la primera vez, ~150MB para base)
model = whisper.load_model("base")

# Transcribir
result = model.transcribe("entrevista.mp3")

print(result["text"])       # texto completo
print(result["language"])   # "es" para español

# Segmentos con timestamps
for seg in result["segments"]:
    start = seg["start"]   # float en segundos
    end   = seg["end"]
    text  = seg["text"].strip()
    print(f"[{start:.2f} → {end:.2f}] {text}")
```

---

## 4. Opciones de transcripción

```python
import whisper

model = whisper.load_model("small")

result = model.transcribe(
    "audio.mp3",
    language="es",          # forzar idioma español (más rápido y preciso)
    task="transcribe",      # "transcribe" o "translate" (→ inglés)
    fp16=False,             # False en CPU (True en GPU)
    verbose=False,          # suprimir output del progreso
    initial_prompt="Studio BC producción audiovisual",  # contexto para mejorar accuracy
    word_timestamps=True,   # timestamps por palabra (requiere modelo >= small)
)
```

---

## 5. Pre-procesar audio antes de transcribir

Whisper funciona mejor con audio normalizado y sin ruido de fondo:

```python
from pathlib import Path
from pydub import AudioSegment
from pydub.effects import normalize
import whisper
import tempfile

def transcribe_preprocessed(audio_path: Path, model_name: str = "base") -> dict:
    # 1. Cargar y pre-procesar con pydub
    audio = AudioSegment.from_file(str(audio_path))
    audio = audio.set_channels(1)           # mono (Whisper lo prefiere)
    audio = audio.set_frame_rate(16000)     # 16 kHz (sample rate nativo de Whisper)
    audio = normalize(audio, headroom=1.0)  # normalizar volumen

    # 2. Exportar a WAV temporal
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        tmp = Path(f.name)
    audio.export(str(tmp), format="wav")

    # 3. Transcribir
    model = whisper.load_model(model_name)
    result = model.transcribe(str(tmp), language="es", fp16=False)

    # 4. Limpiar
    tmp.unlink()
    return result
```

---

## 6. Transcripción con SpeechRecognition (alternativa ligera)

Para casos simples sin GPU ni modelo local pesado:

```python
import speech_recognition as sr

recognizer = sr.Recognizer()
with sr.AudioFile("clip.wav") as source:
    audio_data = recognizer.record(source)

# Google Web Speech API (gratis, requiere internet)
text = recognizer.recognize_google(audio_data, language="es-AR")
print(text)
```

SpeechRecognition es útil para clips cortos. Para transcripciones largas o sin conexión, usar Whisper.

---

## ✅ Resumen

| Aspecto | Recomendación |
|---------|--------------|
| Modelo para CPU | `base` o `small` |
| Modelo para GPU | `medium` o `large` |
| Pre-procesar | Mono, 16 kHz, normalizado |
| Forzar idioma | `language="es"` (más rápido) |
| Con timestamps | `result["segments"]` |
| Alternativa ligera | `SpeechRecognition` + Google API |
