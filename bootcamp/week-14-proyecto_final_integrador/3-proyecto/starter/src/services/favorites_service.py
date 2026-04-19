"""
Servicio de Favoritos.

Este módulo gestiona las ciudades favoritas del usuario,
incluyendo persistencia en JSON.
"""

import logging
from typing import Protocol

from src.storage.json_storage import JsonStorage

logger = logging.getLogger(__name__)


class StorageProtocol(Protocol):
    """Protocolo para el storage (para testing)."""

    def load(self) -> list: ...
    def save(self, data: list) -> None: ...


class FavoritesService:
    """
    Servicio para gestionar ciudades favoritas.

    Proporciona operaciones CRUD para la lista de favoritos
    con persistencia automática en archivo JSON.

    Attributes:
        storage: Sistema de almacenamiento.
        favorites: Lista de ciudades favoritas en memoria.
    """

    def __init__(
        self,
        storage: StorageProtocol | None = None,
        data_dir: str = "data",
    ) -> None:
        """
        Inicializa el servicio de favoritos.

        Args:
            storage: Sistema de almacenamiento. Si es None, crea JsonStorage.
            data_dir: Directorio para archivos de datos.
        """
        # TODO: Implementar
        # 1. Crear storage si no se proporciona
        # 2. Cargar favoritos existentes
        pass

    def _load_favorites(self) -> list[str]:
        """
        Carga los favoritos desde el storage.

        Returns:
            Lista de ciudades favoritas.
        """
        # TODO: Implementar
        pass

    def _save_favorites(self) -> None:
        """Guarda los favoritos en el storage."""
        # TODO: Implementar
        pass

    def add(self, city: str) -> bool:
        """
        Añade una ciudad a favoritos.

        Args:
            city: Nombre de la ciudad.

        Returns:
            True si se añadió, False si ya existía.
        """
        # TODO: Implementar
        # 1. Normalizar nombre (capitalizar)
        # 2. Verificar si ya existe
        # 3. Añadir y guardar
        pass

    def remove(self, city: str) -> bool:
        """
        Elimina una ciudad de favoritos.

        Args:
            city: Nombre de la ciudad.

        Returns:
            True si se eliminó, False si no existía.
        """
        # TODO: Implementar
        pass

    def list_all(self) -> list[str]:
        """
        Lista todas las ciudades favoritas.

        Returns:
            Lista de ciudades (copia para evitar modificación).
        """
        # TODO: Implementar
        pass

    def exists(self, city: str) -> bool:
        """
        Verifica si una ciudad está en favoritos.

        Args:
            city: Nombre de la ciudad.

        Returns:
            True si está en favoritos.
        """
        # TODO: Implementar
        pass

    def clear(self) -> int:
        """
        Elimina todos los favoritos.

        Returns:
            Número de favoritos eliminados.
        """
        # TODO: Implementar
        pass
