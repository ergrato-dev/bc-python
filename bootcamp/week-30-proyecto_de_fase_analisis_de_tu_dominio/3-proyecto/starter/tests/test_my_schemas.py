# Tus tests de la semana 13: sustituye este ejemplo por al menos 6 tests tuyos (paso 14).
# Importa solo de observatorio.core y usa datos de tu dominio.
from observatorio.core import MeasurementIn


def test_example_measurement_in_parses_a_comma() -> None:
    assert MeasurementIn.model_validate({"label": "Norte", "value": "12,5"}).value == 12.5
