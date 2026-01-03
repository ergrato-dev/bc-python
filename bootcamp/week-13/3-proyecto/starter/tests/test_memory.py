"""
Tests para el sistema de memoria de la calculadora.

TODO: Completa los tests siguiendo las instrucciones.
"""
import pytest
from src.calculator import ScientificCalculator
from src.memory import MemoryManager


class TestMemoryBasic:
    """Tests básicos del sistema de memoria."""

    # TODO: Implementa tests para memory_store(), memory_recall(), memory_clear()
    # Casos a cubrir:
    # - Guardar y recuperar un valor
    # - Recuperar memoria vacía (ValueError)
    # - Limpiar memoria

    def test_store_and_recall(self, calculator):
        """Test guardar y recuperar de memoria."""
        # TODO: Implementar
        pass

    def test_recall_empty_memory_raises_error(self, calculator):
        """Test que recuperar memoria vacía lanza ValueError."""
        # TODO: Implementar
        pass

    def test_clear_memory(self, calculator_with_memory):
        """Test limpiar memoria."""
        # TODO: Implementar usando la fixture calculator_with_memory
        pass


class TestMemoryAdd:
    """Tests para memory_add."""

    # TODO: Implementa tests para memory_add()
    # Casos a cubrir:
    # - Sumar a memoria existente
    # - Sumar a memoria vacía (debe inicializar)

    def test_memory_add_to_existing(self, calculator_with_memory):
        """Test sumar a memoria existente."""
        # TODO: La memoria tiene 100, sumar algo y verificar
        pass

    def test_memory_add_to_empty(self, calculator):
        """Test sumar a memoria vacía."""
        # TODO: Implementar
        pass


class TestMemoryManagerDirect:
    """Tests directos del MemoryManager."""

    # Estos tests prueban el MemoryManager directamente,
    # sin pasar por la calculadora.

    def test_is_empty_initially(self, memory):
        """Test que memoria empieza vacía."""
        # TODO: Implementar
        pass

    def test_is_not_empty_after_store(self, memory):
        """Test que memoria no está vacía después de store."""
        # TODO: Implementar
        pass
