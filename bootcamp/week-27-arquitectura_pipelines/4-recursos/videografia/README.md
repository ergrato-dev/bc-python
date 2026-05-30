# Videos — Semana 27: Arquitectura de Pipelines

## Diseño de Pipelines y Patrones

| Recurso | Canal | Descripción |
|---------|-------|-------------|
| [Pipeline Design Pattern in Python](https://www.youtube.com/watch?v=C1ZtKg-XMEc) | ArjanCodes | Diseño de pipelines con Protocol y composición (~30 min) |
| [Python Structural Subtyping (Protocols)](https://www.youtube.com/watch?v=xvb5hGLoK0A) | mCoding | PEP 544, Protocols vs ABC, mypy structural typing (~20 min) |

## Concurrencia y Colas

| Recurso | Canal | Descripción |
|---------|-------|-------------|
| [Python Threading — Producer Consumer](https://www.youtube.com/watch?v=IEEhzQoKtQU) | Corey Schafer | threading.Thread, Queue, producer/consumer con ejemplos (~45 min) |
| [asyncio.Queue — Async Pipelines](https://www.youtube.com/watch?v=t5Bo1Je9EmE) | Tech With Tim | asyncio.Queue, gather, TaskGroup para pipelines asíncronos (~25 min) |
| [Python concurrent.futures](https://www.youtube.com/watch?v=fKl2JW_qrso) | Corey Schafer | ThreadPoolExecutor, ProcessPoolExecutor, as_completed (~20 min) |

## Redis Queue (RQ)

| Recurso | Canal | Descripción |
|---------|-------|-------------|
| [RQ (Redis Queue) Tutorial](https://www.youtube.com/watch?v=UMxVGUMiXoc) | Pretty Printed | Setup, workers, jobs, resultados y DLQ (~20 min) |
| [Redis in Python — Full Guide](https://www.youtube.com/watch?v=Hbt56gFj998) | Tech With Tim | Redis client, operaciones básicas, use cases (~30 min) |

## Retry y Manejo de Errores

| Recurso | Canal | Descripción |
|---------|-------|-------------|
| [tenacity Python Retry Library](https://www.youtube.com/watch?v=wlpn2EWM_8w) | NeuralNine | Decoradores tenacity, backoff exponencial, condiciones (~15 min) |
| [Circuit Breaker Pattern](https://www.youtube.com/watch?v=ADHjBckEPsU) | ByteByteGo | Explicación visual del Circuit Breaker (~8 min) |

## Recomendación de ruta de aprendizaje

```
1. Diseño de pipelines (ArjanCodes) — base arquitectural
2. threading Producer/Consumer (Corey Schafer) — colas y workers
3. RQ Tutorial (Pretty Printed) — jobs en background
4. tenacity retry (NeuralNine) — manejo de errores robusto
```
