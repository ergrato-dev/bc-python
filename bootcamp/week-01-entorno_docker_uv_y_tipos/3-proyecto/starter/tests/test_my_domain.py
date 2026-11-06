"""Tus tests, con valores de TU dominio calculados a mano (paso 9).

Escribe al menos 5. Este primero es un modelo: cámbialo por uno tuyo.
"""

from observatorio.record import describe_record, parse_value


def test_example_reading_of_my_domain() -> None:
    assert describe_record("Ejemplo A", parse_value("12,5"), "unidad") == "Ejemplo A: 12.5 unidad"
