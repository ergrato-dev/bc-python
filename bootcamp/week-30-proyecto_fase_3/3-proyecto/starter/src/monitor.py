"""
MonitorDashboard — Rich Live dashboard del estado del pipeline.

Referencia: semana 29 — dashboard.py
"""
from __future__ import annotations

import time
from typing import Any

from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .pipeline import JobRecord, JobStatus, StateStore


def _status_color(status: JobStatus) -> str:
    return {
        JobStatus.DONE: "green",
        JobStatus.FAILED: "red",
        JobStatus.RUNNING: "yellow",
        JobStatus.PENDING: "dim",
    }.get(status, "white")


def build_jobs_table(jobs: list[JobRecord]) -> Panel:
    table = Table(expand=True, show_header=True, header_style="bold cyan")
    table.add_column("Job ID", style="cyan", width=10)
    table.add_column("Archivo", width=20)
    table.add_column("Estado", width=12)
    table.add_column("Etapa actual", width=14)
    table.add_column("Error", width=30)

    for job in sorted(jobs, key=lambda j: j.created_at, reverse=True)[:20]:
        color = _status_color(job.status)
        table.add_row(
            job.job_id,
            job.input_path.split("/")[-1][:20],
            Text(str(job.status), style=color),
            job.current_stage,
            (job.error or "")[:30],
        )
    return Panel(table, title="Jobs", border_style="blue")


def build_summary_panel(jobs: list[JobRecord]) -> Panel:
    total = len(jobs)
    done = sum(1 for j in jobs if j.status == JobStatus.DONE)
    failed = sum(1 for j in jobs if j.status == JobStatus.FAILED)
    running = sum(1 for j in jobs if j.status == JobStatus.RUNNING)
    error_rate = failed / total if total else 0.0

    color = "green" if error_rate < 0.05 else "yellow" if error_rate < 0.15 else "red"
    text = Text()
    text.append(f"Total: {total}  ", style="bold")
    text.append(f"Done: {done}  ", style="green")
    text.append(f"Running: {running}  ", style="yellow")
    text.append(f"Failed: {failed}  ", style="red")
    text.append(f"Error rate: {error_rate:.1%}", style=color)
    return Panel(text, title="Resumen", border_style=color)


def build_layout(jobs: list[JobRecord]) -> Layout:
    """
    Construye el layout Rich del dashboard.

    TODO:
    1. Crear Layout root y dividirlo con split_column (ratio 7 arriba, 3 abajo)
    2. Arriba: build_jobs_table(jobs)
    3. Abajo: build_summary_panel(jobs)
    4. Retornar el layout

    Referencia: semana 29 — dashboard.py, build_layout()
    """
    raise NotImplementedError


def run_dashboard(store: StateStore, refresh_s: float = 1.0) -> None:
    try:
        with Live(screen=True, refresh_per_second=int(1 / refresh_s)) as live:
            while True:
                jobs = store.list_all()
                live.update(build_layout(jobs))
                time.sleep(refresh_s)
    except KeyboardInterrupt:
        pass
