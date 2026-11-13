# Tus tests de la semana 34: sustituye este ejemplo por al menos 6 tests tuyos (paso 10).
# Usa las etiquetas y los valores de tu dominio y las funciones de test_validation.py
# (frame_of, signal, noise, write), de test_ensembles.py (bump) y de test_neural.py (line):
# una red que aprende tus etiquetas, una que memoriza ruido, un ritmo demasiado alto...
from test_validation import frame_of

from observatorio.core.neural import learn


def test_example_the_network_learns_clean_and_dirty_labels() -> None:
    rows = [("Norte", 8.0), ("Oeste", 9.0), ("Centro", 60.0), ("Sur", 61.0)] * 30
    training = learn(frame_of(rows))
    assert training.improves
