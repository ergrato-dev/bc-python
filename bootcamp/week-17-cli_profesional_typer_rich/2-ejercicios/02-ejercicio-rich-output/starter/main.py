"""
Ejercicio 02 — Rich Output
Studio BC: salidas de terminal ricas y consistentes.
"""

import time
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
from rich.progress import track

console = Console()
err_console = Console(stderr=True)

# Datos de ejemplo
ASSETS = [
    {"name": "intro.mp4",   "type": "video", "size": "128 MB", "status": "ok"},
    {"name": "logo.png",    "type": "image", "size": "2.4 MB", "status": "ok"},
    {"name": "audio_bg.wav","type": "audio", "size": "18 MB",  "status": "ok"},
    {"name": "credits.mp4", "type": "video", "size": "42 MB",  "status": "failed"},
    {"name": "thumb.jpg",   "type": "image", "size": "800 KB", "status": "ok"},
]

STATS = {
    "project": "reel-2025",
    "total": len(ASSETS),
    "ok": sum(1 for a in ASSETS if a["status"] == "ok"),
    "failed": sum(1 for a in ASSETS if a["status"] == "failed"),
    "time": "3.4s",
}


# ─────────────────────────────────────────────
# PASO 1 — reemplazar print() con Console
# ─────────────────────────────────────────────

def greet() -> None:
    # TODO: reemplaza los print() con console.print() usando markup de Rich
    print("Studio BC Pipeline")        # → console.print("[bold cyan]Studio BC Pipeline[/bold cyan]")
    print("Processing assets...")      # → con estilo dim o yellow
    print("Done!")                     # → con green bold
    print("Error: something failed")   # → con err_console en red bold


# ─────────────────────────────────────────────
# PASO 2 — Table para assets
# ─────────────────────────────────────────────

def show_assets_table(assets: list[dict[str, str]]) -> None:
    """
    TODO: construye y muestra una Table con columnas:
    Name (cyan), Type (magenta), Size (right-aligned), Status (center, con íconos de color).

    Status icons:
    - "ok"     → "[green]✅ ok[/green]"
    - "failed" → "[red]❌ failed[/red]"
    """
    # table = Table(title="Assets — reel-2025", show_lines=True)
    # table.add_column(...)
    # ...
    pass


# ─────────────────────────────────────────────
# PASO 3 — Panel para resumen
# ─────────────────────────────────────────────

def show_summary_panel(stats: dict[str, object]) -> None:
    """
    TODO: muestra un Panel con borde cyan y título "Summary".
    Contenido (una línea por clave):
    [bold]Project:[/bold]  reel-2025
    [bold]Total:[/bold]    5 assets
    [bold]OK:[/bold]       4
    [bold]Failed:[/bold]   1
    [bold]Time:[/bold]     3.4s
    """
    pass


# ─────────────────────────────────────────────
# PASO 4 — Progress para operación larga
# ─────────────────────────────────────────────

def run_with_progress(assets: list[dict[str, str]]) -> None:
    """
    TODO: usa track(assets, description="Processing...") para iterar.
    En cada iteración: time.sleep(0.3) y console.print(f"  ✅ {asset['name']}")
    """
    pass


# ─────────────────────────────────────────────
# PASO 5 — Markdown para reporte
# ─────────────────────────────────────────────

def show_markdown_report(assets: list[dict[str, str]]) -> None:
    """
    TODO: genera un string Markdown con:
    # Studio BC Report
    ## Assets
    tabla markdown (| Name | Type | Status |)
    ## Summary
    - Total: N
    - OK: N
    - Failed: N
    Luego: console.print(Markdown(md_text))
    """
    pass


if __name__ == "__main__":
    greet()
    print("\n─── Table ───")
    show_assets_table(ASSETS)

    print("\n─── Summary Panel ───")
    show_summary_panel(STATS)

    print("\n─── Progress ───")
    run_with_progress(ASSETS)

    print("\n─── Markdown Report ───")
    show_markdown_report(ASSETS)
