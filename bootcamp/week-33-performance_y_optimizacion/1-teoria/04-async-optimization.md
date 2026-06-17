# Async Optimization

## 1. El Problema: Blocking Calls en asyncio

`asyncio` es single-threaded. Una llamada blocking bloquea el event loop completo:

```python
import asyncio
import time


async def bad_pipeline(paths: list[str]) -> list[dict]:
    results = []
    for p in paths:
        time.sleep(2)          # BLOCKING — congela todo el event loop
        results.append({"path": p})
    return results              # Total: N × 2 segundos, secuencial
```

```python
async def good_pipeline(paths: list[str]) -> list[dict]:
    results = []
    for p in paths:
        await asyncio.sleep(2)  # NO-blocking — cede el event loop
        results.append({"path": p})
    return results              # Total: N × 2 segundos, pero puede intercalar
```

---

## 2. Paralelismo Real con asyncio.gather

```python
import asyncio
import httpx


async def fetch_metadata(client: httpx.AsyncClient, url: str) -> dict:
    r = await client.get(url)
    return r.json()


async def fetch_all(urls: list[str]) -> list[dict]:
    async with httpx.AsyncClient() as client:
        tasks = [fetch_metadata(client, url) for url in urls]
        return await asyncio.gather(*tasks)  # Todas en paralelo


# Resultados: N requests en ~1 RTT (no N × 1 RTT)
```

---

## 3. asyncio.to_thread — CPU-bound sin Blocking

Para código síncrono lento (cProfile, hashlib, subprocess), usar `asyncio.to_thread`
lo ejecuta en un ThreadPoolExecutor sin bloquear el event loop:

```python
import asyncio
import hashlib
from pathlib import Path


def _sha256_sync(path: Path) -> str:
    """Cálculo síncrono — puede tardar segundos en archivos grandes."""
    sha = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4 * 1024 * 1024), b""):
            sha.update(chunk)
    return sha.hexdigest()


async def sha256_async(path: Path) -> str:
    """Wrapper async — no bloquea el event loop."""
    return await asyncio.to_thread(_sha256_sync, path)


async def process_batch(paths: list[Path]) -> list[str]:
    tasks = [sha256_async(p) for p in paths]
    return await asyncio.gather(*tasks)   # Todos en paralelo (threads)
```

---

## 4. asyncio.Semaphore — Throttling de Concurrencia

Limitar el número de requests simultáneos para no superar rate limits de la API:

```python
import asyncio
import httpx

MAX_CONCURRENT = 5  # máximo 5 llamadas a la API al mismo tiempo


async def analyze_with_throttle(
    client: httpx.AsyncClient,
    sem: asyncio.Semaphore,
    asset_url: str,
) -> dict:
    async with sem:          # bloquea si ya hay 5 corriendo
        response = await client.post(
            "https://api.openai.com/v1/chat/completions",
            json={"model": "gpt-4o-mini", "messages": [...]},
        )
        return response.json()


async def analyze_batch(asset_urls: list[str]) -> list[dict]:
    sem = asyncio.Semaphore(MAX_CONCURRENT)
    async with httpx.AsyncClient() as client:
        tasks = [analyze_with_throttle(client, sem, url) for url in asset_urls]
        return await asyncio.gather(*tasks)
```

Sin Semaphore: 100 requests simultáneos → rate limit error.
Con Semaphore(5): máximo 5 simultáneos → ~20 rondas de 5 → sin errores.

---

## 5. asyncio.wait con FIRST_COMPLETED — Streaming de Resultados

```python
import asyncio


async def process_stream(paths: list[Path]) -> None:
    """Procesa y muestra resultados a medida que terminan, sin esperar al lento."""
    tasks = {asyncio.create_task(analyze_asset(p)): p for p in paths}
    pending = set(tasks.keys())

    while pending:
        done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)
        for task in done:
            result = task.result()
            print(f"Completado: {result['title']}")  # Disponible inmediatamente
```

---

## 6. Evitar Subprocess Blocking

```python
import asyncio


async def run_ffmpeg(cmd: list[str]) -> bytes:
    """Ejecuta ffmpeg sin bloquear el event loop."""
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg error: {stderr.decode()}")
    return stdout


async def extract_audio_async(video_path: Path) -> Path:
    out = video_path.with_suffix(".mp3")
    await run_ffmpeg([
        "ffmpeg", "-i", str(video_path), "-vn",
        "-acodec", "libmp3lame", "-q:a", "4", str(out), "-y",
    ])
    return out
```

---

## 7. Comparación: Sequential vs Parallel vs Throttled

```python
import asyncio, time


async def sequential(n: int) -> float:
    t = time.perf_counter()
    for _ in range(n):
        await asyncio.sleep(0.1)      # simula 100ms de latencia de API
    return time.perf_counter() - t    # ~n * 0.1 seg


async def parallel(n: int) -> float:
    t = time.perf_counter()
    await asyncio.gather(*[asyncio.sleep(0.1) for _ in range(n)])
    return time.perf_counter() - t    # ~0.1 seg independiente de n


async def throttled(n: int, limit: int = 5) -> float:
    sem = asyncio.Semaphore(limit)
    t = time.perf_counter()

    async def _task() -> None:
        async with sem:
            await asyncio.sleep(0.1)

    await asyncio.gather(*[_task() for _ in range(n)])
    return time.perf_counter() - t    # ~ceil(n/limit) * 0.1 seg


asyncio.run(sequential(20))   # ~2.0 seg
asyncio.run(parallel(20))     # ~0.1 seg
asyncio.run(throttled(20, 5)) # ~0.4 seg
```

---

## Resumen

| Técnica | Cuándo |
|---------|--------|
| `asyncio.gather` | Múltiples tareas I/O independientes |
| `asyncio.to_thread` | Código síncrono blocking (I/O, hashlib, subprocess) |
| `asyncio.Semaphore` | Limitar concurrencia para respetar rate limits |
| `asyncio.wait(FIRST_COMPLETED)` | Streaming de resultados a medida que terminan |
| `asyncio.create_subprocess_exec` | Subprocess sin bloquear el event loop |
