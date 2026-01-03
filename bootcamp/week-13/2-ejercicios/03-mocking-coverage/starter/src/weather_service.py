"""
Servicio de clima que consume una API externa.

Este módulo simula un servicio real que hace llamadas HTTP.
En los tests, mockearemos estas llamadas para evitar
depender de servicios externos.
"""
import requests
from dataclasses import dataclass
from typing import Any


class WeatherServiceError(Exception):
    """Excepción personalizada para errores del servicio de clima."""

    pass


@dataclass
class WeatherData:
    """Datos del clima."""

    city: str
    temperature: float
    humidity: int
    description: str
    wind_speed: float

    @property
    def is_hot(self) -> bool:
        """Retorna True si la temperatura es mayor a 30°C."""
        return self.temperature > 30

    @property
    def is_cold(self) -> bool:
        """Retorna True si la temperatura es menor a 10°C."""
        return self.temperature < 10

    def get_summary(self) -> str:
        """Retorna un resumen del clima."""
        return f"{self.city}: {self.temperature}°C, {self.description}"


class WeatherService:
    """Servicio para obtener datos del clima."""

    BASE_URL = "https://api.weather.example.com/v1"
    DEFAULT_TIMEOUT = 10

    def __init__(self, api_key: str) -> None:
        """
        Inicializa el servicio con una API key.

        Args:
            api_key: Clave de API para autenticación
        """
        self.api_key = api_key

    def get_weather(self, city: str) -> WeatherData:
        """
        Obtiene el clima actual de una ciudad.

        Args:
            city: Nombre de la ciudad

        Returns:
            WeatherData con la información del clima

        Raises:
            WeatherServiceError: Si hay error en la API o red
        """
        try:
            response = requests.get(
                f"{self.BASE_URL}/current",
                params={"city": city, "key": self.api_key},
                timeout=self.DEFAULT_TIMEOUT,
            )
            response.raise_for_status()
            data = response.json()

            return WeatherData(
                city=city,
                temperature=data["main"]["temp"],
                humidity=data["main"]["humidity"],
                description=data["weather"][0]["description"],
                wind_speed=data["wind"]["speed"],
            )

        except requests.ConnectionError as e:
            raise WeatherServiceError(f"Connection error: {e}") from e
        except requests.Timeout as e:
            raise WeatherServiceError(f"Request timeout: {e}") from e
        except requests.HTTPError as e:
            raise WeatherServiceError(f"HTTP error: {e}") from e
        except (KeyError, IndexError) as e:
            raise WeatherServiceError(f"Invalid response format: {e}") from e

    def get_forecast(self, city: str, days: int = 5) -> list[dict[str, Any]]:
        """
        Obtiene el pronóstico de varios días.

        Args:
            city: Nombre de la ciudad
            days: Número de días (1-7)

        Returns:
            Lista de pronósticos por día

        Raises:
            WeatherServiceError: Si hay error en la API
            ValueError: Si days está fuera de rango
        """
        if not 1 <= days <= 7:
            raise ValueError("Days must be between 1 and 7")

        try:
            response = requests.get(
                f"{self.BASE_URL}/forecast",
                params={"city": city, "days": days, "key": self.api_key},
                timeout=self.DEFAULT_TIMEOUT,
            )
            response.raise_for_status()
            data = response.json()

            return data["forecast"]

        except requests.RequestException as e:
            raise WeatherServiceError(f"API error: {e}") from e

    def is_available(self) -> bool:
        """
        Verifica si el servicio está disponible.

        Returns:
            True si el servicio responde, False si no
        """
        try:
            response = requests.get(
                f"{self.BASE_URL}/health",
                timeout=5,
            )
            return response.status_code == 200
        except requests.RequestException:
            return False
