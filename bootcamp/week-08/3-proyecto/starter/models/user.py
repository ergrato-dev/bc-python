"""
Clase User - Representa un usuario de la biblioteca.

TODO: Implementa esta clase siguiendo las instrucciones del README.
"""

from __future__ import annotations
import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .loan import Loan


class User:
    """Representa un usuario de la biblioteca."""

    # Atributos de clase
    total_users: int = 0
    MAX_LOANS: int = 3  # Máximo de préstamos simultáneos

    def __init__(self, name: str, email: str, user_id: str | None = None) -> None:
        """
        Inicializa un nuevo usuario.

        Args:
            name: Nombre completo
            email: Dirección de email
            user_id: ID único (se genera automáticamente si no se proporciona)
        """
        # TODO: Asignar user_id (usar generate_id() si no se proporciona)
        # TODO: Asignar name y email
        # TODO: Inicializar active_loans como lista vacía
        # TODO: Inicializar loan_history como lista vacía
        # TODO: Incrementar contador de clase
        pass

    def __str__(self) -> str:
        """
        Retorna representación legible.

        Formato: "Nombre (email)"
        """
        # TODO: Implementar
        pass

    def __repr__(self) -> str:
        """
        Retorna representación técnica.

        Formato: User(user_id='...', name='...', email='...')
        """
        # TODO: Implementar
        pass

    def __eq__(self, other: object) -> bool:
        """Compara igualdad por user_id."""
        # TODO: Implementar
        pass

    def __hash__(self) -> int:
        """Permite usar User en sets y como key de dict."""
        # TODO: Implementar
        pass

    def can_borrow(self) -> bool:
        """
        Verifica si el usuario puede pedir más préstamos.

        Un usuario puede tener máximo MAX_LOANS préstamos activos.

        Returns:
            True si puede pedir más préstamos
        """
        # TODO: Implementar
        pass

    def add_loan(self, loan: "Loan") -> None:
        """
        Agrega un préstamo a la lista de activos.

        Args:
            loan: Préstamo a agregar
        """
        # TODO: Agregar a active_loans
        # TODO: Agregar a loan_history
        pass

    def return_loan(self, loan: "Loan") -> bool:
        """
        Procesa la devolución de un préstamo.

        Args:
            loan: Préstamo a devolver

        Returns:
            True si se procesó correctamente
        """
        # TODO: Remover de active_loans si existe
        # TODO: Retornar True si se encontró y removió
        pass

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        """
        Factory method: crea un User desde un diccionario.

        Args:
            data: Dict con keys 'name', 'email', opcionalmente 'user_id'

        Returns:
            Nueva instancia de User
        """
        # TODO: Implementar
        pass

    @staticmethod
    def generate_id() -> str:
        """
        Genera un ID único para el usuario.

        Returns:
            String con formato 'USR-XXXXXXXX'
        """
        # TODO: Usar uuid.uuid4() para generar ID único
        # Formato: "USR-" + primeros 8 caracteres del UUID
        pass
