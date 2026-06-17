# Semana 33: Performance y Optimización

> **Fase 4 — Arquitectura Master y Sistema de Producción** · _Senior → Master_

## Objetivos de Aprendizaje

Al finalizar esta semana, serás capaz de:

- Perfilar código Python con `cProfile`, `pstats` e identificar bottlenecks
- Medir consumo de memoria con `tracemalloc` y procesar archivos grandes en streaming
- Implementar el patrón cache-aside con Redis usando `redis-py`
- Evitar blocking calls en `asyncio` con `to_thread` y `Semaphore`
- Comparar implementaciones con `timeit` y `pytest-benchmark`

---

## Contenidos

| # | Archivo | Tema |
|---|---------|------|
| 01 | [Profiling con cProfile](1-teoria/01-profiling-cpython.md) | cProfile, pstats, snakeviz, py-spy |
| 02 | [Memory Profiler y Streaming](1-teoria/02-memory-profiler.md) | tracemalloc, generadores, streaming I/O |
| 03 | [Caching con Redis](1-teoria/03-caching-redis.md) | redis-py, cache-aside, TTL, invalidación |
| 04 | [Async Optimization](1-teoria/04-async-optimization.md) | blocking calls, Semaphore, to_thread, throttling |
| 05 | [Benchmarking](1-teoria/05-benchmarking.md) | timeit, pytest-benchmark, comparación de implementaciones |

---

## Estructura de la Semana

```
week-33-performance_y_optimizacion/
├── README.md
├── rubrica-evaluacion.md
├── 1-teoria/
│   ├── 01-profiling-cpython.md
│   ├── 02-memory-profiler.md
│   ├── 03-caching-redis.md
│   ├── 04-async-optimization.md
│   └── 05-benchmarking.md
├── 2-ejercicios/
│   ├── 01-profiling-pipeline/
│   ├── 02-streaming-io/
│   ├── 03-redis-cache/
│   └── 04-benchmark-compare/
├── 3-proyecto/
│   ├── README.md           # studio-optimizer
│   ├── starter/
│   └── solution/
├── 4-recursos/
└── 5-glosario/
```

---

## Distribución del Tiempo (6h)

| Bloque | Actividad | Tiempo |
|--------|-----------|--------|
| 1 | Teoría: cProfile + Memory Profiler | 1.5h |
| 2 | Teoría: Redis + Async + Benchmark | 1.0h |
| 3 | Ejercicios guiados (4) | 2.0h |
| 4 | Proyecto semanal | 1.5h |

---

## Stack de la Semana

| Librería | Rol |
|----------|-----|
| `redis` | Cliente Redis — caching de metadata |
| `memory-profiler` | Decorador `@profile` para memory line-by-line |
| `pytest-benchmark` | Benchmark integrado en pytest |
| `rich` | CLI output con tablas y progress |

---

## Prerequisito

```bash
pip install redis memory-profiler pytest-benchmark rich typer

# Redis local (Docker):
docker run -d -p 6379:6379 redis:7-alpine

# Sin Redis — usar dry_run=True
export DRY_RUN=true
```

---

## Navegación

← [Semana 32 — IA Aplicada a Media](../week-32-ia_aplicada_media/README.md) · [Semana 34 — DevOps y CI/CD](../week-34-devops_y_cicd/README.md) →
