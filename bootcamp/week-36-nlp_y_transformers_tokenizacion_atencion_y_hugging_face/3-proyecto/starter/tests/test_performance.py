"""Tests del rendimiento (semana 22): cuánto trabajo hace `informe`, no cuánto tarda.

Un test que mide segundos falla en una máquina lenta o cargada aunque el código esté bien.
Estos cuentan el trabajo con cProfile: cuántas filas pinta la tabla y cuántas veces se
analiza cada línea. Ese número no depende de la máquina, y crece si alguien vuelve a
pintar 100 000 filas o a leer cada línea dos veces.
"""

import cProfile
import pstats
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path

from hypothesis import given
from hypothesis import strategies as st
from rich.table import Table
from typer.testing import CliRunner, Result

from observatorio import cli
from observatorio.core import Scale, Series, parse_record, process_lines

runner = CliRunner()

LINES = ["Norte;12,5", "Sur;8", "Oriente;55,1", "Norte;48,9"]
SCALE = Scale("u", 10.0, 50.0)
ROOT = Path(__file__).resolve().parent.parent


def lines_of(count: int) -> list[str]:
    """count líneas válidas, con valores que suben de 1 en 1: "L0;0", "L1;1"..."""
    return [f"L{number};{number}" for number in range(count)]


def calls_of(profiler: cProfile.Profile, function: Callable[..., object]) -> int:
    """Cuántas veces llamó el programa perfilado a function, según cProfile.

    pstats identifica cada función por (archivo, primera línea, nombre): los tres salen
    de su código, así que da igual con qué nombre la importó cada módulo.
    """
    code = function.__code__
    key = (code.co_filename, code.co_firstlineno, code.co_name)
    stats = pstats.Stats(profiler).stats  # type: ignore[attr-defined]
    return int(stats[key][1]) if key in stats else 0


def profiled_informe(args: list[str]) -> tuple[Result, cProfile.Profile]:
    """Ejecuta `observatorio informe args` dentro de cProfile y devuelve el resultado."""
    profiler = cProfile.Profile()
    result = profiler.runcall(runner.invoke, cli.app, ["informe", *args])
    return result, profiler


def table_rows(output: str) -> int:
    """Las filas de datos de la tabla: las que empiezan por "│" (los títulos llevan "┃")."""
    return sum(line.startswith("│") for line in output.splitlines())


# --- la tabla limitada ---


def test_twenty_rows_by_default() -> None:
    assert cli.ROWS == 20


def test_informe_shows_at_most_twenty_rows() -> None:
    result = runner.invoke(cli.app, ["informe", *lines_of(25)])
    assert result.exit_code == 0
    assert table_rows(result.stdout) == 20


def test_informe_says_how_many_rows_it_shows() -> None:
    result = runner.invoke(cli.app, ["informe", *lines_of(25)])
    assert "20 de 25 medidas" in result.stdout


def test_informe_shows_the_first_rows() -> None:
    result = runner.invoke(cli.app, ["informe", *lines_of(25)])
    assert "L19" in result.stdout
    assert "L20" not in result.stdout


def test_informe_says_nothing_when_every_row_fits() -> None:
    result = runner.invoke(cli.app, ["informe", *lines_of(20)])
    assert table_rows(result.stdout) == 20
    assert " de 20 medidas" not in result.stdout


def test_informe_rows_option() -> None:
    result = runner.invoke(cli.app, ["informe", "--filas", "2", *LINES])
    assert table_rows(result.stdout) == 2
    assert "2 de 4 medidas" in result.stdout


def test_informe_rows_short_option() -> None:
    result = runner.invoke(cli.app, ["informe", "-n", "3", *LINES])
    assert table_rows(result.stdout) == 3


def test_informe_zero_rows_keeps_the_summary() -> None:
    result = runner.invoke(cli.app, ["informe", "-n", "0", *LINES])
    assert result.exit_code == 0
    assert table_rows(result.stdout) == 0
    assert "0 de 4 medidas" in result.stdout
    assert "mediana: 30.7 unidad" in result.stdout


def test_informe_rejects_negative_rows() -> None:
    result = runner.invoke(cli.app, ["informe", "-n", "-1", *LINES])
    assert result.exit_code == 2


def test_informe_help_mentions_rows() -> None:
    result = runner.invoke(cli.app, ["informe", "--help"])
    assert "--filas" in result.stdout


def test_moving_average_shows_the_last_ones() -> None:
    # Valores 0..9 con ventana 3: medias 1, 2, ..., 8. Con -n 2, las dos últimas.
    result = runner.invoke(cli.app, ["informe", "-n", "2", *lines_of(10)])
    assert "media móvil (3): 7.0 · 8.0\n" in result.stdout


def test_moving_average_with_zero_rows_is_empty() -> None:
    result = runner.invoke(cli.app, ["informe", "-n", "0", *lines_of(10)])
    assert "media móvil (3):" in result.stdout
    assert "1.0 · 2.0" not in result.stdout


def test_table_of_limits_the_rows() -> None:
    table = cli.table_of(Series.from_lines(LINES), SCALE, 2)
    assert table.row_count == 2
    assert table.caption == "2 de 4 medidas"


def test_table_of_has_no_caption_when_everything_fits() -> None:
    table = cli.table_of(Series.from_lines(LINES), SCALE, 4)
    assert table.row_count == 4
    assert table.caption is None


# --- el trabajo que hace informe ---


def test_informe_adds_only_the_rows_it_shows() -> None:
    result, profiler = profiled_informe(lines_of(500))
    assert result.exit_code == 0
    assert calls_of(profiler, Table.add_row) == 20


def test_informe_reads_each_line_once() -> None:
    lines = [*lines_of(50), "# comentario", "", "malo", "Sur;abc"]
    result, profiler = profiled_informe(lines)
    assert result.exit_code == 1
    # 52 líneas de datos (las 50 válidas y las 2 inválidas); el comentario y la vacía
    # se saltan antes de analizarlas.
    assert calls_of(profiler, parse_record) == 52


# --- Series.parse ---


def test_parse_gives_the_series_and_the_errors() -> None:
    series, errors = Series.parse(["Norte;12,5", "malo", "Sur;NA"])
    assert series == Series.from_lines(["Norte;12,5", "Sur;NA"])
    assert errors == ["línea 2: 'malo'"]


def test_parse_counts_the_skipped_lines() -> None:
    _, errors = Series.parse(["# cabecera", "", "Norte;12,5", "Sur;abc"])
    assert errors == ["línea 4: 'Sur;abc'"]


def test_parse_strips_the_lines() -> None:
    series, errors = Series.parse(["  Norte;12,5  \n", " malo \n"])
    assert [str(measurement) for measurement in series] == ["Norte;12,5"]
    assert errors == ["línea 2: 'malo'"]


def test_parse_of_nothing() -> None:
    series, errors = Series.parse([])
    assert len(series) == 0
    assert errors == []


def test_parse_gives_a_new_series_each_time() -> None:
    first, _ = Series.parse(LINES)
    second, _ = Series.parse(LINES)
    first.add(first[0])
    assert len(second) == 4


# Líneas parecidas a las de verdad: etiquetas, ";", números con coma, "NA", espacios,
# comentarios y basura. Con st.text() a secas casi ninguna sería una línea válida.
line = st.one_of(
    st.text(max_size=12),
    st.builds(
        lambda label, value: f"{label};{value}",
        st.sampled_from(["Norte", " Sur ", "", "#x", "Centro"]),
        st.sampled_from(["12,5", "8", "NA", "", "abc", "-3,25", "1e3", "nan", " 7 "]),
    ),
)


@given(st.lists(line, max_size=30))
def test_parse_agrees_with_process_lines_and_from_lines(lines: list[str]) -> None:
    series, errors = Series.parse(lines)
    rows, expected_errors = process_lines(lines, SCALE.unit, SCALE.low, SCALE.high)
    assert errors == expected_errors
    assert [SCALE.row(measurement) for measurement in series] == rows
    assert series == Series.from_lines(lines)


# --- los archivos de perfil ---


def test_profiles_stay_out_of_the_image() -> None:
    # La etapa test copia la carpeta entera (COPY . .): sin esto, los 2 MB de grande.txt
    # y los perfiles acabarían en la imagen.
    ignored = (ROOT / ".dockerignore").read_text(encoding="utf-8").splitlines()
    assert "perfil/" in ignored


def test_the_generator_is_reproducible(tmp_path: Path) -> None:
    first, second = tmp_path / "a.txt", tmp_path / "b.txt"
    for path in (first, second):
        command = [sys.executable, str(ROOT / "scripts" / "generar_medidas.py"), "50", str(path)]
        subprocess.run(command, check=True)
    assert first.read_bytes() == second.read_bytes()
    series, errors = Series.parse(first.read_text(encoding="utf-8").splitlines())
    assert (len(series), errors) == (50, [])
