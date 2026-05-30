# Subtítulos SRT y WebVTT

## Objetivos

- Entender el formato SRT y WebVTT
- Generar archivos `.srt` y `.vtt` desde segmentos de Whisper
- Manejar múltiples líneas y límites de caracteres
- Validar y depurar archivos de subtítulos

---

## 1. Formato SRT

SRT (SubRip Text) es el formato más universal. Cada bloque tiene: número, timestamps y texto.

```
1
00:00:01,280 --> 00:00:04,720
Bienvenidos a Studio BC.
Hoy presentamos nuestro nuevo spot.

2
00:00:05,100 --> 00:00:08,340
Este proyecto fue desarrollado
para Canal 9.
```

Reglas:
- Timestamps: `HH:MM:SS,mmm` (coma como separador de milisegundos)
- Separador `-->` con espacios
- Línea en blanco entre bloques

---

## 2. Formato WebVTT

WebVTT es el estándar para HTML5 `<video>` y YouTube. Muy similar a SRT con pequeñas diferencias:

```
WEBVTT

00:00:01.280 --> 00:00:04.720
Bienvenidos a Studio BC.

00:00:05.100 --> 00:00:08.340
Este proyecto fue desarrollado para Canal 9.
```

Diferencias con SRT:
- Encabezado `WEBVTT` obligatorio
- Punto como separador de milisegundos (no coma)
- No requiere número de bloque (opcional)

---

## 3. Convertir segundos a timestamp

```python
def seconds_to_srt_time(seconds: float) -> str:
    total_ms = int(seconds * 1000)
    ms = total_ms % 1000
    total_s = total_ms // 1000
    s = total_s % 60
    total_m = total_s // 60
    m = total_m % 60
    h = total_m // 60
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def seconds_to_vtt_time(seconds: float) -> str:
    # Igual que SRT pero con punto en lugar de coma
    return seconds_to_srt_time(seconds).replace(",", ".")

print(seconds_to_srt_time(65.283))   # "00:01:05,283"
print(seconds_to_vtt_time(65.283))   # "00:01:05.283"
```

---

## 4. Generar SRT desde segmentos de Whisper

```python
from pathlib import Path

def generate_srt(segments: list[dict], output: Path) -> Path:
    lines = []
    for i, seg in enumerate(segments, start=1):
        start = seconds_to_srt_time(seg["start"])
        end   = seconds_to_srt_time(seg["end"])
        text  = seg["text"].strip()
        lines.append(f"{i}")
        lines.append(f"{start} --> {end}")
        lines.append(text)
        lines.append("")  # línea en blanco entre bloques
    output.write_text("\n".join(lines), encoding="utf-8")
    return output

# Uso con Whisper
import whisper
model = whisper.load_model("base")
result = model.transcribe("entrevista.mp3", language="es", fp16=False)
srt_path = generate_srt(result["segments"], Path("entrevista.srt"))
```

---

## 5. Generar WebVTT

```python
from pathlib import Path

def generate_vtt(segments: list[dict], output: Path) -> Path:
    lines = ["WEBVTT", ""]
    for seg in segments:
        start = seconds_to_vtt_time(seg["start"])
        end   = seconds_to_vtt_time(seg["end"])
        text  = seg["text"].strip()
        lines.append(f"{start} --> {end}")
        lines.append(text)
        lines.append("")
    output.write_text("\n".join(lines), encoding="utf-8")
    return output
```

---

## 6. Dividir líneas largas

Los reproductores recomiendan un máximo de 42 caracteres por línea y 2 líneas por bloque:

```python
import textwrap

def wrap_subtitle_text(text: str, max_chars: int = 42) -> str:
    lines = textwrap.wrap(text, width=max_chars)
    return "\n".join(lines[:2])  # máximo 2 líneas

def generate_srt_wrapped(segments: list[dict], output: Path, max_chars: int = 42) -> Path:
    lines = []
    for i, seg in enumerate(segments, start=1):
        start = seconds_to_srt_time(seg["start"])
        end   = seconds_to_srt_time(seg["end"])
        text  = wrap_subtitle_text(seg["text"].strip(), max_chars)
        lines.extend([str(i), f"{start} --> {end}", text, ""])
    output.write_text("\n".join(lines), encoding="utf-8")
    return output
```

---

## 7. Parsear un SRT existente

Para modificar o convertir subtítulos ya existentes:

```python
import re
from dataclasses import dataclass

@dataclass
class SubtitleBlock:
    index: int
    start: str
    end: str
    text: str

SRT_BLOCK = re.compile(
    r"(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n([\s\S]+?)(?=\n\n|\Z)"
)

def parse_srt(path: str) -> list[SubtitleBlock]:
    content = open(path, encoding="utf-8").read()
    blocks = []
    for m in SRT_BLOCK.finditer(content):
        blocks.append(SubtitleBlock(
            index=int(m.group(1)),
            start=m.group(2),
            end=m.group(3),
            text=m.group(4).strip(),
        ))
    return blocks
```

---

## ✅ Resumen

| Tarea | Función |
|-------|---------|
| Segundos → SRT timestamp | `seconds_to_srt_time(s)` → `HH:MM:SS,mmm` |
| Segundos → VTT timestamp | `seconds_to_vtt_time(s)` → `HH:MM:SS.mmm` |
| Generar SRT | `generate_srt(segments, path)` |
| Generar VTT | `generate_vtt(segments, path)` |
| Dividir líneas largas | `textwrap.wrap(text, width=42)` |
| Parsear SRT | regex con `re.compile()` |
