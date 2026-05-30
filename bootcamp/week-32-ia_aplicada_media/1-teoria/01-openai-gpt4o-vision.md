# OpenAI API y GPT-4o Vision

## 1. Setup del Cliente

```python
from openai import OpenAI

client = OpenAI()  # lee OPENAI_API_KEY del entorno
```

---

## 2. Chat Completions — Texto

```python
from openai import OpenAI

client = OpenAI()


def ask(prompt: str, model: str = "gpt-4o-mini") -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.3,  # más bajo = más determinista
    )
    return response.choices[0].message.content or ""
```

---

## 3. GPT-4o Vision — Análisis de Imágenes

### Opción A: imagen en base64 (archivo local)

```python
import base64
from pathlib import Path


def encode_image(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("utf-8")


def analyze_image(image_path: Path, prompt: str = "Describe esta imagen.") -> str:
    b64 = encode_image(image_path)
    ext = image_path.suffix.lower().replace(".", "")
    mime = f"image/{ext}" if ext in {"jpg", "jpeg", "png", "webp", "gif"} else "image/jpeg"

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}},
            ],
        }],
        max_tokens=1000,
    )
    return response.choices[0].message.content or ""
```

### Opción B: URL pública

```python
def analyze_image_url(url: str, prompt: str = "Describe esta imagen.") -> str:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": url}},
            ],
        }],
        max_tokens=1000,
    )
    return response.choices[0].message.content or ""
```

---

## 4. Salida Estructurada con JSON

Para obtener respuestas parseable, pedir JSON explícitamente en el prompt:

```python
import json


def analyze_image_structured(image_path: Path) -> dict[str, object]:
    b64 = encode_image(image_path)
    prompt = """Analiza esta imagen y responde SOLO con JSON válido (sin markdown):
{
  "description": "descripción detallada del contenido visual",
  "topic": "tema principal del contenido",
  "category": "una de: entrevista, documental, publicidad, evento, deportes, otro",
  "mood": "tono emocional: profesional, alegre, dramático, neutral, etc.",
  "suggested_tags": ["tag1", "tag2", "tag3"]
}"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
            ],
        }],
        max_tokens=500,
        response_format={"type": "json_object"},  # fuerza JSON válido
    )
    return json.loads(response.choices[0].message.content or "{}")
```

`response_format={"type": "json_object"}` garantiza que GPT devuelva JSON parseable.

---

## 5. Extraer Frames de un Video para Análisis

```python
import subprocess
from pathlib import Path


def extract_frames(video_path: Path, output_dir: Path, interval_s: int = 10) -> list[Path]:
    """Extrae un frame cada `interval_s` segundos con ffmpeg."""
    output_dir.mkdir(parents=True, exist_ok=True)
    pattern = output_dir / "frame_%04d.jpg"

    subprocess.run([
        "ffmpeg", "-i", str(video_path),
        "-vf", f"fps=1/{interval_s}",
        "-q:v", "3",
        str(pattern),
        "-y",
    ], check=True, capture_output=True)

    return sorted(output_dir.glob("frame_*.jpg"))


def analyze_video_frames(video_path: Path, n_frames: int = 5) -> list[dict[str, object]]:
    """Analiza N frames distribuidos a lo largo del video."""
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        frames = extract_frames(video_path, Path(tmp), interval_s=10)
        selected = frames[::max(1, len(frames) // n_frames)][:n_frames]
        return [analyze_image_structured(f) for f in selected]
```

---

## 6. Costos y Throttling

| Modelo | Input | Output | Imágenes |
|--------|-------|--------|----------|
| `gpt-4o` | $2.50/1M tokens | $10/1M tokens | según resolución |
| `gpt-4o-mini` | $0.15/1M tokens | $0.60/1M tokens | más barato |

Para producción con muchos assets, usar `gpt-4o-mini` para tagging y `gpt-4o` para descripciones finales.

---

## Resumen

| Operación | API |
|-----------|-----|
| Texto simple | `chat.completions.create(messages=[{"content": "texto"}])` |
| Análisis de imagen | content = `[{"type": "text", ...}, {"type": "image_url", ...}]` |
| Imagen local | `data:image/jpeg;base64,{b64}` |
| JSON forzado | `response_format={"type": "json_object"}` |
| Modelo barato | `gpt-4o-mini` para volumen alto |
