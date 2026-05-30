# Glosario — Semana 27: Arquitectura de Pipelines

## Diseño de Pipelines

| Término | Definición |
|---------|------------|
| **Pipeline** | Cadena de etapas donde la salida de cada una es la entrada de la siguiente |
| **Stage** | Unidad de trabajo con una única responsabilidad; implementa `process(data) → StageResult` |
| **Stage Protocol** | Contrato definido con `typing.Protocol`; no requiere herencia — duck typing estructural |
| **StageResult** | Objeto de retorno de una etapa: `success`, `data` (contexto acumulado), `error` opcional |
| **Pipeline lineal** | Etapas conectadas en serie; falla en una detiene el pipeline completo |
| **Pipeline ramificado** | La siguiente etapa se elige dinámicamente según el resultado de la anterior |
| **Stage decorator** | Envuelve una etapa para agregar logging, retry u otras preocupaciones transversales |
| **Context dict** | Diccionario que fluye entre etapas acumulando datos; cada etapa recibe y devuelve una copia |

## Colas y Concurrencia

| Término | Definición |
|---------|------------|
| **queue.Queue** | Cola FIFO thread-safe de la stdlib Python; `get()` bloquea hasta que haya un item |
| **asyncio.Queue** | Cola async para usar con `await`; no bloquea el event loop |
| **Producer/Consumer** | Patrón donde el producer genera items y el consumer los procesa; la cola los desacopla |
| **Sentinel** | Valor especial (ej. `None`) que señala fin de stream a los consumers |
| **maxsize** | Límite de items en una cola; activa backpressure si el producer es más rápido |
| **Backpressure** | Mecanismo que frena al producer cuando los consumers no pueden seguir el ritmo |
| **task_done()** | Señal a `queue.join()` de que un item fue procesado completamente |
| **ThreadPoolExecutor** | Maneja un pool de threads para ejecutar tareas IO-bound en paralelo |

## Redis Queue (RQ)

| Término | Definición |
|---------|------------|
| **Job** | Unidad de trabajo encolada en RQ: función + argumentos + metadata |
| **Worker** | Proceso separado que consume jobs de una o varias colas |
| **Queue** | Instancia RQ ligada a una conexión Redis; guarda jobs serializados |
| **Job status** | Estado del job: `queued → started → finished / failed` |
| **result_ttl** | Tiempo de vida del resultado en Redis tras completarse el job |
| **failure_ttl** | Tiempo de vida del job fallido en Redis |
| **depends_on** | Encadenamiento de jobs: el siguiente solo inicia cuando el anterior termina |
| **FailedJobRegistry** | Registro RQ de jobs fallidos; accesible con `rq.job.FailedJobRegistry` |

## Manejo de Errores

| Término | Definición |
|---------|------------|
| **Retry** | Reintentar una operación fallida según una política configurable |
| **Backoff exponencial** | Espera entre reintentos que crece exponencialmente: 1s, 2s, 4s, 8s... |
| **tenacity** | Librería Python para retry declarativo: `@retry(stop=..., wait=..., retry=...)` |
| **stop_after_attempt(n)** | Detiene el retry después de n intentos totales |
| **wait_exponential** | Espera con crecimiento exponencial + jitter opcional |
| **retry_if_exception_type** | Solo reintenta para tipos de excepción específicos (errores recuperables) |
| **reraise=True** | Al agotar reintentos, propaga la última excepción en lugar de lanzar `RetryError` |
| **Dead-Letter Queue** | Cola de jobs definitivamente fallidos (agotaron reintentos); para inspección y requeue manual |
| **Skip-on-error** | Política de batch que procesa todos los items aunque algunos fallen |

## Estado y Observabilidad

| Término | Definición |
|---------|------------|
| **JobStatus** | Máquina de estados del job: pending → running → done / failed / retrying |
| **StateStore** | Persistencia de estado de jobs en JSON con escritura atómica |
| **Timestamp de transición** | `started_at` al entrar a RUNNING, `finished_at` al llegar a DONE o FAILED |
| **Throughput** | Jobs completados por segundo — métrica clave de performance del pipeline |
| **Logging por etapa** | Cada etapa usa `logging.getLogger(f"pipeline.{stage.name}")` para trazabilidad |
| **Circuit Breaker** | Patrón que pausa operaciones cuando los errores superan un umbral, evitando cascada de fallos |
