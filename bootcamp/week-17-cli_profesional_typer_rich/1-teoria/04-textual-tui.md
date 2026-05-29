# Textual — TUIs Interactivas

## Objetivos

- Entender la arquitectura de una app Textual
- Crear layouts con widgets estándar
- Manejar eventos y acciones del usuario
- Aplicar estilos con Textual CSS

---

## 1. Textual vs Rich

| | Rich | Textual |
|-|------|---------|
| Paradigma | Render estático / Live | Aplicación reactiva con estado |
| Interactividad | No (solo output) | Sí (teclado, mouse, formularios) |
| Caso de uso | CLI output, dashboards read-only | TUIs completas (tipo htop, lazygit) |
| Basado en | Nada (propio) | Rich + asyncio |

Textual está construido sobre Rich y asyncio. Una app Textual es una corutina async.

---

## 2. App mínima

```python
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static

class HelloApp(App):
    """Una TUI mínima de Studio BC."""

    CSS = """
    Static {
        background: $surface;
        border: round $primary;
        padding: 1 2;
        margin: 1;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Hello from [bold cyan]Studio BC[/bold cyan]!")
        yield Footer()

if __name__ == "__main__":
    app = HelloApp()
    app.run()
```

`compose()` define el árbol de widgets (similar a React's `render`). `CSS` usa Textual CSS — un subconjunto de CSS con variables del tema.

---

## 3. Widgets estándar

```python
from textual.app import App, ComposeResult
from textual.widgets import (
    Header, Footer,
    Button, Input, Label,
    DataTable, ListView, ListItem,
    Checkbox, RadioSet, RadioButton,
    ProgressBar, Log,
)
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer

class StudioApp(App):
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        with Horizontal():
            with Vertical(id="sidebar"):
                yield Label("Projects", classes="section-title")
                yield ListView(
                    ListItem(Label("reel-2025")),
                    ListItem(Label("spot-bc-01")),
                    ListItem(Label("short-film")),
                )

            with Vertical(id="main"):
                yield Label("Assets", classes="section-title")
                table = DataTable()
                table.add_columns("Name", "Type", "Status", "Size")
                table.add_rows([
                    ("intro.mp4",   "video", "✅ ok", "128 MB"),
                    ("logo.png",    "image", "✅ ok", "2.4 MB"),
                    ("credits.mp4", "video", "❌ fail", "—"),
                ])
                yield table

        yield Footer()
```

---

## 4. Eventos y acciones

```python
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Label, Input
from textual.containers import Horizontal

class PipelineApp(App):
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("r", "run_pipeline", "Run pipeline"),
        ("c", "clear_log", "Clear log"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Input(placeholder="Project ID...", id="project-input")
        with Horizontal():
            yield Button("Run", variant="success", id="run-btn")
            yield Button("Clear", variant="default", id="clear-btn")
        yield Label("", id="status")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Evento: se presionó un botón."""
        if event.button.id == "run-btn":
            self.action_run_pipeline()
        elif event.button.id == "clear-btn":
            self.action_clear_log()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Evento: Enter en el input."""
        project_id = event.value
        self.query_one("#status", Label).update(f"Project: [bold]{project_id}[/bold]")

    def action_run_pipeline(self) -> None:
        """Acción vinculada a BINDINGS y al botón."""
        project_id = self.query_one("#project-input", Input).value
        self.query_one("#status", Label).update(f"[yellow]Running pipeline for {project_id}...[/yellow]")

    def action_clear_log(self) -> None:
        self.query_one("#status", Label).update("")
```

### `query_one()` — selección de widgets

```python
# Por ID
label = self.query_one("#status", Label)

# Por tipo
table = self.query_one(DataTable)

# Por clase CSS
panel = self.query_one(".error-panel")
```

---

## 5. Actualización reactiva: `reactive`

```python
from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widgets import Label, Header, Footer

class CounterApp(App):
    count: reactive[int] = reactive(0)

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("0", id="counter")
        yield Footer()

    BINDINGS = [
        ("up", "increment", "Increment"),
        ("down", "decrement", "Decrement"),
    ]

    def watch_count(self, new_value: int) -> None:
        """Se llama automáticamente cuando count cambia."""
        color = "green" if new_value >= 0 else "red"
        self.query_one("#counter", Label).update(f"[{color}]{new_value}[/{color}]")

    def action_increment(self) -> None:
        self.count += 1

    def action_decrement(self) -> None:
        self.count -= 1
```

`reactive` es un descriptor que notifica a `watch_<nombre>()` cada vez que el valor cambia.

---

## 6. Textual CSS

```css
/* styles/app.tcss */
Screen {
    background: $background;
}

#sidebar {
    width: 25%;
    border-right: solid $primary;
    background: $surface;
}

#main {
    width: 1fr;
    padding: 1 2;
}

.section-title {
    color: $accent;
    text-style: bold;
    border-bottom: solid $primary;
    padding-bottom: 1;
}

Button.success {
    background: $success;
}

Button:hover {
    background: $success-darken-1;
}
```

Textual usa variables de tema (`$primary`, `$surface`, `$accent`, etc.) para mantener consistencia visual.

---

## 7. Cuándo usar Textual vs Rich Live

```
Necesito mostrar datos que cambian:
│
├─ ¿Solo lectura (dashboard)? → Rich Live + Layout
│
└─ ¿El usuario interactúa? (navegar, filtrar, escribir)
    └─ Textual
        │
        ├─ ¿Simple? (lista + acciones) → BINDINGS + Widgets estándar
        └─ ¿Complejo? (formularios, pestañas) → Screens + reactives
```

---

## Recursos Adicionales

- [Textual docs](https://textual.textualize.io/)
- [Textual — Getting Started](https://textual.textualize.io/getting_started/)
- [Textual CSS reference](https://textual.textualize.io/css_types/)
