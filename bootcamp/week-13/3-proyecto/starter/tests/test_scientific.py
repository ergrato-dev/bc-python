"""
Tests para operaciones científicas de la calculadora.

TODO: Completa los tests siguiendo las instrucciones.
"""
import pytest
import math
from src.calculator import ScientificCalculator


class TestPower:
    """Tests para la función power."""

    # TODO: Implementa tests para power()
    # Casos a cubrir:
    # - Potencia con exponente positivo
    # - Potencia con exponente cero
    # - Potencia con exponente negativo
    # - Base cero
    # - Base negativa

    def test_power_positive_exponent(self, calculator):
        """Test potencia con exponente positivo."""
        # TODO: Implementar
        pass


class TestSquareRoot:
    """Tests para la función sqrt."""

    # TODO: Implementa tests para sqrt()
    # Casos a cubrir:
    # - Raíz de número positivo
    # - Raíz de cero
    # - Raíz de cuadrado perfecto
    # - Raíz de número negativo (debe lanzar ValueError)

    def test_sqrt_positive(self, calculator):
        """Test raíz de número positivo."""
        # TODO: Implementar
        pass

    def test_sqrt_negative_raises_error(self, calculator):
        """Test que raíz de negativo lanza ValueError."""
        # TODO: Implementar usando pytest.raises
        pass


class TestFactorial:
    """Tests para la función factorial."""

    # TODO: Implementa tests para factorial()
    # Casos a cubrir:
    # - Factorial de 0 (debe ser 1)
    # - Factorial de 1
    # - Factorial de número pequeño
    # - Factorial de número negativo (ValueError)
    # - Factorial de flotante (ValueError)

    @pytest.mark.parametrize("n, expected", [
        # TODO: Agregar casos
        # (0, 1),
        # (1, 1),
        # etc.
    ])
    def test_factorial_valid(self, calculator, n, expected):
        """Test factorial con valores válidos."""
        # TODO: Implementar
        pass

    def test_factorial_negative_raises_error(self, calculator):
        """Test que factorial de negativo lanza ValueError."""
        # TODO: Implementar
        pass


class TestTrigonometry:
    """Tests para funciones trigonométricas."""

    # TODO: Implementa tests para sin(), cos(), tan()
    # Casos a cubrir:
    # - sin(0) = 0
    # - sin(π/2) = 1
    # - cos(0) = 1
    # - cos(π) = -1
    # - tan(0) = 0

    def test_sin_zero(self, calculator):
        """Test seno de cero."""
        # TODO: Implementar
        pass

    def test_cos_zero(self, calculator):
        """Test coseno de cero."""
        # TODO: Implementar
        pass


class TestLogarithms:
    """Tests para funciones logarítmicas."""

    # TODO: Implementa tests para log() y ln()
    # Casos a cubrir:
    # - log base 10 de 100 = 2
    # - log base 2 de 8 = 3
    # - ln(e) = 1
    # - log de número <= 0 (ValueError)
    # - log con base inválida (ValueError)

    def test_log_base_10(self, calculator):
        """Test logaritmo base 10."""
        # TODO: Implementar
        pass

    def test_ln_of_e(self, calculator):
        """Test logaritmo natural de e."""
        # TODO: Implementar - usar pytest.approx
        pass

    def test_log_non_positive_raises_error(self, calculator):
        """Test que log de no positivo lanza ValueError."""
        # TODO: Implementar
        pass
