# 🏭 AsyncIO en Producción: aiofiles, Semaphores y Patrones

## 🎯 Objetivos

- Leer y escribir archivos de forma async con `aiofiles`
- Limitar concurrencia con `asyncio.Semaphore`
- Integrar bibliotecas síncronas en pipelines async
- Aplicar patrones de resiliencia: retry, timeout, circuit breaker básico

---

## 1. `aiofiles` — I/O de archivos sin bloquear

Las funciones `open()`, `read()` y `write()` estándar son síncronas y bloquean el event loop. `aiofiles` provee versiones async:

```python
import asyncio
import aiofiles

async def save_asset_metadata(path: str, metadata: dict[str, str]) -> None:
    import json
    async with aiofiles.open(path, mode="w", encoding="utf-8") as f:
        await f.write(json.dumps(metadata, indent=2))

async def load_asset_list(manifest_path: str) -> list[str]:
    async with aiofiles.open(manifest_path, mode="r", encoding="utf-8") as f:
        content = await f.read()
    return content.strip().splitlines()

async def copy_asset(src: str, dst: str) -> None:
    async with aiofiles.open(src, "rb") as reader:
        async with aiofiles.open(dst, "wb") as writer:
            # Leer y escribir en chunks para archivos grandes
            while chunk := await reader.read(1024 * 1024):   # 1 MB chunks
                await writer.write(chunk)
```

> Para archivos muy grandes (video, audio), siempre leer en chunks para no cargar todo en memoria.

---

## 2. Semáforos — throttling de concurrencia

Sin límite, `gather` intentaría procesar todos los assets a la vez, saturando el sistema. `asyncio.Semaphore` actúa como un "semáforo de acceso":

```python
import asyncio
import httpx

async def download_with_semaphore(
    sem: asyncio.Semaphore,
    client: httpx.AsyncClient,
    url: str,
) -> bytes:
    async with sem:    # solo MAX entra a la vez; el resto espera aquí
        response = await client.get(url)
        return response.content

async def download_batch(urls: list[str], max_concurrent: int = 5) -> list[bytes]:
    sem = asyncio.Semaphore(max_concurrent)
    async with httpx.AsyncClient() as client:
        tasks = [download_with_semaphore(sem, client, url) for url in urls]
        return await asyncio.gather(*tasks, return_exceptions=True)
```

---

## 3. Retry con backoff exponencial

Las redes fallan. Un pipeline robusto reintenta con espera creciente:

```python
import asyncio
import random

async def fetch_with_retry(
    url: str,
    max_retries: int = 3,
    base_delay: float = 1.0,
) -> bytes:
    last_error: Exception | None = None

    for attempt in range(max_retries):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=10.0)
                response.raise_for_status()
                return response.content

        except (httpx.HTTPError, httpx.TimeoutException) as e:
            last_error = e
            if attempt < max_retries - 1:
                # backoff exponencial + jitter para evitar thundering herd
                delay = base_delay * (2 ** attempt) + random.uniform(0, 0.5)
                print(f"attempt {attempt + 1} failed, retrying in {delay:.1f}s")
                await asyncio.sleep(delay)

    raise RuntimeError(f"failed after {max_retries} attempts: {last_error}")
```

> En producción usa la biblioteca `tenacity` (semana 19) en lugar de implementar retry manualmente.

---

## 4. Integrar boto3 y Pillow en pipelines async

Estas bibliotecas son síncronas. Se integran con `run_in_executor`:

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import boto3
from PIL import Image
import io

# I/O con boto3 (síncrono) → ThreadPoolExecutor
def upload_to_s3(data: bytes, bucket: str, key: str) -> str:
    s3 = boto3.client("s3")
    s3.put_object(Bucket=bucket, Key=key, Body=data)
    return f"s3://{bucket}/{key}"

# CPU-bound con Pillow → ProcessPoolExecutor
def generate_thumbnail(image_data: bytes, max_size: tuple[int, int]) -> bytes:
    img = Image.open(io.BytesIO(image_data))
    img.thumbnail(max_size, Image.LANCZOS)
    output = io.BytesIO()
    img.save(output, format="JPEG", quality=85)
    return output.getvalue()

async def process_image_asset(image_data: bytes, name: str) -> str:
    loop = asyncio.get_running_loop()

    # CPU en proceso separado
    with ProcessPoolExecutor() as cpu_pool:
        thumbnail = await loop.run_in_executor(
            cpu_pool, generate_thumbnail, image_data, (800, 600)
        )

    # I/O en thread pool
    with ThreadPoolExecutor() as io_pool:
        s3_url = await loop.run_in_executor(
            io_pool, upload_to_s3, thumbnail, "studio-bc-assets", f"thumbs/{name}"
        )

    return s3_url
```

---

## 5. Patrón: pipeline de assets con progreso

```python
import asyncio
from dataclasses import dataclass, field
from typing import Literal

type PipelineStatus = Literal["pending", "downloading", "processing", "done", "failed"]

@dataclass
class AssetTask:
    name: str
    url: str
    status: PipelineStatus = "pending"
    error: str | None = None

async def run_pipeline(assets: list[AssetTask], max_concurrent: int = 4) -> None:
    sem = asyncio.Semaphore(max_concurrent)
    completed = 0
    total = len(assets)

    async def process_one(task: AssetTask) -> None:
        nonlocal completed
        async with sem:
            try:
                task.status = "downloading"
                await asyncio.sleep(1)    # simula descarga

                task.status = "processing"
                await asyncio.sleep(0.5)  # simula procesamiento

                task.status = "done"
            except Exception as e:
                task.status = "failed"
                task.error = str(e)
            finally:
                completed += 1
                print(f"[{completed}/{total}] {task.name}: {task.status}")

    await asyncio.gather(*[process_one(a) for a in assets])

    done = sum(1 for a in assets if a.status == "done")
    failed = sum(1 for a in assets if a.status == "failed")
    print(f"\nSummary: {done} done, {failed} failed")

async def main() -> None:
    assets = [AssetTask(f"asset_{i:02d}.mp4", f"https://cdn.example.com/asset_{i}.mp4")
              for i in range(8)]
    await run_pipeline(assets, max_concurrent=3)

asyncio.run(main())
```

---

## ✅ Checklist para código async en producción

- [ ] Sin `time.sleep()` — usar `await asyncio.sleep()`
- [ ] Sin `requests` — usar `httpx.AsyncClient` o `aiohttp`
- [ ] Sin `open()` en corutinas — usar `aiofiles`
- [ ] Semáforo para limitar concurrencia cuando el recurso externo tiene límites
- [ ] Manejo de errores con `try/except` en cada tarea (no solo en `gather`)
- [ ] Timeout configurado en todas las llamadas de red
- [ ] Código CPU-bound delegado a `ProcessPoolExecutor`
- [ ] Código I/O síncrono delegado a `ThreadPoolExecutor`

---

## 📚 Recursos Adicionales

- [aiofiles en PyPI](https://github.com/Tinche/aiofiles)
- [asyncio — Best Practices](https://docs.python.org/3/library/asyncio-dev.html)
- [httpx — async client](https://www.python-httpx.org/)
