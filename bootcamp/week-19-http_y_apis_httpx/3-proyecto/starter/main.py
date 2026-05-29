"""
Studio BC API Client — Orquestador principal.

Flujo:
  1. Busca pistas de música genre=cinematic, max_duration=90
  2. Imprime resultados en tabla Rich
  3. Si hay resultados, lanza un render con la primera pista
  4. Imprime job_id y estimated_secs
"""
from __future__ import annotations

import os
from rich.console import Console
from rich.table import Table
from src.music_client import MusicClient
from src.render_client import RenderClient

console = Console()


def main() -> None:
    # Leer credenciales de variables de entorno (o usar placeholders para desarrollo)
    music_api_key = os.getenv("MUSIC_API_KEY", "dev-key-placeholder")
    render_token = os.getenv("RENDER_TOKEN", "dev-token-placeholder")

    # 1. Buscar pistas
    console.print("[bold blue]Buscando pistas en MusicLicensing BC...[/]")
    with MusicClient(api_key=music_api_key) as music:
        # TODO: search_tracks(genre="cinematic", max_duration=90)
        # TODO: manejar excepciones de red con mensaje amigable
        pass

    # 2. Mostrar en tabla (Rich)
    # TODO: tabla con columnas: Título, Artista, Duración, Precio
    # TODO: for track in results: table.add_row(...)
    # TODO: console.print(table)

    # 3. Lanzar render con la primera pista
    console.print("[bold blue]Lanzando render en CloudRender BC...[/]")
    with RenderClient(token=render_token) as render:
        # TODO: submit_job(project_id="spot-canal9-2025", track_id=first_track.track_id)
        # TODO: console.print(f"Job lanzado: {job.job_id} (~{job.estimated_secs}s)")
        pass


if __name__ == "__main__":
    main()
