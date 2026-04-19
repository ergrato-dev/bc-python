"""
Fixtures compartidas para todos los tests del proyecto.
"""
import pytest
from src.calculator import ScientificCalculator
from src.memory import MemoryManager
from src.history import HistoryManager


@pytest.fixture
def calculator() -> ScientificCalculator:
    """
    Provee una instancia limpia de la calculadora.

    Esta fixture se ejecuta antes de cada test,
    garantizando que cada test tiene una calculadora nueva.
    """
    return ScientificCalculator()


@pytest.fixture
def memory() -> MemoryManager:
    """Provee una instancia limpia del gestor de memoria."""
    return MemoryManager()


@pytest.fixture
def history() -> HistoryManager:
    """Provee una instancia limpia del gestor de historial."""
    return HistoryManager()


@pytest.fixture
def calculator_with_history(calculator: ScientificCalculator) -> ScientificCalculator:
    """
    Provee una calculadora con algunas operaciones en el historial.

    Útil para tests que necesitan historial pre-existente.
    """
    calculator.add(10, 5)
    calculator.subtract(20, 8)
    calculator.multiply(3, 4)
    return calculator


@pytest.fixture
def calculator_with_memory(calculator: ScientificCalculator) -> ScientificCalculator:
    """
    Provee una calculadora con un valor en memoria.

    El valor inicial en memoria es 100.
    """
    calculator.memory_store(100)
    return calculator
