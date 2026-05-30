# Proyecto — studio-audio-pipeline

## Descripción

Pipeline de procesamiento de audio para Studio BC: recibe grabaciones en `drop/`,
las normaliza, transcribe con Whisper y genera archivos SRT y VTT en `output/`.

## Comandos

```bash
pip install -e .

# Procesar todos los audios en drop/ de una pasada
python -m studio_audio process

# Modo daemon: monitorear drop/ con watchdog
python -m studio_audio watch

# Transcribir un archivo específico
python -m studio_audio transcribe audio.mp3 --model base
```

## Estructura de salida

```
output/
├── normalized/     # Audio normalizado a -14 dBFS
├── subtitles/
│   ├── entrevista.srt
│   └── entrevista.vtt
```

## Requisitos

- El pipeline normaliza antes de transcribir (mejora accuracy de Whisper)
- Los archivos SRT y VTT deben tener timestamps correctos
- Los archivos corruptos no interrumpen el batch
- mypy --strict pasa sin errores en `src/`

## Archivos a completar

| Archivo | TODOs |
|---------|-------|
| `src/preprocessor.py` | `normalize()`, `to_wav_mono_16k()` |
| `src/transcriber.py` | `transcribe()`, `load_model()` |
| `src/subtitle_writer.py` | `generate_srt()`, `generate_vtt()` |
| `src/pipeline.py` | `process_audio()` — orquesta todo |
| `src/__main__.py` | comandos `process`, `watch`, `transcribe` |
