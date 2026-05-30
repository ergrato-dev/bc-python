# Recursos — Semana 27: Arquitectura de Pipelines

## Webgrafía

### Documentación oficial

| Recurso | URL | Por qué vale la pena |
|---------|-----|----------------------|
| tenacity Docs | https://tenacity.readthedocs.io/ | Referencia de decoradores, estrategias de retry |
| RQ Docs | https://python-rq.org/docs/ | Jobs, Workers, queues, dependencias |
| Python `queue` module | https://docs.python.org/3/library/queue.html | Queue, LifoQueue, PriorityQueue |
| asyncio.Queue | https://docs.python.org/3/library/asyncio-queue.html | Queue async thread-safe |
| typing.Protocol | https://docs.python.org/3/library/typing.html#typing.Protocol | Contratos sin herencia |

### Artículos y patrones

| Recurso | Tema |
|---------|------|
| [Martin Fowler — Pipes and Filters](https://www.enterpriseintegrationpatterns.com/patterns/messaging/PipesAndFilters.html) | Patrón canónico de pipelines |
| [RQ — Job Queues in Python](https://python-rq.org/) | Tutorial completo de RQ |
| [tenacity — GitHub README](https://github.com/jd/tenacity) | Ejemplos prácticos de retry |
| [Python Concurrency — Real Python](https://realpython.com/python-concurrency/) | Threading vs asyncio vs multiprocessing |
| [Dead Letter Queue Pattern](https://aws.amazon.com/what-is/dead-letter-queue/) | Concepto de DLQ |

---

## Stack técnico de la semana

```
tenacity     # retry declarativo con backoff, condiciones y callbacks
rq           # Redis Queue — jobs en background con workers separados
redis        # cliente Python para Redis
```

### Instalación rápida

```bash
# Dependencias base (sin Redis)
pip install tenacity typer rich

# Con RQ
pip install rq redis

# Redis local
docker run -d -p 6379:6379 redis:alpine
```

---

## Herramientas complementarias

| Herramienta | Uso |
|-------------|-----|
| [RQ Dashboard](https://github.com/Parallels/rq-dashboard) | UI web para monitorear jobs RQ |
| [Flower](https://flower.readthedocs.io/) | Dashboard para Celery (alternativa a RQ) |
| [Celery](https://docs.celeryq.dev/) | Sistema de tareas distribuido — más features que RQ, más complejo |
| [Dramatiq](https://dramatiq.io/) | Alternativa moderna a Celery, más simple |
| [Apache Airflow](https://airflow.apache.org/) | Orquestador de workflows complejos con DAGs |

---

## Patrones clave de diseño

| Patrón | Descripción |
|--------|-------------|
| **Pipes & Filters** | Pipeline = tubería de filtros con contratos definidos |
| **Producer/Consumer** | Desacoplar producción de consumo con una cola intermedia |
| **Dead Letter Queue** | Cola de jobs definitivamente fallidos para inspección manual |
| **Circuit Breaker** | Pausar reintentos cuando el servicio externo está caído (ver `tenacity.stop_after_delay`) |
| **Saga** | Coordinar transacciones distribuidas con compensaciones en caso de fallo |

---

## Navegación

← [Teoría](../1-teoria/) · [Proyecto](../3-proyecto/)
