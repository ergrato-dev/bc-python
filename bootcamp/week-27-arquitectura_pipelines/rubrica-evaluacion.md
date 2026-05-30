# Rúbrica de Evaluación — Semana 27: Arquitectura de Pipelines

## Puntaje Total: 100 puntos · Mínimo para aprobar: 70 pts

---

## Conocimiento (30 pts)

| Indicador | Puntos |
|-----------|--------|
| Explica qué es un contrato de etapa (`Protocol`) y por qué es preferible a herencia para pipelines | 7 |
| Describe la diferencia entre `queue.Queue` (threading) y `asyncio.Queue` (coroutines) y cuándo usar cada uno | 8 |
| Explica cómo funciona `tenacity.retry` con `wait_exponential` y `stop_after_attempt` | 8 |
| Describe la secuencia de estados `pending → running → done/failed` y qué dispara cada transición | 7 |

## Desempeño (40 pts)

| Indicador | Puntos |
|-----------|--------|
| Implementa un `Stage` con el protocolo `process(input) → Result` y lo encadena en un `Pipeline` | 10 |
| Implementa un Producer/Consumer con `queue.Queue` y `threading.Thread` | 10 |
| Aplica `@retry` de tenacity a una función que puede fallar, con backoff exponencial y máximo de reintentos | 10 |
| Encola un job con `rq` y recupera su resultado o estado de error | 10 |

## Producto (30 pts)

| Indicador | Puntos |
|-----------|--------|
| `studio-pipeline` encadena etapas `Ingest → Process → Export` con contrato `Stage` | 12 |
| Cada job persiste su estado en `.pipeline_state.json` con transiciones correctas | 10 |
| Los errores en una etapa activan retry (max 3) y pasan el job a `failed` si se agotan los intentos | 5 |
| mypy --strict pasa sin errores en el módulo principal | 3 |
