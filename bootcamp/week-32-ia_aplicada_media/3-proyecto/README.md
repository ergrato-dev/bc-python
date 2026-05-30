# Proyecto Semana 32 — studio-ai-tagger

## Descripción

Módulo de IA que analiza un asset de video/audio/imagen de Studio BC y genera
automáticamente toda la metadata necesaria para su distribución:

- **title**: título SEO optimizado
- **description**: snippet + descripción completa
- **tags**: hasta 15 tags SEO
- **category**: categoría automática (publicidad, documental, etc.)
- **transcription**: texto completo con timestamps de segmentos
- **chapters**: capítulos con timestamps para YouTube/Vimeo
- **visual_analysis**: descripción del contenido visual (frames del video)

## Estructura

```
starter/
├── pyproject.toml
├── src/
│   ├── __init__.py
│   ├── config.py           # AIConfig desde .env (COMPLETE)
│   ├── vision.py           # FrameAnalyzer — GPT-4o Vision (TODO)
│   ├── transcriber.py      # AssetTranscriber — Whisper (TODO)
│   ├── tagger.py           # AutoTagger — tags + category (TODO)
│   ├── metadata.py         # MetadataGenerator — title + description (TODO)
│   ├── analyzer.py         # AssetAnalyzer — orquesta todo (COMPLETE)
│   └── __main__.py         # CLI: analyze, dry-run (COMPLETE)
└── tests/
    ├── __init__.py
    └── test_metadata.py    # Tests con mocks (TODO)
```

## Comandos

```bash
pip install -e .

# Analizar un video (requiere OPENAI_API_KEY)
python -m src analyze footage/spot_verano.mp4 --output metadata.json

# Modo dry-run (sin llamadas a la API)
python -m src analyze footage/spot_verano.mp4 --dry-run

# Tests
pytest tests/ -v
mypy --strict src/
```

## Configuración

```bash
export OPENAI_API_KEY=sk-...
export VISION_MODEL=gpt-4o        # para análisis de frames
export TEXT_MODEL=gpt-4o-mini     # para título, tags, descripción
export EMBEDDING_MODEL=text-embedding-3-small
```

## Tareas del Estudiante

### `vision.py` — `FrameAnalyzer`
- `extract_frames(video_path, n=5)`: extraer N frames con ffmpeg/ffprobe (o mock en dry_run)
- `analyze_frame(image_path)`: llamar a GPT-4o Vision con base64
- `analyze_video(video_path)`: orquestar extracción + análisis

### `transcriber.py` — `AssetTranscriber`
- `transcribe(audio_path)`: Whisper verbose_json con segmentos
- `extract_audio(video_path)`: ffmpeg para extraer audio del video
- `to_srt(segments)`: convertir segmentos a SRT

### `tagger.py` — `AutoTagger`
- `generate_tags(description, transcript)`: tags SEO con GPT
- `classify(description)`: categoría con GPT

### `metadata.py` — `MetadataGenerator`
- `generate_title(description, tags)`: título SEO
- `generate_description(description, transcript)`: snippet + full
- `generate_chapters(segments)`: capítulos desde segmentos Whisper

### `tests/test_metadata.py`
- Tests con mock de `openai.OpenAI` — sin OPENAI_API_KEY
- Al menos 5 tests verificando el formato de la salida

## Criterios de Aceptación

- [ ] `python -m src analyze --dry-run` produce JSON completo
- [ ] `pytest tests/ -v` pasa sin OPENAI_API_KEY
- [ ] `mypy --strict src/` pasa sin errores
- [ ] El JSON de salida tiene title, description, tags, chapters, transcription
