# Semana 32: IA Aplicada a Media

> **Fase 4 — Arquitectura Master y Sistema de Producción** · _Senior → Master_

## Objetivos de Aprendizaje

Al finalizar esta semana, serás capaz de:

- Llamar a GPT-4o Vision para analizar frames de video y describir contenido visual
- Transcribir audio con Whisper obteniendo timestamps a nivel de palabra y segmento
- Generar embeddings con `text-embedding-3-small` e implementar búsqueda semántica
- Construir un sistema de auto-tagging con embeddings + similitud coseno
- Generar automáticamente títulos SEO, descripciones, tags y capítulos de video

---

## Contenidos

| # | Archivo | Tema |
|---|---------|------|
| 01 | [OpenAI API y GPT-4o Vision](1-teoria/01-openai-gpt4o-vision.md) | Chat completions, análisis de imágenes, prompting estructurado |
| 02 | [Whisper — Transcripción Avanzada](1-teoria/02-whisper-avanzado.md) | verbose_json, timestamps de palabra, segmentos, idioma |
| 03 | [Embeddings y Búsqueda Semántica](1-teoria/03-embeddings-busqueda.md) | text-embedding-3-small, cosine similarity, índice en memoria |
| 04 | [Auto-Tagging y Clasificación](1-teoria/04-auto-tagging.md) | Few-shot prompting, clasificación por similitud, taxonomía |
| 05 | [Generación Automática de Metadata](1-teoria/05-generacion-metadata.md) | Títulos SEO, descripciones, capítulos con timestamps |

---

## Estructura de la Semana

```
week-32-ia_aplicada_media/
├── README.md
├── rubrica-evaluacion.md
├── 1-teoria/               # 5 archivos .md
├── 2-ejercicios/
│   ├── 01-vision-frame/
│   ├── 02-whisper-timestamps/
│   ├── 03-semantic-search/
│   └── 04-metadata-generator/
├── 3-proyecto/
│   ├── README.md           # studio-ai-tagger
│   ├── starter/
│   └── solution/
├── 4-recursos/
└── 5-glosario/
```

---

## Distribución del Tiempo (6h)

| Bloque | Actividad | Tiempo |
|--------|-----------|--------|
| 1 | Teoría: Vision + Whisper | 1.5h |
| 2 | Teoría: Embeddings + Auto-tagging + Metadata | 1.0h |
| 3 | Ejercicios guiados (4) | 2.0h |
| 4 | Proyecto semanal | 1.5h |

---

## Stack de la Semana

| Librería | Rol |
|----------|-----|
| `openai` | Cliente oficial — Chat Completions, Whisper, Embeddings |
| `numpy` | Similitud coseno, operaciones vectoriales |
| `base64` | Codificar imágenes para Vision API |
| `pathlib` | Manejo de archivos de audio/imagen/video |

---

## Prerequisito

```bash
pip install openai numpy
export OPENAI_API_KEY=sk-...
```

---

## Navegación

← [Semana 31 — Clean Architecture y DDD](../week-31-clean_architecture_ddd/README.md) · [Semana 33 — Performance y Optimización](../week-33-performance_y_optimizacion/README.md) →
