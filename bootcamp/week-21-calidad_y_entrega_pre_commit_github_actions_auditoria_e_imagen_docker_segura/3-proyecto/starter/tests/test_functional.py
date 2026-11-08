"""Tests de las funciones como valores: Series.where, closures, decoradores y describe (semana 12)."""

from functools import partial

import pytest

from observatorio.core import (
    Measurement,
    Scale,
    Series,
    above,
    describe,
    rounded,
    skip_missing,
)

NORTE = Measurement("Norte", 12.5)
SUR = Measurement("Sur", None)
CENTRO = Measurement("Centro", 55.1)
NORTE_50 = Measurement("Norte", 50.0)


def series_of(*measurements: Measurement) -> Series:
    return Series(list(measurements))


# --- Series.where: una función como argumento ---


def test_where_keeps_the_matching_measurements_in_order() -> None:
    series = series_of(NORTE, SUR, CENTRO, NORTE_50)
    assert list(series.where(lambda m: m.label == "Norte")) == [NORTE, NORTE_50]


def test_where_returns_a_new_series_and_keeps_the_original() -> None:
    series = series_of(NORTE, SUR)
    kept = series.where(lambda m: m.has_value)
    assert kept is not series
    assert list(kept) == [NORTE]
    assert len(series) == 2


def test_where_accepts_a_named_function() -> None:
    def has_no_value(measurement: Measurement) -> bool:
        return measurement.value is None

    assert list(series_of(NORTE, SUR).where(has_no_value)) == [SUR]


def test_where_with_nothing_matching_is_an_empty_series() -> None:
    assert not series_of(NORTE, SUR).where(lambda m: False)


# --- above: una closure ---


def test_above_returns_a_function() -> None:
    assert callable(above(10.0))


def test_above_is_true_for_a_greater_value() -> None:
    assert above(10.0)(NORTE)


def test_above_is_strict() -> None:
    assert not above(50.0)(NORTE_50)


def test_above_is_false_without_value() -> None:
    assert not above(-1000.0)(SUR)


def test_each_above_remembers_its_own_limit() -> None:
    above_10, above_50 = above(10.0), above(50.0)
    assert above_10(NORTE)
    assert not above_50(NORTE)
    assert above_10(CENTRO) and above_50(CENTRO)


def test_above_filters_a_series() -> None:
    series = series_of(NORTE, SUR, CENTRO, NORTE_50)
    assert list(series.where(above(20.0))) == [CENTRO, NORTE_50]


# --- skip_missing: un decorador ---


def test_skip_missing_calls_the_function_with_a_value() -> None:
    @skip_missing
    def double(value: float) -> float:
        return value * 2

    assert double(4.0) == 8.0


def test_skip_missing_returns_none_without_calling_the_function() -> None:
    calls: list[float] = []

    @skip_missing
    def remember(value: float) -> float:
        calls.append(value)
        return value

    assert remember(None) is None
    assert calls == []


def test_skip_missing_keeps_the_name_and_the_docstring() -> None:
    @skip_missing
    def to_fahrenheit(celsius: float) -> float:
        """Grados Celsius a Fahrenheit."""
        return celsius * 9 / 5 + 32

    assert to_fahrenheit.__name__ == "to_fahrenheit"
    assert to_fahrenheit.__doc__ == "Grados Celsius a Fahrenheit."


def test_skip_missing_keeps_the_original_function_in_wrapped() -> None:
    def half(value: float) -> float:
        return value / 2

    assert getattr(skip_missing(half), "__wrapped__", None) is half


def test_skip_missing_maps_a_list_with_gaps() -> None:
    to_fahrenheit = skip_missing(lambda celsius: celsius * 9 / 5 + 32)
    assert [to_fahrenheit(value) for value in [10.0, None, 0.0]] == [50.0, None, 32.0]


# --- rounded: un decorador con argumento ---


def test_rounded_rounds_the_result() -> None:
    @rounded(1)
    def third(value: float) -> float:
        return value / 3

    assert third(10.0) == 3.3


def test_rounded_passes_positional_and_keyword_arguments() -> None:
    @rounded(2)
    def scaled(value: float, *, factor: float = 1.0) -> float:
        return value * factor

    assert scaled(1.23456) == 1.23
    assert scaled(1.23456, factor=10.0) == 12.35


def test_each_rounded_keeps_its_own_digits() -> None:
    def tenth(value: float) -> float:
        return value / 10

    assert rounded(0)(tenth)(123.0) == 12.0
    assert rounded(2)(tenth)(123.0) == 12.3


def test_rounded_keeps_the_name() -> None:
    @rounded(1)
    def mean_of(values: list[float]) -> float:
        return sum(values) / len(values)

    assert mean_of.__name__ == "mean_of"
    assert mean_of([10.0, 20.0, 20.0]) == 16.7


def test_rounded_works_with_a_method_of_the_model() -> None:
    series = Series.from_lines(["Norte;10", "Norte;20", "Norte;20"])
    mean_of_norte = rounded(1)(lambda: series.means()["Norte"])
    assert mean_of_norte() == 16.7


def test_skip_missing_and_rounded_stack_with_partial() -> None:
    def scaled(value: float, factor: float) -> float:
        return value * factor

    to_ppb = skip_missing(rounded(1)(partial(scaled, factor=0.509)))
    assert to_ppb(55.1) == 28.0
    assert to_ppb(None) is None


# --- describe: singledispatch ---


def test_describe_a_measurement() -> None:
    assert describe(NORTE) == "Norte: 12,5"


def test_describe_a_measurement_without_value() -> None:
    assert describe(SUR) == "Sur: sin dato"


def test_describe_a_series() -> None:
    assert describe(series_of(NORTE, SUR, NORTE_50)) == "medidas: 3 · etiquetas: 2"


def test_describe_an_empty_series() -> None:
    assert describe(Series()) == "medidas: 0 · etiquetas: 0"


def test_describe_a_scale() -> None:
    assert describe(Scale("°C", 10.0, 50.0)) == "°C entre 10 y 50"


def test_describe_rejects_other_types() -> None:
    with pytest.raises(TypeError, match="describe no acepta int"):
        describe(12)


def test_describe_has_one_function_per_model_type() -> None:
    assert {Measurement, Series, Scale} <= set(describe.registry)


def test_describe_a_filtered_series() -> None:
    series = series_of(NORTE, SUR, CENTRO, NORTE_50)
    assert describe(series.where(above(20.0))) == "medidas: 2 · etiquetas: 2"
