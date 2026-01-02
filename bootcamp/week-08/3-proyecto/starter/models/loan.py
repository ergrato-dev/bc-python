"""
Clase Loan - Representa un préstamo de libro.

TODO: Implementa esta clase siguiendo las instrucciones del README.
"""

from __future__ import annotations
import uuid
from datetime import date, timedelta
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .book import Book
    from .user import User


class Loan:
    """Representa un préstamo de libro."""

    # Días de préstamo por defecto
    DEFAULT_LOAN_DAYS: int = 14

    def __init__(
        self,
        book: "Book",
        user: "User",
        loan_days: int | None = None
    ) -> None:
        """
        Inicializa un nuevo préstamo.

        Args:
            book: Libro a prestar
            user: Usuario que solicita el préstamo
            loan_days: Días de préstamo (usa DEFAULT_LOAN_DAYS si no se especifica)
        """
        # TODO: Generar loan_id usando generate_loan_id()
        # TODO: Asignar book y user
        # TODO: Asignar loan_date como fecha de hoy
        # TODO: Calcular due_date (loan_date + loan_days)
        # TODO: Inicializar return_date como None
        # TODO: Inicializar is_returned como False
        pass

    def __str__(self) -> str:
        """
        Retorna representación legible.

        Formato: "Préstamo: 'Título' a Usuario (vence: YYYY-MM-DD)"
        """
        # TODO: Implementar
        pass

    def __repr__(self) -> str:
        """
        Retorna representación técnica.

        Formato: Loan(loan_id='...', book='...', user='...', due_date=...)
        """
        # TODO: Implementar
        pass

    def is_overdue(self) -> bool:
        """
        Verifica si el préstamo está vencido.

        Un préstamo está vencido si:
        - No ha sido devuelto Y
        - La fecha actual es posterior a due_date

        Returns:
            True si está vencido
        """
        # TODO: Implementar
        pass

    def days_until_due(self) -> int:
        """
        Calcula los días hasta el vencimiento.

        Returns:
            Días restantes (negativo si está vencido)
        """
        # TODO: Implementar
        # Si ya fue devuelto, retornar 0
        # Si no, calcular diferencia entre due_date y hoy
        pass

    def complete_return(self) -> None:
        """
        Marca el préstamo como devuelto.

        Actualiza:
        - return_date con la fecha actual
        - is_returned a True
        """
        # TODO: Implementar
        pass

    @staticmethod
    def generate_loan_id() -> str:
        """
        Genera un ID único para el préstamo.

        Returns:
            String con formato 'LOAN-XXXXXXXX'
        """
        # TODO: Usar uuid.uuid4() para generar ID único
        # Formato: "LOAN-" + primeros 8 caracteres del UUID
        pass
