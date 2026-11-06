"""Tests del modelo: Scale, Measurement y Series (semana 9)."""

import dataclasses

import pytest

import observatorio.__main__ as entry
from observatorio.core import Measurement, Scale, Series

SCALE = Scale("µg/m³", 10.0, 50.0)

LINES = ["Norte;12,5", "# comentario", "Sur;8", "malo", "Norte;48,9", "Este;NA", ""]


# --- Scale ---


def test_scale_keeps_its_fields() -> None:
    assert (SCALE.unit, SCALE.low, SCALE.high) == ("µg/m³", 10.0, 50.0)


def test_scale_repr_is_generated() -> None:
    assert repr(SCALE) == "Scale(unit='µg/m³', low=10.0, high=50.0)"


def test_scales_with_the_same_fields_are_equal() -> None:
    assert Scale("µg/m³", 10.0, 50.0) == SCALE
    assert Scale("µg/m³", 10.0, 60.0) != SCALE


@pytest.mark.parametrize(("low", "high"), [(50.0, 10.0), (10.0, 10.0)])
def test_scale_rejects_impossible_thresholds(low: float, high: float) -> None:
    with pytest.raises(ValueError, match="umbrales imposibles"):
        Scale("µg/m³", low, high)


def test_scale_is_frozen() -> None:
    with pytest.raises(dataclasses.FrozenInstanceError):
        SCALE.low = 0.0  # type: ignore[misc]


@pytest.mark.parametrize(
    ("value", "level"),
    [(None, "sin dato"), (9.9, "bajo"), (10.0, "medio"), (49.9, "medio"), (50.0, "alto")],
)
def test_scale_level(value: float | None, level: str) -> None:
    assert SCALE.level(value) == level


def test_scale_row() -> None:
    assert SCALE.row(Measurement("Norte", 12.54)) == "Norte               12.5 µg/m³ | medio"
    assert SCALE.row(Measurement("Este", None)) == "Este                  sin dato | sin dato"


def test_main_builds_its_scale_from_its_constants() -> None:
    # getattr y no un import: si SCALE aún no existe, falla solo este test.
    assert getattr(entry, "SCALE", None) == Scale(entry.UNIT, entry.LOW, entry.HIGH)


# --- Measurement ---


def test_measurement_fields_and_repr() -> None:
    measurement = Measurement("Norte", 12.5)
    assert measurement.label == "Norte"
    assert measurement.value == 12.5
    assert repr(measurement) == "Measurement(label='Norte', value=12.5)"


def test_measurement_from_line() -> None:
    assert Measurement.from_line(" Norte ;12,5") == Measurement("Norte", 12.5)
    assert Measurement.from_line("Sur;NA") == Measurement("Sur", None)


@pytest.mark.parametrize("line", ["malo", "a;b;c", " ;12"])
def test_measurement_from_invalid_line_is_none(line: str) -> None:
    assert Measurement.from_line(line) is None


def test_measurement_has_value() -> None:
    assert Measurement("Norte", 0.0).has_value
    assert not Measurement("Sur", None).has_value


def test_measurement_is_frozen() -> None:
    with pytest.raises(dataclasses.FrozenInstanceError):
        Measurement("Norte", 12.5).value = 0.0  # type: ignore[misc]


def test_measurements_are_hashable() -> None:
    repeated = {Measurement("Norte", 12.5), Measurement("Norte", 12.5), Measurement("Sur", 8.0)}
    assert len(repeated) == 2


def test_model_classes_use_slots() -> None:
    assert not hasattr(Measurement("Norte", 12.5), "__dict__")
    assert not hasattr(Series(), "__dict__")


# --- Series ---


def test_series_from_lines_keeps_valid_lines_in_order() -> None:
    assert Series.from_lines(LINES).measurements == [
        Measurement("Norte", 12.5),
        Measurement("Sur", 8.0),
        Measurement("Norte", 48.9),
        Measurement("Este", None),
    ]


def test_empty_series_do_not_share_their_list() -> None:
    first, second = Series(), Series()
    first.add(Measurement("Norte", 12.5))
    assert first.measurements == [Measurement("Norte", 12.5)]
    assert second.measurements == []


def test_series_add_appends_at_the_end() -> None:
    series = Series.from_lines(["Norte;12,5"])
    series.add(Measurement("Sur", None))
    assert series.measurements[-1] == Measurement("Sur", None)
    assert len(series.measurements) == 2


def test_series_records_are_tuples() -> None:
    assert Series.from_lines(LINES).records == [
        ("Norte", 12.5),
        ("Sur", 8.0),
        ("Norte", 48.9),
        ("Este", None),
    ]


def test_series_values_labels_and_means() -> None:
    series = Series.from_lines(LINES)
    assert series.values() == [12.5, 8.0, 48.9]
    assert series.labels() == {"Norte", "Sur", "Este"}
    assert series.means() == pytest.approx({"Norte": 30.7, "Sur": 8.0})


def test_series_most_common() -> None:
    assert Series.from_lines(LINES).most_common(2) == [("Norte", 2), ("Sur", 1)]


def test_empty_series() -> None:
    series = Series()
    assert (series.values(), series.labels(), series.means()) == ([], set(), {})
    assert series.most_common(3) == []
