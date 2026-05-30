# Sitios Web — Semana 29: Monitoreo de Pipelines

## Structured Logging

| Recurso | Descripción |
|---------|-------------|
| [structlog Documentation](https://www.structlog.org/en/stable/) | Referencia completa: processors, configuración, contextvars, output JSON |
| [structlog — Getting Started](https://www.structlog.org/en/stable/getting-started.html) | Guía de inicio rápido con ConsoleRenderer y JSONRenderer |
| [Python `logging` module](https://docs.python.org/3/library/logging.html) | Base de stdlib que structlog integra via `stdlib.LoggerFactory` |
| [loguru Docs](https://loguru.readthedocs.io/) | Alternativa simple a structlog — ergonómica con `logger.bind()` |

## Métricas y Observabilidad

| Recurso | Descripción |
|---------|-------------|
| [Prometheus Python Client](https://github.com/prometheus/client_python) | Contadores, histogramas, gauges y exposición HTTP para Prometheus/Grafana |
| [Python `statistics` module](https://docs.python.org/3/library/statistics.html) | `quantiles()`, `median()`, `mean()` — cálculo de percentiles sin dependencias |
| [OpenTelemetry Python](https://opentelemetry-python.readthedocs.io/) | Estándar moderno para trazas, métricas y logs distribuidos |

## Alertas

| Recurso | Descripción |
|---------|-------------|
| [Slack Incoming Webhooks](https://api.slack.com/messaging/webhooks) | Enviar alertas simples sin bot token — solo una URL |
| [PagerDuty Events API](https://developer.pagerduty.com/api-reference/368ae3d938c9e-send-an-event-to-pager-duty) | Alertas con escalamiento automático para producción |
| [Alertmanager (Prometheus)](https://prometheus.io/docs/alerting/latest/alertmanager/) | Routing y deduplicación de alertas — complemento de Prometheus |

## Dashboard y Terminal UI

| Recurso | Descripción |
|---------|-------------|
| [Rich Documentation](https://rich.readthedocs.io/) | Live, Layout, Table, Panel, Progress — referencia completa |
| [Rich — Live Display](https://rich.readthedocs.io/en/stable/live.html) | API de `Live`: `screen=True`, `refresh_per_second`, `update()` |
| [Rich — Layout](https://rich.readthedocs.io/en/stable/layout.html) | División de terminal en secciones: `split_column`, `split_row`, `ratio` |
| [Textual Docs](https://textual.textualize.io/) | Framework reactivo para TUIs complejas — sucesor de Rich Live |

## Health Checks

| Recurso | Descripción |
|---------|-------------|
| [Python `threading.Timer`](https://docs.python.org/3/library/threading.html#threading.Timer) | Timer de un solo disparo — base del WatchdogTimer |
| [Python `shutil.disk_usage`](https://docs.python.org/3/library/shutil.html#shutil.disk_usage) | Verificar espacio libre en disco sin dependencias externas |
