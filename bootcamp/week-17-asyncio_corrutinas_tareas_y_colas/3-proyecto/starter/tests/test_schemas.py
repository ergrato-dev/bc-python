"""Tests de la capa 12: el resumen tipado (Summary) y la frontera con Pydantic (schemas)."""

from pathlib import Path

import pytest
from pydantic import ValidationError

from observatorio.core import (
    DataFileError,
    Measurement,
    MeasurementIn,
    Scale,
    Series,
    Summary,
    read_measurements,
    read_scale,
    summary_data,
)

# ---------- Summary: un TypedDict ----------


def test_summary_is_a_plain_dict() -> None:
    summary: Summary = summary_data([("Norte", 12.5)])
    assert type(summary) is dict


def test_summary_keys_follow_the_typed_dict() -> None:
    summary = summary_data([("Norte", 12.5), ("Sur", None)])
    assert list(summary) == list(Summary.__annotations__)


def test_summary_types_follow_the_typed_dict() -> None:
    summary = summary_data([("Norte", 12.5), ("Sur", 8.0)])
    assert isinstance(summary["registros"], int)
    assert isinstance(summary["mediana"], float)


# ---------- MeasurementIn: el esquema de una medida en JSON ----------


def test_measurement_in_validates_a_dict() -> None:
    item = MeasurementIn.model_validate({"label": "Norte", "value": 12.5})
    assert (item.label, item.value) == ("Norte", 12.5)


def test_measurement_in_accepts_an_integer_and_null() -> None:
    assert MeasurementIn.model_validate({"label": "Norte", "value": 12}).value == 12.0
    assert MeasurementIn.model_validate({"label": "Sur", "value": None}).value is None


@pytest.mark.parametrize(("text", "expected"), [("12,5", 12.5), ("8.0", 8.0), ("NA", None)])
def test_measurement_in_parses_text_values(text: str, expected: float | None) -> None:
    assert MeasurementIn.model_validate({"label": "Norte", "value": text}).value == expected


def test_measurement_in_strips_the_label() -> None:
    assert MeasurementIn.model_validate({"label": "  Sur ", "value": 8}).label == "Sur"


@pytest.mark.parametrize("label", ["", "   "])
def test_measurement_in_rejects_an_empty_label(label: str) -> None:
    with pytest.raises(ValidationError, match="at least 1 character"):
        MeasurementIn.model_validate({"label": label, "value": 1})


def test_measurement_in_rejects_a_boolean_value() -> None:
    with pytest.raises(ValidationError, match="valid number"):
        MeasurementIn.model_validate({"label": "Norte", "value": True})


def test_measurement_in_rejects_a_text_that_is_not_a_number() -> None:
    with pytest.raises(ValidationError, match="could not convert string to float"):
        MeasurementIn.model_validate({"label": "Norte", "value": "doce"})


def test_measurement_in_rejects_extra_keys() -> None:
    with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
        MeasurementIn.model_validate({"label": "Norte", "value": 1, "unit": "ppm"})


def test_measurement_in_requires_the_value() -> None:
    with pytest.raises(ValidationError, match="Field required"):
        MeasurementIn.model_validate({"label": "Norte"})


def test_measurement_in_is_frozen() -> None:
    item = MeasurementIn(label="Norte", value=1.0)
    with pytest.raises(ValidationError, match="frozen"):
        item.value = 2.0  # type: ignore[misc]


def test_measurement_in_converts_to_the_model() -> None:
    item = MeasurementIn(label="Norte", value=12.5)
    assert item.to_measurement() == Measurement("Norte", 12.5)


def test_measurement_in_dumps_to_json() -> None:
    item = MeasurementIn(label="Norte", value=12.5)
    assert item.model_dump_json() == '{"label":"Norte","value":12.5}'


# ---------- read_measurements y read_scale: archivos JSON validados ----------


def write(tmp_path: Path, text: str) -> Path:
    path = tmp_path / "datos.json"
    path.write_text(text, encoding="utf-8")
    return path


def test_read_measurements_returns_a_series(tmp_path: Path) -> None:
    path = write(tmp_path, '[{"label": "Norte", "value": "12,5"}, {"label": "Sur", "value": null}]')
    series = read_measurements(path)
    assert isinstance(series, Series)
    assert list(series) == [Measurement("Norte", 12.5), Measurement("Sur", None)]


def test_read_measurements_with_an_empty_list(tmp_path: Path) -> None:
    assert len(read_measurements(write(tmp_path, "[]"))) == 0


def test_read_measurements_says_where_the_error_is(tmp_path: Path) -> None:
    path = write(tmp_path, '[{"label": "Norte", "value": 1}, {"label": "", "value": 2}]')
    with pytest.raises(DataFileError, match=r"^datos no válidos en .*datos\.json: 1\.label: "):
        read_measurements(path)


def test_read_measurements_rejects_an_object(tmp_path: Path) -> None:
    path = write(tmp_path, '{"label": "Norte", "value": 1}')
    with pytest.raises(DataFileError, match="Input should be a valid array"):
        read_measurements(path)


def test_read_measurements_rejects_broken_json(tmp_path: Path) -> None:
    with pytest.raises(DataFileError, match="Invalid JSON"):
        read_measurements(write(tmp_path, '[{"label": "Norte"'))


def test_read_measurements_keeps_the_validation_error_as_cause(tmp_path: Path) -> None:
    with pytest.raises(DataFileError) as caught:
        read_measurements(write(tmp_path, "[1]"))
    assert isinstance(caught.value.__cause__, ValidationError)


def test_read_measurements_of_a_missing_file(tmp_path: Path) -> None:
    with pytest.raises(DataFileError, match="no existe el archivo"):
        read_measurements(tmp_path / "no-existe.json")


def test_read_scale_returns_a_scale(tmp_path: Path) -> None:
    path = write(tmp_path, '{"unit": "µg/m³", "low": 10, "high": 50}')
    assert read_scale(path) == Scale("µg/m³", 10.0, 50.0)


def test_read_scale_runs_the_rule_of_the_model(tmp_path: Path) -> None:
    path = write(tmp_path, '{"unit": "µg/m³", "low": 50, "high": 10}')
    with pytest.raises(DataFileError, match="umbrales imposibles"):
        read_scale(path)


def test_read_scale_requires_every_field(tmp_path: Path) -> None:
    path = write(tmp_path, '{"unit": "µg/m³", "low": 10}')
    with pytest.raises(DataFileError, match="high: Field required"):
        read_scale(path)


def test_read_scale_rejects_a_text_threshold(tmp_path: Path) -> None:
    path = write(tmp_path, '{"unit": "µg/m³", "low": "diez", "high": 50}')
    with pytest.raises(DataFileError, match="low: Input should be a valid number"):
        read_scale(path)
