"""La línea de comandos del Observatorio: informes, archivos, HTTP y PostgreSQL.

Qué: una aplicación Typer con veintiséis comandos (`informe`, `estadisticas`, `filtrar`,
`resumir`, `evolucion`, `graficar`, `comparar`, `exportar`, `sql`, `validar`, `lote`,
`vigilar`, `descargar`, `guardar`, `cargas`, `consultar`, `extraer`, `hallazgos`, `modelo`,
`ajustar`, `competir`, `agrupar`, `red`, `pronosticar`, `borrar` y `servir`);
Rich escribe las tablas y los errores.
Para qué: Typer lee los argumentos a partir de las anotaciones de cada función, y
genera la ayuda y los errores de uso; tú solo escribes qué hace cada comando.
Impacto: es la única parte del Observatorio que toca la terminal. El paquete `core`
no sabe que existe, y la API de la semana 20 lo usará igual que este archivo.
"""

import asyncio
import logging
import math
import sys
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Annotated

import typer
from psycopg.errors import UndefinedTable
from pydantic import ValidationError
from rich.console import Console
from rich.table import Table
from rich.text import Text
from sqlalchemy import make_url
from sqlalchemy.exc import ArgumentError, OperationalError, ProgrammingError
from sqlalchemy.orm import Session

from observatorio import __version__
from observatorio.core import (
    DataFileError,
    FileReport,
    LinesSource,
    Load,
    Measurement,
    Scale,
    Series,
    Source,
    count_level,
    delete_load,
    download_all,
    label_stats,
    largest_jump,
    list_loads,
    longest_streak,
    make_client,
    make_engine,
    median,
    moving_average,
    open_file,
    read_measurements,
    read_scale,
    report_files,
    save_series,
    share,
    summarize,
    summary_data,
    top,
    watch_files,
    write_json,
)
from observatorio.settings import Settings

if TYPE_CHECKING:
    # Solo para mypy: en ejecución no se importan NumPy ni pandas al cargar la CLI. Desde
    # Python 3.14 las anotaciones se evalúan cuando alguien las pide, así que `Stats` y
    # `pd.DataFrame` pueden aparecer en las firmas sin estar importados de verdad.
    import pandas as pd

    from observatorio.core.arrays import Counts, Floats, Stats
    from observatorio.core.clustering import Clustering
    from observatorio.core.ensembles import Contest
    from observatorio.core.learning import Evaluation
    from observatorio.core.validation import CrossValidation

# Tu unidad y tus umbrales de la semana 2.
UNIT = "unidad"
LOW = 10.0
HIGH = 50.0
SCALE = Scale(UNIT, LOW, HIGH)

TOP = 3
WINDOW = 3
# Cuántas filas de la tabla y cuántas medias móviles escribe `informe` si no se dice
# otra cosa con --filas. Pintar 100 000 filas con Rich tarda más de 20 segundos.
ROWS = 20
# Tiempo entre dos medidas y tamaño de cada periodo en `evolucion`.
EVERY = "1h"
PERIOD = "1D"
# Cuántos archivos lee `lote` a la vez si no se dice otra cosa con --trabajadores.
WORKERS = 4
# A partir de cuántas desviaciones de la media es atípica una medida en `estadisticas`,
# y en cuántos intervalos reparte su histograma, si no se dice con --umbral e --intervalos.
THRESHOLD = 2.0
BINS = 5
# Cuántos caracteres mide la barra del intervalo con más medidas en el histograma.
BAR = 30
# Segundos entre dos medidas de un mismo archivo en `vigilar`, si no se dice con --intervalo.
INTERVAL = 0.5
# Segundos antes del primer reintento de `descargar`; cada reintento espera el doble.
BACKOFF = 0.5

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


def table_of(series: Series, scale: Scale, rows: int = ROWS) -> Table:
    """Una fila por medida, solo las `rows` primeras: etiqueta, valor y nivel, con su color.

    Si hay más medidas que filas, el pie de la tabla dice cuántas se muestran.
    """
    shown = series.measurements[:rows]
    caption = f"{len(shown)} de {len(series)} medidas" if len(shown) < len(series) else None
    table = Table(title="Medidas", caption=caption)
    table.add_column("Etiqueta")
    table.add_column("Valor", justify="right")
    table.add_column("Nivel")
    for measurement in shown:
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
    filas: Annotated[
        int,
        typer.Option(
            "--filas", "-n", min=0, help="Cuántas filas de la tabla y medias móviles escribe."
        ),
    ] = ROWS,
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
    series, errors = Series.parse(lines)
    for error in errors:
        err.print(f"error: {error}")
    rows = [scale.row(measurement) for measurement in series]
    out.print(table_of(series, scale, filas))
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
        # Las últimas: son las más recientes. [-0:] daría todas, por eso el `if`.
        recent = moving_average(values, WINDOW)[-filas:] if filas else []
        averages = " · ".join(f"{average:.1f}" for average in recent)
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


def stats_table(stats: Stats, unit: str) -> Table:
    """Una fila por número del resumen: cuántas, media, desviación y cuartiles."""
    table = Table(title="Estadísticas")
    table.add_column("Medida")
    table.add_column("Valor", justify="right")
    table.add_row("con valor", str(stats.count))
    table.add_row("sin dato", str(stats.missing))
    for name, value in [
        ("media", stats.mean),
        ("desviación", stats.std),
        ("mínimo", stats.minimum),
        ("Q1", stats.q1),
        ("mediana", stats.median),
        ("Q3", stats.q3),
        ("máximo", stats.maximum),
    ]:
        table.add_row(name, f"{value:.1f} {unit}")
    return table


def histogram_lines(counts: Counts, edges: Floats) -> list[str]:
    """Una línea por intervalo: sus bordes, una barra proporcional y cuántas medidas caen."""
    longest = counts.max()
    return [
        f"{low:6.1f} – {high:6.1f}  {'█' * round(count / longest * BAR):<{BAR}} {count}"
        for low, high, count in zip(edges[:-1], edges[1:], counts, strict=True)
    ]


@app.command()
def estadisticas(
    ruta: Annotated[Path, typer.Argument(metavar="RUTA", help="Un .txt o un .csv de medidas.")],
    umbral: Annotated[
        float,
        typer.Option("--umbral", "-u", min=0, help="Desviaciones a partir de las que es atípica."),
    ] = THRESHOLD,
    intervalos: Annotated[
        int, typer.Option("--intervalos", "-i", min=1, help="Intervalos del histograma.")
    ] = BINS,
) -> None:
    """Resume los valores con NumPy: estadísticas, histograma, atípicas y medias."""
    # Importar aquí: NumPy tarda alrededor de 0,1 s en cargarse, y solo lo usa este comando.
    from observatorio.core import arrays

    try:
        lines = open_file(ruta).lines()
    except DataFileError as problem:
        raise fail(str(problem), 2) from problem
    series, errors = Series.parse(lines)
    for error in errors:
        err.print(f"error: {error}")
    values = arrays.values_array(series)
    stats = arrays.stats_of(values)
    if stats is None:
        out.print("ninguna medida con valor")
    else:
        out.print(stats_table(stats, UNIT))
        counts, edges = arrays.histogram(values, intervalos)
        out.print(
            "\n".join([f"histograma ({intervalos} intervalos):", *histogram_lines(counts, edges)])
        )
        z = arrays.zscores(values)
        found = arrays.outliers(values, umbral)
        atypical = (
            ", ".join(f"{series[i].label} {values[i]:.1f} (z {z[i]:+.1f})" for i in found)
            or "ninguna"
        )
        means = arrays.group_means(arrays.labels_array(series), values)
        out.print(f"atípicas (|z| > {umbral:g}): {atypical}")
        out.print(
            "media por etiqueta: "
            + ", ".join(f"{label} {mean:.1f}" for label, mean in means.items())
        )
    if errors:
        raise typer.Exit(1)


# Los nombres de las columnas y de los índices de las tablas de pandas, en español. La
# clave admite int porque así lo pide `rename_axis` en pandas-stubs.
NAMES: dict[str | int, str] = {
    "position": "posición",
    "label": "etiqueta",
    "value": "valor",
    "level": "nivel",
    "count": "medidas",
    "missing": "faltan",
    "mean": "media",
    "minimum": "mínimo",
    "maximum": "máximo",
    "before": "antes",
    "after": "después",
    "change": "cambio",
    "time": "periodo",
}


def frame_text(frame: pd.DataFrame) -> str:
    """La tabla de pandas con los nombres en español, un decimal y "sin dato" si falta."""
    return (
        frame.rename(columns=NAMES)
        .rename_axis(index=NAMES, columns=NAMES)
        .to_string(na_rep="sin dato", float_format=lambda value: f"{value:.1f}")
    )


@app.command()
def filtrar(
    ruta: Annotated[Path, typer.Argument(metavar="RUTA", help="Un .txt o un .csv de medidas.")],
    etiquetas: Annotated[
        list[str] | None,
        typer.Option("--etiqueta", "-e", help="Solo esta etiqueta; repítela para elegir varias."),
    ] = None,
    desde: Annotated[float | None, typer.Option(help="Solo valores desde este, incluido.")] = None,
    hasta: Annotated[float | None, typer.Option(help="Solo valores hasta este, incluido.")] = None,
    ordenar: Annotated[bool, typer.Option("--ordenar", help="De mayor a menor valor.")] = False,
    filas: Annotated[
        int, typer.Option("--filas", "-n", min=1, help="Cuántas filas escribe, como mucho.")
    ] = ROWS,
    salida: Annotated[
        Path | None,
        typer.Option("--salida", "-o", metavar="CSV", help="Guarda las medidas elegidas."),
    ] = None,
) -> None:
    """Elige medidas con pandas, por etiqueta y por valor; las ordena o las guarda."""
    # Importar aquí, como NumPy en `estadisticas`: pandas tarda en cargarse.
    from observatorio.core import frames

    try:
        lines = open_file(ruta).lines()
    except DataFileError as problem:
        raise fail(str(problem), 2) from problem
    series, errors = Series.parse(lines)
    for error in errors:
        err.print(f"error: {error}")
    frame = frames.with_levels(frames.frame_of(series), SCALE)
    chosen = frames.select(frame, labels=etiquetas or (), low=desde, high=hasta)
    if ordenar:
        chosen = frames.by_value(chosen)
    if chosen.empty:
        out.print("ninguna medida cumple el filtro")
    else:
        out.print(frame_text(chosen.head(filas)))
    if len(chosen) > filas:
        out.print(f"… y {len(chosen) - filas} más (usa --filas para verlas)")
    counts = ", ".join(f"{label} {n}" for label, n in frames.label_counts(chosen).items())
    out.print(f"{len(chosen)} de {len(frame)} medidas" + (f" · {counts}" if counts else ""))
    if salida is not None:
        try:
            frames.write_frame(chosen, salida)
        except OSError as problem:
            raise fail(f"no se pudo guardar {salida}: {problem}", 2) from problem
        out.print(f"guardadas en {salida}")
    if errors:
        raise typer.Exit(1)


def parsed(ruta: Path) -> tuple[Series, list[str]]:
    """La serie de un archivo y sus errores, que escribe en stderr; código 2 si no se lee."""
    try:
        lines = open_file(ruta).lines()
    except DataFileError as problem:
        raise fail(str(problem), 2) from problem
    series, errors = Series.parse(lines)
    for error in errors:
        err.print(f"error: {ruta.name}: {error}")
    return series, errors


@app.command()
def resumir(
    ruta: Annotated[Path, typer.Argument(metavar="RUTA", help="Un .txt o un .csv de medidas.")],
    contra: Annotated[
        Path | None,
        typer.Option("--contra", "-c", metavar="OTRA", help="Compara las medias con otro archivo."),
    ] = None,
) -> None:
    """Resume cada etiqueta con pandas, o compara sus medias con las de otro archivo."""
    # Importar aquí, como en `filtrar`: pandas tarda en cargarse.
    from observatorio.core import frames, summaries

    series, errors = parsed(ruta)
    table = summaries.summary(frames.frame_of(series))
    if contra is None:
        out.print(frame_text(table) if len(table) else "ninguna medida")
        out.print(f"{len(table)} etiquetas · {len(series)} medidas")
    else:
        other, other_errors = parsed(contra)
        errors += other_errors
        changes = summaries.compare(table, summaries.summary(frames.frame_of(other)))
        out.print(frame_text(changes) if len(changes) else "ninguna medida")
        out.print(f"{changes['change'].count()} de {len(changes)} etiquetas en los dos archivos")
    if errors:
        raise typer.Exit(1)


def evolution_of(
    ruta: Path, inicio: datetime, cada: str, periodo: str
) -> tuple[pd.DataFrame, Series, list[str]]:
    """La tabla de summaries.evolution de un archivo, su serie y sus errores, para `evolucion` y
    `graficar`; código 2 si cada o periodo no son duraciones."""
    from observatorio.core import frames, summaries

    try:
        every, period = summaries.duration(cada), summaries.duration(periodo)
    except ValueError as problem:
        raise fail(str(problem), 2) from problem
    series, errors = parsed(ruta)
    table = summaries.evolution(summaries.timed(frames.frame_of(series), inicio, every), period)
    return table, series, errors


@app.command()
def evolucion(
    ruta: Annotated[Path, typer.Argument(metavar="RUTA", help="Un .txt o un .csv de medidas.")],
    inicio: Annotated[
        datetime,
        typer.Option(help="Cuándo se tomó la primera medida, como 2026-11-01T08:00:00."),
    ],
    cada: Annotated[str, typer.Option(help="Tiempo entre dos medidas: 1h, 15min, 1D...")] = EVERY,
    periodo: Annotated[str, typer.Option(help="Tamaño de cada periodo: 3h, 1D, 7D...")] = PERIOD,
    filas: Annotated[
        int, typer.Option("--filas", "-n", min=1, help="Cuántos periodos escribe, como mucho.")
    ] = ROWS,
) -> None:
    """La media de cada etiqueta por periodos de tiempo, con pandas."""
    table, series, errors = evolution_of(ruta, inicio, cada, periodo)
    out.print(frame_text(table.head(filas)) if len(table) else "ninguna medida")
    if len(table) > filas:
        out.print(f"… y {len(table) - filas} más (usa --filas para verlos)")
    out.print(f"{len(table)} periodos · {len(series)} medidas")
    if errors:
        raise typer.Exit(1)


@app.command()
def graficar(
    ruta: Annotated[Path, typer.Argument(metavar="RUTA", help="Un .txt o un .csv de medidas.")],
    salida: Annotated[
        Path, typer.Argument(metavar="SALIDA", help="El gráfico: un .png, un .svg o un .pdf.")
    ],
    inicio: Annotated[
        datetime,
        typer.Option(help="Cuándo se tomó la primera medida, como 2026-11-01T08:00:00."),
    ],
    cada: Annotated[str, typer.Option(help="Tiempo entre dos medidas: 1h, 15min, 1D...")] = EVERY,
    periodo: Annotated[str, typer.Option(help="Tamaño de cada periodo: 3h, 1D, 7D...")] = PERIOD,
) -> None:
    """Dibuja con matplotlib la media de cada etiqueta por periodos, como `evolucion`."""
    # Importar aquí, como en `exportar`: matplotlib tarda en cargarse.
    from observatorio.core import charts

    table, series, errors = evolution_of(ruta, inicio, cada, periodo)
    figure = charts.evolution_figure(table, f"{ruta.name}: media cada {periodo}")
    try:
        charts.save(figure, salida)
    except (OSError, ValueError) as problem:
        # ValueError: una extensión que matplotlib no sabe escribir, como .txt.
        raise fail(f"no se puede escribir {salida}: {problem}", 2) from problem
    out.print(
        f"{len(table.columns)} etiquetas y {len(table)} periodos de {len(series)} medidas"
        f" en {salida.name} · {salida.stat().st_size} bytes"
    )
    if errors:
        raise typer.Exit(1)


@app.command()
def comparar(
    ruta: Annotated[Path, typer.Argument(metavar="RUTA", help="Un .txt o un .csv de medidas.")],
    etiqueta: Annotated[str, typer.Argument(metavar="ETIQUETA", help="La primera etiqueta.")],
    otra: Annotated[str, typer.Argument(metavar="OTRA", help="La etiqueta con la que compara.")],
    confianza: Annotated[
        float, typer.Option(min=0.5, max=0.999, help="Nivel del intervalo: 0.9, 0.95, 0.99...")
    ] = 0.95,
) -> None:
    """Contrasta con SciPy si las medias de dos etiquetas son distintas, o si puede ser azar."""
    # Importar aquí, como en `graficar`: scipy.stats tarda en cargarse.
    from observatorio.core import inference

    series, errors = parsed(ruta)
    first, second = inference.sample(series, etiqueta), inference.sample(series, otra)
    try:
        result = inference.difference(first, second, confianza)
    except ValueError as problem:
        raise fail(f"no se puede comparar {etiqueta} con {otra}: {problem}", 2) from problem
    for label, size, mean, std in zip(
        (etiqueta, otra), result.sizes, result.means, result.stds, strict=True
    ):
        out.print(f"{label}: {size} medidas, media {mean:.2f}, desviación {std:.2f}")
    out.print(
        f"diferencia {etiqueta} - {otra}: {result.difference:.2f},"
        f" IC {confianza * 100:g} %: [{result.low:.2f}, {result.high:.2f}]"
    )
    out.print(f"tamaño del efecto (d de Cohen): {result.effect:.2f}")
    out.print(f"p (Welch): {result.p_welch:.3g} · p (Mann-Whitney): {result.p_ranks:.3g}")
    if errors:
        raise typer.Exit(1)


def cell_text(value: object) -> str:
    """Un valor de Polars o de DuckDB como texto: "sin dato" si falta y un decimal si es float."""
    if value is None:
        return "sin dato"
    return f"{value:.1f}" if isinstance(value, float) else str(value)


def rows_table(columns: list[str], rows: list[tuple[object, ...]]) -> Table:
    """Una tabla de Rich, una fila por tupla, con las columnas que están en NAMES en español."""
    table = Table()
    for column in columns:
        table.add_column(NAMES.get(column, column))
    for row in rows:
        table.add_row(*(cell_text(value) for value in row))
    return table


@app.command()
def exportar(
    ruta: Annotated[Path, typer.Argument(metavar="RUTA", help="Un .txt o un .csv de medidas.")],
    salida: Annotated[
        Path, typer.Argument(metavar="PARQUET", help="El archivo Parquet que escribe.")
    ],
) -> None:
    """Guarda las medidas en Parquet con Polars, y resume lo que guardó."""
    # Importar aquí, como en `filtrar`: Polars y DuckDB tardan en cargarse.
    import polars as pl

    from observatorio.core import columnar

    series, errors = parsed(ruta)
    try:
        columnar.frame_of(series).write_parquet(salida)
    except OSError as problem:
        raise fail(f"no se puede escribir {salida}: {problem}", 2) from problem
    # Resume el archivo, no la tabla en memoria: así se ve lo que de verdad quedó guardado.
    table = columnar.summary(pl.scan_parquet(salida)).collect()
    out.print(rows_table(table.columns, table.rows()) if len(table) else "ninguna medida")
    out.print(f"{len(series)} medidas en {salida.name} · {salida.stat().st_size} bytes")
    if errors:
        raise typer.Exit(1)


@app.command()
def sql(
    parquet: Annotated[
        Path, typer.Argument(metavar="PARQUET", help="Un archivo escrito por `exportar`.")
    ],
    consulta: Annotated[
        str, typer.Argument(metavar="CONSULTA", help="SQL sobre la tabla medidas (label, value).")
    ],
    filas: Annotated[
        int, typer.Option("--filas", "-n", min=1, help="Cuántas filas escribe, como mucho.")
    ] = ROWS,
) -> None:
    """Pregunta con SQL (DuckDB) a un archivo Parquet, que se llama medidas."""
    import duckdb

    from observatorio.core import columnar

    try:
        columns, rows = columnar.query(parquet, consulta)
    except duckdb.Error as problem:
        raise fail(str(problem), 2) from problem
    out.print(rows_table(columns, rows[:filas]))
    if len(rows) > filas:
        out.print(f"… y {len(rows) - filas} más (usa --filas para verlas)")
    out.print(f"{len(rows)} filas")


def files_table(reports: list[FileReport]) -> Table:
    """Una fila por archivo leído: ruta, medidas, medidas con valor y media."""
    table = Table(title="Archivos")
    table.add_column("Archivo")
    table.add_column("Medidas", justify="right")
    table.add_column("Con valor", justify="right")
    table.add_column("Media", justify="right")
    for report in reports:
        mean = "sin dato" if report.mean is None else f"{report.mean:.1f} {UNIT}"
        table.add_row(str(report.path), str(report.measurements), str(report.with_value), mean)
    return table


@app.command()
def lote(
    archivos: Annotated[
        list[Path], typer.Argument(metavar="ARCHIVOS", help="Los .txt o .csv que se resumen.")
    ],
    trabajadores: Annotated[
        int,
        typer.Option("--trabajadores", "-t", min=1, help="Cuántos archivos se leen a la vez."),
    ] = WORKERS,
    procesos: Annotated[
        bool, typer.Option("--procesos", help="Reparte los archivos entre procesos, no hilos.")
    ] = False,
) -> None:
    """Resume varios archivos a la vez: una fila por archivo."""
    show_reports(report_files(archivos, workers=trabajadores, processes=procesos))


def show_reports(reports: list[FileReport]) -> None:
    """Los errores a stderr, la tabla de los archivos leídos y el total; código 1 si falló alguno."""
    failed = [report for report in reports if report.error is not None]
    for report in failed:
        err.print(f"error: {report.error}")
    out.print(files_table([report for report in reports if report.error is None]))
    out.print(f"archivos: {len(reports)} · con error: {len(failed)}")
    if failed:
        raise typer.Exit(1)


def show_reading(path: Path, measurement: Measurement) -> None:
    """Una línea por medida en cuanto llega: archivo, etiqueta, valor y nivel con su color."""
    line = Text(f"{path} · {measurement.label}: ")
    if measurement.value is None:
        line.append("sin dato")
    else:
        level = SCALE.level(measurement.value)
        line.append(f"{measurement.value:.1f} {UNIT} ")
        line.append(level, style=STYLES.get(level, ""))
    out.print(line)


@app.command()
def vigilar(
    archivos: Annotated[
        list[Path], typer.Argument(metavar="ARCHIVOS", help="Los .txt o .csv que se vigilan.")
    ],
    intervalo: Annotated[
        float,
        typer.Option("--intervalo", "-i", min=0, help="Segundos entre dos medidas de un archivo."),
    ] = INTERVAL,
    limite: Annotated[
        int, typer.Option("--limite", "-l", min=1, help="Cuántos archivos se vigilan a la vez.")
    ] = WORKERS,
    tiempo: Annotated[
        float | None,
        typer.Option("--tiempo", min=0, help="Para a los SEGUNDOS indicados.", metavar="SEGUNDOS"),
    ] = None,
) -> None:
    """Reproduce varios archivos a la vez, como si las medidas llegaran en directo."""

    async def watch() -> list[FileReport]:
        # timeout(None) no pone límite: la misma línea sirve con y sin --tiempo.
        async with asyncio.timeout(tiempo):
            return await watch_files(
                archivos, interval=intervalo, limit=limite, on_reading=show_reading
            )

    try:
        reports = asyncio.run(watch())
    except TimeoutError:
        raise fail(f"tiempo agotado a los {tiempo:g} s", 1) from None
    show_reports(reports)


def read_settings() -> Settings:
    """La configuración de OBSERVATORIO_* y .env; si no es válida, sale con código 2."""
    try:
        return Settings()
    except ValidationError as problem:
        first = problem.errors()[0]
        name = f"OBSERVATORIO_{str(first['loc'][0]).upper()}"
        raise fail(f"configuración no válida: {name}: {first['msg']}", 2) from None


@app.command()
def descargar(
    urls: Annotated[
        list[str], typer.Argument(metavar="URLS", help="Las URLs de los JSON de medidas.")
    ],
    carpeta: Annotated[
        Path, typer.Option("--carpeta", "-c", help="Dónde se guardan los .txt descargados.")
    ] = Path("descargas"),
    limite: Annotated[
        int, typer.Option("--limite", "-l", min=1, help="Cuántas URLs se descargan a la vez.")
    ] = WORKERS,
) -> None:
    """Baja JSON de medidas por HTTP, los valida y los guarda como .txt.

    Lee OBSERVATORIO_TOKEN, OBSERVATORIO_TIMEOUT y OBSERVATORIO_RETRIES del entorno o de .env.
    """
    for url in urls:
        if not url.startswith(("http://", "https://")):
            raise typer.BadParameter(
                f"{url!r} no empieza por http:// ni https://", param_hint="URLS"
            )
    settings = read_settings()
    token = None if settings.token is None else settings.token.get_secret_value()
    try:
        carpeta.mkdir(parents=True, exist_ok=True)
    except OSError as problem:
        raise fail(f"no se pudo crear {carpeta}: {problem.strerror}", 2) from problem

    async def fetch() -> list[FileReport]:
        # `async with` cierra las conexiones del cliente al terminar, haya error o no.
        async with make_client(token=token, timeout=settings.timeout) as client:
            return await download_all(
                client, urls, carpeta, limit=limite, retries=settings.retries, backoff=BACKOFF
            )

    show_reports(asyncio.run(fetch()))


def database_url() -> str:
    """La URL de OBSERVATORIO_DATABASE_URL; si falta o no es válida, sale con código 2."""
    settings = read_settings()
    if settings.database_url is None:
        raise fail("falta OBSERVATORIO_DATABASE_URL (en el entorno o en .env)", 2)
    url = settings.database_url.get_secret_value()
    try:
        # get_dialect: también falla si el tipo de base no existe (nada://...).
        make_url(url).get_dialect()
    except ArgumentError:
        raise fail("OBSERVATORIO_DATABASE_URL no es una URL de base de datos válida", 2) from None
    return url


@contextmanager
def database() -> Iterator[Session]:
    """Una sesión con la base de OBSERVATORIO_DATABASE_URL, que se cierra al salir.

    Los problemas de configuración o de conexión salen con código 2 y un mensaje sin la
    contraseña; los demás errores de la base de datos llegan como siempre.
    """
    url = database_url()
    engine = make_engine(url)
    try:
        with Session(engine) as session:
            yield session
    except OperationalError:
        # Solo el servidor y el puerto: el texto del error podría llevar el usuario.
        where = make_url(url)
        raise fail(f"no se pudo conectar con PostgreSQL en {where.host}:{where.port}", 2) from None
    except ProgrammingError as problem:
        if isinstance(problem.orig, UndefinedTable):
            raise fail("faltan las tablas: ejecuta `uv run alembic upgrade head`", 2) from None
        raise
    finally:
        # Cierra las conexiones del pool: la CLI termina enseguida y no las reutiliza.
        engine.dispose()


@app.command()
def guardar(
    archivos: Annotated[
        list[Path], typer.Argument(metavar="ARCHIVOS", help="Los .txt o .csv que se guardan.")
    ],
) -> None:
    """Guarda cada archivo en PostgreSQL como una carga nueva, en su propia transacción.

    Lee OBSERVATORIO_DATABASE_URL del entorno o de .env.
    """
    failed = 0
    with database() as session:
        for path in archivos:
            try:
                series = Series.from_lines(open_file(path).lines())
            except DataFileError as problem:
                err.print(f"error: {problem}")
                failed += 1
                continue
            load_id = save_series(session, str(path), series).id
            # Un commit por archivo: si el siguiente falla, este ya está guardado.
            session.commit()
            out.print(f"carga {load_id}: {path}, {len(series)} medidas")
    if failed:
        raise typer.Exit(1)


@app.command()
def cargas() -> None:
    """Lista las cargas guardadas: número, origen, fecha y medidas."""
    with database() as session:
        loads = list_loads(session)
    if not loads:
        out.print("no hay cargas: guarda una con `observatorio guardar`")
        return
    table = Table(title="Cargas")
    table.add_column("Carga", justify="right")
    table.add_column("Origen")
    table.add_column("Fecha")
    table.add_column("Medidas", justify="right")
    for load in loads:
        date = f"{load.created_at:%Y-%m-%d %H:%M}"
        table.add_row(str(load.id), load.source, date, str(load.measurements))
    out.print(table)


@app.command()
def consultar(
    carga: Annotated[
        int | None, typer.Option("--carga", "-c", help="Solo las medidas de esta carga.")
    ] = None,
) -> None:
    """Resume por etiqueta las medidas guardadas: PostgreSQL agrupa, cuenta y promedia."""
    with database() as session:
        if carga is not None and session.get(Load, carga) is None:
            raise fail(f"no existe la carga {carga}", 1)
        stats = label_stats(session, carga)
    table = Table(title="Etiquetas")
    table.add_column("Etiqueta")
    table.add_column("Medidas", justify="right")
    table.add_column("Con valor", justify="right")
    table.add_column("Media", justify="right")
    for row in stats:
        mean = "sin dato" if row.mean is None else f"{row.mean:.1f} {UNIT}"
        table.add_row(row.label, str(row.measurements), str(row.with_value), mean)
    out.print(table)


@app.command()
def extraer(
    salida: Annotated[Path, typer.Argument(metavar="SALIDA", help="El CSV que escribe.")],
    carga: Annotated[
        int | None, typer.Option("--carga", "-c", help="Solo las medidas de esta carga.")
    ] = None,
) -> None:
    """Extrae de PostgreSQL las medidas guardadas y escribe una instantánea CSV con su nivel.

    Lee OBSERVATORIO_DATABASE_URL del entorno o de .env.
    """
    # Importar aquí, como en `filtrar`: pandas tarda en cargarse.
    from observatorio.core import etl

    with database() as session:
        if carga is not None and session.get(Load, carga) is None:
            raise fail(f"no existe la carga {carga}", 1)
        frame = etl.extract(session.connection(), carga)
    if frame.empty:
        raise fail("no hay medidas que extraer: guarda una carga con `observatorio guardar`", 1)
    snapshot = etl.transform(frame, SCALE)
    try:
        digest = etl.write_snapshot(snapshot, salida)
    except OSError as problem:
        raise fail(f"no se puede escribir {salida}: {problem}", 2) from problem
    loads = snapshot["carga"].nunique()
    out.print(f"{salida.name}: {len(snapshot)} medidas · cargas: {loads}")
    out.print(f"sha256: {digest}")


@app.command()
def hallazgos(
    instantanea: Annotated[
        Path, typer.Argument(metavar="INSTANTANEA", help="El CSV que escribió `extraer`.")
    ],
    carpeta: Annotated[
        Path, typer.Argument(metavar="CARPETA", help="Donde escribe el informe y la figura.")
    ],
    huella: Annotated[
        str | None, typer.Option(help="La huella SHA-256 que debe tener la instantánea.")
    ] = None,
    confianza: Annotated[
        float, typer.Option(min=0.5, max=0.999, help="Nivel de los intervalos: 0.9, 0.95...")
    ] = 0.95,
    alfa: Annotated[
        float,
        typer.Option(min=0.001, max=0.5, help="Umbral del p corregido para decir que difieren."),
    ] = 0.05,
) -> None:
    """Compara cada par de etiquetas de una instantánea y escribe el informe de hallazgos."""
    # Importar aquí, como en `comparar`: pandas, scipy y matplotlib tardan en cargarse.
    from observatorio.core import charts, findings

    try:
        frame, digest = findings.read_snapshot(instantanea, huella)
        found = findings.compare_all(frame, confianza)
    except OSError as problem:
        raise fail(f"no se puede leer {instantanea}: {problem}", 2) from problem
    except ValueError as problem:
        raise fail(str(problem), 1) from problem
    report = findings.render(
        frame, found, name=instantanea.name, digest=digest, confidence=confianza, alpha=alfa
    )
    try:
        carpeta.mkdir(parents=True, exist_ok=True)
        charts.save(findings.differences_figure(found, UNIT, alfa), carpeta / findings.FIGURE)
        (carpeta / findings.REPORT).write_text(report, encoding="utf-8")
    except OSError as problem:
        raise fail(f"no se puede escribir en {carpeta}: {problem}", 2) from problem
    out.print(f"{instantanea.name}: {len(frame)} medidas · sha256: {digest}")
    out.print(findings.headline(found, alfa))
    out.print(f"informe: {carpeta / findings.REPORT} · figura: {carpeta / findings.FIGURE}")


def evaluation_table(evaluation: Evaluation) -> Table:
    """Una fila por métrica: el modelo, la referencia y si el modelo la mejora."""
    table = Table(
        title=f"{evaluation.task} · {evaluation.train_size} para entrenar,"
        f" {evaluation.test_size} para probar"
    )
    table.add_column("Métrica")
    table.add_column("Modelo", justify="right")
    table.add_column("Referencia", justify="right")
    table.add_column("¿Mejora?")
    for score in evaluation.scores:
        table.add_row(
            score.name,
            f"{score.model:.3f}",
            f"{score.baseline:.3f}",
            "sí" if score.improves else "no",
        )
    return table


@app.command()
def modelo(
    instantanea: Annotated[
        Path, typer.Argument(metavar="INSTANTANEA", help="El CSV que escribió `extraer`.")
    ],
    huella: Annotated[
        str | None, typer.Option(help="La huella SHA-256 que debe tener la instantánea.")
    ] = None,
    prueba: Annotated[
        float,
        typer.Option(min=0.1, max=0.5, help="Parte de las medidas que se aparta para probar."),
    ] = 0.25,
    semilla: Annotated[int, typer.Option(help="La semilla del reparto: la misma, el mismo.")] = 31,
) -> None:
    """Entrena una regresión y una clasificación con la etiqueta, y las compara con una referencia."""
    # Importar aquí: scikit-learn tarda en cargarse, y el resto de comandos no lo usa.
    from observatorio.core import findings, learning

    try:
        frame, digest = findings.read_snapshot(instantanea, huella)
        evaluations = [
            learning.regress(frame, prueba, semilla),
            learning.classify(frame, prueba, semilla),
        ]
    except OSError as problem:
        raise fail(f"no se puede leer {instantanea}: {problem}", 2) from problem
    except ValueError as problem:
        raise fail(str(problem), 1) from problem
    out.print(f"{instantanea.name}: {len(frame)} medidas · sha256: {digest}")
    for evaluation in evaluations:
        out.print(evaluation_table(evaluation))
        verdict = "mejora" if evaluation.improves else "no mejora"
        out.print(f"{evaluation.task}: el modelo {verdict} la referencia")


def cross_validation_table(validation: CrossValidation) -> Table:
    """Una fila por pliegue y otra con la media: el modelo, la referencia y quién gana."""
    table = Table(title=f"{validation.task} · {validation.metric} en cada pliegue")
    table.add_column("Pliegue", justify="right")
    table.add_column("Modelo", justify="right")
    table.add_column("Referencia", justify="right")
    table.add_column("¿Mejora?")
    rows = zip(validation.model, validation.baseline, validation.beats, strict=True)
    for number, (model, baseline, beats) in enumerate(rows, start=1):
        table.add_row(str(number), f"{model:.3f}", f"{baseline:.3f}", "sí" if beats else "no")
    model_mean = sum(validation.model) / len(validation.model)
    baseline_mean = sum(validation.baseline) / len(validation.baseline)
    table.add_row("media", f"{model_mean:.3f}", f"{baseline_mean:.3f}", "", style="bold")
    return table


@app.command()
def ajustar(
    instantanea: Annotated[
        Path, typer.Argument(metavar="INSTANTANEA", help="El CSV que escribió `extraer`.")
    ],
    huella: Annotated[
        str | None, typer.Option(help="La huella SHA-256 que debe tener la instantánea.")
    ] = None,
    pliegues: Annotated[int, typer.Option(min=2, max=10, help="En cuántas partes se reparte.")] = 5,
    tiempo: Annotated[
        bool, typer.Option(help="Pliegues por tiempo: cada prueba, después de su entrenamiento.")
    ] = False,
) -> None:
    """Ajusta la regresión y la clasificación, y las valida por pliegues frente a una referencia."""
    # Importar aquí: scikit-learn tarda en cargarse, y el resto de comandos no lo usa.
    from observatorio.core import findings, validation

    try:
        frame, digest = findings.read_snapshot(instantanea, huella)
        validations = [
            validation.validate(frame, "valor", pliegues, tiempo),
            validation.validate(frame, "nivel", pliegues, tiempo),
        ]
    except OSError as problem:
        raise fail(f"no se puede leer {instantanea}: {problem}", 2) from problem
    except ValueError as problem:
        raise fail(str(problem), 1) from problem
    order = "por tiempo" if tiempo else "al azar"
    out.print(f"{instantanea.name}: {len(frame)} medidas · sha256: {digest} · pliegues {order}")
    for result in validations:
        out.print(cross_validation_table(result))
        params = ", ".join(f"{name}={value:g}" for name, value in result.params.items())
        verdict = "mejora" if result.improves else "no mejora"
        out.print(
            f"{result.task}: con {params}, gana en {sum(result.beats)} de {len(result.model)}"
            f" pliegues: el modelo {verdict} la referencia"
        )


def contest_table(contest: Contest) -> Table:
    """Una fila por modelo: la métrica en cada pliegue, la media y en cuántos gana a la
    referencia."""
    folds = len(next(iter(contest.scores.values())))
    table = Table(title=f"{contest.task} · {contest.metric} en cada pliegue")
    table.add_column("Modelo")
    for number in range(1, folds + 1):
        table.add_column(str(number), justify="right")
    table.add_column("Media", justify="right")
    table.add_column("Gana", justify="right")
    wins = contest.wins
    for name, scores in contest.scores.items():
        won = f"{wins[name]} de {folds}" if name in wins else ""
        cells = [f"{score:.3f}" for score in scores]
        table.add_row(name, *cells, f"{contest.means[name]:.3f}", won)
    return table


@app.command()
def competir(
    instantanea: Annotated[
        Path, typer.Argument(metavar="INSTANTANEA", help="El CSV que escribió `extraer`.")
    ],
    huella: Annotated[
        str | None, typer.Option(help="La huella SHA-256 que debe tener la instantánea.")
    ] = None,
    pliegues: Annotated[int, typer.Option(min=2, max=10, help="En cuántas partes se reparte.")] = 5,
    tiempo: Annotated[
        bool, typer.Option(help="Pliegues por tiempo: cada prueba, después de su entrenamiento.")
    ] = False,
) -> None:
    """Compara la referencia, el modelo lineal, un árbol, un bosque y un boosting, pliegue a
    pliegue."""
    # Importar aquí: scikit-learn tarda en cargarse, y el resto de comandos no lo usa.
    from observatorio.core import ensembles, findings

    try:
        frame, digest = findings.read_snapshot(instantanea, huella)
        contests = [
            ensembles.compete(frame, "valor", pliegues, tiempo),
            ensembles.compete(frame, "nivel", pliegues, tiempo),
        ]
    except OSError as problem:
        raise fail(f"no se puede leer {instantanea}: {problem}", 2) from problem
    except ValueError as problem:
        raise fail(str(problem), 1) from problem
    order = "por tiempo" if tiempo else "al azar"
    out.print(f"{instantanea.name}: {len(frame)} medidas · sha256: {digest} · pliegues {order}")
    for contest in contests:
        out.print(contest_table(contest))
        best = contest.best
        if best == ensembles.BASELINE:
            out.print(f"{contest.task}: ningún modelo mejora la media de la referencia")
            continue
        verdict = "mejora" if contest.improves else "no mejora"
        out.print(
            f"{contest.task}: el mejor es {best}, gana en {contest.wins[best]} de"
            f" {pliegues} pliegues: {verdict} la referencia"
        )


def clustering_table(frame: pd.DataFrame, clustering: Clustering) -> Table:
    """Una fila por etiqueta: su grupo y su perfil."""
    table = Table(title="Grupos de etiquetas")
    for name in ("Etiqueta", "Grupo", "Media", "Mediana", "Desviación"):
        table.add_column(name, justify="left" if name == "Etiqueta" else "right")
    for label, row in frame.iterrows():
        table.add_row(
            str(label),
            str(clustering.groups[str(label)]),
            f"{row['media']:.1f}",
            f"{row['mediana']:.1f}",
            f"{row['desviacion']:.1f}",
        )
    return table


@app.command()
def agrupar(
    instantanea: Annotated[
        Path, typer.Argument(metavar="INSTANTANEA", help="El CSV que escribió `extraer`.")
    ],
    huella: Annotated[
        str | None, typer.Option(help="La huella SHA-256 que debe tener la instantánea.")
    ] = None,
    grupos: Annotated[
        int, typer.Option("--grupos", "-g", min=2, help="En cuántos grupos se reparten.")
    ] = 2,
) -> None:
    """Agrupa las etiquetas que se parecen con KMeans, y mide con la silueta si se separan."""
    # Importar aquí: scikit-learn tarda en cargarse, y el resto de comandos no lo usa.
    from observatorio.core import clustering, findings

    try:
        frame, digest = findings.read_snapshot(instantanea, huella)
        result = clustering.cluster(frame, grupos)
    except OSError as problem:
        raise fail(f"no se puede leer {instantanea}: {problem}", 2) from problem
    except ValueError as problem:
        raise fail(str(problem), 1) from problem
    out.print(f"{instantanea.name}: {len(frame)} medidas · sha256: {digest}")
    out.print(clustering_table(clustering.profiles(frame), result))
    verdict = "grupos separados" if result.separated else "grupos que se solapan"
    out.print(f"{grupos} grupos · silueta {result.silhouette:.2f}: {verdict}")


def loss_table(losses: tuple[float, ...], title: str) -> Table:
    """La pérdida en seis épocas como mucho: la primera, unas repartidas y la última."""
    epochs = len(losses)
    # ceil: con 13 épocas, cada 3 (1, 4, 7, 10 y 13); con epochs // 5, cada 2, y saldrían 7.
    shown = sorted({*range(0, epochs, math.ceil(epochs / 5)), epochs - 1})
    table = Table(title=title)
    table.add_column("Época", justify="right")
    table.add_column("Pérdida", justify="right")
    for index in shown:
        table.add_row(str(index + 1), f"{losses[index]:.4f}")
    return table


@app.command()
def red(
    instantanea: Annotated[
        Path, typer.Argument(metavar="INSTANTANEA", help="El CSV que escribió `extraer`.")
    ],
    huella: Annotated[
        str | None, typer.Option(help="La huella SHA-256 que debe tener la instantánea.")
    ] = None,
    oculta: Annotated[int, typer.Option(min=1, help="Neuronas de la capa oculta.")] = 16,
    epocas: Annotated[
        int, typer.Option(min=1, max=10_000, help="Pasadas por todo el entrenamiento.")
    ] = 300,
    ritmo: Annotated[
        float, typer.Option(min=0.0001, max=1.0, help="El ritmo de aprendizaje de Adam.")
    ] = 0.01,
    semilla: Annotated[
        int, typer.Option(help="La semilla del reparto y de los pesos: la misma, la misma red.")
    ] = 31,
) -> None:
    """Entrena una red neuronal pequeña que predice el valor, y la compara con la referencia."""
    # Importar aquí: PyTorch tarda aún más que scikit-learn en cargarse.
    from observatorio.core import findings, neural

    try:
        frame, digest = findings.read_snapshot(instantanea, huella)
        training = neural.learn(frame, oculta, epocas, ritmo, semilla)
    except OSError as problem:
        raise fail(f"no se puede leer {instantanea}: {problem}", 2) from problem
    except ValueError as problem:
        raise fail(str(problem), 1) from problem
    out.print(f"{instantanea.name}: {len(frame)} medidas · sha256: {digest}")
    out.print(
        f"red de {oculta} neuronas ocultas y {training.parameters} parámetros"
        f" · {epocas} épocas · ritmo {ritmo}"
    )
    out.print(loss_table(training.losses, "Pérdida en entrenamiento (MSE del valor escalado)"))
    if not training.learned:
        out.print("la pérdida no bajó: prueba otro --ritmo o más --epocas")
    verdict = "mejora" if training.improves else "no mejora"
    out.print(
        f"regresión del valor · MAE en prueba: red {training.mae:.3f}"
        f" · referencia {training.baseline:.3f}: la red {verdict} la referencia"
    )


@app.command()
def pronosticar(
    instantanea: Annotated[
        Path, typer.Argument(metavar="INSTANTANEA", help="El CSV que escribió `extraer`.")
    ],
    huella: Annotated[
        str | None, typer.Option(help="La huella SHA-256 que debe tener la instantánea.")
    ] = None,
    etiqueta: Annotated[
        str | None, typer.Option(help="Solo la serie de esta etiqueta; sin ella, todas.")
    ] = None,
    ventana: Annotated[
        int, typer.Option(min=3, max=100, help="Cuántos valores anteriores mira la red.")
    ] = 8,
    epocas: Annotated[int, typer.Option(min=1, max=1000, help="Épocas como máximo.")] = 100,
    paciencia: Annotated[
        int, typer.Option(min=1, help="Épocas sin mejorar en validación antes de parar.")
    ] = 10,
    semilla: Annotated[
        int, typer.Option(help="La semilla de los pesos y de los lotes: la misma, la misma red.")
    ] = 31,
    guardar: Annotated[
        Path | None, typer.Option(help="El archivo en el que guardar los pesos de la red.")
    ] = None,
    desde: Annotated[
        Path | None,
        typer.Option(help="Los pesos de otra red: congela sus filtros y reentrena la salida."),
    ] = None,
) -> None:
    """Entrena una red convolucional que pronostica cada valor con los anteriores."""
    # Importar aquí: PyTorch tarda en cargarse. pickle, para el error de un archivo de pesos
    # que trae algo más que pesos.
    import pickle

    from observatorio.core import convolution, findings

    start = None
    try:
        frame, digest = findings.read_snapshot(instantanea, huella)
        if desde is not None:
            # La ventana es la de la red guardada: sus capas tienen ese tamaño.
            start, ventana = convolution.load(desde)
        result, model = convolution.forecast(
            frame, ventana, epocas, paciencia, semilla, etiqueta, start
        )
        if guardar is not None:
            convolution.save(model, ventana, guardar)
    except OSError as problem:
        raise fail(f"no se puede usar {problem.filename}: {problem.strerror}", 2) from problem
    except pickle.UnpicklingError as problem:
        raise fail(f"{desde} no es un archivo de pesos: weights_only no lo carga", 2) from problem
    except ValueError as problem:
        raise fail(str(problem), 1) from problem
    train, validation, test = result.sizes
    out.print(f"{instantanea.name}: {len(frame)} medidas · sha256: {digest}")
    out.print(
        f"serie de {etiqueta or 'todas las etiquetas'} · ventanas de {ventana} valores"
        f" · {train} para entrenar, {validation} para validar, {test} para prueba"
    )
    origin = "filtros congelados de " + desde.name if desde else "desde cero"
    out.print(
        f"red convolucional, {origin} · {result.parameters} parámetros,"
        f" {result.trainable} entrenables"
    )
    out.print(loss_table(result.losses, "Pérdida en validación (MSE del valor escalado)"))
    epochs = len(result.losses)
    stop = f"paró en la época {epochs}" if epochs < epocas else f"entrenó {epochs} épocas"
    out.print(
        f"{stop}; se queda con la {result.best + 1}, pérdida {result.losses[result.best]:.4f}"
    )
    verdict = "mejora" if result.improves else "no mejora"
    out.print(
        f"pronóstico del siguiente valor · MAE en prueba: red {result.mae:.3f}"
        f" · referencia {result.baseline:.3f}: la red {verdict} la referencia"
    )
    if guardar is not None:
        out.print(f"pesos guardados en {guardar}")


@app.command()
def borrar(
    carga: Annotated[int, typer.Argument(metavar="CARGA", help="El número de la carga.")],
) -> None:
    """Borra una carga y todas sus medidas."""
    with database() as session:
        if not delete_load(session, carga):
            raise fail(f"no existe la carga {carga}", 1)
        session.commit()
    out.print(f"carga {carga} borrada")


@app.command()
def servir(
    host: Annotated[
        str, typer.Option("--host", help="La dirección en la que escucha; 0.0.0.0 en Docker.")
    ] = "127.0.0.1",
    puerto: Annotated[
        int, typer.Option("--puerto", "-p", min=1, max=65535, help="El puerto en el que escucha.")
    ] = 8000,
) -> None:
    """Sirve la API HTTP con uvicorn hasta Ctrl+C. La documentación, en /docs.

    Lee OBSERVATORIO_DATABASE_URL del entorno o de .env.
    """
    url = database_url()
    # Importar aquí: FastAPI y uvicorn solo se cargan al servir, no en cada comando.
    import uvicorn

    from observatorio.api import create_app

    uvicorn.run(create_app(url), host=host, port=puerto)
