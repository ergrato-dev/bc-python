# Benchmarking

## 1. timeit — Benchmark Rápido en Código

```python
import timeit

# Benchmark inline
elapsed = timeit.timeit(
    stmt="sum(range(10_000))",
    number=10_000,    # repeticiones
)
print(f"{elapsed:.4f}s — {elapsed/10_000*1_000_000:.1f} µs/op")


# Benchmark de una función existente
def compute_checksum(data: bytes) -> str:
    import hashlib
    return hashlib.sha256(data).hexdigest()


data = b"x" * 1_024_000  # 1 MB

elapsed = timeit.timeit(
    stmt=lambda: compute_checksum(data),
    number=100,
)
print(f"SHA-256 (1 MB): {elapsed/100*1000:.2f} ms/op")
```

---

## 2. Comparar Dos Implementaciones

```python
import timeit
from pathlib import Path


def read_full(path: Path) -> int:
    """Carga completa."""
    return len(path.read_bytes())


def read_streaming(path: Path) -> int:
    """Streaming en chunks."""
    total = 0
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4 * 1024 * 1024), b""):
            total += len(chunk)
    return total


path = Path("footage/sample_4k.mp4")
n = 10

t_full = timeit.timeit(lambda: read_full(path), number=n)
t_stream = timeit.timeit(lambda: read_streaming(path), number=n)

print(f"Full:      {t_full/n*1000:.1f} ms/op")
print(f"Streaming: {t_stream/n*1000:.1f} ms/op")
print(f"Speedup:   {t_full/t_stream:.2f}×")
```

---

## 3. pytest-benchmark — Benchmark Integrado en Tests

```bash
pip install pytest-benchmark
```

```python
# tests/test_benchmark.py
from pathlib import Path
import hashlib


def sha256_loop(data: bytes) -> str:
    sha = hashlib.sha256()
    sha.update(data)
    return sha.hexdigest()


def sha256_one_shot(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def test_sha256_loop(benchmark) -> None:
    data = b"a" * 1_000_000
    result = benchmark(sha256_loop, data)
    assert len(result) == 64


def test_sha256_oneshot(benchmark) -> None:
    data = b"a" * 1_000_000
    result = benchmark(sha256_one_shot, data)
    assert len(result) == 64
```

```bash
pytest tests/test_benchmark.py -v --benchmark-sort=mean

# Salida:
# Name                      Min        Max        Mean    StdDev  Median    IQR
# test_sha256_loop        1.23ms    1.41ms    1.28ms    0.05ms   1.26ms   0.07ms
# test_sha256_oneshot     1.19ms    1.35ms    1.21ms    0.04ms   1.20ms   0.05ms
```

---

## 4. Opciones Útiles de pytest-benchmark

```bash
# Guardar resultados para comparar después
pytest --benchmark-save=before_opt

# Comparar con run anterior
pytest --benchmark-compare=before_opt

# Más repeticiones para mayor precisión
pytest --benchmark-min-rounds=50

# Warmup antes de medir
pytest --benchmark-warmup=on

# Exportar a JSON
pytest --benchmark-json=results.json

# Solo mostrar, sin fallar por performance
pytest --benchmark-disable-gc --benchmark-sort=mean
```

---

## 5. Benchmark con Fixtures de Datos

```python
import pytest
from pathlib import Path


@pytest.fixture(scope="session")
def sample_data() -> bytes:
    return b"a" * 10_000_000  # 10 MB — se crea una sola vez


def json_serialize_fast(data: dict) -> str:
    import json
    return json.dumps(data, separators=(",", ":"))


def json_serialize_pretty(data: dict) -> str:
    import json
    return json.dumps(data, indent=2)


def test_json_fast(benchmark, sample_data: bytes) -> None:
    payload = {"data": sample_data[:100].hex(), "tags": list(range(20))}
    result = benchmark(json_serialize_fast, payload)
    assert isinstance(result, str)


def test_json_pretty(benchmark, sample_data: bytes) -> None:
    payload = {"data": sample_data[:100].hex(), "tags": list(range(20))}
    result = benchmark(json_serialize_pretty, payload)
    assert isinstance(result, str)
```

---

## 6. Pipeline Benchmark: Cache vs Sin Cache

```python
import time
from pathlib import Path


def benchmark_pipeline(pipeline, paths: list[Path], runs: int = 5) -> dict[str, float]:
    """Mide tiempo promedio del pipeline sobre una lista de assets."""
    times = []
    for _ in range(runs):
        t0 = time.perf_counter()
        for p in paths:
            pipeline.process(p)
        times.append(time.perf_counter() - t0)

    avg = sum(times) / len(times)
    return {
        "runs": runs,
        "avg_total_s": round(avg, 3),
        "avg_per_asset_ms": round(avg / len(paths) * 1000, 1),
        "min_s": round(min(times), 3),
        "max_s": round(max(times), 3),
    }


# Comparar
slow_stats = benchmark_pipeline(SlowPipeline(), asset_paths)
fast_stats = benchmark_pipeline(OptimizedPipeline(), asset_paths)
speedup = slow_stats["avg_total_s"] / fast_stats["avg_total_s"]
print(f"Speedup: {speedup:.1f}×")
```

---

## 7. Reglas de Benchmarking Confiable

```
1. Usar datos representativos — no solo 1 byte
2. Warmup — las primeras N corridas pueden ser más lentas (JIT, caches del OS)
3. Múltiples repeticiones — al menos 5-10 para promediar ruido
4. Aislar variables — no comparar A+B vs C cuando solo quieres A vs C
5. Medir lo correcto — wall clock para I/O, CPU time para cálculo puro
6. Documentar el baseline — guardar resultados antes de optimizar
```

---

## Resumen

| Herramienta | Uso |
|-------------|-----|
| `timeit.timeit` | Benchmark rápido de expresiones o funciones |
| `time.perf_counter` | Medición de wall clock en código de aplicación |
| `pytest-benchmark` | Benchmark integrado en la suite de tests |
| `--benchmark-compare` | Comparar antes/después de una optimización |
| `--benchmark-save` | Guardar resultados baseline para comparación futura |
