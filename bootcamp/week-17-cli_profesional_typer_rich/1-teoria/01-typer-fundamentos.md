# Typer — Fundamentos

## Objetivos

- Crear comandos y subcomandos con Typer
- Diferenciar `Argument` vs `Option` y sus usos
- Añadir validación, callbacks y autocompletion
- Entender la relación con Click bajo el capó

---

## 1. Typer vs Click

Typer está construido sobre Click pero expone una API basada en **type hints** en lugar de decoradores explícitos:

```python
# Click — explícito pero verboso
import click

@click.command()
@click.argument("name")
@click.option("--count", default=1, type=int, help="Number of greetings")
def greet(name: str, count: int) -> None:
    for _ in range(count):
        click.echo(f"Hello, {name}!")

# Typer — types inferidos de las anotaciones
import typer

app = typer.Typer()

@app.command()
def greet(name: str, count: int = typer.Option(1, help="Number of greetings")) -> None:
    for _ in range(count):
        typer.echo(f"Hello, {name}!")

if __name__ == "__main__":
    app()
```

Typer genera automáticamente el `--help`, la validación de tipos y la conversión.

---

## 2. `Argument` vs `Option`

```python
import typer
from pathlib import Path

app = typer.Typer()

@app.command()
def process(
    # Argument: posicional, requerido por defecto
    input_file: Path = typer.Argument(..., help="Path to input file"),

    # Option: --flag, tiene valor por defecto
    output_dir: Path = typer.Option(Path("./output"), "--out", "-o", help="Output directory"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
    workers: int = typer.Option(4, help="Number of parallel workers"),
) -> None:
    if verbose:
        typer.echo(f"Processing {input_file} → {output_dir} with {workers} workers")
```

| | `Argument` | `Option` |
|-|-----------|---------|
| Sintaxis CLI | `cmd valor` | `cmd --flag valor` |
| Requerido | Por defecto sí | Por defecto no (tiene default) |
| Uso | Entrada principal | Configuración / modificadores |
| `...` como default | Requerido sin default | Requerido (raro en options) |

---

## 3. Subcomandos con `app.add_typer()`

```python
import typer

app = typer.Typer(help="Studio BC asset management CLI")
assets_app = typer.Typer(help="Manage project assets")
projects_app = typer.Typer(help="Manage projects")

app.add_typer(assets_app, name="assets")
app.add_typer(projects_app, name="projects")


@assets_app.command("list")
def assets_list(project_id: str = typer.Argument(..., help="Project ID")) -> None:
    """List all assets for a project."""
    typer.echo(f"Assets for project: {project_id}")


@assets_app.command("add")
def assets_add(
    project_id: str,
    name: str,
    asset_type: str = typer.Option("video", "--type", "-t"),
) -> None:
    """Add an asset to a project."""
    typer.echo(f"Added {asset_type} asset '{name}' to {project_id}")


@projects_app.command("list")
def projects_list() -> None:
    """List all projects."""
    typer.echo("Projects: reel-2025, spot-bc-01")
```

```
$ python main.py --help
$ python main.py assets --help
$ python main.py assets list my-project
$ python main.py assets add my-project intro.mp4 --type video
```

---

## 4. Estado compartido con `ctx.obj`

Para pasar configuración global (token de API, verbosidad) a todos los subcomandos:

```python
import typer
from dataclasses import dataclass

app = typer.Typer()

@dataclass
class Config:
    verbose: bool = False
    api_url: str = "https://api.studio.bc"

@app.callback()
def main(
    ctx: typer.Context,
    verbose: bool = typer.Option(False, "--verbose", "-v"),
    api_url: str = typer.Option("https://api.studio.bc", envvar="BC_API_URL"),
) -> None:
    """Studio BC CLI — manage projects and assets."""
    ctx.ensure_object(dict)
    ctx.obj = Config(verbose=verbose, api_url=api_url)

@app.command()
def status(ctx: typer.Context) -> None:
    """Show API connection status."""
    cfg: Config = ctx.obj
    if cfg.verbose:
        typer.echo(f"Connecting to {cfg.api_url}...")
    typer.echo("✅ API connection OK")
```

---

## 5. Validación y callbacks

```python
import typer

def validate_project_id(value: str) -> str:
    if not value.replace("-", "").replace("_", "").isalnum():
        raise typer.BadParameter("project-id must be alphanumeric with - or _")
    return value.lower()

app = typer.Typer()

@app.command()
def create(
    project_id: str = typer.Argument(..., callback=validate_project_id),
    budget: float = typer.Option(..., help="Budget in USD", min=0.0),
    priority: int = typer.Option(1, min=1, max=5, help="Priority 1-5"),
) -> None:
    """Create a new project."""
    typer.echo(f"Created: {project_id} (budget: ${budget:.2f}, priority: {priority})")
```

El parámetro `min`/`max` aplica validación de rango automáticamente para `int` y `float`.

---

## 6. Autocompletion

```python
import typer

ASSET_TYPES = ["video", "audio", "image", "document"]

def complete_asset_type(incomplete: str) -> list[str]:
    return [t for t in ASSET_TYPES if t.startswith(incomplete)]

app = typer.Typer()

@app.command()
def upload(
    asset_type: str = typer.Option(
        "video",
        autocompletion=complete_asset_type,
        help="Type of asset",
    ),
    path: str = typer.Argument(...),
) -> None:
    typer.echo(f"Uploading {path} as {asset_type}")

# Instalar autocompletion:
# $ myapp --install-completion
# $ myapp --show-completion
```

---

## 7. Salida: `typer.echo` vs `typer.secho`

```python
import typer

@app.command()
def demo() -> None:
    typer.echo("Neutral message")
    typer.secho("Success!", fg=typer.colors.GREEN, bold=True)
    typer.secho("Warning!", fg=typer.colors.YELLOW)
    typer.secho("Error!", fg=typer.colors.RED, err=True)   # stderr

    # Confirmar acción destructiva
    confirmed = typer.confirm("Delete all assets?")
    if confirmed:
        typer.echo("Deleted.")

    # Prompt interactivo
    name = typer.prompt("Project name", default="untitled")
    typer.echo(f"Creating: {name}")
```

> En semana 17 usaremos `rich.Console` en lugar de `typer.secho` para salida más sofisticada.

---

## ✅ Resumen

| Concepto | API |
|---------|-----|
| Comando raíz | `app = typer.Typer(); @app.command()` |
| Subcomandos | `app.add_typer(sub_app, name="sub")` |
| Argumento posicional | `typer.Argument(...)` |
| Opción con flag | `typer.Option(default, "--flag")` |
| Estado global | `@app.callback()` + `ctx.obj` |
| Validación | `callback=fn` o `min=` / `max=` |
| Autocompletion | `autocompletion=fn` |

---

## Recursos Adicionales

- [Typer docs](https://typer.tiangolo.com/)
- [Click docs](https://click.palletsprojects.com/)
