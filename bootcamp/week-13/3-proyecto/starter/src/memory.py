"""
Sistema de memoria para la calculadora.
"""


class MemoryManager:
    """Gestiona la memoria de la calculadora."""

    def __init__(self) -> None:
        """Inicializa la memoria vacía."""
        self._value: float | None = None

    def store(self, value: float) -> None:
        """
        Guarda un valor en memoria.

        Args:
            value: Valor a guardar
        """
        self._value = value

    def recall(self) -> float:
        """
        Recupera el valor de memoria.

        Returns:
            El valor almacenado

        Raises:
            ValueError: Si la memoria está vacía
        """
        if self._value is None:
            raise ValueError("Memory is empty")
        return self._value

    def clear(self) -> None:
        """Limpia la memoria."""
        self._value = None

    def add(self, value: float) -> None:
        """
        Suma un valor a la memoria actual.

        Si la memoria está vacía, equivale a store.

        Args:
            value: Valor a sumar
        """
        if self._value is None:
            self._value = value
        else:
            self._value += value

    def is_empty(self) -> bool:
        """
        Verifica si la memoria está vacía.

        Returns:
            True si está vacía, False si tiene valor
        """
        return self._value is None
