# Tus tests de la semana 33: sustituye este ejemplo por al menos 6 tests tuyos (paso 9).
# Usa las etiquetas y los valores de tu dominio y las funciones de test_validation.py
# (frame_of, signal, noise, write) y de test_ensembles.py (bump): un valor que cambia con
# la posición sin seguir una recta, dos grupos de etiquetas de tu dominio que se separan,
# el comando con la huella de tu instantánea...
from test_validation import frame_of

from observatorio.core.clustering import cluster


def test_example_clean_and_dirty_labels_make_two_groups() -> None:
    rows = [("Norte", 8.0), ("Norte", 10.0), ("Oeste", 9.0), ("Oeste", 11.0)]
    rows += [("Centro", 60.0), ("Centro", 62.0), ("Sur", 59.0), ("Sur", 61.0)]
    groups = cluster(frame_of(rows), 2).groups
    assert groups["Norte"] == groups["Oeste"] != groups["Centro"] == groups["Sur"]
