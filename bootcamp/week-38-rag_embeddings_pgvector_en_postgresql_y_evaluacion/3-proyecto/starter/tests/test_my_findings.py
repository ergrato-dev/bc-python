# Tus tests de la semana 30: sustituye este ejemplo por al menos 6 tests tuyos (paso 9).
# Usa las etiquetas y los valores de tu dominio y las funciones de test_findings.py
# (frame_of, write, finding): dos etiquetas de tu dominio que difieren y dos que no, una
# etiqueta de tu dominio con una sola medida que queda sin comparar, el informe con tu
# unidad, una huella que no coincide...
from test_findings import frame_of

from observatorio.core.findings import compare_all


def test_example_two_labels_far_apart_differ() -> None:
    rows = [("Norte", 10.0), ("Norte", 11.0), ("Norte", 12.0)]
    rows += [("Sur", 30.0), ("Sur", 31.0), ("Sur", 32.0)]
    (found,) = compare_all(frame_of(rows))
    assert found.p_adjusted < 0.05
