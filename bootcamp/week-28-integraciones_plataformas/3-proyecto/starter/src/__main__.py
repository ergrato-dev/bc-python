from __future__ import annotations

import typer
from pathlib import Path
from rich.console import Console
from rich.table import Table

from .config import DistributorConfig
from .distributor import Distributor
from .notifier import SlackNotifier, DiscordNotifier
from .notion_updater import NotionUpdater

app = typer.Typer(name="studio-distributor", help="Distribución de media Studio BC")
console = Console()


def _build_distributor(cfg: DistributorConfig) -> Distributor:
    yt = None
    vimeo_pub = None
    slack = None
    discord = None
    notion = None

    if cfg.youtube_client_secrets.exists():
        from .youtube_publisher import YouTubePublisher
        yt = YouTubePublisher(cfg.youtube_client_secrets, cfg.youtube_token_path)

    if cfg.vimeo_token:
        from .vimeo_publisher import VimeoPublisher
        vimeo_pub = VimeoPublisher(cfg.vimeo_token, cfg.vimeo_key, cfg.vimeo_secret, cfg.vimeo_album)

    if cfg.slack_bot_token:
        slack = SlackNotifier(cfg.slack_bot_token, cfg.slack_channel)

    if cfg.discord_webhook_url:
        discord = DiscordNotifier(cfg.discord_webhook_url)

    if cfg.notion_token and cfg.notion_database_id:
        notion = NotionUpdater(cfg.notion_token, cfg.notion_database_id)

    return Distributor(yt, vimeo_pub, slack, discord, notion)


@app.command()
def publish(
    path: str = typer.Option(..., "--path", "-p", help="Ruta al video"),
    title: str = typer.Option(..., "--title", "-t", help="Título del video"),
    project: str = typer.Option(..., "--project", help="Slug del proyecto"),
    client: str = typer.Option("", "--client", help="Nombre del cliente"),
    description: str = typer.Option("", "--description", "-d"),
    thumbnail: str = typer.Option("", "--thumbnail", help="Ruta al thumbnail JPG"),
) -> None:
    """Publica en todas las plataformas configuradas."""
    cfg = DistributorConfig()
    distributor = _build_distributor(cfg)
    thumb_path = Path(thumbnail) if thumbnail else None

    console.print(f"[bold cyan]Distribuyendo:[/] {title}")
    result = distributor.distribute(
        video_path=Path(path),
        title=title,
        project=project,
        client=client,
        description=description,
        thumbnail_path=thumb_path,
    )

    t = Table("Plataforma", "Estado", "URL / ID")
    t.add_row("YouTube", "[green]OK[/]" if result.youtube_url else "[red]FALLO[/]",
              result.youtube_url or result.errors.get("youtube", ""))
    t.add_row("Vimeo", "[green]OK[/]" if result.vimeo_url else "[red]FALLO[/]",
              result.vimeo_url or result.errors.get("vimeo", ""))
    t.add_row("Slack", "[green]OK[/]" if result.slack_ts else "[dim]skip[/]",
              result.slack_ts or "")
    t.add_row("Notion", "[green]OK[/]" if result.notion_page_id else "[dim]skip[/]",
              result.notion_page_id[:20] + "..." if result.notion_page_id else "")
    console.print(t)

    if result.errors:
        console.print(f"[yellow]Advertencia:[/] {len(result.errors)} plataforma(s) con error: {list(result.errors.keys())}")
    else:
        console.print("[bold green]Distribución completa[/]")


@app.command()
def notify(
    project: str = typer.Option(..., "--project"),
    youtube_url: str = typer.Option("", "--youtube-url"),
    vimeo_url: str = typer.Option("", "--vimeo-url"),
    client: str = typer.Option("", "--client"),
) -> None:
    """Envía notificaciones sin publicar video."""
    cfg = DistributorConfig()
    if cfg.slack_bot_token:
        notifier = SlackNotifier(cfg.slack_bot_token, cfg.slack_channel)
        ts = notifier.notify_delivery(project, client, youtube_url, vimeo_url)
        console.print(f"[green]Slack notificado[/] ts={ts}")
    if cfg.discord_webhook_url:
        disc = DiscordNotifier(cfg.discord_webhook_url)
        disc.notify_delivery(project, client, youtube_url, vimeo_url)
        console.print("[green]Discord notificado[/]")


if __name__ == "__main__":
    app()
