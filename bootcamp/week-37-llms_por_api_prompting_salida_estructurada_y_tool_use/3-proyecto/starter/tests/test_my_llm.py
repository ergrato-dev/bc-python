# Tus tests de la semana 37: sustituye este ejemplo por al menos 6 tests tuyos (paso 11).
# Usa los tipos y las frases de tus notas y las funciones de test_llm.py (easy, write, fake,
# message, client_for): una respuesta cortada, un tipo que no existe, el coste de tus notas,
# una nota con instrucciones dentro, una grabación que no tiene la petición...
import pytest

from observatorio.core.llm import Report


def test_example_a_thousand_notes_cost_about_one_dollar() -> None:
    # 470 tokens de entrada y 30 de salida por nota, con los precios de Sonnet 5.5.
    assert Report((), input_tokens=1000 * 470, output_tokens=1000 * 30).cost == pytest.approx(1.24)
