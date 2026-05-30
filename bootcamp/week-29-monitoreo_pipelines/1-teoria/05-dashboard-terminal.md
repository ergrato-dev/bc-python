# Dashboard de Terminal con Rich Live

## 1. `Rich Live` — Panel en Tiempo Real

`Live` de Rich re-renderiza un panel en el terminal a intervalos definidos sin limpiar el historial de la sesión completa.

```python
from rich.live import Live
from rich.table import Table
import time


def build_table(data: list[dict[str, str]]) -> Table:
    table = Table(title="Jobs activos")
    table.add_column("Job ID", style="cyan")
    table.add_column("Estado")
    table.add_column("Etapa")
    table.add_column("Duración")

    for row in data:
        color = {"done": "green", "failed": "red", "running": "yellow"}.get(row["status"], "white")
        table.add_row(
            row["job_id"],
            f"[{color}]{row['status']}[/{color}]",
            row["stage"],
            row["duration"],
        )
    return table


with Live(build_table([]), refresh_per_second=2) as live:
    for _ in range(10):
        live.update(build_table(get_current_jobs()))  # función que lee el estado
        time.sleep(0.5)
```

---

## 2. Layout con Múltiples Paneles

```python
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, BarColumn, TaskProgressColumn
import time


def build_dashboard(
    jobs: list[dict[str, object]],
    metrics: dict[str, object],
    health: dict[str, object],
) -> Layout:
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="body"),
        Layout(name="footer", size=5),
    )
    layout["body"].split_row(
        Layout(name="jobs", ratio=2),
        Layout(name="metrics", ratio=1),
    )

    # Header
    status = health.get("status", "unknown")
    color = {"healthy": "green", "degraded": "yellow", "unhealthy": "red"}.get(str(status), "white")
    layout["header"].update(
        Panel(f"[bold]Studio BC — Pipeline Monitor[/bold]  [{color}]{status.upper()}[/{color}]")
    )

    # Jobs table
    jobs_table = Table(expand=True)
    jobs_table.add_column("Job", style="cyan", width=10)
    jobs_table.add_column("Estado", width=10)
    jobs_table.add_column("Etapa", width=12)
    for job in jobs[-15:]:  # últimos 15 jobs
        s = str(job.get("status", ""))
        c = {"done": "green", "failed": "red", "running": "yellow", "pending": "dim"}.get(s, "white")
        jobs_table.add_row(
            str(job.get("job_id", ""))[:8],
            f"[{c}]{s}[/{c}]",
            str(job.get("current_stage", "")),
        )
    layout["jobs"].update(Panel(jobs_table, title="Jobs"))

    # Metrics panel
    metrics_text = Text()
    metrics_text.append(f"Throughput: {float(str(metrics.get('throughput_per_s', 0))):.3f} j/s\n")
    metrics_text.append(f"Error rate: {float(str(metrics.get('error_rate', 0))):.1%}\n")
    metrics_text.append(f"Done: {metrics.get('jobs_done', 0)}\n")
    metrics_text.append(f"Failed: {metrics.get('jobs_failed', 0)}\n")
    layout["metrics"].update(Panel(metrics_text, title="Métricas"))

    # Footer: health components
    comp_text = Text()
    for comp in health.get("components", []):  # type: ignore[union-attr]
        c_status = str(comp.get("status", ""))  # type: ignore[union-attr]
        icon = {"healthy": "[green]●[/green]", "degraded": "[yellow]●[/yellow]", "unhealthy": "[red]●[/red]"}.get(c_status, "○")
        comp_text.append_text(Text.from_markup(f"{icon} {comp.get('name', '')}: {comp.get('message', '')}\n"))  # type: ignore[union-attr]
    layout["footer"].update(Panel(comp_text, title="Health"))

    return layout
```

---

## 3. Dashboard Completo con Live

```python
def run_dashboard(
    state_path: Path,
    metrics_path: Path,
    refresh_s: float = 2.0,
) -> None:
    import json
    from rich.live import Live

    health_checker = HealthChecker(state_path, metrics_path)

    def load_jobs() -> list[dict[str, object]]:
        if not state_path.exists():
            return []
        raw = json.loads(state_path.read_text())
        return list(raw.values())

    def load_metrics() -> dict[str, object]:
        if not metrics_path.exists():
            return {}
        return json.loads(metrics_path.read_text())

    with Live(
        build_dashboard([], {}, {"status": "unknown", "components": []}),
        refresh_per_second=1 / refresh_s,
        screen=True,
    ) as live:
        try:
            while True:
                jobs = load_jobs()
                metrics = load_metrics()
                health = health_checker.check_all()
                live.update(build_dashboard(jobs, metrics, health))
                time.sleep(refresh_s)
        except KeyboardInterrupt:
            pass
```

`screen=True` usa el modo alternativo del terminal (como `htop`) — al salir, restaura el estado anterior.

---

## 4. Progress Bar en Live

```python
from rich.progress import Progress, SpinnerColumn, BarColumn, TimeElapsedColumn


def run_batch_with_progress(files: list[str]) -> None:
    progress = Progress(
        SpinnerColumn(),
        "[progress.description]{task.description}",
        BarColumn(),
        TaskProgressColumn(),
        TimeElapsedColumn(),
    )

    with Live(progress, refresh_per_second=4):
        task = progress.add_task("Procesando batch...", total=len(files))
        for f in files:
            process_file(f)  # type: ignore[name-defined]
            progress.advance(task)
```

---

## Resumen

| Componente | Uso |
|------------|-----|
| `Live(renderable, refresh_per_second=N)` | Re-renderiza en lugar actualizado |
| `live.update(new_renderable)` | Reemplaza el contenido del panel |
| `Layout` | Divide el terminal en secciones (columnas/filas) con `ratio` |
| `Panel` | Borde + título alrededor de cualquier renderable |
| `screen=True` | Modo alternativo: limpia el terminal al salir (como htop) |
| `Progress` | Barra de progreso componible con columnas personalizables |
