# Tus tests de la semana 36: sustituye este ejemplo por al menos 6 tests tuyos (paso 9).
# Usa los tipos y las frases de tus notas y las funciones de test_language.py (easy, write,
# outcome): una nota con una palabra que nunca vio el tokenizador, un tipo con pocas notas,
# dos notas iguales con tipos distintos, una nota nueva con --nota...
import pandas as pd

from observatorio.core.language import classify


def test_example_the_models_learn_two_kinds_of_notes() -> None:
    rows = [("Centro", "averia", f"el sensor {i} no responde") for i in range(15)]
    rows += [("Centro", "limpieza", f"se limpió el filtro {i}") for i in range(15)]
    notes = pd.DataFrame(rows, columns=["etiqueta", "tipo", "texto"])
    result, _, _ = classify(notes, size=60, epochs=30)
    assert result.improves
