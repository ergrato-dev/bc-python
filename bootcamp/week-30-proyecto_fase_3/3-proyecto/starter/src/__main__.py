"""CLI entry point — studio-production-pipeline."""
from __future__ import annotations

import logging
import queue
import sys
import time
from pathlib import Path

import typer
from rich.console import Console

from .config import PipelineConfig
from .pipeline import PipelineRunner, StateStore
from .stages.cloud import CloudStage
from .stages.distribute import DistributeStage
from .stages.ingest import IngestStage
from .stages.transcode import TranscodeStage
from .stages.validate import ValidateStage

app = typer.Typer(name="studio-pipeline", help="Pipeline de producción Studio BC — Fase 3")
console = Console()
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def _build_pipeline(cfg: PipelineConfig) -> PipelineRunner:
    cfg.ensure_dirs()
    store = StateStore(cfg.state_file)
    stages = [
        IngestStage(),
        ValidateStage(),
        TranscodeStage(cfg.output_dir),
        CloudStage(cfg.s3_bucket, cfg.project_slug, cfg.aws_default_region, cfg.dry_run),
        DistributeStage(cfg.slack_webhook_url, cfg.dry_run),
    ]
    return PipelineRunner(stages, store)


@app.command()
def watch() -> None:
    """Daemon: monitorea drop/ y procesa cada archivo nuevo automáticamente."""
    from .watcher import start_watcher

    cfg = PipelineConfig()
    cfg.ensure_dirs()
    pipeline = _build_pipeline(cfg)

    file_queue: queue.Queue[str] = queue.Queue()
    observer = start_watcher(cfg.drop_dir, file_queue)
    console.print(f"[bold green]Watching[/] {cfg.drop_dir}/ — Ctrl+C para detener")

    try:
        while True:
            try:
                path = file_queue.get(timeout=1.0)
                console.print(f"[cyan]Procesando:[/] {path}")
                result = pipeline.run(path, cfg.project_slug)
                if result.success:
                    console.print(f"[green]OK[/] — {path}")
                else:
                    console.print(f"[red]FALLO[/] — {result.error}")
            except queue.Empty:
                pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


@app.command()
def run(
    path: str = typer.Argument(..., help="Ruta al archivo a procesar"),
    project: str = typer.Option("", "--project", "-p", help="Slug del proyecto"),
) -> None:
    """Procesa un archivo manualmente a través del pipeline completo."""
    cfg = PipelineConfig()
    if project:
        cfg.project_slug = project

    pipeline = _build_pipeline(cfg)
    console.print(f"[bold cyan]Procesando:[/] {path}")
    result = pipeline.run(path, cfg.project_slug)

    if result.success:
        console.print("[bold green]OK[/] — Pipeline completado")
        for k, v in result.data.items():
            if k not in ("path", "project", "job_id"):
                console.print(f"  {k}: {v}")
    else:
        console.print(f"[bold red]FALLO[/] — {result.error}")
        raise typer.Exit(1)


@app.command()
def status() -> None:
    """Muestra el estado de todos los jobs registrados."""
    cfg = PipelineConfig()
    store = StateStore(cfg.state_file)
    jobs = store.list_all()

    if not jobs:
        console.print("[dim]No hay jobs registrados.[/]")
        return

    from rich.table import Table
    t = Table("Job ID", "Archivo", "Estado", "Etapa", "Error")
    for job in sorted(jobs, key=lambda j: j.created_at, reverse=True):
        color = {"done": "green", "failed": "red", "running": "yellow"}.get(str(job.status), "white")
        t.add_row(
            job.job_id,
            job.input_path.split("/")[-1],
            f"[{color}]{job.status}[/{color}]",
            job.current_stage,
            (job.error or "")[:40],
        )
    console.print(t)


@app.command()
def dashboard() -> None:
    """Dashboard Rich en tiempo real del estado del pipeline."""
    from .monitor import run_dashboard
    cfg = PipelineConfig()
    store = StateStore(cfg.state_file)
    run_dashboard(store)


if __name__ == "__main__":
    app()
