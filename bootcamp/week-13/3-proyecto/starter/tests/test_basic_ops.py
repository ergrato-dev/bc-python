"""
Tests para operaciones básicas de la calculadora.

TODO: Completa los tests siguiendo las instrucciones.
"""
import pytest
from src.calculator import ScientificCalculator


class TestAddition:
    """Tests para la operación de suma."""

    # TODO: Implementa tests para add()
    # Casos a cubrir:
    # - Suma de dos números positivos
    # - Suma de dos números negativos
    # - Suma con cero
    # - Suma de flotantes
    # - Suma de números grandes

    def test_add_positive_numbers(self, calculator):
        """Test suma de números positivos."""
        # TODO: Implementar
        pass

    @pytest.mark.parametrize("a, b, expected", [
        # TODO: Agregar casos de prueba
        # (valor_a, valor_b, resultado_esperado),
    ])
    def test_add_parametrized(self, calculator, a, b, expected):
        """Test suma con múltiples casos."""
        # TODO: Implementar
        pass


class TestSubtraction:
    """Tests para la operación de resta."""

    # TODO: Implementa tests para subtract()
    # Casos a cubrir:
    # - Resta con resultado positivo
    # - Resta con resultado negativo
    # - Resta con resultado cero
    # - Resta de flotantes

    def test_subtract_positive_result(self, calculator):
        """Test resta con resultado positivo."""
        # TODO: Implementar
        pass


class TestMultiplication:
    """Tests para la operación de multiplicación."""

    # TODO: Implementa tests para multiply()
    # Casos a cubrir:
    # - Multiplicación de positivos
    # - Multiplicación con negativos
    # - Multiplicación por cero
    # - Multiplicación por uno

    def test_multiply_positive_numbers(self, calculator):
        """Test multiplicación de positivos."""
        # TODO: Implementar
        pass


class TestDivision:
    """Tests para la operación de división."""

    # TODO: Implementa tests para divide()
    # Casos a cubrir:
    # - División exacta
    # - División con decimales
    # - División por cero (debe lanzar ZeroDivisionError)
    # - División de cero entre otro número

    def test_divide_exact(self, calculator):
        """Test división exacta."""
        # TODO: Implementar
        pass

    def test_divide_by_zero_raises_error(self, calculator):
        """Test que división por cero lanza ZeroDivisionError."""
        # TODO: Implementar usando pytest.raises
        pass
