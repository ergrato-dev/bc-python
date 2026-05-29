# Proyecto Semana 16 — Asset Pipeline Async

## Descripción

Construir un pipeline de procesamiento de assets para Studio BC que integre todas las herramientas de concurrencia vistas en la semana: asyncio, concurrent.futures, semáforos, y manejo robusto de errores.

El pipeline completo debe:

1. Leer un manifiesto de assets desde un archivo JSON (async con `aiofiles`)
2. Descargar los assets desde CDN simulado con control de concurrencia (`Semaphore`)
3. Generar thumbnails (simulado, CPU-bound con `ProcessPoolExecutor`)
4. Guardar los resultados en un archivo de reporte (async con `aiofiles`)
5. Mostrar progreso en tiempo real (`as_completed`)

---

## Estructura del proyecto

```
starter/
├── src/
│   ├── models.py       — dataclasses: AssetManifest, AssetResult, PipelineReport
│   ├── downloader.py   — descarga async con semáforo y retry
│   ├── processor.py    — thumbnail generation con ProcessPoolExecutor
│   └── reporter.py     — escritura async del reporte final
├── main.py             — orquestación del pipeline completo
├── manifest.json       — datos de entrada (ya provisto)
└── pyproject.toml
```

---

## Requerimientos

### `src/models.py`

```python
@dataclass
class AssetManifest:
    project_id: str
    assets: list[dict[str, str]]   # {name, url, type}

@dataclass
class AssetResult:
    name: str
    status: Literal["ok", "failed"]
    size_bytes: int = 0
    thumbnail_path: str | None = None
    error: str | None = None

@dataclass
class PipelineReport:
    project_id: str
    started_at: str
    finished_at: str
    results: list[AssetResult]

    @property
    def summary(self) -> dict[str, int]:
        # retorna {"ok": N, "failed": M}
        ...
```

### `src/downloader.py`

- `async def download_asset(sem, client, name, url) -> AssetResult`
  - Usa `asyncio.Semaphore` (máx 4 concurrentes)
  - Retry hasta 2 veces con backoff exponencial
  - Timeout de 5s por intento
  - En caso de error definitivo: retorna `AssetResult(status="failed", error=...)`

### `src/processor.py`

- `def generate_thumbnail_sync(image_data: bytes, name: str) -> tuple[str, bytes]`
  - Función síncrona (para ProcessPoolExecutor)
  - Simula trabajo CPU con `hashlib` loops
  - Retorna `(thumbnail_path, thumbnail_bytes)`

- `async def process_assets_cpu(results: list[AssetResult]) -> list[AssetResult]`
  - Solo procesa los `status="ok"` con tipo imagen
  - Usa `loop.run_in_executor(ProcessPoolExecutor())`

### `src/reporter.py`

- `async def write_report(report: PipelineReport, output_path: str) -> None`
  - Serializa con `json.dumps(..., indent=2)`
  - Escribe async con `aiofiles`

### `main.py`

- Lee `manifest.json` con `aiofiles`
- Muestra progreso con `asyncio.as_completed()`
- Ejecuta todo el pipeline
- Escribe `output/report.json`

---

## Rúbrica (30 pts)

| Criterio | Puntos |
|----------|--------|
| models.py completo con tipos correctos y `summary` property | 5 |
| downloader con semáforo, retry y timeout | 8 |
| processor usa ProcessPoolExecutor correctamente | 5 |
| reporter escribe JSON con aiofiles | 4 |
| main.py orquesta el pipeline y muestra progreso | 5 |
| mypy --strict pasa sin errores | 3 |

---

## Ejecutar

```bash
cd starter
uv run python main.py
```

Resultado esperado:
```
[0.8s] ✅ logo.png OK
[1.2s] ✅ intro.mp4 OK
[1.5s] ❌ broken_asset.mp4 FAILED: timeout
...
── Reporte ──
  ok: 7, failed: 1
  Guardado en: output/report.json
```
