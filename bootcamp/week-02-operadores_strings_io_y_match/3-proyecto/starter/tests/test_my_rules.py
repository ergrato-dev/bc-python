"""Tus tests, con valores de TU dominio calculados a mano (paso 9).

Escribe al menos 6. Este primero es un modelo: cámbialo por uno tuyo.
"""

from observatorio.rules import classify


def test_example_limit_of_my_domain() -> None:
    assert classify(10.0, 10.0, 50.0) == "medio"
