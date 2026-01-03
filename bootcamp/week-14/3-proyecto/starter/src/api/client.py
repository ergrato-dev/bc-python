"""
Cliente HTTP para OpenWeatherMap API.

Este módulo implementa el cliente que se comunica con
la API de OpenWeatherMap para obtener datos meteorológicos.
"""

import logging
from typing import Any

import requests

from src.api.exceptions import (
    APIError,
    CityNotFoundError,
    ConnectionError,
    InvalidAPIKeyError,
    RateLimitError,
)
from src.utils.config import Config

logger = logging.getLogger(__name__)


class WeatherClient:
    """
    Cliente HTTP para la API de OpenWeatherMap.

    Maneja todas las comunicaciones con la API externa,
    incluyendo autenticación, timeouts y manejo de errores.

    Attributes:
        base_url: URL base de la API.
        api_key: Clave de autenticación.
        timeout: Timeout para requests en segundos.
    """

    def __init__(self, config: Config | None = None) -> None:
        """
        Inicializa el cliente de API.

        Args:
            config: Configuración de la aplicación. Si es None,
                   carga la configuración por defecto.
        """
        # TODO: Implementar inicialización
        # 1. Cargar configuración si no se proporciona
        # 2. Extraer api_key, base_url, timeout
        # 3. Crear sesión de requests
        pass

    def _create_session(self) -> requests.Session:
        """
        Crea una sesión de requests configurada.

        Returns:
            Sesión de requests con headers por defecto.
        """
        # TODO: Implementar
        # 1. Crear sesión
        # 2. Configurar headers (User-Agent, Accept)
        pass

    def _handle_response(self, response: requests.Response) -> dict[str, Any]:
        """
        Procesa la respuesta de la API.

        Args:
            response: Respuesta HTTP de requests.

        Returns:
            Diccionario con datos JSON.

        Raises:
            CityNotFoundError: Si la ciudad no existe.
            InvalidAPIKeyError: Si la API key es inválida.
            RateLimitError: Si se excede el límite.
            APIError: Para otros errores.
        """
        # TODO: Implementar manejo de respuestas
        # 1. Verificar status_code
        # 2. Mapear errores a excepciones específicas:
        #    - 401 -> InvalidAPIKeyError
        #    - 404 -> CityNotFoundError
        #    - 429 -> RateLimitError
        #    - Otros -> APIError
        # 3. Parsear y retornar JSON
        pass

    def get_current_weather(self, city: str) -> dict[str, Any]:
        """
        Obtiene el clima actual de una ciudad.

        Args:
            city: Nombre de la ciudad (ej: "Madrid" o "London,UK").

        Returns:
            Diccionario con datos del clima actual.

        Raises:
            CityNotFoundError: Si la ciudad no existe.
            APIError: Si hay error en la API.
            ConnectionError: Si hay problemas de red.

        Example:
            >>> client = WeatherClient()
            >>> weather = client.get_current_weather("Madrid")
            >>> print(weather["main"]["temp"])
            22.5
        """
        # TODO: Implementar
        # 1. Construir URL: /weather?q={city}&appid={key}&units=metric&lang=es
        # 2. Hacer request GET con timeout
        # 3. Manejar excepciones de conexión
        # 4. Procesar respuesta
        # 5. Loggear resultado
        pass

    def get_forecast(self, city: str) -> dict[str, Any]:
        """
        Obtiene el pronóstico de 5 días para una ciudad.

        Args:
            city: Nombre de la ciudad.

        Returns:
            Diccionario con datos del pronóstico.

        Raises:
            CityNotFoundError: Si la ciudad no existe.
            APIError: Si hay error en la API.
            ConnectionError: Si hay problemas de red.

        Example:
            >>> client = WeatherClient()
            >>> forecast = client.get_forecast("Barcelona")
            >>> print(len(forecast["list"]))  # 40 (cada 3 horas)
            40
        """
        # TODO: Implementar
        # Similar a get_current_weather pero usando /forecast
        pass
