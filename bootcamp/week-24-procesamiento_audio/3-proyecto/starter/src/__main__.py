"""Entry point: python -m studio_audio <comando>"""

import logging
import time
from pathlib import Path
from typing import Any

import typer
from rich.console import Console
from rich.table import Table

from .pipeline import process_audio, AUDIO_EXTENSIONS
from .transcriber import load_model

app = typer.Typer(help="studio-audio-pipeline — Transcripción automática para Studio BC")
console = Console()

DROP_DIR = Path("drop")
OUTPUT_DIR = Path("output")

_model: Any = None  # cache del modelo Whisper


@app.command()
def process(
    drop: Path = typer.Option(DROP_DIR),
    dest: Path = typer.Option(OUTPUT_DIR),
    model_name: str = typer.Option("base", help="Modelo Whisper: tiny/base/small/medium"),
    language: str = typer.Option("es"),
) -> None:
    """Procesa todos los audios en drop/ de una pasada."""
    global _model
    sources = [f for f in drop.rglob("*") if f.suffix.lower() in AUDIO_EXTENSIONS]
    if not sources:
        console.print("[yellow]No se encontraron audios en drop/[/]")
        raise typer.Exit(0)

    _model = load_model(model_name)
    if _model is None:
        console.print("[yellow]Whisper no instalado — usando segmentos de muestra[/]")

    # TODO: iterar sources con progress bar, llamar process_audio, contar OK/errores
    raise NotImplementedError


@app.command()
def transcribe_cmd(
    audio: Path = typer.Argument(help="Archivo de audio"),
    dest: Path = typer.Option(OUTPUT_DIR),
    model_name: str = typer.Option("base"),
    language: str = typer.Option("es"),
) -> None:
    """Transcribe un archivo específico."""
    model = load_model(model_name)
    srt, vtt = process_audio(audio, dest, model=model, language=language)
    console.print(f"[green]SRT:[/] {srt}")
    console.print(f"[green]VTT:[/] {vtt}")


@app.command()
def watch(
    drop: Path = typer.Option(DROP_DIR),
    dest: Path = typer.Option(OUTPUT_DIR),
    model_name: str = typer.Option("base"),
) -> None:
    """Monitorea drop/ y procesa cada audio nuevo."""
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler, FileSystemEvent

    model = load_model(model_name)

    class AudioHandler(FileSystemEventHandler):
        def on_created(self, event: FileSystemEvent) -> None:
            if event.is_directory:
                return
            path = Path(event.src_path)
            if path.suffix.lower() not in AUDIO_EXTENSIONS:
                return
            time.sleep(0.5)
            if path.exists():
                console.print(f"[cyan]Procesando:[/] {path.name}")
                try:
                    process_audio(path, dest, model=model)
                except Exception as e:
                    console.print(f"[red]Error:[/] {e}")

    # TODO: Observer setup
    raise NotImplementedError


if __name__ == "__main__":
    app()
