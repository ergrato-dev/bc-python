"""CLI — studio-optimizer."""
from __future__ import annotations

import json
import os
import time
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from .cache import MetadataCache
from .config import AppConfig
from .pipeline import OptimizedPipeline, SlowPipeline
from .profiler import PipelineProfiler

app = typer.Typer(
    name="studio-optimizer",
    help="Profiling, caching y benchmarking del pipeline Studio BC",
)
console = Console()


@app.command()
def profile(
    asset: str = typer.Argument(..., help="Ruta al asset (puede ser ficticio en dry_run)"),
    top: int = typer.Option(10, "--top", help="Top N funciones en el reporte"),
) -> None:
    """Ejecuta el pipeline lento bajo cProfile y muestra el reporte."""
    cfg = AppConfig()
    path = Path(asset)
    pipeline = SlowPipeline()
    profiler = PipelineProfiler(top_n=top)

    console.print(f"[cyan]Profiling pipeline:[/] {asset}")
    result = profiler.profile(pipeline.process, path)

    console.print("\n[bold]Reporte cProfile:[/]")
    console.print(profiler.report())

    top_fns = profiler.top_functions(3)
    if top_fns:
        console.print("[yellow]Top 3 bottlenecks:[/]")
        for name, cumtime in top_fns:
            console.print(f"  {cumtime:.4f}s — {name}")


@app.command()
def benchmark(
    asset: str = typer.Argument("mock_asset.mp4", help="Ruta al asset"),
    runs: int = typer.Option(5, "--runs", help="Número de ejecuciones"),
) -> None:
    """Compara SlowPipeline vs OptimizedPipeline y muestra el speedup."""
    cfg = AppConfig()
    path = Path(asset)
    slow = SlowPipeline()
    fast = OptimizedPipeline(config=cfg)

    console.print(f"[yellow]SlowPipeline ({runs} runs)...[/]")
    t0 = time.perf_counter()
    for _ in range(runs):
        slow.process(path)
    slow_time = time.perf_counter() - t0

    console.print(f"[green]OptimizedPipeline ({runs} runs)...[/]")
    t0 = time.perf_counter()
    for _ in range(runs):
        fast.process(path)
    fast_time = time.perf_counter() - t0

    speedup = slow_time / fast_time if fast_time > 0 else 0.0

    table = Table(title="Benchmark: Slow vs Optimized")
    table.add_column("Pipeline", style="bold")
    table.add_column("Total (s)", justify="right")
    table.add_column("Avg/run (ms)", justify="right")
    table.add_column("Speedup", justify="right")
    table.add_row("SlowPipeline", f"{slow_time:.2f}", f"{slow_time/runs*1000:.1f}", "1.0×")
    table.add_row(
        "OptimizedPipeline",
        f"{fast_time:.2f}",
        f"{fast_time/runs*1000:.1f}",
        f"[green]{speedup:.1f}×[/]",
    )
    console.print(table)


@app.command(name="cache-stats")
def cache_stats() -> None:
    """Muestra estadísticas del cache (Redis o mock)."""
    cfg = AppConfig()
    cache = MetadataCache(cfg)
    stats = cache.stats()
    console.print("[bold]Cache Stats:[/]")
    console.print(json.dumps(stats, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    app()
