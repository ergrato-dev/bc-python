"""Una CLI pequeña para probar: clasifica valores y cuenta las líneas de un archivo.

No hay que cambiar nada aquí, salvo en el paso 6, que te pide romperla a propósito.
"""

import sys
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

LOW = 10.0
HIGH = 50.0

app = typer.Typer(no_args_is_help=True, add_completion=False)
out = Console(markup=False, highlight=False, soft_wrap=True)
err = Console(stderr=True, markup=False, highlight=False, soft_wrap=True)


def level(value: float) -> str:
    """bajo por debajo de LOW, alto por encima de HIGH y medio entre los dos, incluidos."""
    if value < LOW:
        return "bajo"
    if value > HIGH:
        return "alto"
    return "medio"


@app.callback()
def main() -> None:
    """Ejercicio 04 · Probar la CLI."""


@app.command()
def clasificar(values: Annotated[list[float] | None, typer.Argument()] = None) -> None:
    """Clasifica los valores; sin valores, los lee de stdin. Con alguno alto, código 1."""
    data = values or [float(line) for line in sys.stdin if line.strip()]
    for value in data:
        out.print(f"{value:g} → {level(value)}")
    high = sum(level(value) == "alto" for value in data)
    if high:
        err.print(f"aviso: {high} valores altos")
        raise typer.Exit(1)


@app.command()
def contar(path: Annotated[Path, typer.Argument(exists=True, dir_okay=False)]) -> None:
    """Cuenta las líneas con datos de un archivo."""
    lines = path.read_text(encoding="utf-8").splitlines()
    count = sum(1 for line in lines if line.strip())
    out.print(f"{path.name}: {count} líneas con datos")


if __name__ == "__main__":
    app()
