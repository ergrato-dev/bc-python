"""Ejercicio 04: tests con pytest. Descomenta cada PASO cuando el README te lo pida y ejecuta:
    uv run pytest
"""

import pytest

from temperature import average, celsius_to_fahrenheit, classify_temperature, parse_celsius

# ============================================
# PASO 1: un test es una función test_* con assert
# ============================================
# pytest busca archivos test_*.py, ejecuta cada función test_* y mira si algún assert falla.
# Descomenta las siguientes líneas:
# def test_boiling_point() -> None:
#     assert celsius_to_fahrenheit(100) == 212


# ============================================
# PASO 2: leer un fallo, y comparar decimales con approx
# ============================================
# 36.6 °C son 97.88 °F... en papel. Ejecuta y lee qué dice pytest.
# Descomenta las siguientes líneas:
# def test_body_temperature() -> None:
#     assert celsius_to_fahrenheit(36.6) == 97.88


# ============================================
# PASO 3: comprobar que algo FALLA como debe
# ============================================
# pytest.raises pasa si el bloque lanza ese error, y falla si no lo lanza.
# Descomenta las siguientes líneas:
# def test_average() -> None:
#     assert average([10.0, 20.0, 30.0]) == 20.0
#
#
# def test_average_of_nothing_is_an_error() -> None:
#     with pytest.raises(ValueError, match="vacía"):
#         average([])


# ============================================
# PASO 4: un test, muchos casos, y los límites
# ============================================
# Los errores viven en los límites: prueba justo antes y justo en cada umbral.
# Descomenta las siguientes líneas:
# @pytest.mark.parametrize(
#     ("celsius", "expected"),
#     [(14.9, "frío"), (15.0, "templado"), (24.9, "templado"), (25.0, "calor"), (-3.0, "frío")],
# )
# def test_classify_temperature(celsius: float, expected: str) -> None:
#     assert classify_temperature(celsius) == expected


# ============================================
# PASO 5: preparar, actuar, comprobar
# ============================================
# Un test legible tiene tres partes separadas por una línea en blanco.
# Descomenta las siguientes líneas:
# def test_parse_celsius_with_comma_and_unit() -> None:
#     text = " 21,5 °C "
#
#     result = parse_celsius(text)
#
#     assert result == 21.5
#
#
# def test_parse_celsius_rejects_text() -> None:
#     with pytest.raises(ValueError):
#         parse_celsius("templado")
