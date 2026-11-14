# Tus tests de la semana 38: sustituye este ejemplo por al menos 6 tests tuyos (paso 9).
# Usa las frases de tus notas y las funciones de test_rag.py (notes, hit, fake) y de
# test_llm.py (write, client_for): una búsqueda con las palabras de tu dominio, un empate,
# una pregunta que tus notas no responden, una cita inventada, una nota con instrucciones...
from observatorio.core.rag import Hit, vote


def test_example_one_close_note_does_not_outvote_two_farther_ones() -> None:
    hits = [
        Hit(1, "Norte", "limpieza", "filtro con polvo", 0.05),
        Hit(2, "Norte", "averia", "equipo apagado", 0.30),
        Hit(3, "Sur", "averia", "equipo roto", 0.35),
    ]
    assert vote(hits) == "averia"
