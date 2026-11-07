"""Tests del data model: los dunders de Measurement y Series y los generadores (semana 11)."""

import itertools
from collections.abc import Generator, Iterable, Sized
from pathlib import Path

import pytest

from observatorio.core import (
    DataFileError,
    Measurement,
    Series,
    iter_lines,
    iter_measurements,
    read_lines,
    running_mean,
)

NORTE = Measurement("Norte", 12.5)
SUR = Measurement("Sur", None)
CENTRO = Measurement("Centro", 8.0)
LINES = ["# comentario", "Norte;12,5", "", "Sur 9,5", "Sur;NA", "Centro;8"]


def series_of(*measurements: Measurement) -> Series:
    return Series(list(measurements))


# --- Measurement: __str__ ---


def test_measurement_str_is_its_line() -> None:
    assert str(NORTE) == "Norte;12,5"


def test_measurement_without_value_str_uses_na() -> None:
    assert str(SUR) == "Sur;NA"


def test_measurement_str_round_trips_with_from_line() -> None:
    for measurement in [NORTE, SUR, CENTRO, Measurement("Este", -0.25)]:
        assert Measurement.from_line(str(measurement)) == measurement


# --- Series: tamaño y verdad ---


def test_len_of_an_empty_series_is_0() -> None:
    assert len(Series()) == 0


def test_len_counts_the_measurements() -> None:
    assert len(series_of(NORTE, SUR, CENTRO)) == 3


def test_an_empty_series_is_falsy() -> None:
    assert not Series()
    assert series_of(NORTE)


# --- Series: iteración y pertenencia ---


def test_a_series_iterates_its_measurements_in_order() -> None:
    assert list(series_of(NORTE, SUR, CENTRO)) == [NORTE, SUR, CENTRO]


def test_each_iter_starts_a_new_iterator() -> None:
    series = series_of(NORTE, SUR)
    first, second = iter(series), iter(series)
    assert first is not second
    assert next(first) == NORTE
    assert next(second) == NORTE


def test_in_finds_a_measurement() -> None:
    series = series_of(NORTE, SUR)
    assert Measurement("Norte", 12.5) in series
    assert CENTRO not in series


def test_a_series_is_sized_and_iterable() -> None:
    assert isinstance(Series(), Sized)
    assert isinstance(Series(), Iterable)


# --- Series: posición ---


def test_getitem_by_position() -> None:
    series = series_of(NORTE, SUR, CENTRO)
    assert series[0] == NORTE
    assert series[-1] == CENTRO


def test_getitem_out_of_range_raises_index_error() -> None:
    with pytest.raises(IndexError):
        series_of(NORTE)[1]


# --- Series: suma ---


def test_add_joins_two_series_in_order() -> None:
    assert list(series_of(NORTE) + series_of(SUR, CENTRO)) == [NORTE, SUR, CENTRO]


def test_add_does_not_change_the_operands() -> None:
    first, second = series_of(NORTE), series_of(SUR)
    total = first + second
    assert list(first) == [NORTE]
    assert list(second) == [SUR]
    assert total is not first


def test_add_with_a_list_raises_type_error() -> None:
    with pytest.raises(TypeError, match="unsupported operand"):
        series_of(NORTE) + [SUR]  # type: ignore[operator]


# --- iter_lines ---


def test_iter_lines_is_a_generator(tmp_path: Path) -> None:
    path = tmp_path / "medidas.txt"
    path.write_text("Norte;12,5\n", encoding="utf-8")
    assert isinstance(iter_lines(path), Generator)


def test_iter_lines_gives_the_same_lines_as_read_lines(tmp_path: Path) -> None:
    path = tmp_path / "medidas.txt"
    path.write_text("# medidas\nNorte;12,5\n\nSur;NA\n", encoding="utf-8")
    assert list(iter_lines(path)) == read_lines(path)


def test_iter_lines_fails_on_the_first_next_not_on_the_call(tmp_path: Path) -> None:
    lines = iter_lines(tmp_path / "no-existe.txt")
    with pytest.raises(DataFileError, match="no existe el archivo"):
        next(lines)


def test_iter_lines_of_a_folder_raises_data_file_error(tmp_path: Path) -> None:
    with pytest.raises(DataFileError, match="es una carpeta"):
        list(iter_lines(tmp_path))


# --- iter_measurements ---


def test_iter_measurements_follows_series_from_lines() -> None:
    assert list(iter_measurements(LINES)) == Series.from_lines(LINES).measurements


def test_iter_measurements_works_with_an_endless_input() -> None:
    endless = itertools.cycle(["Norte;12,5", "basura", "Sur;NA"])
    assert list(itertools.islice(iter_measurements(endless), 3)) == [NORTE, SUR, NORTE]


# --- running_mean ---


def test_running_mean_yields_each_partial_mean() -> None:
    assert list(running_mean([10.0, 20.0, 30.0])) == [10.0, 15.0, 20.0]


def test_running_mean_of_nothing_is_empty() -> None:
    assert list(running_mean([])) == []


def test_running_mean_works_with_an_endless_input() -> None:
    assert list(itertools.islice(running_mean(itertools.count(1)), 4)) == [1.0, 1.5, 2.0, 2.5]


def test_a_generator_is_used_up_after_one_pass() -> None:
    means = running_mean([1.0, 3.0])
    assert list(means) == [1.0, 2.0]
    assert list(means) == []
