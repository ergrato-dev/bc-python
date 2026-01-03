"""
Tests para el sistema de historial de la calculadora.

TODO: Completa los tests siguiendo las instrucciones.
"""
import pytest
import json
from src.calculator import ScientificCalculator
from src.history import HistoryManager


class TestHistoryRecording:
    """Tests para el registro de operaciones."""

    # TODO: Implementa tests para verificar que las operaciones
    # se registran correctamente en el historial.

    def test_operation_recorded(self, calculator):
        """Test que una operación se registra en el historial."""
        # TODO: Realizar una operación y verificar que está en historial
        pass

    def test_history_contains_operands_and_result(self, calculator):
        """Test que el historial contiene operandos y resultado."""
        # TODO: Verificar estructura del historial
        pass

    def test_multiple_operations_recorded(self, calculator):
        """Test que múltiples operaciones se registran."""
        # TODO: Realizar varias operaciones y verificar cantidad
        pass


class TestHistoryClear:
    """Tests para limpiar historial."""

    def test_clear_history(self, calculator_with_history):
        """Test limpiar historial."""
        # TODO: Usar fixture calculator_with_history, limpiar y verificar
        pass


class TestHistoryExport:
    """Tests para exportar historial."""

    # TODO: Implementa tests para export_history()
    # Casos a cubrir:
    # - Exportar a JSON
    # - Exportar a CSV
    # - Formato no soportado (ValueError)

    def test_export_json(self, calculator_with_history):
        """Test exportar a JSON."""
        # TODO: Exportar y verificar que es JSON válido
        pass

    def test_export_csv(self, calculator_with_history):
        """Test exportar a CSV."""
        # TODO: Exportar y verificar formato CSV
        pass

    def test_export_invalid_format_raises_error(self, calculator):
        """Test que formato inválido lanza ValueError."""
        # TODO: Implementar
        pass


class TestHistoryManagerDirect:
    """Tests directos del HistoryManager."""

    def test_count_starts_at_zero(self, history):
        """Test que historial empieza vacío."""
        # TODO: Implementar
        pass

    def test_record_increases_count(self, history):
        """Test que record aumenta el contador."""
        # TODO: Implementar
        pass

    def test_get_last(self, history):
        """Test obtener últimas n entradas."""
        # TODO: Registrar varias operaciones y usar get_last
        pass

    def test_filter_by_operation(self, history):
        """Test filtrar por tipo de operación."""
        # TODO: Registrar diferentes operaciones y filtrar
        pass
