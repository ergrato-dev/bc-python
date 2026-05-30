from __future__ import annotations

import typer
from rich.console import Console
from rich.table import Table

from .config import BackupConfig
from .sync_engine import SyncEngine

app = typer.Typer(name="studio-cloud-backup", help="Backup automático de assets Studio BC a S3 y Drive")
console = Console()
config = BackupConfig()
engine = SyncEngine(config)


@app.command()
def backup(
    project: str = typer.Option(..., "--project", "-p", help="Slug del proyecto: cliente/nombre"),
    client_email: str = typer.Option("", "--client-email", help="Email del cliente para compartir en Drive"),
    force: bool = typer.Option(False, "--force", "-f", help="Forzar re-subida de todos los archivos"),
) -> None:
    """Backup completo o incremental de output/ → S3 + Drive."""
    console.print(f"[bold cyan]Backup:[/] proyecto=[yellow]{project}[/] forzado={force}")

    try:
        stats = engine.incremental_backup(project, force=force)
    except RuntimeError as e:
        console.print(f"[bold red]Error:[/] {e}")
        raise typer.Exit(1)

    t = Table("Métrica", "Valor")
    t.add_row("Subidos", str(stats["uploaded"]))
    t.add_row("Saltados", str(stats["skipped"]))
    t.add_row("Errores", str(stats["errors"]))
    console.print(t)

    if stats["errors"] > 0:
        raise typer.Exit(1)


@app.command()
def sync(
    project: str = typer.Option(..., "--project", "-p", help="Slug del proyecto"),
) -> None:
    """Sync incremental sin forzar (alias de backup sin --force)."""
    stats = engine.incremental_backup(project, force=False)
    console.print(f"[green]Sync OK[/] — subidos={stats['uploaded']} saltados={stats['skipped']}")


@app.command()
def status() -> None:
    """Muestra el estado del último sync."""
    info = engine.get_status()
    console.print(f"Archivos registrados: [bold]{info['total_files']}[/]")
    console.print(f"Último sync: [cyan]{info.get('last_sync', 'nunca')}[/]")
    console.print(f"State file: {info.get('state_path', 'N/A')}")


if __name__ == "__main__":
    app()
