# Semana 27: Arquitectura de Pipelines

> **Fase 3 — Automatización y Pipelines de Media** · _Mid-level → Senior_

## Objetivos de Aprendizaje

Al finalizar esta semana, serás capaz de:

- Diseñar pipelines como cadenas de etapas con contratos explícitos (`Protocol`)
- Implementar comunicación entre etapas con `queue.Queue` y `asyncio.Queue`
- Encolar trabajos en background con Redis Queue (`rq`)
- Aplicar retry con backoff exponencial usando `tenacity`
- Modelar el estado de un job con una máquina de estados y persistirlo en JSON

---

## Contenidos

| # | Archivo | Tema |
|---|---------|------|
| 01 | [Diseño de Pipelines](1-teoria/01-diseno-pipelines.md) | Etapas, contratos, composición lineal y ramificada |
| 02 | [Colas y Threading](1-teoria/02-colas-threading.md) | `queue.Queue`, Producer/Consumer, `asyncio.Queue` |
| 03 | [Redis Queue — RQ](1-teoria/03-redis-rq.md) | Jobs, Workers, enqueue, resultados, monitoreo |
| 04 | [Manejo de Errores y Retry](1-teoria/04-manejo-errores-retry.md) | tenacity, backoff exponencial, dead-letter queue |
| 05 | [Estado y Observabilidad](1-teoria/05-estado-observabilidad.md) | Máquina de estados, logging por etapa, throughput |

---

## Estructura de la Semana

```
week-27-arquitectura_pipelines/
├── README.md
├── rubrica-evaluacion.md
├── 0-assets/               # SVGs de apoyo a la teoría
├── 1-teoria/               # 5 archivos .md
├── 2-ejercicios/
│   ├── 01-queue-producer-consumer/
│   ├── 02-pipeline-lineal/
│   ├── 03-retry-backoff/
│   └── 04-rq-worker/
├── 3-proyecto/
│   ├── README.md           # studio-pipeline
│   ├── starter/
│   └── solution/
├── 4-recursos/
└── 5-glosario/
```

---

## Distribución del Tiempo (6h)

| Bloque | Actividad | Tiempo |
|--------|-----------|--------|
| 1 | Teoría: diseño + colas + RQ | 1.5h |
| 2 | Teoría: errores + estado/observabilidad | 1.0h |
| 3 | Ejercicios guiados (4) | 2.0h |
| 4 | Proyecto semanal | 1.5h |

---

## Stack de la Semana

| Librería | Rol |
|----------|-----|
| `queue` | Colas thread-safe de la stdlib (FIFO, LIFO, Priority) |
| `asyncio` | `asyncio.Queue` para pipelines asíncronos |
| `rq` | Redis Queue — encolar y ejecutar jobs en workers separados |
| `redis` | Cliente Python para Redis |
| `tenacity` | Retry con backoff exponencial y condiciones declarativas |

---

## Navegación

← [Semana 26 — Cloud Storage y Assets](../week-26-cloud_storage/README.md) · [Semana 28 — Integraciones con Plataformas](../week-28-integraciones_plataformas/README.md) →
