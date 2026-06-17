# Profiling con cProfile

## 1. ¿Por qué perfilar antes de optimizar?

> "Premature optimization is the root of all evil." — Donald Knuth

El 90% del tiempo de ejecución suele estar en el 10% del código. Perfilar primero
revela exactamente dónde está ese 10%.

---

## 2. cProfile — Profiler Determinístico

```python
import cProfile
import pstats
import io
from pathlib import Path


def process_asset(path: Path) -> dict[str, object]:
    """Simula el pipeline de Studio BC."""
    data = path.read_bytes()           # I/O
    checksum = _compute_checksum(data)  # CPU
    metadata = _extract_metadata(data)  # CPU + I/O
    return {"checksum": checksum, "metadata": metadata}


# Forma 1: context manager
with cProfile.Profile() as pr:
    result = process_asset(Path("footage/spot_verano.mp4"))

# Ver resultados ordenados por cumulative time
ps = pstats.Stats(pr)
ps.sort_stats("cumulative").print_stats(20)
```

---

## 3. Entender la salida de pstats

```
         1234 function calls in 2.456 seconds

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
       1    0.001    0.001    2.456    2.456  pipeline.py:12(process_asset)
       1    0.012    0.012    1.890    1.890  pipeline.py:24(_extract_metadata)
      50    1.823    0.036    1.878    0.038  ffmpeg.py:8(_run_ffmpeg)
       1    0.545    0.545    0.565    0.565  pipeline.py:19(_compute_checksum)
```

| Columna | Significado |
|---------|-------------|
| `ncalls` | Número de llamadas |
| `tottime` | Tiempo propio (sin subcalls) |
| `cumtime` | Tiempo acumulado (con subcalls) — **el más útil** |
| `percall` | Tiempo por llamada |

El bottleneck es la función con mayor `cumtime`: aquí `_extract_metadata` → `_run_ffmpeg`.

---

## 4. Guardar y recargar stats

```python
import cProfile, pstats

pr = cProfile.Profile()
pr.enable()
run_pipeline()
pr.disable()

# Guardar en archivo binario
pr.dump_stats("pipeline.prof")

# Cargar y analizar después
stats = pstats.Stats("pipeline.prof")
stats.sort_stats("cumulative")
stats.print_stats(20)

# Filtrar por módulo
stats.print_stats("pipeline")  # solo funciones de pipeline.py
```

---

## 5. Decorador `@profile_fn` reutilizable

```python
import cProfile
import pstats
import io
from collections.abc import Callable
from typing import Any


def profile_fn(top_n: int = 20) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            pr = cProfile.Profile()
            pr.enable()
            try:
                result = fn(*args, **kwargs)
            finally:
                pr.disable()
            s = io.StringIO()
            pstats.Stats(pr, stream=s).sort_stats("cumulative").print_stats(top_n)
            print(s.getvalue())
            return result
        return wrapper
    return decorator


@profile_fn(top_n=10)
def analyze_batch(paths: list[Path]) -> list[dict[str, object]]:
    return [process_asset(p) for p in paths]
```

---

## 6. snakeviz — Visualización Interactiva

```bash
pip install snakeviz

# Generar el .prof
python -m cProfile -o pipeline.prof mi_script.py

# Abrir en browser
snakeviz pipeline.prof
```

Muestra un flame graph interactivo: barras proporcionales a `cumtime`.

---

## 7. py-spy — Sampling Profiler (sin instrumentar)

py-spy no requiere modificar el código — se adjunta a un proceso Python en ejecución:

```bash
pip install py-spy

# Profiling de un proceso existente (necesita sudo)
py-spy top --pid 12345

# Generar flame graph de un script
py-spy record -o profile.svg -- python mi_script.py

# Sampling a 100 Hz durante 30 segundos
py-spy record --rate 100 --duration 30 -o profile.svg -- python pipeline.py
```

| Herramienta | Overhead | Uso |
|-------------|----------|-----|
| `cProfile` | Alto (~10-30%) | Desarrollo — análisis detallado |
| `py-spy` | Muy bajo (<1%) | Producción — sin parar el proceso |

---

## 8. Flujo de trabajo típico

```
1. Medir baseline: tiempo total del pipeline
2. Perfilar con cProfile → identificar top 3 funciones por cumtime
3. Optimizar la función más costosa
4. Medir de nuevo → verificar mejora
5. Repetir hasta alcanzar el objetivo de performance
```

---

## Resumen

| Herramienta | Comando | Cuándo usar |
|-------------|---------|-------------|
| `cProfile` | `python -m cProfile -o out.prof script.py` | Análisis detallado en desarrollo |
| `pstats` | `stats.sort_stats("cumulative").print_stats(N)` | Analizar .prof en código |
| `snakeviz` | `snakeviz out.prof` | Visualización interactiva |
| `py-spy` | `py-spy record -o out.svg -- python script.py` | Profiling en producción |
