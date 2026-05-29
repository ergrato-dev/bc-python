# Rich — Live Display, Progress y Layout

## Objetivos

- Mostrar progreso de operaciones largas con `Progress`
- Actualizar la terminal en tiempo real con `Live`
- Componer layouts complejos con `Layout`
- Combinar múltiples elementos en un dashboard de terminal

---

## 1. `Progress` — barras de progreso

```python
import time
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

assets = ["intro.mp4", "logo.png", "soundtrack.wav", "credits.mp4"]

with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    TaskProgressColumn(),
    transient=True,   # borra la barra al completar
) as progress:
    task = progress.add_task("Downloading assets...", total=len(assets))

    for asset in assets:
        time.sleep(0.8)   # simula trabajo
        progress.advance(task)
        progress.print(f"✅ {asset}")   # no interfiere con la barra

progress.print("[green bold]All assets downloaded!")
```

### Múltiples tareas

```python
with Progress() as progress:
    dl_task = progress.add_task("[cyan]Downloading...", total=10)
    proc_task = progress.add_task("[magenta]Processing...", total=10, start=False)

    for i in range(10):
        time.sleep(0.3)
        progress.advance(dl_task)

    progress.start_task(proc_task)
    for i in range(10):
        time.sleep(0.2)
        progress.advance(proc_task)
```

### Columnas predefinidas

```python
from rich.progress import (
    Progress, SpinnerColumn, BarColumn,
    DownloadColumn, TransferSpeedColumn, TimeRemainingColumn,
)

progress = Progress(
    SpinnerColumn(),
    "[progress.description]{task.description}",
    BarColumn(),
    DownloadColumn(),
    TransferSpeedColumn(),
    TimeRemainingColumn(),
)
```

---

## 2. `track()` — el shortcut más simple

```python
from rich.progress import track
import time

items = list(range(20))

for item in track(items, description="Processing..."):
    time.sleep(0.1)
```

Equivalente a un Progress con una sola tarea — ideal para bucles simples.

---

## 3. `Live` — actualización en tiempo real

```python
import time
from rich.console import Console
from rich.live import Live
from rich.table import Table

console = Console()

def build_status_table(jobs: list[dict[str, str]]) -> Table:
    table = Table("Asset", "Status", "Time")
    for job in jobs:
        icon = "⏳" if job["status"] == "running" else "✅"
        table.add_row(job["name"], f"{icon} {job['status']}", job.get("elapsed", "—"))
    return table

jobs = [
    {"name": "intro.mp4",    "status": "pending"},
    {"name": "logo.png",     "status": "pending"},
    {"name": "credits.mp4",  "status": "pending"},
]

with Live(build_status_table(jobs), refresh_per_second=4, console=console) as live:
    for job in jobs:
        job["status"] = "running"
        live.update(build_status_table(jobs))
        time.sleep(1.0)
        job["status"] = "done"
        job["elapsed"] = "1.0s"
        live.update(build_status_table(jobs))
```

`Live` re-dibuja el contenido en lugar de imprimir nuevas líneas — perfecto para dashboards de pipeline.

---

## 4. `Layout` — composición de paneles

```python
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table

console = Console()

def make_layout() -> Layout:
    layout = Layout()

    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="body"),
        Layout(name="footer", size=3),
    )

    layout["body"].split_row(
        Layout(name="left"),
        Layout(name="right"),
    )

    return layout

layout = make_layout()

layout["header"].update(Panel("[bold cyan]Studio BC — Pipeline Dashboard[/bold cyan]"))

assets_table = Table("Asset", "Status", "Size")
assets_table.add_row("intro.mp4",   "✅ done",    "128 MB")
assets_table.add_row("logo.png",    "✅ done",    "2.4 MB")
assets_table.add_row("credits.mp4", "⏳ running", "—")
layout["left"].update(Panel(assets_table, title="Assets"))

layout["right"].update(Panel(
    "[bold]Project:[/bold] reel-2025\n"
    "[bold]Total:[/bold]   3 assets\n"
    "[bold]Done:[/bold]    2 / 3",
    title="Summary",
))

layout["footer"].update(Panel("[dim]Press Ctrl+C to stop[/dim]"))

console.print(layout)
```

---

## 5. Live + Layout: dashboard dinámico

```python
import time
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table

console = Console()
jobs = [
    {"name": "intro.mp4",   "status": "pending", "elapsed": "—"},
    {"name": "logo.png",    "status": "pending", "elapsed": "—"},
    {"name": "credits.mp4", "status": "pending", "elapsed": "—"},
]

def make_dashboard(jobs: list[dict[str, str]]) -> Layout:
    layout = Layout()
    layout.split_row(Layout(name="assets"), Layout(name="summary", size=30))

    table = Table("Asset", "Status", "Time", box=None)
    for j in jobs:
        color = "green" if j["status"] == "done" else "yellow" if j["status"] == "running" else "white"
        table.add_row(j["name"], f"[{color}]{j['status']}[/{color}]", j["elapsed"])
    layout["assets"].update(Panel(table, title="Assets"))

    done = sum(1 for j in jobs if j["status"] == "done")
    layout["summary"].update(Panel(
        f"Total:  {len(jobs)}\nDone:   {done}\nFailed: 0",
        title="Stats",
    ))
    return layout

with Live(make_dashboard(jobs), console=console, refresh_per_second=4) as live:
    for i, job in enumerate(jobs):
        job["status"] = "running"
        live.update(make_dashboard(jobs))
        time.sleep(1.0)
        job["status"] = "done"
        job["elapsed"] = f"{i + 1}.0s"
        live.update(make_dashboard(jobs))
```

---

## ✅ Resumen

| Herramienta | Cuándo usar |
|-------------|------------|
| `Progress` | Barra de progreso para tareas con total conocido |
| `track()` | Shortcut para un bucle simple con progress |
| `Live` | Actualizar cualquier renderable sin borrar la terminal |
| `Layout` | Dividir la terminal en secciones independientes |
| `Live + Layout` | Dashboard dinámico multi-panel |

---

## Recursos Adicionales

- [Rich docs — Progress](https://rich.readthedocs.io/en/stable/progress.html)
- [Rich docs — Live](https://rich.readthedocs.io/en/stable/live.html)
- [Rich docs — Layout](https://rich.readthedocs.io/en/stable/layout.html)
