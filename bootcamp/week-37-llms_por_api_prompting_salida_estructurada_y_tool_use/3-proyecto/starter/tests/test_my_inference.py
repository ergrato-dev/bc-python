# Tus tests de la semana 28: sustituye este ejemplo por al menos 6 tests tuyos (paso 11).
# Usa los valores de tu dominio y las funciones de test_inference.py (floats, write,
# comparar): dos etiquetas de tu dominio que deberían ser distintas, dos que no, una
# diferencia que solo se ve con muchas medidas, una medida extrema que mueve a Welch y no
# a Mann-Whitney...
from test_inference import floats

from observatorio.core.inference import difference


def test_example_the_difference_is_first_minus_second() -> None:
    assert difference(floats(12.5, 14.0, 13.0), floats(8.0, 9.5, 8.5)).difference == 4.5
