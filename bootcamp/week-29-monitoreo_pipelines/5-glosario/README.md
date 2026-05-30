# Glosario — Semana 29: Monitoreo de Pipelines

## Logging estructurado

| Término | Definición |
|---------|------------|
| **Structured logging** | Logs emitidos como pares clave-valor (JSON) en lugar de texto libre; facilita filtrado y análisis |
| **structlog** | Librería Python para logging estructurado con processors configurables y contexto inmutable |
| **Processor** | Función en la cadena de structlog que transforma el evento antes de emitirlo (ej. `add_log_level`) |
| **BoundLogger** | Logger de structlog con contexto adjunto; cada `bind()` crea una copia nueva (inmutable) |
| **contextvars** | Módulo Python para variables de contexto por coroutine/thread; usado para propagar `job_id` sin pasarlo |
| **JSONRenderer** | Processor de structlog que serializa el evento a JSON; ideal para producción |
| **ConsoleRenderer** | Processor de structlog con salida legible en terminal con colores; ideal para desarrollo |
| **censor_secrets** | Processor personalizado que enmascara valores de claves sensibles (password, token, key) |

## Métricas

| Término | Definición |
|---------|------------|
| **P50 / P95 / P99** | Percentiles de latencia: el 50/95/99 % de las peticiones tienen latencia menor o igual a este valor |
| **Throughput** | Cantidad de trabajo completado por unidad de tiempo (jobs/s, req/s) |
| **Error rate** | Proporción de operaciones que terminan en error respecto al total |
| **Counter** | Métrica que solo aumenta (total de jobs procesados); tipo Prometheus |
| **Gauge** | Métrica que sube y baja (disco libre, jobs en cola); tipo Prometheus |
| **Histogram** | Agrupa observaciones en buckets para calcular percentiles; tipo Prometheus |
| **Cardinality** | Número de combinaciones únicas de labels en Prometheus; alta cardinalidad degrada performance |
| **Scrape** | Acto de Prometheus de recolectar métricas de un endpoint `/metrics` |

## Alertas

| Término | Definición |
|---------|------------|
| **Threshold** | Umbral numérico que dispara una alerta cuando se supera (gt/lt) |
| **Cooldown** | Período mínimo entre dos disparos de la misma alerta; evita spam de notificaciones |
| **Alert fatigue** | Desensibilización ante alertas por exceso de notificaciones; se previene con cooldown y agrupación |
| **Dead-man switch** | Alerta que se dispara cuando una señal *deja* de llegar (p.ej., heartbeat ausente) |
| **Escalation** | Protocolo que aumenta el canal de notificación si la alerta no se reconoce en N minutos |

## Health checks

| Término | Definición |
|---------|------------|
| **Health check** | Verificación del estado de un componente del sistema (disco, base de datos, proceso) |
| **Liveness probe** | Check que verifica si el proceso está vivo (Kubernetes); falla → reinicio |
| **Readiness probe** | Check que verifica si el servicio está listo para recibir tráfico; falla → quitar del load balancer |
| **Watchdog timer** | Timer que dispara una acción (ej. reinicio) si no se reinicia periódicamente; detecta bloqueos |
| **Heartbeat** | Señal periódica que indica que un proceso sigue activo |

## Dashboard y visualización

| Término | Definición |
|---------|------------|
| **Rich** | Librería Python para output de terminal enriquecido: tablas, paneles, progreso, colores |
| **Live** | Contexto de Rich que actualiza la pantalla sin scroll (in-place rendering) |
| **Layout** | Contenedor de Rich que divide la pantalla en regiones; `split_column` y `split_row` |
| **Panel** | Marco decorativo de Rich alrededor de cualquier renderable |
| **Renderable** | Cualquier objeto que Rich puede imprimir: str, Table, Panel, Layout, etc. |
| **TUI** | Terminal User Interface — aplicación interactiva que vive en la terminal |

## Observabilidad

| Término | Definición |
|---------|------------|
| **Observabilidad** | Capacidad de inferir el estado interno de un sistema a partir de sus salidas externas (logs, métricas, trazas) |
| **Three pillars** | Los tres pilares de observabilidad: **logs** (eventos), **métricas** (series temporales), **trazas** (flujo entre servicios) |
| **Four golden signals** | Latency, Traffic, Errors, Saturation — las cuatro métricas fundamentales según Google SRE |
| **RED method** | Rate, Errors, Duration — framework para monitorear servicios orientados a requests |
| **USE method** | Utilization, Saturation, Errors — framework para monitorear recursos de sistema |
| **SLI** | Service Level Indicator — métrica que mide el nivel de servicio (ej. error rate) |
| **SLO** | Service Level Objective — objetivo numérico para un SLI (ej. error rate < 1 %) |
| **SLA** | Service Level Agreement — contrato formal con el cliente sobre niveles de servicio |
