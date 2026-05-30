# Sitios Web — Semana 27: Arquitectura de Pipelines

## Diseño de Pipelines

| Recurso | Descripción |
|---------|-------------|
| [Martin Fowler — Pipes and Filters](https://www.enterpriseintegrationpatterns.com/patterns/messaging/PipesAndFilters.html) | Patrón canónico de pipelines: origen, filtros, sink |
| [Python `typing.Protocol`](https://docs.python.org/3/library/typing.html#typing.Protocol) | Contratos estructurales sin herencia — referencia oficial |
| [PEP 544 — Protocols](https://peps.python.org/pep-0544/) | Motivación y diseño del sistema de Protocols en Python |
| [Real Python — Python Concurrency](https://realpython.com/python-concurrency/) | threading vs asyncio vs multiprocessing con ejemplos prácticos |

## Colas y Threading

| Recurso | Descripción |
|---------|-------------|
| [Python `queue` module](https://docs.python.org/3/library/queue.html) | Queue, LifoQueue, PriorityQueue — referencia completa de la stdlib |
| [asyncio.Queue](https://docs.python.org/3/library/asyncio-queue.html) | Queue async thread-safe — para pipelines con `await` |
| [Python `threading` module](https://docs.python.org/3/library/threading.html) | Thread, Lock, Event, Semaphore |
| [concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html) | ThreadPoolExecutor y ProcessPoolExecutor |

## Redis Queue (RQ)

| Recurso | Descripción |
|---------|-------------|
| [RQ — Python RQ Docs](https://python-rq.org/docs/) | Jobs, Workers, queues, dependencias, timeouts — referencia completa |
| [RQ — GitHub](https://github.com/rq/rq) | Código fuente, changelog, ejemplos avanzados |
| [RQ Dashboard](https://github.com/Parallels/rq-dashboard) | UI web para monitorear jobs RQ en tiempo real |
| [redis-py Docs](https://redis-py.readthedocs.io/) | Cliente Python oficial de Redis |

## Manejo de Errores y Retry

| Recurso | Descripción |
|---------|-------------|
| [tenacity Docs](https://tenacity.readthedocs.io/) | Referencia completa de decoradores, estrategias y callbacks |
| [tenacity — GitHub](https://github.com/jd/tenacity) | Ejemplos prácticos y casos de uso reales |
| [AWS — Dead Letter Queue](https://aws.amazon.com/what-is/dead-letter-queue/) | Concepto de DLQ con contexto de sistemas distribuidos |
| [Circuit Breaker Pattern — Martin Fowler](https://martinfowler.com/bliki/CircuitBreaker.html) | Patrón complementario al retry para fallos en cascada |

## Comparativa de sistemas de colas

| Recurso | Descripción |
|---------|-------------|
| [RQ vs Celery vs Dramatiq](https://docs.celeryq.dev/en/stable/getting-started/introduction.html) | Introducción de Celery con comparativa implícita |
| [Dramatiq Docs](https://dramatiq.io/) | Alternativa moderna a Celery: más simple, orientada a RQ |
| [Apache Airflow — Intro](https://airflow.apache.org/docs/apache-airflow/stable/index.html) | Orquestador de DAGs — para pipelines más complejos |
