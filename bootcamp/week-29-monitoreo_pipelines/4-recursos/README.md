# Recursos — Semana 29: Monitoreo de Pipelines

## Documentación oficial

| Recurso | URL |
|---------|-----|
| structlog — documentación | https://www.structlog.org/en/stable/ |
| structlog — processors | https://www.structlog.org/en/stable/processors.html |
| Rich — Live display | https://rich.readthedocs.io/en/stable/live.html |
| Rich — Layout | https://rich.readthedocs.io/en/stable/layout.html |
| Rich — Tables | https://rich.readthedocs.io/en/stable/tables.html |
| Prometheus Python client | https://github.com/prometheus/client_python |
| Python statistics module | https://docs.python.org/3/library/statistics.html |
| threading.Timer | https://docs.python.org/3/library/threading.html#threading.Timer |

## Lecturas recomendadas

| Título | Descripción |
|--------|-------------|
| [The Twelve-Factor App — Logs](https://12factor.net/logs) | Trata logs como event streams; fundamento del logging estructurado |
| [Brendan Gregg — USE Method](https://www.brendangregg.com/usemethod.html) | Utilization, Saturation, Errors: framework para métricas de sistema |
| [Google SRE Book — Monitoring](https://sre.google/sre-book/monitoring-distributed-systems/) | Síntomas vs causas, four golden signals (latency, traffic, errors, saturation) |
| [Distributed Systems Observability (O'Reilly)](https://www.oreilly.com/library/view/distributed-systems-observability/9781492033431/) | Libro corto (~100 pp) sobre trazas, métricas y logs |

## Herramientas del stack

| Herramienta | Rol |
|-------------|-----|
| `structlog` | Logging estructurado con processors configurables |
| `rich` | Dashboard de terminal: Live, Layout, Table, Panel, Progress |
| `prometheus_client` | Exposition de métricas en formato Prometheus (Counter, Gauge, Histogram) |
| `threading.Timer` | Watchdog timer: dispara callback si no se reinicia en N segundos |
| `statistics` | `quantiles(data, n=20)[18]` → percentil 95 sin dependencias externas |

## Testing sin servicios reales

```python
# structlog en tests — deshabilitar output
import structlog
structlog.configure(processors=[], wrapper_class=structlog.BoundLogger,
                    context_class=dict, logger_factory=structlog.PrintLoggerFactory())

# Rich en tests — capturar con Console(file=StringIO())
from io import StringIO
from rich.console import Console
buf = StringIO()
console = Console(file=buf, width=80)

# AlertManager en dry_run
mgr = AlertManager(rules=rules, dry_run=True)
```

## Patrones de monitoreo

### Four Golden Signals (Google SRE)

| Signal | Qué medir | Ejemplo |
|--------|-----------|---------|
| Latency | Tiempo de respuesta (P50, P95, P99) | Tiempo de transcode |
| Traffic | Volumen de trabajo | Jobs/segundo |
| Errors | Tasa de fallos | `error_count / total` |
| Saturation | Uso de recursos | CPU %, disco libre |

### RED Method (servicios)

| Métrica | Descripción |
|---------|-------------|
| Rate | Requests/segundo |
| Errors | Porcentaje de requests que fallan |
| Duration | Distribución de latencias |
