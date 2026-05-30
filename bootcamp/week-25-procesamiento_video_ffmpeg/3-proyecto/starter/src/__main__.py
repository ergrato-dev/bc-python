"""Entry point: python -m studio_post <comando>"""

import logging
import time
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from .pipeline import process_video, VIDEO_EXTENSIONS
from .inspector import get_video_info

app = typer.Typer(help="studio-post-pipeline — Post-producción automática")
console = Console()

DROP_DIR = Path("drop")
OUTPUT_DIR = Path("output")


@app.command()
def process(
    drop: Path = typer.Option(DROP_DIR),
    dest: Path = typer.Option(OUTPUT_DIR),
) -> None:
    """Procesa todos los videos en drop/."""
    sources = [f for f in drop.rglob("*") if f.suffix.lower() in VIDEO_EXTENSIONS]
    if not sources:
        console.print("[yellow]No hay videos en drop/[/]")
        raise typer.Exit(0)

    # TODO: iterar con Rich Progress, llamar process_video, contar OK/errores
    raise NotImplementedError


@app.command()
def watch(
    drop: Path = typer.Option(DROP_DIR),
    dest: Path = typer.Option(OUTPUT_DIR),
) -> None:
    """Monitorea drop/ con watchdog."""
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler, FileSystemEvent

    class PostHandler(FileSystemEventHandler):
        def on_created(self, event: FileSystemEvent) -> None:
            if event.is_directory:
                return
            path = Path(event.src_path)
            if path.suffix.lower() not in VIDEO_EXTENSIONS:
                return
            time.sleep(1.0)  # esperar escritura completa
            if path.exists():
                console.print(f"[cyan]Procesando:[/] {path.name}")
                try:
                    process_video(path, dest)
                except Exception as e:
                    console.print(f"[red]Error:[/] {e}")

    # TODO: Observer setup
    raise NotImplementedError


@app.command()
def info(video: Path = typer.Argument(help="Video a inspeccionar")) -> None:
    """Muestra metadata técnica de un video."""
    try:
        data = get_video_info(video)
    except Exception as e:
        console.print(f"[red]Error:[/] {e}")
        raise typer.Exit(1)

    table = Table(title=f"Metadata: {video.name}")
    table.add_column("Campo")
    table.add_column("Valor")
    for k, v in data.items():
        table.add_row(str(k), str(v))
    console.print(table)


if __name__ == "__main__":
    app()
