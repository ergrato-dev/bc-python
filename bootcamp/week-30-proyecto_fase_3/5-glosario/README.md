# Glosario — Semana 30: Proyecto Fase 3

## Arquitectura del Pipeline

| Término | Definición |
|---------|------------|
| **Pipeline end-to-end** | Sistema que toma un archivo crudo y lo transforma, sube y notifica sin intervención manual |
| **Stage Protocol** | Contrato de etapa con `process(data) → StageResult`; sin herencia, duck typing estructural |
| **StageResult** | Objeto de retorno de una etapa: `success`, `data` acumulado, `error` opcional |
| **Context dict** | Diccionario que fluye entre etapas acumulando datos (path, stem, media_type, s3_url, etc.) |
| **DLQ (Dead-Letter Queue)** | Cola de jobs definitivamente fallidos — para inspección y reencola manual |
| **Idempotencia** | Propiedad de una operación que produce el mismo resultado si se repite múltiples veces |

## Procesamiento de Media

| Término | Definición |
|---------|------------|
| **Proxy** | Copia de baja resolución (ej. 25 % original) para edición no destructiva o preview rápido |
| **Web encode** | Versión optimizada para streaming web: H.264 CRF 23, máx 1080p, `+faststart` |
| **Thumbnail** | Frame extraído del segundo 5 del video — para preview o plataformas |
| **Transcode** | Convertir un video de un codec/contenedor a otro sin cambiar el contenido |
| **CRF (Constant Rate Factor)** | Parámetro de calidad H.264/H.265; 0 = lossless, 23 = buena calidad, 51 = mínima |
| **Ingest** | Primera etapa del pipeline: leer el archivo y extraer metadata básica |

## Cloud y Storage

| Término | Definición |
|---------|------------|
| **S3 key** | Ruta del objeto en S3; ej. `canal9/spot/video/web/2024-11-15/clip_web.mp4` |
| **dry_run** | Modo de ejecución sin llamadas reales a APIs externas — para tests y desarrollo |
| **StateStore** | Clase que persiste el estado de cada job en JSON con escritura atómica |
| **JobStatus** | Máquina de estados: `pending → running → done / failed` |

## Distribución

| Término | Definición |
|---------|------------|
| **Webhook** | URL que recibe POST con JSON — mecanismo más simple de notificación |
| **Block Kit** | Componentes visuales de Slack: header, section, actions, divider |
| **Embed (Discord)** | Mensaje enriquecido con color, campos, imagen y footer |

## Observabilidad

| Término | Definición |
|---------|------------|
| **Daemon** | Proceso que corre indefinidamente en background sin intervención del usuario |
| **Watchdog** | Proceso que monitorea actividad y actúa si detecta anomalías o bloqueos |
| **Observer (watchdog lib)** | Hilo que monitorea el filesystem y llama al handler en cada evento |
| **FileCreatedEvent** | Evento de watchdog emitido al crear un archivo en la carpeta monitoreada |
| **Dashboard Live** | Panel Rich actualizado en tiempo real con `Live(screen=True)` |
