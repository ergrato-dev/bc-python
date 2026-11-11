"""Tests de la capa 13: fixtures, parametrize, Hypothesis, logging y mocks.

Además de probar el código, cada bloque usa una herramienta de la semana 14. Los
bloques de parametrize, Hypothesis y mocks reproducen tres bugs reales de las capas
anteriores: un valor como "abc" tumbaba main, "nan" e "inf" pasaban por medidas
y un archivo sin permiso de lectura salía como PermissionError.
"""

import logging
import math
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path
from unittest import mock

import pytest
from hypothesis import given
from hypothesis import strategies as st
from pydantic import ValidationError
from typer.testing import CliRunner

from observatorio import cli
from observatorio.core import (
    DataFileError,
    Measurement,
    MeasurementIn,
    Scale,
    Series,
    is_data_line,
    iter_lines,
    median,
    moving_average,
    parse_line,
    parse_record,
    parse_value,
    process_lines,
    read_lines,
    records_of,
    write_json,
)

# Números del dominio: finitos y de un tamaño razonable. Sin límites, Hypothesis prueba
# 1e308, y (1e308 + 1e308) / 2 desborda a inf en median.
NUMBERS = st.floats(min_value=-1e6, max_value=1e6, allow_nan=False)
# Etiquetas válidas: sin ";" y sin espacios a los lados (parse_record los quita).
LABELS = st.text(min_size=1).filter(lambda text: ";" not in text and text == text.strip())

# ---------- Fixtures: las de tests/conftest.py ----------


def test_scale_fixture(scale: Scale) -> None:
    assert scale == Scale("unidad", 10.0, 50.0)


def test_series_fixture_uses_the_lines_fixture(lines: list[str], series: Series) -> None:
    assert len(lines) == 5
    assert series.labels() == {"Norte", "Sur", "Este"}


def test_series_fixture_can_be_changed(series: Series) -> None:
    series.add(Measurement("Oeste", 30.0))
    assert len(series) == 4


def test_series_fixture_is_new_in_each_test(series: Series) -> None:
    assert len(series) == 3


def test_write_file_is_a_factory(tmp_path: Path, write_file: Callable[[str, str], Path]) -> None:
    first = write_file("uno.txt", "Norte;12,5\n")
    second = write_file("dos.txt", "Sur;8\n")
    assert first == tmp_path / "uno.txt"
    assert read_lines(second) == ["Sur;8"]


# ---------- parametrize: valores que no son números finitos ----------


@pytest.mark.parametrize(
    ("text", "expected"),
    [("12,5", 12.5), (" 8 ", 8.0), ("-3,25", -3.25), ("NA", None), ("", None)],
)
def test_parse_value_still_reads_good_values(text: str, expected: float | None) -> None:
    assert parse_value(text) == expected


@pytest.mark.parametrize("text", ["nan", "NaN", "inf", "-inf", "Infinity"])
def test_parse_value_rejects_non_finite_values(text: str) -> None:
    with pytest.raises(ValueError, match="valor no finito"):
        parse_value(text)


@pytest.mark.parametrize("line", ["Norte;abc", "Norte;12,5,3", "Norte;nan", "Norte;inf"])
def test_parse_record_rejects_bad_values(line: str) -> None:
    assert parse_record(line) is None


@pytest.mark.parametrize("line", ["Norte;abc", "Norte;nan"])
def test_parse_line_rejects_bad_values(line: str) -> None:
    assert parse_line(line, "u", 10.0, 50.0) is None


def test_measurement_from_line_rejects_nan() -> None:
    assert Measurement.from_line("Norte;nan") is None


def test_process_lines_reports_a_bad_value_as_an_error() -> None:
    rows, errors = process_lines(["Norte;abc", "Sur;12"], "u", 10.0, 50.0)
    assert len(rows) == 1
    assert errors == ["línea 1: 'Norte;abc'"]


def test_cli_does_not_crash_on_a_bad_value() -> None:
    result = CliRunner().invoke(cli.app, ["informe", "Norte;abc", "Sur;12"])
    assert result.exit_code == 1
    assert "error: línea 1: 'Norte;abc'" in result.stderr


@pytest.mark.parametrize(
    ("data", "error_type"),
    [
        ('{"label": "Norte", "value": NaN}', "finite_number"),
        ('{"label": "Norte", "value": "inf"}', "value_error"),
    ],
    ids=["json-nan", "text-inf"],
)
def test_measurement_in_rejects_non_finite_values(data: str, error_type: str) -> None:
    with pytest.raises(ValidationError) as caught:
        MeasurementIn.model_validate_json(data)
    assert caught.value.errors()[0]["type"] == error_type


# ---------- Hypothesis: propiedades que valen para cualquier dato ----------


@given(NUMBERS)
def test_parse_value_reads_back_what_str_writes(number: float) -> None:
    assert parse_value(str(number)) == number
    assert parse_value(str(number).replace(".", ",")) == number


@given(st.floats() | st.text())
def test_parse_value_gives_none_a_finite_number_or_value_error(text: float | str) -> None:
    try:
        value = parse_value(str(text))
    except ValueError:
        return
    assert value is None or math.isfinite(value)


@given(LABELS, st.none() | NUMBERS)
def test_measurement_round_trips_through_str(label: str, value: float | None) -> None:
    measurement = Measurement(label, value)
    assert Measurement.from_line(str(measurement)) == measurement


@given(st.lists(st.text() | st.builds("{};{}".format, st.text(), st.text())))
def test_process_lines_never_crashes_and_counts_every_data_line(lines: list[str]) -> None:
    rows, errors = process_lines(lines, "u", 10.0, 50.0)
    assert len(rows) + len(errors) == sum(is_data_line(line.strip()) for line in lines)


@given(st.lists(NUMBERS, min_size=1))
def test_median_is_between_min_and_max(values: list[float]) -> None:
    assert min(values) <= median(values) <= max(values)


@given(st.lists(NUMBERS), st.integers(min_value=1, max_value=10))
def test_moving_average_has_one_value_per_full_window(values: list[float], window: int) -> None:
    assert len(moving_average(values, window)) == max(0, len(values) - window + 1)


@given(st.floats())
def test_measurement_in_accepts_only_finite_numbers(number: float) -> None:
    try:
        measurement = MeasurementIn.model_validate({"label": "Norte", "value": number})
    except ValidationError:
        assert not math.isfinite(number)
    else:
        assert measurement.value == number


# ---------- logging: el paquete escribe, main configura ----------


def test_each_module_has_its_own_logger() -> None:
    from observatorio.core import groups, storage

    assert storage.logger.name == "observatorio.core.storage"
    assert groups.logger.name == "observatorio.core.groups"


def test_the_package_adds_no_handlers() -> None:
    assert logging.getLogger("observatorio.core.storage").handlers == []
    assert logging.getLogger("observatorio").handlers == []


def test_records_of_logs_each_ignored_line(caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.DEBUG, logger="observatorio")
    records_of(["Norte;12,5", "malo", "Sur;abc"])
    assert caplog.messages == ["línea ignorada: 'malo'", "línea ignorada: 'Sur;abc'"]
    assert {record.name for record in caplog.records} == {"observatorio.core.groups"}
    assert {record.levelname for record in caplog.records} == {"DEBUG"}


def test_records_of_logs_nothing_for_good_lines(caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.DEBUG, logger="observatorio")
    records_of(["# comentario", "Norte;12,5", ""])
    assert caplog.records == []


def test_read_lines_logs_how_many_lines_it_read(
    caplog: pytest.LogCaptureFixture, write_file: Callable[[str, str], Path]
) -> None:
    caplog.set_level(logging.DEBUG, logger="observatorio")
    path = write_file("medidas.txt", "Norte;12,5\nSur;8\n")
    read_lines(path)
    assert caplog.messages == [f"2 líneas leídas de {path}"]


def test_debug_messages_are_hidden_by_default(caplog: pytest.LogCaptureFixture) -> None:
    records_of(["malo"])
    assert caplog.records == []


def test_cli_accepts_verbose_before_the_command() -> None:
    result = CliRunner().invoke(cli.app, ["-v", "--version"])
    assert result.exit_code == 0
    assert result.stdout.startswith("observatorio ")


def test_verbose_shows_debug_messages_on_stderr(write_file: Callable[[str, str], Path]) -> None:
    path = write_file("medidas.txt", "Norte;12,5\nmalo\n")
    command = [sys.executable, "-m", "observatorio", "-v", "informe", "-f", str(path)]
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    assert f"DEBUG observatorio.core.storage: 2 líneas leídas de {path}" in result.stderr
    assert "DEBUG observatorio.core.groups: línea ignorada: 'malo'" in result.stderr
    assert "DEBUG" not in result.stdout


def test_without_verbose_there_are_no_debug_messages(
    write_file: Callable[[str, str], Path],
) -> None:
    path = write_file("medidas.txt", "Norte;12,5\nmalo\n")
    command = [sys.executable, "-m", "observatorio", "informe", "-f", str(path)]
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    assert "DEBUG" not in result.stderr


# ---------- mocks: fallos que no se pueden provocar de verdad en un test ----------


def test_read_lines_without_permission_raises_data_file_error(tmp_path: Path) -> None:
    denied = PermissionError(13, "Permission denied")
    with (
        mock.patch.object(Path, "open", side_effect=denied),
        pytest.raises(DataFileError, match="sin permiso para leer") as caught,
    ):
        read_lines(tmp_path / "medidas.txt")
    assert caught.value.__cause__ is denied


def test_iter_lines_without_permission_raises_data_file_error(tmp_path: Path) -> None:
    with (
        mock.patch.object(Path, "open", side_effect=PermissionError(13, "Permission denied")),
        pytest.raises(DataFileError, match="sin permiso para leer"),
    ):
        next(iter_lines(tmp_path / "medidas.txt"))


def test_cli_without_permission_says_error(write_file: Callable[[str, str], Path]) -> None:
    path = write_file("medidas.txt", "Norte;12,5\n")
    with mock.patch.object(Path, "open", side_effect=PermissionError(13, "Permission denied")):
        result = CliRunner().invoke(cli.app, ["informe", "-f", str(path)])
    assert result.exit_code == 2
    assert result.stderr == f"error: sin permiso para leer {path}\n"


def test_write_json_with_a_full_disk_raises_data_file_error(tmp_path: Path) -> None:
    with (
        mock.patch.object(Path, "open", side_effect=OSError(28, "No space left on device")),
        pytest.raises(DataFileError, match="no se puede escribir"),
    ):
        write_json({"registros": 1}, tmp_path / "resumen.json")


def test_cli_calls_write_json_once_with_the_output_path(
    write_file: Callable[[str, str], Path], tmp_path: Path
) -> None:
    path = write_file("medidas.txt", "Norte;12,5\nSur;8\n")
    output = tmp_path / "resumen.json"
    with mock.patch.object(cli, "write_json", autospec=True) as fake:
        result = CliRunner().invoke(cli.app, ["informe", "-f", str(path), "-j", str(output)])
    assert result.exit_code == 0
    fake.assert_called_once()
    data, where = fake.call_args.args
    assert data["registros"] == 2
    assert where == output
    assert not output.exists()
