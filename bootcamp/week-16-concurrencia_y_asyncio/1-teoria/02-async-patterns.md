# 🔄 Patrones Async: gather, wait, TaskGroup, timeout

## 🎯 Objetivos

- Ejecutar múltiples corutinas con `asyncio.gather()`
- Usar `asyncio.wait()` para procesamiento parcial
- Procesar resultados según van llegando con `asyncio.as_completed()`
- Aplicar concurrencia estructurada con `TaskGroup` (Python 3.11+)
- Controlar tiempos de espera con `asyncio.timeout()`

---

## 1. `asyncio.gather()` — el más común

Ejecuta múltiples awaitables **concurrentemente** y retorna sus resultados en el mismo orden:

```python
import asyncio

async def fetch(name: str, delay: float) -> str:
    await asyncio.sleep(delay)
    return f"{name} ready"

async def main() -> None:
    results = await asyncio.gather(
        fetch("video.mp4", 2.0),
        fetch("image.png", 0.5),
        fetch("audio.mp3", 1.0),
    )
    # results está en el orden de los argumentos, no de finalización
    print(results)
    # ['video.mp4 ready', 'image.png ready', 'audio.mp3 ready']

asyncio.run(main())
```

### Manejo de errores en gather

Por defecto, si una corutina lanza una excepción, `gather` propaga el **primer** error y cancela el resto:

```python
async def main() -> None:
    try:
        results = await asyncio.gather(
            fetch("video.mp4", 1.0),
            fail_task(),              # lanza RuntimeError
            fetch("audio.mp3", 0.5),
        )
    except RuntimeError as e:
        print(f"failed: {e}")        # los otros tasks fueron cancelados

    # Con return_exceptions=True: errores como valores, no se propagan
    results = await asyncio.gather(
        fetch("video.mp4", 1.0),
        fail_task(),
        fetch("audio.mp3", 0.5),
        return_exceptions=True,
    )
    # results = ['video.mp4 ready', RuntimeError('...'), 'audio.mp3 ready']
    for r in results:
        if isinstance(r, Exception):
            print(f"error: {r}")
        else:
            print(f"ok: {r}")
```

---

## 2. `asyncio.TaskGroup` — concurrencia estructurada (Python 3.11+)

`TaskGroup` es la forma moderna y segura de gestionar múltiples tasks. Si **cualquier** task falla, cancela los demás automáticamente:

```python
import asyncio

async def main() -> None:
    results: list[str] = []

    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(fetch("video.mp4", 2.0))
        task2 = tg.create_task(fetch("image.png", 0.5))
        task3 = tg.create_task(fetch("audio.mp3", 1.0))
    # Al salir del bloque, todos los tasks terminaron (o uno falló)

    results = [task1.result(), task2.result(), task3.result()]
    print(results)
```

### `gather` vs `TaskGroup`

| | `gather` | `TaskGroup` |
|--|---------|-------------|
| Versión | 3.4+ | 3.11+ |
| Error handling | `return_exceptions=True` | Cancela el resto automáticamente |
| Estilo | Funcional | Context manager (structured) |
| Tasks dinámicos | No (lista fija) | Sí (`tg.create_task()` dentro del bloque) |
| Recomendado | Código legacy / compatibilidad | Código nuevo en 3.11+ |

---

## 3. `asyncio.wait()` — control granular

`wait()` retorna dos sets: los completados y los pendientes. Útil para "procesa los primeros N que terminen":

```python
import asyncio

async def main() -> None:
    tasks = {
        asyncio.create_task(fetch("video.mp4", 3.0), name="video"),
        asyncio.create_task(fetch("image.png", 1.0), name="image"),
        asyncio.create_task(fetch("audio.mp3", 2.0), name="audio"),
    }

    # Esperar solo hasta que el PRIMERO termine
    done, pending = await asyncio.wait(
        tasks,
        return_when=asyncio.FIRST_COMPLETED
    )

    for task in done:
        print(f"first done: {task.result()}")

    # Cancelar los que aún están pendientes
    for task in pending:
        task.cancel()

    # return_when opciones:
    # FIRST_COMPLETED — retorna cuando termina cualquiera
    # FIRST_EXCEPTION — retorna cuando uno lanza excepción
    # ALL_COMPLETED   — retorna cuando todos terminan (default)
```

---

## 4. `asyncio.as_completed()` — procesar en orden de llegada

Cuando quieres procesar cada resultado **apenas esté disponible**, sin esperar a todos:

```python
import asyncio
import time

async def main() -> None:
    coroutines = [
        fetch("video.mp4", 3.0),
        fetch("image.png", 0.5),
        fetch("audio.mp3", 1.5),
    ]

    start = time.perf_counter()

    # as_completed itera en orden de FINALIZACIÓN, no de creación
    async for coro in asyncio.as_completed(coroutines):
        result = await coro
        elapsed = time.perf_counter() - start
        print(f"[{elapsed:.1f}s] {result}")

    # Output:
    # [0.5s] image.png ready
    # [1.5s] audio.mp3 ready
    # [3.0s] video.mp4 ready
```

Ideal para pipelines donde cada resultado se procesa de inmediato (ej: mostrar progreso, escribir a disco según van llegando).

---

## 5. `asyncio.timeout()` — límite de tiempo (Python 3.11+)

```python
import asyncio

async def slow_download(name: str) -> str:
    await asyncio.sleep(10)      # simula descarga lenta
    return f"{name} done"

async def main() -> None:
    # Forma moderna (3.11+)
    try:
        async with asyncio.timeout(3.0):     # máximo 3 segundos
            result = await slow_download("video.mp4")
    except TimeoutError:
        print("download timed out")

    # Forma alternativa: asyncio.wait_for() (funciona en 3.10+)
    try:
        result = await asyncio.wait_for(slow_download("video.mp4"), timeout=3.0)
    except TimeoutError:
        print("download timed out")

asyncio.run(main())
```

---

## 6. Semáforos — limitar concurrencia

Sin límite, `gather` intentaría abrir 1000 conexiones simultáneas. `asyncio.Semaphore` limita cuántas corutinas avanzan a la vez:

```python
import asyncio

async def download_with_limit(
    sem: asyncio.Semaphore,
    name: str,
    delay: float,
) -> str:
    async with sem:                   # solo MAX_CONCURRENT a la vez
        await asyncio.sleep(delay)
        return f"{name} ready"

async def main() -> None:
    MAX_CONCURRENT = 3
    sem = asyncio.Semaphore(MAX_CONCURRENT)

    asset_names = [f"asset_{i:02d}.mp4" for i in range(10)]

    tasks = [
        download_with_limit(sem, name, 1.0)
        for name in asset_names
    ]

    results = await asyncio.gather(*tasks)
    print(f"Downloaded {len(results)} assets")
    # Se procesaron en lotes de 3, total ~4s en lugar de ~10s

asyncio.run(main())
```

---

## ✅ Resumen de patrones

| Patrón | Cuándo usar |
|--------|------------|
| `gather(*coros)` | Ejecutar N corutinas, necesitas todos los resultados |
| `gather(..., return_exceptions=True)` | Como gather pero errores como valores |
| `TaskGroup` (3.11+) | Concurrencia estructurada, cancelación automática |
| `wait(..., FIRST_COMPLETED)` | Procesar el primero que termine, cancelar el resto |
| `as_completed()` | Procesar resultados según van llegando |
| `timeout()` / `wait_for()` | Limitar tiempo máximo de espera |
| `Semaphore(N)` | Limitar concurrencia máxima simultánea |

---

## 📚 Recursos Adicionales

- [PEP 654 — Exception Groups (TaskGroup)](https://peps.python.org/pep-0654/)
- [asyncio.gather docs](https://docs.python.org/3/library/asyncio-task.html#asyncio.gather)
- [asyncio.TaskGroup docs](https://docs.python.org/3/library/asyncio-task.html#asyncio.TaskGroup)
