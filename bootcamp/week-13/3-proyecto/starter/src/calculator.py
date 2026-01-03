"""
Calculadora Científica.

Módulo principal que implementa una calculadora con operaciones
básicas y científicas.
"""
import math
from typing import Any
from .memory import MemoryManager
from .history import HistoryManager


class CalculatorError(Exception):
    """Excepción base para errores de la calculadora."""

    pass


class ScientificCalculator:
    """
    Calculadora científica con memoria e historial.

    Soporta operaciones aritméticas básicas, funciones científicas,
    sistema de memoria y registro de historial.
    """

    def __init__(self) -> None:
        """Inicializa la calculadora con memoria e historial vacíos."""
        self._memory = MemoryManager()
        self._history = HistoryManager()

    # ==========================================
    # Operaciones Básicas
    # ==========================================

    def add(self, a: float, b: float) -> float:
        """
        Suma dos números.

        Args:
            a: Primer sumando
            b: Segundo sumando

        Returns:
            La suma de a y b
        """
        result = a + b
        self._history.record("add", {"a": a, "b": b}, result)
        return result

    def subtract(self, a: float, b: float) -> float:
        """
        Resta b de a.

        Args:
            a: Minuendo
            b: Sustraendo

        Returns:
            El resultado de a - b
        """
        result = a - b
        self._history.record("subtract", {"a": a, "b": b}, result)
        return result

    def multiply(self, a: float, b: float) -> float:
        """
        Multiplica dos números.

        Args:
            a: Primer factor
            b: Segundo factor

        Returns:
            El producto de a y b
        """
        result = a * b
        self._history.record("multiply", {"a": a, "b": b}, result)
        return result

    def divide(self, a: float, b: float) -> float:
        """
        Divide a entre b.

        Args:
            a: Dividendo
            b: Divisor

        Returns:
            El cociente de a / b

        Raises:
            ZeroDivisionError: Si b es cero
        """
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        result = a / b
        self._history.record("divide", {"a": a, "b": b}, result)
        return result

    # ==========================================
    # Operaciones Científicas
    # ==========================================

    def power(self, base: float, exponent: float) -> float:
        """
        Calcula base elevado a exponent.

        Args:
            base: La base
            exponent: El exponente

        Returns:
            base ^ exponent
        """
        result = math.pow(base, exponent)
        self._history.record("power", {"base": base, "exponent": exponent}, result)
        return result

    def sqrt(self, n: float) -> float:
        """
        Calcula la raíz cuadrada de n.

        Args:
            n: Número del cual calcular la raíz

        Returns:
            La raíz cuadrada de n

        Raises:
            ValueError: Si n es negativo
        """
        if n < 0:
            raise ValueError("Cannot calculate square root of negative number")
        result = math.sqrt(n)
        self._history.record("sqrt", {"n": n}, result)
        return result

    def factorial(self, n: int) -> int:
        """
        Calcula el factorial de n.

        Args:
            n: Número del cual calcular factorial

        Returns:
            n!

        Raises:
            ValueError: Si n es negativo o no es entero
        """
        if not isinstance(n, int):
            raise ValueError("Factorial requires an integer")
        if n < 0:
            raise ValueError("Factorial is not defined for negative numbers")
        result = math.factorial(n)
        self._history.record("factorial", {"n": n}, result)
        return result

    def sin(self, x: float) -> float:
        """
        Calcula el seno de x (en radianes).

        Args:
            x: Ángulo en radianes

        Returns:
            sin(x)
        """
        result = math.sin(x)
        self._history.record("sin", {"x": x}, result)
        return result

    def cos(self, x: float) -> float:
        """
        Calcula el coseno de x (en radianes).

        Args:
            x: Ángulo en radianes

        Returns:
            cos(x)
        """
        result = math.cos(x)
        self._history.record("cos", {"x": x}, result)
        return result

    def tan(self, x: float) -> float:
        """
        Calcula la tangente de x (en radianes).

        Args:
            x: Ángulo en radianes

        Returns:
            tan(x)
        """
        result = math.tan(x)
        self._history.record("tan", {"x": x}, result)
        return result

    def log(self, x: float, base: float = 10) -> float:
        """
        Calcula el logaritmo de x en la base especificada.

        Args:
            x: Número del cual calcular logaritmo
            base: Base del logaritmo (default: 10)

        Returns:
            log_base(x)

        Raises:
            ValueError: Si x <= 0 o base <= 0 o base == 1
        """
        if x <= 0:
            raise ValueError("Logarithm is not defined for non-positive numbers")
        if base <= 0 or base == 1:
            raise ValueError("Invalid logarithm base")
        result = math.log(x, base)
        self._history.record("log", {"x": x, "base": base}, result)
        return result

    def ln(self, x: float) -> float:
        """
        Calcula el logaritmo natural de x.

        Args:
            x: Número del cual calcular logaritmo natural

        Returns:
            ln(x)

        Raises:
            ValueError: Si x <= 0
        """
        if x <= 0:
            raise ValueError("Natural logarithm is not defined for non-positive numbers")
        result = math.log(x)
        self._history.record("ln", {"x": x}, result)
        return result

    # ==========================================
    # Sistema de Memoria
    # ==========================================

    def memory_store(self, value: float) -> None:
        """
        Guarda un valor en memoria.

        Args:
            value: Valor a guardar
        """
        self._memory.store(value)

    def memory_recall(self) -> float:
        """
        Recupera el valor de memoria.

        Returns:
            El valor almacenado en memoria

        Raises:
            ValueError: Si la memoria está vacía
        """
        return self._memory.recall()

    def memory_clear(self) -> None:
        """Limpia la memoria."""
        self._memory.clear()

    def memory_add(self, value: float) -> None:
        """
        Suma un valor a la memoria actual.

        Args:
            value: Valor a sumar
        """
        self._memory.add(value)

    # ==========================================
    # Historial
    # ==========================================

    def get_history(self) -> list[dict[str, Any]]:
        """
        Obtiene el historial de operaciones.

        Returns:
            Lista de operaciones realizadas
        """
        return self._history.get_all()

    def clear_history(self) -> None:
        """Limpia el historial de operaciones."""
        self._history.clear()

    def export_history(self, format: str = "json") -> str:
        """
        Exporta el historial en el formato especificado.

        Args:
            format: Formato de exportación ("json" o "csv")

        Returns:
            String con el historial formateado

        Raises:
            ValueError: Si el formato no es soportado
        """
        return self._history.export(format)
