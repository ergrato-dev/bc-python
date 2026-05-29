# Rich — Output: Console, Tables, Panels, Syntax

## Objetivos

- Usar `Console` como reemplazo de `print()`
- Construir tablas y panels con Rich
- Resaltar código con syntax highlighting
- Renderizar Markdown en terminal

---

## 1. `Console` — el punto de entrada

```python
from rich.console import Console

console = Console()

# Markup similar a BBCode
console.print("Hello [bold cyan]Studio BC[/bold cyan]!")
console.print("[green]✅ Success[/green]")
console.print("[red bold]❌ Error:[/red bold] file not found")

# stderr
err_console = Console(stderr=True)
err_console.print("[red]Fatal error[/red]", style="bold")

# Log con timestamp automático
console.log("Pipeline started", style="dim")
console.log("[bold]Pipeline complete[/bold]")
```

### Estilos disponibles

```python
# Colores: red, green, yellow, blue, magenta, cyan, white, bright_*
# Modifiers: bold, italic, underline, dim, strike, blink
# Combinar: "bold red on white"
console.print("Alert!", style="bold red on white")
```

---

## 2. `Table` — tablas estructuradas

```python
from rich.console import Console
from rich.table import Table

console = Console()

def show_assets(assets: list[dict[str, str]]) -> None:
    table = Table(title="Studio BC — Project Assets", show_lines=True)

    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("Type", style="magenta")
    table.add_column("Size", justify="right", style="green")
    table.add_column("Status", justify="center")

    status_icons = {"ok": "[green]✅ ok[/green]", "failed": "[red]❌ failed[/red]"}

    for asset in assets:
        table.add_row(
            asset["name"],
            asset["type"],
            asset.get("size", "—"),
            status_icons.get(asset.get("status", ""), asset.get("status", "—")),
        )

    console.print(table)

show_assets([
    {"name": "intro.mp4", "type": "video", "size": "128 MB", "status": "ok"},
    {"name": "logo.png",  "type": "image", "size": "2.4 MB", "status": "ok"},
    {"name": "raw.mp4",   "type": "video", "size": "4.1 GB", "status": "failed"},
])
```

### Opciones de tabla

```python
Table(
    title="...",
    caption="Total: N assets",
    box=rich.box.ROUNDED,       # SIMPLE, MINIMAL, DOUBLE, ASCII, etc.
    show_header=True,
    show_lines=False,           # separadores entre filas
    expand=True,                # ocupa todo el ancho
    highlight=True,             # resalta números
)
```

---

## 3. `Panel` — contenido enmarcado

```python
from rich.console import Console
from rich.panel import Panel

console = Console()

# Panel simple
console.print(Panel("Pipeline complete", title="Studio BC", border_style="green"))

# Panel con markup interno
console.print(Panel(
    "[bold]Project:[/bold] reel-2025\n"
    "[bold]Assets:[/bold]  12 processed, 1 failed\n"
    "[bold]Time:[/bold]    4.2s",
    title="[cyan]Summary[/cyan]",
    border_style="cyan",
    expand=False,          # ancho ajustado al contenido
))

# Panel de error
console.print(Panel(
    "[red]Network timeout after 3 retries[/red]\n"
    "Asset: broken.mp4",
    title="[red bold]Error[/red bold]",
    border_style="red",
))
```

---

## 4. Syntax Highlighting

```python
from rich.console import Console
from rich.syntax import Syntax

console = Console()

code = '''
async def download_asset(sem: asyncio.Semaphore, url: str) -> bytes:
    async with sem:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10.0)
            return response.content
'''

syntax = Syntax(code, "python", theme="monokai", line_numbers=True)
console.print(syntax)

# Desde archivo
syntax = Syntax.from_path("src/downloader.py", theme="github-dark", line_numbers=True)
console.print(syntax)
```

Temas disponibles: `monokai`, `dracula`, `github-dark`, `solarized-dark`, `one-dark`, `vs`.

---

## 5. Markdown

```python
from rich.console import Console
from rich.markdown import Markdown

console = Console()

md_text = """
# Studio BC Pipeline Report

## Summary
- **12** assets processed
- **1** failed (network timeout)
- Total time: **4.2s**

## Failed Assets
| Name | Error |
|------|-------|
| broken.mp4 | Timeout after 3 retries |

> Run with `--verbose` to see full error details.
"""

console.print(Markdown(md_text))
```

---

## 6. `Columns` y layout horizontal

```python
from rich.columns import Columns
from rich.panel import Panel
from rich.console import Console

console = Console()

panels = [
    Panel(f"[green]✅ ok[/green]", title="intro.mp4"),
    Panel(f"[green]✅ ok[/green]", title="logo.png"),
    Panel(f"[red]❌ failed[/red]", title="broken.mp4"),
]

console.print(Columns(panels, equal=True, expand=True))
```

---

## 7. Integrar Rich con Typer

```python
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer()
console = Console()
err_console = Console(stderr=True, style="red")

@app.command()
def list_assets(project_id: str) -> None:
    """List all assets for a project."""
    try:
        assets = fetch_assets(project_id)   # puede lanzar
    except ValueError as e:
        err_console.print(f"Error: {e}")
        raise typer.Exit(code=1)

    table = Table("Name", "Type", "Status")
    for a in assets:
        table.add_row(a["name"], a["type"], a["status"])
    console.print(table)
```

> El exit code `1` señala error al shell; `0` es éxito implícito.

---

## ✅ Resumen

| Componente | Uso |
|-----------|-----|
| `Console.print()` | Reemplaza `print()` con markup y estilos |
| `Console.log()` | Como print pero con timestamp |
| `Table` | Datos tabulares con columnas tipadas |
| `Panel` | Contenido enmarcado con título |
| `Syntax` | Código con syntax highlighting |
| `Markdown` | Render de Markdown en terminal |
| `Columns` | Layout horizontal de varios renderables |

---

## Recursos Adicionales

- [Rich docs — Console](https://rich.readthedocs.io/en/stable/console.html)
- [Rich docs — Tables](https://rich.readthedocs.io/en/stable/tables.html)
- [Rich markup reference](https://rich.readthedocs.io/en/stable/markup.html)
