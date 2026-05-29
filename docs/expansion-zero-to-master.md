# Plan de Expansión: Zero to Master

> **bc-python Bootcamp** · Documento de planificación curricular  
> Versión: 2.0 · Fecha: Mayo 2026

---

## Contexto

El bootcamp bc-python nació como un programa de **14 semanas (84h)** orientado a llevar estudiantes de cero a un nivel **Junior**. Este documento define la expansión a **36 semanas (216h)** para alcanzar el nivel **Master**, con énfasis en:

- **Python moderno** (3.13+, type system avanzado, async/await)
- **Automatización** (file system, batch processing, pipelines)
- **Procesamiento de media** (imagen, audio, video con FFmpeg)
- **Dominio aplicado**: Studio BC — estudio de producción audiovisual ficticio

El hilo conductor de toda la expansión es **Studio BC**, una empresa de producción audiovisual con proyectos reales, clientes, assets y flujos de entrega. Cada semana agrega una capacidad nueva al sistema del estudio.

---

## Arquitectura Curricular

| Fase | Semanas | Horas | Nivel alcanzado | Descripción |
|:----:|:-------:|:-----:|:---------------:|-------------|
| **1** | 1 – 14 | 84h | **Junior** | Fundamentos, POO, testing (programa original) |
| **2** | 15 – 21 | 42h | **Mid-level** | Python profesional: types, async, CLI, datos, BD |
| **3** | 22 – 30 | 54h | **Senior** | Automatización y pipelines de media |
| **4** | 31 – 36 | 36h | **Master** | Arquitectura, IA, performance, DevOps, seguridad |
| **Total** | **36** | **216h** | **Master** | |

---

## Fase 1 — Fundamentos y POO (Semanas 1–14, programa original)

> Estas semanas no se modifican. Se documentan aquí para referencia.

| Etapa | Semanas | Temas |
|-------|---------|-------|
| Fundamentos | 1–4 | Variables, tipos, condicionales, bucles, funciones |
| Estructuras de datos | 5–7 | Listas, diccionarios, sets, algoritmos |
| POO y modularidad | 8–10 | Clases, herencia, módulos, paquetes |
| Temas avanzados | 11–13 | Archivos, excepciones, decoradores, testing |
| Proyecto integrador | 14 | Weather Dashboard CLI |

**Proyecto de fase:** Weather Dashboard CLI (consume API de clima, persiste datos, genera reportes).

---

## Fase 2 — Python Profesional (Semanas 15–21)

**Objetivo:** Dominar las herramientas del ecosistema Python moderno para construir software de producción.  
**Proyecto de fase:** Herramienta CLI de gestión de proyectos, clientes y entregables para Studio BC.

### Semana 15 · Python Moderno Avanzado

**Carpeta:** `week-15-python_moderno_avanzado`

| Tema | Contenido |
|------|-----------|
| Type system | `Protocol`, `TypeGuard`, `TypeAlias`, `ParamSpec`, `Concatenate` |
| Structural Pattern Matching | Guards, capture patterns, class patterns, sequence patterns |
| Dataclasses avanzadas | `__slots__`, `__post_init__`, `KW_ONLY`, `field(default_factory=...)` |
| Generics nativos | `list[T]`, `Self` type (3.11+), `LiteralString` |
| Python 3.12/3.13 | `type` keyword para aliases, f-strings mejoradas, `@override` |

**Stack:** Python 3.13, mypy, pyright  
**Proyecto semanal:** Modelar todas las entidades del estudio (Proyecto, Cliente, Fase, Asset) con tipos estrictos y Protocols.

---

### Semana 16 · Concurrencia y AsyncIO

**Carpeta:** `week-16-concurrencia_y_asyncio`

| Tema | Contenido |
|------|-----------|
| asyncio core | Event loop, corutinas, Tasks, Futures, `asyncio.run()` |
| Patterns async | `gather`, `wait`, `as_completed`, `TaskGroup` (3.11+) |
| concurrent.futures | `ThreadPoolExecutor`, `ProcessPoolExecutor`, `map` vs `submit` |
| Cuándo usar qué | I/O-bound → threads/async · CPU-bound → processes |
| Caso media | Procesamiento paralelo de lotes de archivos de video/audio |

**Stack:** asyncio, concurrent.futures, aiofiles  
**Proyecto semanal:** Sistema de procesamiento por lotes que descarga y organiza assets del estudio en paralelo.

---

### Semana 17 · CLI Profesional con Typer y Rich

**Carpeta:** `week-17-cli_profesional_typer_rich`

| Tema | Contenido |
|------|-----------|
| Typer | Comandos, subcomandos, opciones, argumentos, callbacks, autocompletion |
| Rich | Tables, panels, progress bars, syntax highlighting, markdown, Live |
| Textual | Widgets, layouts, eventos, TUIs reactivas |
| Click vs Typer | Comparación, migración, ecosistema |
| Testing CLIs | `typer.testing.CliRunner`, fixtures |

**Stack:** typer, rich, textual  
**Proyecto semanal:** Herramienta CLI `studio` con subcomandos (`studio projects list`, `studio clients add`, etc.).

---

### Semana 18 · Gestión de Datos con Polars

**Carpeta:** `week-18-gestion_datos_polars`

| Tema | Contenido |
|------|-----------|
| Polars vs Pandas | API, performance, lazy vs eager evaluation |
| DataFrames | Selección, filtrado, transformación, agregación |
| Expresiones | `pl.col()`, `pl.when()`, `pl.lit()`, expresiones encadenadas |
| I/O | CSV, Excel (`openpyxl`), Parquet, JSON, bases de datos |
| Caso estudio | Análisis de horas trabajadas, presupuesto vs real, KPIs del estudio |

**Stack:** polars, openpyxl, pyarrow  
**Proyecto semanal:** Dashboard de reportes del estudio: horas por proyecto, rentabilidad por cliente, tendencias.

---

### Semana 19 · HTTP y APIs con httpx

**Carpeta:** `week-19-http_y_apis_httpx`

| Tema | Contenido |
|------|-----------|
| httpx | Cliente sync y async, sessions, transports |
| Autenticación | Bearer Token, API Key, OAuth2 (client credentials flow) |
| Resiliencia | Retry con `tenacity`, timeouts, circuit breaker básico |
| Rate limiting | Token bucket, sliding window, respeto a `Retry-After` |
| Manejo de errores | `HTTPStatusError`, `ConnectError`, respuestas malformadas |

**Stack:** httpx, tenacity, pydantic (para validar respuestas)  
**Proyecto semanal:** Cliente de APIs que consulta servicios de clientes y proveedores del estudio.

---

### Semana 20 · Bases de Datos con SQLModel

**Carpeta:** `week-20-bases_de_datos_sqlmodel`

| Tema | Contenido |
|------|-----------|
| SQLModel | Modelos como Pydantic + SQLAlchemy, tipado completo |
| Relaciones | One-to-many, many-to-many, `Relationship`, `link_model` |
| Migraciones | Alembic: `env.py`, `upgrade`/`downgrade`, autogenerate |
| Queries | Filtros, joins, subqueries, `select()`, `session.exec()` |
| Patrones | Repository básico, Unit of Work, transacciones |

**Stack:** sqlmodel, alembic, sqlite  
**Proyecto semanal:** Catálogo completo del estudio: Clientes, Proyectos, Fases, Entregables y Assets con relaciones.

---

### Semana 21 · Proyecto Fase 2: Herramienta de Producción

**Carpeta:** `week-21-proyecto_fase_2`

**Descripción:** Proyecto integrador de toda la Fase 2. Sistema de gestión Studio BC.

**Entregables:**
- CLI `studio` con Typer + Rich (comandos completos)
- BD SQLModel con Alembic (clientes, proyectos, fases, entregables)
- Integración con al menos una API externa (httpx)
- Reportes exportables con Polars (PDF/Excel)
- Tests con pytest + cobertura > 80%

**Evaluación:** 150 puntos · Defensa técnica obligatoria

---

## Fase 3 — Automatización y Pipelines de Media (Semanas 22–30)

**Objetivo:** Construir pipelines de automatización que procesen imagen, audio y video, y los integren con plataformas de distribución.  
**Proyecto de fase:** Pipeline end-to-end de producción: watch → validate → process → deliver → notify.

### Semana 22 · Automatización del Sistema de Archivos

**Carpeta:** `week-22-automatizacion_sistema_archivos`

| Tema | Contenido |
|------|-----------|
| watchdog | `Observer`, `FileSystemEventHandler`, eventos: created/modified/deleted |
| pathlib avanzado | Glob patterns, operaciones masivas, comparación de árboles |
| Naming conventions | Estándares de nomenclatura para producción audiovisual |
| Organización automática | Mover, clasificar y renombrar archivos según reglas |
| Idempotencia | Evitar reprocesamiento, lock files, checksums |

**Stack:** watchdog, pathlib, hashlib  
**Proyecto semanal:** Daemon que monitorea carpeta de entrega y auto-organiza archivos en la estructura del estudio.

---

### Semana 23 · Procesamiento de Imágenes

**Carpeta:** `week-23-procesamiento_imagenes`

| Tema | Contenido |
|------|-----------|
| Pillow | Resize, crop, rotate, color modes, composite, draw |
| Formatos | JPG, PNG, WebP, TIFF, RAW (rawpy) |
| Thumbnails | Generación en múltiples resoluciones (web, social, print) |
| Watermarks | Overlays de logo, texto, metadata EXIF |
| Batch processing | Procesamiento de cientos de imágenes con progress bar |

**Stack:** Pillow, imageio, rawpy (RAW), piexif (EXIF)  
**Proyecto semanal:** Pipeline de arte: recibir imágenes → generar thumbnails web/social → aplicar watermark → exportar.

---

### Semana 24 · Procesamiento de Audio

**Carpeta:** `week-24-procesamiento_audio`

| Tema | Contenido |
|------|-----------|
| pydub | Segmentación, mezcla, normalización, fade in/out, export |
| Análisis | Detección de silencio, amplitud, duración, BPM básico |
| Formatos | MP3, WAV, FLAC, AAC, OGG |
| Transcripción | SpeechRecognition (local), OpenAI Whisper (API y modelo local) |
| Metadata | Tags ID3, BPM, key detection |

**Stack:** pydub, librosa, openai-whisper, SpeechRecognition  
**Proyecto semanal:** Pipeline: audio crudo → normalizar → detectar segmentos → transcribir → generar SRT/VTT.

---

### Semana 25 · Procesamiento de Video con FFmpeg

**Carpeta:** `week-25-procesamiento_video_ffmpeg`

| Tema | Contenido |
|------|-----------|
| ffmpeg-python | Nodes, filtros, streams, inputs/outputs, run() |
| Transcodificación | H.264, H.265 (HEVC), AV1, ProRes, DNxHD |
| Proxies | Generación de versiones de baja resolución para edición |
| Extracción | Clips, stills, thumbnails, audio separado |
| Metadata | MediaInfo, duración, codec, resolución, framerate |

**Stack:** ffmpeg-python, pymediainfo, subprocess (FFprobe)  
**Proyecto semanal:** Pipeline de post: ingest RAW → generar proxy → extraer thumbnail → transcodificar para web → archivar.

---

### Semana 26 · Cloud Storage y Assets

**Carpeta:** `week-26-cloud_storage`

| Tema | Contenido |
|------|-----------|
| boto3 / S3 | Upload/download, multipart, presigned URLs, versioning |
| Google Drive API | OAuth2, carpetas, permisos, upload/download |
| Estrategia de storage | Hot/cold storage, naming en cloud, estructura de buckets |
| Sincronización | Sync bidireccional, detección de cambios, checksums |
| Costos y optimización | Storage classes, lifecycle policies |

**Stack:** boto3, google-api-python-client, google-auth  
**Proyecto semanal:** Sistema de backup automático: producción local → S3 (master) + Drive (compartido con cliente).

---

### Semana 27 · Arquitectura de Pipelines

**Carpeta:** `week-27-arquitectura_pipelines`

| Tema | Contenido |
|------|-----------|
| Diseño | Etapas, contratos entre etapas, composición |
| Colas | `queue.Queue`, `asyncio.Queue`, RQ (Redis Queue) básico |
| Manejo de errores | Retry con backoff, skip-on-error, dead-letter queue |
| Estado | Máquina de estados: pending → running → done → failed |
| Observabilidad | Logging por etapa, métricas de throughput |

**Stack:** rq (Redis Queue), redis, tenacity  
**Proyecto semanal:** Framework de pipeline propio del estudio con etapas conectables y manejo de errores.

---

### Semana 28 · Integraciones con Plataformas

**Carpeta:** `week-28-integraciones_plataformas`

| Tema | Contenido |
|------|-----------|
| YouTube Data API v3 | Upload, metadata, thumbnails, listas de reproducción |
| Vimeo API | Upload chunked, privacidad, álbumes, showcase |
| Slack API | Webhooks, Block Kit, subida de archivos |
| Discord Webhooks | Mensajes enriquecidos, embeds |
| Notion API | Bases de datos, actualización de propiedades, bloques |

**Stack:** google-api-python-client, vimeo, slack-sdk, httpx  
**Proyecto semanal:** Módulo de distribución: publicar en YouTube + Vimeo + notificar Slack + actualizar Notion.

---

### Semana 29 · Monitoreo de Pipelines

**Carpeta:** `week-29-monitoreo_pipelines`

| Tema | Contenido |
|------|-----------|
| Structured logging | structlog: contexto, processors, JSON output |
| Métricas | Tiempos por etapa, tasa de error, throughput, cola pendiente |
| Alertas | Thresholds, notificaciones automáticas, escalamiento |
| Health checks | Endpoints de status, watchdog timers |
| Dashboard | Rich Live panel como dashboard de terminal |

**Stack:** structlog, loguru, rich (Live), prometheus-client (básico)  
**Proyecto semanal:** Sistema de monitoreo del pipeline con dashboard en terminal y alertas a Slack.

---

### Semana 30 · Proyecto Fase 3: Pipeline de Producción

**Carpeta:** `week-30-proyecto_fase_3`

**Descripción:** Sistema completo de pipeline de producción para Studio BC.

**Entregables:**
- Daemon watchdog que detecta nuevos archivos entregados
- Pipeline: validate → transcode → thumbnail → cloud upload
- Publicación automatizada en YouTube/Vimeo
- Notificaciones a Slack/Discord con estado
- Dashboard de monitoreo en terminal
- Tests de integración del pipeline completo

**Evaluación:** 200 puntos · Demo en vivo del pipeline ejecutándose

---

## Fase 4 — Arquitectura Master y Sistema de Producción (Semanas 31–36)

**Objetivo:** Integrar todo el conocimiento en un sistema de producción real, aplicando arquitectura limpia, IA, performance y DevOps.  
**Proyecto de fase:** Sistema integrado completo de Studio BC — producción-ready.

### Semana 31 · Clean Architecture y DDD

**Carpeta:** `week-31-clean_architecture_ddd`

| Tema | Contenido |
|------|-----------|
| Clean Architecture | Capas: Domain, Application, Infrastructure, Presentation |
| Regla de dependencias | Dependencias siempre hacia adentro |
| DDD básico | Entities, Value Objects, Aggregates, Domain Events |
| Repository Pattern | Abstracción del acceso a datos, ports & adapters |
| Dependency Injection | DI manual, `dependency-injector`, `dishka` |

**Stack:** dependency-injector o dishka  
**Proyecto semanal:** Refactorizar el sistema Studio BC con Clean Architecture (separar dominio de infraestructura).

---

### Semana 32 · IA Aplicada a Media

**Carpeta:** `week-32-ia_aplicada_media`

| Tema | Contenido |
|------|-----------|
| OpenAI API | GPT-4o Vision: análisis de frames, descripción de contenido |
| Whisper avanzado | Speaker diarization, timestamps a nivel de palabra, idioma |
| Auto-tagging | Clasificación de contenido con embeddings + similitud coseno |
| Embeddings | `text-embedding-3-small`, búsqueda semántica de assets |
| Generación automática | Títulos SEO, descripciones, tags, capítulos de video |

**Stack:** openai, sentence-transformers, numpy  
**Proyecto semanal:** Módulo de IA que analiza un asset de video y genera: título, descripción, tags, capítulos y transcripción.

---

### Semana 33 · Performance y Optimización

**Carpeta:** `week-33-performance_y_optimizacion`

| Tema | Contenido |
|------|-----------|
| Profiling | cProfile, snakeviz, py-spy (sampling), memory_profiler |
| Caching | Redis: cache-aside, write-through, TTL, invalidación |
| Streaming I/O | Procesamiento de archivos grandes sin cargar en memoria |
| Async optimization | Evitar blocking calls, semáforos, throttling |
| Benchmarking | pytest-benchmark, comparación de implementaciones |

**Stack:** redis, py-spy, memory-profiler, pytest-benchmark  
**Proyecto semanal:** Optimizar el pipeline para procesar archivos 4K/8K: profiling → identificar bottlenecks → optimizar → benchmark.

---

### Semana 34 · DevOps y CI/CD

**Carpeta:** `week-34-devops_y_cicd`

| Tema | Contenido |
|------|-----------|
| Docker avanzado | Multi-stage builds, build args, secrets, non-root user |
| Docker Compose prod | Profiles, healthchecks, restart policies, secrets |
| GitHub Actions | Triggers, jobs, artifacts, cache, matrix, environments |
| Makefile | Interfaz unificada: `make test`, `make build`, `make deploy` |
| Secrets management | GitHub Secrets, `.env` patterns, rotación |

**Stack:** Docker, GitHub Actions, make  
**Proyecto semanal:** Pipeline CI/CD completo para el sistema Studio BC: test → lint → build → deploy.

---

### Semana 35 · Seguridad en Python

**Carpeta:** `week-35-seguridad`

| Tema | Contenido |
|------|-----------|
| Gestión de secretos | python-dotenv, Vault básico, AWS Secrets Manager |
| Autenticación APIs | JWT, API Keys, OAuth2 server-side |
| OWASP aplicado | Injection, broken auth, sensitive data, SSRF, path traversal |
| Validación | Input sanitization avanzada, Pydantic strict mode |
| Auditoría | bandit (SAST), safety (dependencias), semgrep básico |

**Stack:** bandit, safety, pydantic (strict), python-jose  
**Proyecto semanal:** Auditoría y hardening completo del sistema Studio BC con reporte de seguridad.

---

### Semana 36 · Proyecto Final Master

**Carpeta:** `week-36-proyecto_final_master`

**Descripción:** Sistema integrado completo Studio BC — producción-ready.

**Entregables:**

1. **Sistema de Gestión** (Fase 2)
   - CLI `studio` completa
   - BD con todas las entidades
   - Reportes y análisis

2. **Pipeline de Producción** (Fase 3)
   - Watch → validate → transcode → thumbnail → cloud → publish
   - Monitoreo y dashboard en terminal

3. **Módulo de IA** (Fase 4)
   - Auto-generación de metadatos
   - Búsqueda semántica de assets

4. **Infraestructura** (Fase 4)
   - CI/CD completo
   - Docker production-ready
   - Seguridad auditada

5. **Documentación**
   - README técnico completo
   - Diagramas de arquitectura
   - Guía de despliegue

**Evaluación:** 300 puntos · Presentación de 20 minutos + defensa técnica

---

## Stack Tecnológico Completo

### Fase 1 (original)
`Python 3.13+` · `pytest` · `uv` · `Docker`

### Fase 2 (nuevo)
`mypy` · `pyright` · `asyncio` · `typer` · `rich` · `textual` · `polars` · `openpyxl` · `httpx` · `tenacity` · `sqlmodel` · `alembic` · `sqlite`

### Fase 3 (nuevo)
`watchdog` · `Pillow` · `imageio` · `pydub` · `librosa` · `openai-whisper` · `ffmpeg-python` · `pymediainfo` · `boto3` · `google-api-python-client` · `rq` · `redis` · `slack-sdk` · `structlog` · `loguru`

### Fase 4 (nuevo)
`openai` · `sentence-transformers` · `numpy` · `py-spy` · `memory-profiler` · `pytest-benchmark` · `dependency-injector` · `bandit` · `safety` · `python-jose` · `GitHub Actions` · `Docker multi-stage`

---

## Convenciones del Dominio (Studio BC)

Todos los proyectos de la expansión usan estas entidades como base:

```python
# Entidades principales del dominio Studio BC
Client        # Cliente del estudio
Project       # Proyecto de producción
Phase         # Fase del proyecto (preproducción, producción, post, entrega)
Deliverable   # Entregable asociado a una fase
Asset         # Archivo de media (video, audio, imagen, documento)
Pipeline      # Configuración de un pipeline de automatización
PipelineRun   # Ejecución de un pipeline
```

---

## Progresión de Proyectos

Cada fase construye sobre la anterior. Al final de cada fase, el estudiante tiene un sistema funcional más completo:

```
Fase 1  →  Weather Dashboard CLI (proyecto independiente)
Fase 2  →  Studio BC CLI + BD (herramienta de gestión)
Fase 3  →  Studio BC + Pipeline de automatización
Fase 4  →  Studio BC completo: gestión + pipelines + IA + CI/CD
```

---

## Historial de Cambios

| Versión | Fecha | Descripción |
|---------|-------|-------------|
| 1.0 | Ene 2026 | Programa original: 14 semanas, Zero to Junior |
| 2.0 | May 2026 | Expansión: +22 semanas, Zero to Master, dominio audiovisual |
