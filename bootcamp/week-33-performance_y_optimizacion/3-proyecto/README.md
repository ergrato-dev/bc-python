# Proyecto Semana 33 — studio-optimizer

## Descripción

CLI de optimización del pipeline de Studio BC que:

- **Profila** el pipeline con `cProfile` e identifica bottlenecks
- **Cachea** metadata generada por IA en Redis (patrón cache-aside)
- **Streaming**: calcula checksum e itera manifiestos JSONL sin cargar en memoria
- **Benchmarca** pipeline lento vs optimizado mostrando el speedup

## Estructura

```
starter/
├── pyproject.toml
├── src/
│   ├── __init__.py
│   ├── config.py        # AppConfig desde env (COMPLETE)
│   ├── pipeline.py      # SlowPipeline + OptimizedPipeline (COMPLETE)
│   ├── profiler.py      # PipelineProfiler — cProfile wrapper (TODO)
│   ├── cache.py         # MetadataCache — Redis cache-aside (TODO)
│   ├── streamer.py      # AssetStreamer — streaming I/O (TODO)
│   └── __main__.py      # CLI: profile, benchmark, cache-stats (COMPLETE)
└── tests/
    ├── __init__.py
    ├── conftest.py
    └── test_cache.py    # Tests con mock (TODO)
```

## Comandos

```bash
pip install -e ".[dev]"

# Benchmark (dry_run por defecto — sin Redis ni OPENAI_API_KEY)
python -m src benchmark mock_asset.mp4

# Profiling del pipeline lento
python -m src profile mock_asset.mp4 --top 10

# Estadísticas del cache
python -m src cache-stats

# Tests
pytest tests/ -v
mypy --strict src/
```

## Configuración

```bash
export DRY_RUN=true          # Sin Redis (mock en memoria)
export REDIS_HOST=localhost
export REDIS_PORT=6379
export CACHE_TTL=3600        # segundos
export CHUNK_SIZE=4194304    # 4 MB en bytes
```

## Tareas del Estudiante

### `profiler.py` — `PipelineProfiler`
- `profile(fn, *args, **kwargs)`: ejecutar `fn` bajo `cProfile`, guardar el `Profile`
- `report()`: generar string con top N funciones ordenadas por `cumtime`
- `top_functions(n)`: retornar `list[tuple[str, float]]` de (nombre, cumtime)

### `cache.py` — `MetadataCache`
- `get(key)`: leer del cache — `None` si miss
- `set(key, value, ttl)`: guardar con TTL
- `delete(key)`: invalidar entrada
- `stats()`: retornar dict con métricas del cache

### `streamer.py` — `AssetStreamer`
- `checksum(path)`: SHA-256 en streaming (sin cargar en memoria)
- `file_stats(path)`: `{size_bytes, size_mb, checksum}`
- `iter_lines(path)`: generador de líneas
- `iter_json_records(path)`: generador de registros JSONL

### `tests/test_cache.py`
- Al menos 6 tests con mock (sin Redis real)
- Cubrir: get miss, set+get, delete, overwrite, stats

## Criterios de Aceptación

- [ ] `python -m src benchmark --dry-run mock.mp4` muestra tabla con speedup
- [ ] `pytest tests/ -v` pasa sin Redis (DRY_RUN=true)
- [ ] `mypy --strict src/` pasa sin errores
- [ ] El speedup del pipeline optimizado es > 2× en la segunda corrida (cache hits)
