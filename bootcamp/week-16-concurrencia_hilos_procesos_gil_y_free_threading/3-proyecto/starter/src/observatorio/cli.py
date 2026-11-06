"""La línea de comandos del Observatorio: `observatorio informe`, `observatorio validar`.

Qué: una aplicación Typer con dos comandos; Rich escribe las tablas y los errores.
Para qué: Typer lee los argumentos a partir de las anotaciones de cada función, y
genera la ayuda y los errores de uso; tú solo escribes qué hace cada comando.
Impacto: es la única parte del Observatorio que toca la terminal. El paquete `core`
no sabe que existe, y la API de la semana 20 lo usará igual que este archivo.
"""

import logging
import sys
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table
from rich.text import Text

from observatorio import __version__
from observatorio.core import (
    DataFileError,
    LinesSource,
    Scale,
    Series,
    Source,
    count_level,
    largest_jump,
    longest_streak,
    median,
    moving_average,
    open_file,
    process_lines,
    read_measurements,
    read_scale,
    share,
    summarize,
    summary_data,
    top,
    write_json,
)

# Tu unidad y tus umbrales de la semana 2.
UNIT = "unidad"
LOW = 10.0
HIGH = 50.0
SCALE = Scale(UNIT, LOW, HIGH)

TOP = 3
WINDOW = 3

# El color de cada nivel en la tabla. Sin terminal (una tubería, un archivo, los
# tests), Rich no pone colores y el texto queda igual.
STYLES = {"bajo": "cyan", "medio": "green", "alto": "bold red"}

app = typer.Typer(
    help="Observatorio de datos de mi dominio.",
    no_args_is_help=True,
    add_completion=False,
)
# Dos consolas: el resultado va a stdout y los errores a stderr, como en la semana 3.
# markup=False: Rich no interpreta los corchetes de los datos ("Sala [b]") como estilos.
# highlight=False: no colorea por su cuenta los números y las rutas.
# soft_wrap=True: no corta las líneas largas al ancho de la terminal (80 sin terminal).
out = Console(markup=False, highlight=False, soft_wrap=True)
err = Console(stderr=True, markup=False, highlight=False, soft_wrap=True)


def fail(message: str, code: int) -> typer.Exit:
    """Escribe "error: <mensaje>" en stderr y devuelve la salida con ese código."""
    err.print(f"error: {message}")
    return typer.Exit(code)


def show_version(value: bool) -> None:
    """Con --version, escribe la versión y termina antes de mirar nada más."""
    if value:
        out.print(f"observatorio {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    verbose: Annotated[
        bool, typer.Option("--verbose", "-v", help="Muestra el registro DEBUG en stderr.")
    ] = False,
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            "-V",
            callback=show_version,
            is_eager=True,
            help="Muestra la versión y termina.",
        ),
    ] = False,
) -> None:
    """Observatorio de datos de mi dominio."""
    if verbose:
        # Solo el programa configura el registro (semana 14).
        logging.basicConfig(level=logging.DEBUG, format="%(levelname)s %(name)s: %(message)s")


def table_of(series: Series, scale: Scale) -> Table:
    """Una fila por medida: etiqueta, valor y nivel, con el color del nivel."""
    table = Table(title="Medidas")
    table.add_column("Etiqueta")
    table.add_column("Valor", justify="right")
    table.add_column("Nivel")
    for measurement in series:
        level = scale.level(measurement.value)
        value = "sin dato" if measurement.value is None else f"{measurement.value:.1f} {scale.unit}"
        table.add_row(measurement.label, value, Text(level, style=STYLES.get(level, "")))
    return table


@app.command()
def informe(
    lineas: Annotated[
        list[str] | None,
        typer.Argument(
            metavar="LINEAS", help='Líneas "etiqueta;valor". Sin líneas ni --archivo, lee stdin.'
        ),
    ] = None,
    archivo: Annotated[
        Path | None, typer.Option("--archivo", "-f", help="Lee las líneas de un .txt o un .csv.")
    ] = None,
    json_path: Annotated[
        Path | None, typer.Option("--json", "-j", help="Guarda el resumen en este JSON.")
    ] = None,
    escala: Annotated[
        Path | None, typer.Option("--escala", "-e", help="Lee la unidad y los umbrales de un JSON.")
    ] = None,
) -> None:
    """Clasifica las medidas y escribe la tabla y el resumen."""
    if lineas and archivo is not None:
        raise typer.BadParameter("usa líneas o --archivo, no los dos", param_hint="LINEAS")
    source: Source
    if archivo is not None:
        source = open_file(archivo)
    elif lineas:
        source = LinesSource(lineas)
    else:
        source = LinesSource(list(sys.stdin))
    try:
        scale = SCALE if escala is None else read_scale(escala)
        lines = source.lines()
    except DataFileError as problem:
        raise fail(str(problem), 2) from problem
    rows, errors = process_lines(lines, scale.unit, scale.low, scale.high)
    for error in errors:
        err.print(f"error: {error}")
    series = Series.from_lines(lines)
    out.print(table_of(series, scale))
    summary = [
        summarize(rows),
        f"racha más larga en alto: {longest_streak(rows, 'alto')}",
        f"en alto: {share(count_level(rows, 'alto'), len(rows))}",
        f"etiquetas distintas: {len(series.labels())}",
        "medias más altas: "
        + ", ".join(f"{label} {mean:.1f}" for label, mean in top(series.means(), TOP)),
        "más frecuentes: "
        + ", ".join(f"{label} {count}" for label, count in series.most_common(TOP)),
    ]
    values = series.values()
    if values:
        averages = " · ".join(f"{average:.1f}" for average in moving_average(values, WINDOW))
        summary += [
            f"mediana: {median(values):.1f} {scale.unit}",
            f"media móvil ({WINDOW}): {averages}",
            f"mayor salto: {largest_jump(values):+.1f} {scale.unit}",
        ]
    out.print("\n".join(summary))
    if json_path is not None:
        try:
            write_json(summary_data(series.records), json_path)
        except DataFileError as problem:
            raise fail(str(problem), 2) from problem
        out.print(f"resumen guardado en {json_path}")
    if errors:
        raise typer.Exit(1)


@app.command()
def validar(
    ruta: Annotated[Path, typer.Argument(help="Un JSON con una lista de medidas.")],
) -> None:
    """Comprueba un JSON de medidas con Pydantic sin escribir el informe."""
    try:
        series = read_measurements(ruta)
    except DataFileError as problem:
        raise fail(str(problem), 2) from problem
    out.print(f"{ruta}: {len(series)} medidas válidas")
