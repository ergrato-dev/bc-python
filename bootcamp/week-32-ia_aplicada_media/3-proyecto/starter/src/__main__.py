"""CLI — studio-ai-tagger."""
from __future__ import annotations

import json
import os
from pathlib import Path

import typer
from rich.console import Console
from rich.json import JSON

from .analyzer import AssetAnalyzer
from .config import AIConfig

app = typer.Typer(name="studio-ai-tagger", help="Genera metadata de IA para assets de Studio BC")
console = Console()


@app.command()
def analyze(
    asset: str = typer.Argument(..., help="Ruta al asset (video, audio o imagen)"),
    output: str = typer.Option("", "--output", "-o", help="Guardar resultado en JSON"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Usar datos mockeados (sin API key)"),
) -> None:
    """Analiza un asset y genera metadata completa."""
    if dry_run:
        os.environ["DRY_RUN"] = "true"

    cfg = AIConfig()
    if not cfg.dry_run and not os.getenv("OPENAI_API_KEY"):
        console.print("[red]Error:[/] OPENAI_API_KEY no está configurado. Usa --dry-run para pruebas.")
        raise typer.Exit(1)

    asset_path = Path(asset)
    if not asset_path.exists() and not cfg.dry_run:
        console.print(f"[red]Error:[/] Archivo no encontrado: {asset}")
        raise typer.Exit(1)

    console.print(f"[cyan]Analizando:[/] {asset} {'[dim](dry-run)[/]' if cfg.dry_run else ''}")

    analyzer = AssetAnalyzer(cfg)
    result = analyzer.analyze(asset_path if asset_path.exists() else Path("mock.mp4"))

    data = result.to_dict()

    if output:
        Path(output).write_text(json.dumps(data, indent=2, ensure_ascii=False))
        console.print(f"[green]Guardado en:[/] {output}")
    else:
        console.print(JSON(json.dumps(data, indent=2, ensure_ascii=False)))


if __name__ == "__main__":
    app()
