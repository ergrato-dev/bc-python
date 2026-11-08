"""La línea de comandos del Observatorio: informes, archivos, HTTP y PostgreSQL.

Qué: una aplicación Typer con nueve comandos (`informe`, `validar`, `lote`, `vigilar`,
`descargar`, `guardar`, `cargas`, `consultar` y `borrar`); Rich escribe las tablas y los errores.
Para qué: Typer lee los argumentos a partir de las anotaciones de cada función, y
genera la ayuda y los errores de uso; tú solo escribes qué hace cada comando.
Impacto: es la única parte del Observatorio que toca la terminal. El paquete `core`
no sabe que existe, y la API de la semana 20 lo usará igual que este archivo.
"""

import asyncio
import logging
import sys
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Annotated

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
    process_lines,
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

# Tu unidad y tus umbrales de la semana 2.
UNIT = "unidad"
LOW = 10.0
HIGH = 50.0
SCALE = Scale(UNIT, LOW, HIGH)

TOP = 3
WINDOW = 3
# Cuántos archivos lee `lote` a la vez si no se dice otra cosa con --trabajadores.
WORKERS = 4
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


@contextmanager
def database() -> Iterator[Session]:
    """Una sesión con la base de OBSERVATORIO_DATABASE_URL, que se cierra al salir.

    Los problemas de configuración o de conexión salen con código 2 y un mensaje sin la
    contraseña; los demás errores de la base de datos llegan como siempre.
    """
    settings = read_settings()
    if settings.database_url is None:
        raise fail("falta OBSERVATORIO_DATABASE_URL (en el entorno o en .env)", 2)
    url = settings.database_url.get_secret_value()
    try:
        engine = make_engine(url)
    except ArgumentError:
        raise fail("OBSERVATORIO_DATABASE_URL no es una URL de base de datos válida", 2) from None
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
def borrar(
    carga: Annotated[int, typer.Argument(metavar="CARGA", help="El número de la carga.")],
) -> None:
    """Borra una carga y todas sus medidas."""
    with database() as session:
        if not delete_load(session, carga):
            raise fail(f"no existe la carga {carga}", 1)
        session.commit()
    out.print(f"carga {carga} borrada")
