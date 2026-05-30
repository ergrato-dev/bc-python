# Glosario — Semana 32: IA Aplicada a Media

## Modelos y APIs de OpenAI

| Término | Definición |
|---------|------------|
| **GPT-4o** | Modelo multimodal de OpenAI — procesa texto e imágenes en la misma llamada |
| **GPT-4o-mini** | Versión más rápida y económica de GPT-4o — ideal para tagging y generación de texto |
| **Whisper** | Modelo de speech-to-text de OpenAI — multilingüe, con timestamps por segmento y palabra |
| **Chat Completions** | Endpoint principal de OpenAI: `client.chat.completions.create()` — entrada mensajes, salida texto |
| **Vision API** | Capacidad de GPT-4o para analizar imágenes pasadas como `image_url` en el mensaje |
| **response_format** | Parámetro `{"type": "json_object"}` que fuerza a GPT a devolver JSON parseable |
| **temperature** | Control de aleatoriedad (0.0 = determinista, 1.0 = creativo) — usar < 0.3 para extracciones |
| **max_tokens** | Límite de tokens en la respuesta — ajustar según longitud esperada del output |

## Whisper y Transcripción

| Término | Definición |
|---------|------------|
| **verbose_json** | `response_format` que devuelve texto + segmentos + palabras con timestamps precisos |
| **timestamp_granularities** | `["segment"]` o `["word", "segment"]` — nivel de detalle de los timestamps |
| **Segmento** | Bloque de texto continuo con `{id, start, end, text}` — base para capítulos y SRT |
| **SRT** | SubRip Text — formato de subtítulos: número, `HH:MM:SS,mmm --> HH:MM:SS,mmm`, texto |
| **VTT** | WebVTT — formato de subtítulos para web, similar a SRT pero con coma reemplazada por punto |
| **Chunking** | Dividir audio >25 MB en partes para enviarlas a la API dentro del límite de tamaño |

## Embeddings y Similitud

| Término | Definición |
|---------|------------|
| **Embedding** | Vector de números (`list[float]`) que representa el significado semántico de un texto |
| **text-embedding-3-small** | Modelo de embeddings de OpenAI — 1536 dimensiones, balance costo/precisión óptimo |
| **Similitud Coseno** | Medida entre -1 y 1 que indica cuán parecidos son dos vectores: `dot(a,b)/(‖a‖·‖b‖)` |
| **Índice de Embeddings** | Estructura en memoria que guarda textos y sus vectores para búsqueda rápida |
| **Búsqueda Semántica** | Encontrar textos por significado, no por palabras exactas — usando embeddings + coseno |
| **Batch Embedding** | Pasar `input=["texto1", "texto2"]` en una sola llamada — más eficiente que llamadas individuales |

## Metadata SEO

| Término | Definición |
|---------|------------|
| **Título SEO** | Máximo 60-70 caracteres, keyword principal al inicio, atractivo y descriptivo |
| **Snippet / Metadescripción** | Descripción de 150-160 caracteres que aparece en resultados de búsqueda |
| **Tag SEO** | Palabra clave para clasificación — sin tildes, sin espacios (guiones), en minúsculas |
| **Capítulo** | Marcador de tiempo en YouTube/Vimeo: `M:SS Título del capítulo` en la descripción |
| **Call to Action** | Frase de cierre que invita a una acción: suscribirse, contactar, compartir |

## Patrones de Implementación

| Término | Definición |
|---------|------------|
| **Base64** | Codificación de binarios (imagen) a texto ASCII — requerido para pasar imágenes locales a la API |
| **MIME type** | Tipo de contenido de un archivo: `image/jpeg`, `image/png`, `image/webp` |
| **dry_run** | Modo de ejecución sin llamadas a la API — usa datos mockeados para tests y desarrollo |
| **Prompt Engineering** | Técnica de diseño del prompt para obtener outputs de mejor calidad y formato consistente |
| **Few-shot Prompting** | Incluir 2-3 ejemplos de input/output en el prompt para guiar el modelo |
| **json_object mode** | `response_format={"type": "json_object"}` — garantiza JSON válido, evita markdown en la respuesta |
| **Orquestador** | Clase o función que coordina múltiples módulos — `AssetAnalyzer` es el orquestador del proyecto |
