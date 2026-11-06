from hypothesis import example, given
from hypothesis import strategies as st

from codec import chunks, from_line, mean, to_line

# Números finitos: sin nan ni infinitos.
FINITE = st.floats(allow_nan=False, allow_infinity=False)


# ============================================
# PASO 1: Una propiedad: to_line y from_line son inversas
# ============================================
# Descomenta las siguientes líneas:
# @given(FINITE)
# def test_value_round_trips(value: float) -> None:
#     assert from_line(to_line("Norte", value)) == ("Norte", value)


# ============================================
# PASO 2: La misma propiedad con cualquier etiqueta
# ============================================
# Descomenta las siguientes líneas:
# @given(st.text(), FINITE)
# def test_any_label_round_trips(label: str, value: float) -> None:
#     assert from_line(to_line(label, value)) == (label, value)


# ============================================
# PASO 3: La etiqueta de verdad no lleva ";": la estrategia lo dice
# ============================================
# Descomenta las siguientes líneas:
# LABELS = st.text().filter(lambda text: ";" not in text)
#
#
# @given(LABELS, FINITE)
# def test_valid_label_round_trips(label: str, value: float) -> None:
#     assert from_line(to_line(label, value)) == (label, value)


# ============================================
# PASO 4: Dos propiedades de chunks: no pierde nada y ningún trozo se pasa
# ============================================
# Descomenta las siguientes líneas:
# @given(st.lists(st.integers()), st.integers(min_value=1, max_value=5))
# def test_chunks_keep_every_item(items: list[int], size: int) -> None:
#     pieces = chunks(items, size)
#     assert [item for piece in pieces for item in piece] == items
#     assert all(1 <= len(piece) <= size for piece in pieces)


# ============================================
# PASO 5: La media está entre el mínimo y el máximo... ¿siempre?
# ============================================
# Descomenta las siguientes líneas:
# @given(st.lists(FINITE, min_size=1))
# def test_mean_is_between_min_and_max(values: list[float]) -> None:
#     assert min(values) <= mean(values) <= max(values)


# ============================================
# PASO 6: El dominio real y un ejemplo que se prueba siempre
# ============================================
# Descomenta las siguientes líneas:
# READINGS = st.floats(min_value=0, max_value=1000)
#
#
# @given(st.lists(READINGS, min_size=1))
# @example([12.5])
# def test_mean_of_readings(values: list[float]) -> None:
#     average = mean(values)
#     assert min(values) - 1e-9 <= average <= max(values) + 1e-9
