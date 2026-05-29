# Ejercicio 03 — concurrent.futures

## Objetivos

- Usar `ThreadPoolExecutor` para paralelizar I/O síncrono
- Usar `ProcessPoolExecutor` para trabajo CPU-bound real
- Elegir entre `submit()` y `map()` según la necesidad
- Integrar un executor en una corutina async con `run_in_executor`

## Duración estimada

40 minutos

---

## Contexto

Studio BC tiene un script legacy que usa `requests` para descargar assets y `hashlib` para validar checksums. Necesita paralelizarlo sin reescribir todo como async.

---

## Pasos

### Paso 1 — ThreadPoolExecutor con `map()`

Paraleliza `validate_asset_sync` (que usa `time.sleep` simulando I/O) con `ThreadPoolExecutor(max_workers=4)` y `executor.map()`. Compara el tiempo con la versión secuencial.

### Paso 2 — ThreadPoolExecutor con `submit()` y `as_completed`

Convierte a `submit()` + `as_completed`. Imprime cada resultado en el orden en que termina, no en el orden de input.

### Paso 3 — ProcessPoolExecutor para CPU-bound

`compute_checksum` hace trabajo CPU-intensivo (simulado con un bucle). Paraleliza con `ProcessPoolExecutor`. Verifica que el tiempo se reduce con múltiples cores.

### Paso 4 — Integrar en async con `run_in_executor`

Desde una corutina `async def process_project()`, delega `validate_asset_sync` a `ThreadPoolExecutor` y `compute_checksum` a `ProcessPoolExecutor` usando `loop.run_in_executor()`.

---

## Ejecutar

```bash
cd starter
uv run python main.py
```

## Criterios de éxito

- Paso 1: tiempo ≈ ceil(N/workers) × delay
- Paso 2: resultados impresos en orden de finalización (no de input)
- Paso 3: tiempo CPU se reduce con más procesos
- Paso 4: la corutina no bloquea el event loop durante los ejecutores
