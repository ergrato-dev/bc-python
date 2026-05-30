from __future__ import annotations

import typer
from pathlib import Path
from rich.console import Console
from rich.table import Table

from .pipeline import Pipeline
from .stages import IngestStage, ValidateStage, ProcessStage, ExportStage
from .state import StateStore, JobStatus
from .retry import DeadLetterQueue

app = typer.Typer(name="studio-pipeline", help="Pipeline de media Studio BC")
console = Console()

_STATE_PATH = Path(".pipeline_state.json")
_DLQ_PATH = Path(".dlq.jsonl")


def _make_pipeline() -> Pipeline:
    store = StateStore(_STATE_PATH)
    return Pipeline(
        stages=[IngestStage(), ValidateStage(), ProcessStage(), ExportStage()],
        store=store,
    )


@app.command()
def run(
    path: str = typer.Option(..., "--path", "-p", help="Ruta al archivo a procesar"),
    project: str = typer.Option("", "--project", help="Slug del proyecto (ej. canal9/spot)"),
) -> None:
    """Procesa un archivo a través del pipeline completo."""
    console.print(f"[bold cyan]Procesando:[/] {path} proyecto=[yellow]{project or 'sin proyecto'}[/]")
    pipeline = _make_pipeline()
    result = pipeline.run(path, project)

    if result.success:
        console.print("[bold green]OK[/] — Pipeline completado")
        for k, v in result.data.items():
            if k not in ("path", "project"):
                console.print(f"  {k}: {v}")
    else:
        console.print(f"[bold red]FALLO[/] — {result.error}")
        raise typer.Exit(1)


@app.command()
def status() -> None:
    """Muestra el estado de todos los jobs."""
    store = StateStore(_STATE_PATH)
    jobs = store.list_all()

    if not jobs:
        console.print("[dim]No hay jobs registrados.[/]")
        return

    t = Table("Job ID", "Archivo", "Estado", "Etapa", "Intentos", "Error")
    for job in sorted(jobs, key=lambda j: j.created_at, reverse=True):
        status_color = {
            "done": "green", "failed": "red",
            "running": "yellow", "pending": "dim", "retrying": "cyan",
        }.get(str(job.status), "white")
        t.add_row(
            job.job_id,
            Path(job.input_path).name,
            f"[{status_color}]{job.status}[/{status_color}]",
            job.current_stage,
            str(job.attempt),
            (job.error or "")[:40],
        )
    console.print(t)

    failed = store.list_by_status(JobStatus.FAILED)
    if failed:
        console.print(f"\n[bold red]{len(failed)} job(s) fallidos.[/] Usar [cyan]requeue --job-id ID[/] para reintentar.")


@app.command()
def requeue(
    job_id: str = typer.Option(..., "--job-id", help="ID del job a reencolar"),
) -> None:
    """Reencola un job de la DLQ."""
    dlq = DeadLetterQueue(_DLQ_PATH)
    data = dlq.pop(job_id)
    if data is None:
        console.print(f"[red]No se encontró job {job_id} en la DLQ[/]")
        raise typer.Exit(1)

    path = str(data.get("path", ""))
    project = str(data.get("project", ""))
    console.print(f"Reencolando job {job_id}: {path}")
    pipeline = _make_pipeline()
    result = pipeline.run(path, project)
    if result.success:
        console.print("[green]OK[/] — Re-procesado exitosamente")
    else:
        console.print(f"[red]FALLO nuevamente[/] — {result.error}")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
