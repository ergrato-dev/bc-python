# Glosario — Semana 33: Performance y Optimización

## Profiling

| Término | Definición |
|---------|------------|
| **Profiling** | Proceso de medir dónde gasta tiempo (o memoria) un programa para identificar bottlenecks |
| **Deterministic profiling** | Profiling que instrumenta cada llamada a función — preciso pero con overhead (~cProfile) |
| **Sampling profiler** | Profiler que muestrea el stack a intervalos regulares — bajo overhead (~py-spy) |
| **cumtime** | Tiempo acumulado de una función + todas sus subcalls — la métrica más útil para identificar bottlenecks |
| **tottime** | Tiempo propio de la función sin contar el tiempo de las funciones que llama |
| **ncalls** | Número de llamadas a una función durante el profiling |
| **Bottleneck** | Función o sección del código que consume el mayor porcentaje del tiempo de ejecución |
| **Flame graph** | Visualización del call stack donde el ancho de cada barra es proporcional al tiempo — genera py-spy |
| **snakeviz** | Visualizador web interactivo de archivos `.prof` generados por cProfile |

## Memoria

| Término | Definición |
|---------|------------|
| **tracemalloc** | Módulo stdlib de Python para tracing de allocaciones de memoria — snapshots por línea |
| **memory_profiler** | Librería que decora funciones con `@profile` para ver uso de RAM línea a línea |
| **Peak memory** | Uso máximo de memoria alcanzado durante la ejecución — el dato más relevante para OOM |
| **OOM (Out of Memory)** | Error cuando el proceso consume más RAM de la disponible — causa que el OS lo mate |
| **Streaming** | Procesar datos en fragmentos secuenciales sin cargar todo el archivo en memoria |
| **Generador** | Función con `yield` que produce valores lazily — usa O(1) memoria independiente del dataset |
| **Chunk** | Fragmento de datos de tamaño fijo leído en cada iteración — típico 4–64 MB para I/O |
| **JSONL (JSON Lines)** | Formato donde cada línea es un JSON independiente — streameable sin parsear el archivo completo |

## Redis y Caching

| Término | Definición |
|---------|------------|
| **Redis** | Base de datos in-memory de tipo key-value — extremadamente rápida, usada como cache |
| **Cache** | Capa de almacenamiento rápido que guarda resultados costosos para evitar recalcularlos |
| **Cache-aside** | Patrón donde la app maneja el cache: GET → miss → generar → SET. La forma más común |
| **Write-through** | Patrón donde escribir en DB y cache ocurre simultáneamente — consistencia garantizada |
| **TTL (Time To Live)** | Tiempo de expiración de una entrada del cache — después del cual Redis la elimina automáticamente |
| **Cache hit** | El dato solicitado se encontró en el cache — respuesta inmediata sin costos de generación |
| **Cache miss** | El dato no está en el cache — hay que generarlo desde la fuente y luego guardarlo |
| **Invalidación** | Proceso de eliminar entradas del cache cuando el dato subyacente cambia |
| **SETEX** | Comando Redis que hace SET + EXPIRE en una sola operación atómica |
| **SCAN** | Comando Redis para iterar claves con un patrón — no usa `KEYS *` que bloquea |

## Async y Concurrencia

| Término | Definición |
|---------|------------|
| **Blocking call** | Llamada que congela el event loop de asyncio hasta que termina (`time.sleep`, `os.read`) |
| **asyncio.to_thread** | Ejecuta una función síncrona blocking en un ThreadPoolExecutor sin bloquear el event loop |
| **asyncio.Semaphore** | Límita cuántas corrutinas pueden ejecutarse simultáneamente — control de concurrencia |
| **Throttling** | Limitar el número de operaciones por unidad de tiempo — evita superar rate limits de APIs |
| **asyncio.gather** | Ejecuta múltiples corrutinas en paralelo y retorna cuando todas terminan |
| **Rate limit** | Límite de la API sobre cuántas requests se pueden hacer por segundo/minuto |

## Benchmarking

| Término | Definición |
|---------|------------|
| **Benchmark** | Medición reproducible del tiempo de ejecución de una función para comparar implementaciones |
| **timeit** | Módulo stdlib para medir tiempo de ejecución con warmup y múltiples repeticiones |
| **pytest-benchmark** | Plugin de pytest que integra benchmarks en la suite de tests con estadísticas detalladas |
| **Speedup** | Ratio entre el tiempo de la implementación lenta y la rápida: `t_slow / t_fast` |
| **Warmup** | Ejecuciones previas ignoradas en el benchmark para calentar caches del OS/CPU |
| **wall clock time** | Tiempo real transcurrido — incluye esperas de I/O. `time.perf_counter()` lo mide |
| **Baseline** | Medición de referencia antes de una optimización — para verificar la mejora |
