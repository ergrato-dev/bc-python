"""
Ejercicio 04 — TUI con Textual
Studio BC: visor de assets con filtrado en tiempo real.
"""

from textual.app import App, ComposeResult
from textual.widgets import DataTable, Footer, Header, Input, Label
from textual.containers import Vertical

ASSETS = [
    {"name": "intro.mp4",    "type": "video", "size": "128 MB", "status": "ok"},
    {"name": "logo.png",     "type": "image", "size": "2.4 MB", "status": "ok"},
    {"name": "audio_bg.wav", "type": "audio", "size": "18 MB",  "status": "ok"},
    {"name": "credits.mp4",  "type": "video", "size": "42 MB",  "status": "failed"},
    {"name": "thumb.jpg",    "type": "image", "size": "800 KB", "status": "ok"},
    {"name": "outro.mp4",    "type": "video", "size": "96 MB",  "status": "ok"},
    {"name": "bg_music.mp3", "type": "audio", "size": "6 MB",   "status": "ok"},
]


class AssetViewer(App):
    """Studio BC — Asset Viewer TUI."""

    CSS = """
    Screen {
        background: $background;
    }

    #filter-input {
        margin: 1 2;
        border: round $primary;
    }

    #status-label {
        margin: 0 2;
        color: $text-muted;
    }

    DataTable {
        margin: 0 2 1 2;
        height: 1fr;
    }
    """

    # TODO: añade BINDINGS para:
    # ("q", "quit", "Quit")
    # ("r", "reload", "Reload")
    # ("d", "delete_selected", "Delete")
    BINDINGS = []

    def compose(self) -> ComposeResult:
        # TODO: Paso 1 — implementa compose() con:
        # yield Header(show_clock=True)
        # with Vertical():
        #     yield Input(placeholder="Filter by name...", id="filter-input")
        #     yield Label("", id="status-label")
        #     yield DataTable(id="assets-table")
        # yield Footer()
        yield Header()
        yield Label("TODO: implement compose()")
        yield Footer()

    def on_mount(self) -> None:
        # TODO: Paso 2 — pobla la DataTable
        # table = self.query_one("#assets-table", DataTable)
        # table.add_columns("Name", "Type", "Size", "Status")
        # self._load_assets(ASSETS)
        pass

    def _load_assets(self, assets: list[dict[str, str]]) -> None:
        # TODO: helper que limpia la tabla y añade filas
        # table = self.query_one("#assets-table", DataTable)
        # table.clear()
        # for a in assets:
        #     status = "[green]✅ ok[/green]" if a["status"] == "ok" else "[red]❌ failed[/red]"
        #     table.add_row(a["name"], a["type"], a["size"], status)
        # self.query_one("#status-label", Label).update(f"{len(assets)} asset(s)")
        pass

    def on_input_changed(self, event: Input.Changed) -> None:
        # TODO: Paso 3 — filtra ASSETS por name.startswith(event.value.lower())
        # y llama self._load_assets(filtered)
        pass

    def action_reload(self) -> None:
        # TODO: Paso 4 — limpia el Input y recarga todos los assets
        pass

    def action_delete_selected(self) -> None:
        # TODO: Paso 4 — elimina la fila con cursor de la tabla
        # (investiga: table.get_cell_at(table.cursor_row, 0) para obtener el nombre)
        pass


if __name__ == "__main__":
    app = AssetViewer()
    app.run()
