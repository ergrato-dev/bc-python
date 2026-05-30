# Rúbrica de Evaluación — Semana 32: IA Aplicada a Media

## Puntaje Total: 100 puntos · Mínimo para aprobar: 70 pts

---

## Conocimiento (30 pts)

| Indicador | Puntos |
|-----------|--------|
| Explica qué hace GPT-4o Vision y cómo se le pasa una imagen (base64 vs URL) | 8 |
| Describe la diferencia entre `response_format="text"` y `"verbose_json"` en Whisper | 7 |
| Explica qué es un embedding y qué mide la similitud coseno | 8 |
| Describe el flujo de generación automática de metadata para un video | 7 |

---

## Desempeño (40 pts)

| Indicador | Puntos |
|-----------|--------|
| Analiza un frame con GPT-4o Vision y extrae descripción, tema y categoría en JSON | 10 |
| Transcribe un audio con Whisper y extrae segmentos con timestamps de inicio/fin | 10 |
| Genera embeddings y encuentra el texto más similar a una query con cosine similarity | 10 |
| Genera título SEO, descripción y lista de tags para un asset dado su contenido | 10 |

---

## Producto (30 pts)

| Indicador | Puntos |
|-----------|--------|
| `studio-ai-tagger analyze` produce JSON con title, description, tags, transcription, chapters | 15 |
| Los capítulos incluyen timestamps derivados de los segmentos de Whisper | 8 |
| El módulo tiene modo `--dry-run` que usa datos mockeados sin llamar a la API de OpenAI | 4 |
| `mypy --strict src/` pasa sin errores | 3 |
