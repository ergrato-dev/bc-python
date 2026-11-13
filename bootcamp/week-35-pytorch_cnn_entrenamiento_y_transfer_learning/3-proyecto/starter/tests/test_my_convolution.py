# Tus tests de la semana 35: sustituye este ejemplo por al menos 6 tests tuyos (paso 9).
# Usa las etiquetas y los valores de tu dominio y las funciones de test_validation.py
# (frame_of, noise, write) y de test_convolution.py (wave, two_labels): una serie que se
# repite, una que no, una etiqueta con pocos valores, unos pesos guardados y reutilizados...
from test_validation import frame_of

from observatorio.core.convolution import forecast


def test_example_the_network_follows_a_daily_cycle() -> None:
    day = [10.0, 12.0, 30.0, 55.0, 60.0, 35.0, 20.0, 14.0]
    result, _ = forecast(frame_of([("Centro", value) for value in day * 25]))
    assert result.improves
