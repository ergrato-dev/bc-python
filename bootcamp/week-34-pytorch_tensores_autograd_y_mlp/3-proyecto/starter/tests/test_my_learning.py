# Tus tests de la semana 31: sustituye este ejemplo por al menos 6 tests tuyos (paso 9).
# Usa las etiquetas y los valores de tu dominio y las funciones de test_learning.py
# (frame_of, write, signal): una etiqueta de tu dominio que decide el nivel y otra que no,
# un nivel de tu dominio con una sola medida, el comando con la huella de tu instantánea...
from test_learning import frame_of

from observatorio.core.learning import classify


def test_example_labels_that_decide_the_level_beat_the_baseline() -> None:
    rows = [("Norte", 5.0)] * 8 + [("Sur", 30.0)] * 8 + [("Centro", 70.0)] * 8
    assert classify(frame_of(rows)).improves
