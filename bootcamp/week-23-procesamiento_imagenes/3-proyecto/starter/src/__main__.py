"""Entry point: python -m studio_art <comando>"""

import logging
import time
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from .pipeline import process_image
from .profiles import PROFILES

app = typer.Typer(help="studio-art-pipeline — Thumbnails + watermarks para Studio BC")
console = Console()

DROP_DIR = Path("drop")
OUTPUT_DIR = Path("output")


@app.command()
def process(
    drop: Path = typer.Option(DROP_DIR),
    dest: Path = typer.Option(OUTPUT_DIR),
    logo: Path | None = typer.Option(None, help="Path al logo PNG"),
) -> None:
    """Procesa todas las imágenes en drop/ de una pasada."""
    sources = [f for f in drop.rglob("*") if f.suffix.lower() in {".jpg", ".jpeg", ".png", ".tiff", ".webp"}]
    if not sources:
        console.print("[yellow]No se encontraron imágenes en drop/[/]")
        raise typer.Exit(0)

    total = 0
    # TODO: iterar sources, llamar process_image, acumular total
    # Mostrar progress bar con Rich
    raise NotImplementedError


@app.command()
def watch(
    drop: Path = typer.Option(DROP_DIR),
    dest: Path = typer.Option(OUTPUT_DIR),
    logo: Path | None = typer.Option(None),
) -> None:
    """Monitorea drop/ con watchdog y procesa cada imagen nueva."""
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler, FileSystemEvent

    IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".tiff", ".webp"}

    class ArtHandler(FileSystemEventHandler):
        def on_created(self, event: FileSystemEvent) -> None:
            if event.is_directory:
                return
            path = Path(event.src_path)
            if path.suffix.lower() not in IMAGE_EXTS:
                return
            time.sleep(0.3)
            if path.exists():
                console.print(f"[cyan]Procesando:[/] {path.name}")
                process_image(path, dest, logo_path=logo)

    # TODO: Observer, schedule, start, loop, stop, join
    raise NotImplementedError


@app.command()
def stats(dest: Path = typer.Option(OUTPUT_DIR)) -> None:
    """Muestra estadísticas de archivos generados por variante."""
    table = Table(title="Output stats")
    table.add_column("Variante")
    table.add_column("Archivos", justify="right")
    table.add_column("Tamaño total", justify="right")

    for profile in PROFILES:
        folder = dest / profile.name
        if not folder.exists():
            continue
        files = list(folder.glob("*"))
        total_size = sum(f.stat().st_size for f in files if f.is_file())
        table.add_row(profile.name, str(len(files)), f"{total_size // 1024} KB")

    console.print(table)


if __name__ == "__main__":
    app()
