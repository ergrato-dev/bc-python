# Rúbrica de Evaluación — Semana 33: Performance y Optimización

## Puntaje Total: 100 puntos · Mínimo para aprobar: 70 pts

---

## Conocimiento (30 pts)

| Indicador | Puntos |
|-----------|--------|
| Explica qué mide `cumtime` en cProfile y cómo identificar el bottleneck principal | 8 |
| Describe la diferencia entre procesar un archivo completo en memoria vs streaming con generadores | 7 |
| Explica el patrón cache-aside: flujo de lectura, escritura y expiración con TTL | 8 |
| Describe cuándo usar `asyncio.to_thread` vs `asyncio.Semaphore` y por qué | 7 |

---

## Desempeño (40 pts)

| Indicador | Puntos |
|-----------|--------|
| `PipelineProfiler.profile()` ejecuta `fn` bajo `cProfile` y devuelve su resultado | 10 |
| `MetadataCache.get/set/delete` funciona correctamente en dry_run (mock Redis) | 10 |
| `AssetStreamer.checksum()` calcula SHA-256 de un archivo sin cargarlo completo | 10 |
| `AssetStreamer.iter_json_records()` itera un JSONL sin cargar el archivo completo | 10 |

---

## Producto (30 pts)

| Indicador | Puntos |
|-----------|--------|
| `python -m src benchmark --dry-run` muestra tabla con speedup del pipeline optimizado | 12 |
| `pytest tests/ -v` pasa sin Redis ni OPENAI_API_KEY (dry_run mock) | 10 |
| `python -m src profile --dry-run` muestra reporte de cProfile con top funciones | 5 |
| `mypy --strict src/` pasa sin errores | 3 |
