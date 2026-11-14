"""Tests de la CLI (semana 15): la aplicación Typer de observatorio.cli.

CliRunner ejecuta la aplicación como si la llamaras desde la terminal, pero dentro del
test: recoge stdout, stderr y el código de salida sin lanzar otro proceso.
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest
from rich.console import Console
from typer.testing import CliRunner

from observatorio import __version__, cli
from observatorio.core import Scale, Series

runner = CliRunner()

LINES = ["Norte;12,5", "Sur;8", "Oriente;55,1", "Norte;48,9"]


# --- la aplicación ---


def test_cli_keeps_its_scale() -> None:
    assert cli.SCALE == Scale(cli.UNIT, cli.LOW, cli.HIGH)


def test_without_arguments_shows_the_help() -> None:
    result = runner.invoke(cli.app, [])
    assert result.exit_code == 2
    assert "informe" in result.output
    assert "validar" in result.output


@pytest.mark.parametrize("flag", ["--version", "-V"])
def test_version(flag: str) -> None:
    result = runner.invoke(cli.app, [flag])
    assert result.exit_code == 0
    assert result.stdout == f"observatorio {__version__}\n"


def test_help_lists_the_options() -> None:
    result = runner.invoke(cli.app, ["--help"])
    assert result.exit_code == 0
    for option in ["--verbose", "--version", "informe", "validar"]:
        assert option in result.stdout


def test_unknown_command() -> None:
    result = runner.invoke(cli.app, ["inventado"])
    assert result.exit_code == 2
    assert "No such command" in result.stderr


def test_python_m_runs_the_same_application() -> None:
    command = [sys.executable, "-m", "observatorio", "--version"]
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    assert result.returncode == 0
    assert result.stdout == f"observatorio {__version__}\n"


# --- informe ---


def test_informe_help() -> None:
    result = runner.invoke(cli.app, ["informe", "--help"])
    assert result.exit_code == 0
    for option in ["--archivo", "--json", "--escala", "LINEAS"]:
        assert option in result.stdout


def test_informe_shows_a_table_with_every_measurement() -> None:
    result = runner.invoke(cli.app, ["informe", *LINES])
    assert result.exit_code == 0
    assert "Medidas" in result.stdout
    for cell in ["Etiqueta", "Valor", "Nivel", "Norte", "12.5 unidad", "Oriente", "alto"]:
        assert cell in result.stdout


def table_rows(output: str) -> list[list[str]]:
    """Las celdas de las filas de datos de la tabla: las líneas entre "│" sin cabecera."""
    lines = [line for line in output.splitlines() if line.startswith("│")]
    return [[cell.strip() for cell in line.split("│")[1:-1]] for line in lines]


def test_informe_rows_follow_the_lines() -> None:
    result = runner.invoke(cli.app, ["informe", *LINES])
    assert table_rows(result.stdout) == [
        ["Norte", "12.5 unidad", "medio"],
        ["Sur", "8.0 unidad", "bajo"],
        ["Oriente", "55.1 unidad", "alto"],
        ["Norte", "48.9 unidad", "medio"],
    ]


def test_table_colors_each_level() -> None:
    # CliRunner no es una terminal y Rich no pone colores: el color se prueba aparte,
    # con una consola que finge ser una terminal y graba lo que escribe.
    console = Console(record=True, force_terminal=True, color_system="standard", width=80)
    console.print(cli.table_of(Series.from_lines(["Norte;12,5", "Sur;8", "Este;60"]), cli.SCALE))
    text = console.export_text(styles=True)
    assert "\x1b[32mmedio" in text
    assert "\x1b[36mbajo" in text
    assert "\x1b[1;31malto" in text


def test_informe_writes_the_summary() -> None:
    result = runner.invoke(cli.app, ["informe", *LINES])
    expected = [
        "registros: 4 | bajo: 1 | medio: 2 | alto: 1 | sin dato: 0",
        "racha más larga en alto: 1",
        "en alto: 25.0 %",
        "etiquetas distintas: 3",
        "medias más altas: Oriente 55.1, Norte 30.7, Sur 8.0",
        "más frecuentes: Norte 2, Sur 1, Oriente 1",
        "mediana: 30.7 unidad",
        "media móvil (3): 25.2 · 37.3",
        "mayor salto: +47.1 unidad",
    ]
    assert result.stdout.splitlines()[-len(expected) :] == expected


def test_informe_without_values_skips_the_trends() -> None:
    result = runner.invoke(cli.app, ["informe", "Norte;NA"])
    assert result.exit_code == 0
    assert "sin dato" in result.stdout
    assert "mediana" not in result.stdout


def test_informe_errors_go_to_stderr_with_code_1() -> None:
    result = runner.invoke(cli.app, ["informe", "Norte;12,5", "malo", "Sur;abc"])
    assert result.exit_code == 1
    assert result.stderr == "error: línea 2: 'malo'\nerror: línea 3: 'Sur;abc'\n"
    assert "Norte" in result.stdout
    assert "malo" not in result.stdout


def test_informe_shows_brackets_in_labels() -> None:
    # Con markup, Rich tomaría "[b]" por "negrita" y lo borraría de la etiqueta.
    result = runner.invoke(cli.app, ["informe", "Sala [b];12"])
    assert "Sala [b]" in result.stdout


def test_informe_reads_stdin() -> None:
    result = runner.invoke(cli.app, ["informe"], input="Norte;12,5\nSur;8\n")
    assert result.exit_code == 0
    assert "registros: 2" in result.stdout


def test_informe_with_empty_stdin() -> None:
    result = runner.invoke(cli.app, ["informe"], input="")
    assert result.exit_code == 0
    assert "registros: 0" in result.stdout


def test_informe_reads_a_csv_file(tmp_path: Path) -> None:
    path = tmp_path / "medidas.csv"
    path.write_text("etiqueta;valor\nNorte;12,5\nSur;8\n", encoding="utf-8")
    result = runner.invoke(cli.app, ["informe", "--archivo", str(path)])
    assert result.exit_code == 0
    assert "registros: 2" in result.stdout


def test_informe_reads_a_text_file_with_the_short_option(tmp_path: Path) -> None:
    path = tmp_path / "medidas.txt"
    path.write_text("Norte;12,5\n", encoding="utf-8")
    result = runner.invoke(cli.app, ["informe", "-f", str(path)])
    assert "registros: 1" in result.stdout


def test_informe_missing_file(tmp_path: Path) -> None:
    result = runner.invoke(cli.app, ["informe", "-f", str(tmp_path / "no-existe.csv")])
    assert result.exit_code == 2
    assert result.stderr.startswith("error: no existe el archivo")
    assert result.stdout == ""


def test_informe_does_not_accept_lines_and_a_file() -> None:
    result = runner.invoke(cli.app, ["informe", "Norte;1", "-f", "medidas.csv"])
    assert result.exit_code == 2
    assert "usa líneas o --archivo, no los dos" in result.stderr


def test_informe_saves_the_summary(tmp_path: Path) -> None:
    output = tmp_path / "resumen.json"
    result = runner.invoke(cli.app, ["informe", *LINES, "--json", str(output)])
    assert result.exit_code == 0
    assert result.stdout.endswith(f"resumen guardado en {output}\n")
    assert json.loads(output.read_text(encoding="utf-8"))["registros"] == 4


def test_informe_cannot_save_the_summary(tmp_path: Path) -> None:
    output = tmp_path / "no-existe" / "resumen.json"
    result = runner.invoke(cli.app, ["informe", "Norte;1", "-j", str(output)])
    assert result.exit_code == 2
    assert result.stderr.startswith("error: ")


def test_informe_reads_the_scale(tmp_path: Path) -> None:
    path = tmp_path / "escala.json"
    path.write_text('{"unit": "°C", "low": 0, "high": 10}', encoding="utf-8")
    result = runner.invoke(cli.app, ["informe", "Norte;12,5", "--escala", str(path)])
    assert result.exit_code == 0
    # La tabla también usa la escala leída, no solo el resumen.
    assert table_rows(result.stdout) == [["Norte", "12.5 °C", "alto"]]
    assert "alto: 1" in result.stdout


def test_informe_rejects_an_impossible_scale(tmp_path: Path) -> None:
    path = tmp_path / "escala.json"
    path.write_text('{"unit": "°C", "low": 10, "high": 0}', encoding="utf-8")
    result = runner.invoke(cli.app, ["informe", "Norte;1", "-e", str(path)])
    assert result.exit_code == 2
    assert "umbrales imposibles" in result.stderr


# --- validar ---


def test_validar_counts_the_measurements(tmp_path: Path) -> None:
    path = tmp_path / "medidas.json"
    path.write_text('[{"label": "Norte", "value": 12.5}, {"label": "Sur", "value": null}]')
    result = runner.invoke(cli.app, ["validar", str(path)])
    assert result.exit_code == 0
    assert result.stdout == f"{path}: 2 medidas válidas\n"


def test_validar_explains_what_is_wrong(tmp_path: Path) -> None:
    path = tmp_path / "medidas.json"
    path.write_text('[{"label": "", "value": 12.5}]', encoding="utf-8")
    result = runner.invoke(cli.app, ["validar", str(path)])
    assert result.exit_code == 2
    assert result.stderr.startswith(f"error: datos no válidos en {path}: 0.label")


def test_validar_needs_a_path() -> None:
    result = runner.invoke(cli.app, ["validar"])
    assert result.exit_code == 2
    assert "Missing argument" in result.stderr
