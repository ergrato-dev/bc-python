"""
Módulo de gestión de usuarios para practicar fixtures y parametrización.
"""
from dataclasses import dataclass, field
from datetime import datetime
import re


@dataclass
class User:
    """Representa un usuario del sistema."""

    name: str
    email: str
    role: str = "user"
    id: int | None = None
    created_at: datetime = field(default_factory=datetime.now)

    def is_admin(self) -> bool:
        """Verifica si el usuario es administrador."""
        return self.role == "admin"

    def get_display_name(self) -> str:
        """Retorna el nombre para mostrar."""
        prefix = "[Admin] " if self.is_admin() else ""
        return f"{prefix}{self.name}"


class UserManager:
    """Gestiona operaciones CRUD de usuarios."""

    def __init__(self) -> None:
        self._users: dict[int, User] = {}
        self._next_id: int = 1

    def create(self, name: str, email: str, role: str = "user") -> User:
        """
        Crea un nuevo usuario.

        Args:
            name: Nombre del usuario
            email: Email del usuario
            role: Rol del usuario (default: "user")

        Returns:
            El usuario creado

        Raises:
            ValueError: Si el email es inválido o ya existe
        """
        if not self.validate_email(email):
            raise ValueError(f"Invalid email: {email}")

        if self.find_by_email(email):
            raise ValueError(f"Email already exists: {email}")

        user = User(
            id=self._next_id,
            name=name,
            email=email,
            role=role,
        )
        self._users[user.id] = user
        self._next_id += 1

        return user

    def get(self, user_id: int) -> User | None:
        """Obtiene un usuario por ID."""
        return self._users.get(user_id)

    def find_by_email(self, email: str) -> User | None:
        """Busca un usuario por email."""
        for user in self._users.values():
            if user.email == email:
                return user
        return None

    def update(self, user_id: int, **kwargs) -> User:
        """
        Actualiza un usuario.

        Args:
            user_id: ID del usuario a actualizar
            **kwargs: Campos a actualizar (name, email, role)

        Returns:
            El usuario actualizado

        Raises:
            ValueError: Si el usuario no existe
        """
        user = self.get(user_id)
        if not user:
            raise ValueError(f"User not found: {user_id}")

        for key, value in kwargs.items():
            if hasattr(user, key) and key not in ("id", "created_at"):
                if key == "email" and not self.validate_email(value):
                    raise ValueError(f"Invalid email: {value}")
                setattr(user, key, value)

        return user

    def delete(self, user_id: int) -> bool:
        """
        Elimina un usuario.

        Args:
            user_id: ID del usuario a eliminar

        Returns:
            True si se eliminó, False si no existía
        """
        if user_id in self._users:
            del self._users[user_id]
            return True
        return False

    def list_all(self) -> list[User]:
        """Retorna todos los usuarios."""
        return list(self._users.values())

    def count(self) -> int:
        """Retorna el número de usuarios."""
        return len(self._users)

    def list_by_role(self, role: str) -> list[User]:
        """Retorna usuarios con un rol específico."""
        return [u for u in self._users.values() if u.role == role]

    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Valida formato de email.

        Args:
            email: Email a validar

        Returns:
            True si es válido, False si no
        """
        if not email:
            return False
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))

    @staticmethod
    def validate_name(name: str) -> bool:
        """
        Valida nombre de usuario.

        Args:
            name: Nombre a validar

        Returns:
            True si es válido (2-50 caracteres), False si no
        """
        return bool(name) and 2 <= len(name.strip()) <= 50
