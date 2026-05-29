"""Entry point: python -m studio_ingest <comando>"""

import logging
import time
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table
from watchdog.observers import Observer

from .handler import IngestHandler
from .organizer import FileOrganizer
from .registry import load_registry

app = typer.Typer(help="studio-ingest-daemon — Organización automática de entregables")
console = Console()

DROP_DIR = Path("drop")
ORGANIZED_DIR = Path("organized")


@app.command()
def watch(
    drop: Path = typer.Option(DROP_DIR, help="Carpeta a monitorear"),
    dest: Path = typer.Option(ORGANIZED_DIR, help="Carpeta de destino"),
) -> None:
    """Inicia el daemon watchdog."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    drop.mkdir(parents=True, exist_ok=True)

    organizer = FileOrganizer(dest)
    handler = IngestHandler(organizer)

    # TODO:
    # 1. Crear Observer, schedule handler en drop (recursive=False)
    # 2. observer.start()
    # 3. console.print(f"[green]Monitoring {drop.resolve()} — Ctrl+C to stop[/]")
    # 4. while True: time.sleep(1)
    # 5. except KeyboardInterrupt: observer.stop()
    # 6. observer.join()
    raise NotImplementedError


@app.command()
def organize(
    drop: Path = typer.Option(DROP_DIR, help="Carpeta con archivos a organizar"),
    dest: Path = typer.Option(ORGANIZED_DIR, help="Carpeta de destino"),
) -> None:
    """Organiza todos los archivos existentes en drop/ sin daemon."""
    organizer = FileOrganizer(dest)
    moved = organizer.organize_folder(drop)
    console.print(f"[green]Organizados: {len(moved)} archivos[/]")


@app.command()
def stats() -> None:
    """Muestra estadísticas del registro de procesados."""
    registry = load_registry()
    table = Table(title="Archivos procesados")
    table.add_column("SHA-256 (12 chars)", style="dim")
    table.add_column("Destino")
    for digest, dest in list(registry.items())[:20]:
        table.add_row(digest[:12] + "...", dest)
    console.print(table)
    console.print(f"Total: {len(registry)} archivos")


if __name__ == "__main__":
    app()
