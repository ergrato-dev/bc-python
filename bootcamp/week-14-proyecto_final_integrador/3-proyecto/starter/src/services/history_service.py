"""
Servicio de Historial.

Este módulo gestiona el historial de búsquedas del usuario.
"""

import logging
from datetime import datetime
from typing import Any, Protocol

from src.storage.json_storage import JsonStorage
from src.models.weather import Weather

logger = logging.getLogger(__name__)


class StorageProtocol(Protocol):
    """Protocolo para el storage (para testing)."""

    def load(self) -> list: ...
    def save(self, data: list) -> None: ...


class HistoryEntry:
    """
    Entrada individual del historial.

    Attributes:
        city: Ciudad consultada.
        country: País de la ciudad.
        temperature: Temperatura al momento de la consulta.
        timestamp: Momento de la consulta.
    """

    def __init__(
        self,
        city: str,
        country: str,
        temperature: float,
        timestamp: datetime | None = None,
    ) -> None:
        """
        Inicializa una entrada de historial.

        Args:
            city: Ciudad consultada.
            country: País de la ciudad.
            temperature: Temperatura registrada.
            timestamp: Momento de la consulta.
        """
        self.city = city
        self.country = country
        self.temperature = temperature
        self.timestamp = timestamp or datetime.now()

    @classmethod
    def from_weather(cls, weather: Weather) -> "HistoryEntry":
        """
        Crea una entrada desde un objeto Weather.

        Args:
            weather: Datos del clima.

        Returns:
            Entrada de historial.
        """
        # TODO: Implementar
        pass

    def to_dict(self) -> dict[str, Any]:
        """Convierte a diccionario para JSON."""
        # TODO: Implementar
        pass

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "HistoryEntry":
        """Crea desde diccionario JSON."""
        # TODO: Implementar
        pass


class HistoryService:
    """
    Servicio para gestionar el historial de búsquedas.

    Attributes:
        storage: Sistema de almacenamiento.
        max_entries: Número máximo de entradas a mantener.
        entries: Lista de entradas en memoria.
    """

    DEFAULT_MAX_ENTRIES = 50

    def __init__(
        self,
        storage: StorageProtocol | None = None,
        data_dir: str = "data",
        max_entries: int = DEFAULT_MAX_ENTRIES,
    ) -> None:
        """
        Inicializa el servicio de historial.

        Args:
            storage: Sistema de almacenamiento.
            data_dir: Directorio para archivos.
            max_entries: Máximo de entradas a guardar.
        """
        # TODO: Implementar
        pass

    def _load_entries(self) -> list[HistoryEntry]:
        """Carga las entradas desde storage."""
        # TODO: Implementar
        pass

    def _save_entries(self) -> None:
        """Guarda las entradas en storage."""
        # TODO: Implementar
        pass

    def add(self, weather: Weather) -> None:
        """
        Añade una consulta al historial.

        Args:
            weather: Datos del clima consultado.
        """
        # TODO: Implementar
        # 1. Crear entrada desde Weather
        # 2. Añadir al inicio de la lista
        # 3. Truncar si excede max_entries
        # 4. Guardar
        pass

    def get_recent(self, limit: int = 10) -> list[HistoryEntry]:
        """
        Obtiene las consultas más recientes.

        Args:
            limit: Número máximo de entradas.

        Returns:
            Lista de entradas ordenadas por fecha descendente.
        """
        # TODO: Implementar
        pass

    def clear(self) -> int:
        """
        Limpia todo el historial.

        Returns:
            Número de entradas eliminadas.
        """
        # TODO: Implementar
        pass

    def count(self) -> int:
        """
        Cuenta las entradas en el historial.

        Returns:
            Número de entradas.
        """
        # TODO: Implementar
        pass
