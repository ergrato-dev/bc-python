# Tus tests de la semana 32: sustituye este ejemplo por al menos 6 tests tuyos (paso 9).
# Usa las etiquetas y los valores de tu dominio y las funciones de test_validation.py
# (frame_of, signal, noise, write): una etiqueta de tu dominio que decide el valor y otra
# que no, una etiqueta que solo aparece al final con pliegues por tiempo, el comando con la
# huella de tu instantánea...
from test_validation import frame_of

from observatorio.core.validation import validate


def test_example_labels_that_decide_the_level_win_every_fold() -> None:
    rows = [("Norte", 5.0), ("Sur", 30.0), ("Centro", 70.0)] * 10
    assert validate(frame_of(rows), "nivel", 3).improves
