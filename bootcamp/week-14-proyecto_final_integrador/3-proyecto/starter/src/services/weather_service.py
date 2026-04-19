"""
Servicio de Clima.

Este módulo contiene la lógica de negocio para
obtener información meteorológica.
"""

import logging
from typing import Protocol

from src.api.client import WeatherClient
from src.models.weather import Weather
from src.models.forecast import Forecast

logger = logging.getLogger(__name__)


class WeatherClientProtocol(Protocol):
    """Protocolo para el cliente de clima (para testing)."""

    def get_current_weather(self, city: str) -> dict: ...
    def get_forecast(self, city: str) -> dict: ...


class WeatherService:
    """
    Servicio para obtener información meteorológica.

    Actúa como intermediario entre la CLI y el cliente de API,
    transformando las respuestas en modelos de dominio.

    Attributes:
        client: Cliente de API para comunicación con OpenWeatherMap.
    """

    def __init__(self, client: WeatherClientProtocol | None = None) -> None:
        """
        Inicializa el servicio de clima.

        Args:
            client: Cliente de API. Si es None, crea uno por defecto.
        """
        # TODO: Implementar
        # Usar inyección de dependencias
        pass

    def get_current_weather(self, city: str) -> Weather:
        """
        Obtiene el clima actual de una ciudad.

        Args:
            city: Nombre de la ciudad.

        Returns:
            Objeto Weather con los datos del clima.

        Raises:
            CityNotFoundError: Si la ciudad no existe.
            APIError: Si hay error en la API.
        """
        # TODO: Implementar
        # 1. Llamar al cliente
        # 2. Convertir respuesta a modelo Weather
        # 3. Loggear resultado
        pass

    def get_forecast(self, city: str, days: int = 5) -> Forecast:
        """
        Obtiene el pronóstico de una ciudad.

        Args:
            city: Nombre de la ciudad.
            days: Número de días (máx. 5).

        Returns:
            Objeto Forecast con el pronóstico.

        Raises:
            CityNotFoundError: Si la ciudad no existe.
            APIError: Si hay error en la API.
        """
        # TODO: Implementar
        pass

    def get_weather_for_cities(self, cities: list[str]) -> list[Weather]:
        """
        Obtiene el clima de múltiples ciudades.

        Args:
            cities: Lista de nombres de ciudades.

        Returns:
            Lista de objetos Weather (omite ciudades con error).
        """
        # TODO: Implementar
        # Útil para consultar favoritos
        pass
