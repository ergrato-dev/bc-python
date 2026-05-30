"""CLI de presentación — usa el DI Container."""
from __future__ import annotations

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(name="studio-refactored", help="Studio BC — Clean Architecture")
console = Console()


def _make_container():  # type: ignore[return]
    from ..infrastructure.containers import Container
    container = Container()
    container.config.from_dict({
        "state_file": ".pipeline_state.json",
        "s3_bucket": "studio-bc-prod",
        "aws_region": "us-east-1",
        "dry_run": True,
    })
    return container


@app.command()
def run(
    path: str = typer.Argument(..., help="Ruta al archivo a procesar"),
    project: str = typer.Option("studio-bc/default", "--project", "-p"),
) -> None:
    """Procesa un asset a través del use case."""
    container = _make_container()
    use_case = container.process_use_case()
    console.print(f"[cyan]Procesando:[/] {path}")
    job = use_case.execute(path, project)
    color = "green" if str(job.status) == "done" else "red"
    console.print(f"[{color}]{job.status}[/{color}] — Job {job.job_id}")
    if job.error:
        console.print(f"[red]Error:[/] {job.error}")


@app.command()
def status() -> None:
    """Lista todos los jobs registrados."""
    container = _make_container()
    use_case = container.get_status_use_case()
    jobs = use_case.list_all()
    if not jobs:
        console.print("[dim]No hay jobs.[/]")
        return
    t = Table("Job ID", "Asset", "Estado", "Error")
    for job in sorted(jobs, key=lambda j: j.created_at, reverse=True):
        color = {"done": "green", "failed": "red", "running": "yellow"}.get(str(job.status), "white")
        t.add_row(
            job.job_id,
            job.asset_path.split("/")[-1],
            f"[{color}]{job.status}[/{color}]",
            (job.error or "")[:40],
        )
    console.print(t)


if __name__ == "__main__":
    app()
