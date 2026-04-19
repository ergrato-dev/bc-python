"""
Modelo Weather - Datos del clima actual.

Este módulo define la estructura de datos para
representar el clima actual de una ciudad.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class Weather:
    """
    Representa el clima actual de una ciudad.

    Attributes:
        city: Nombre de la ciudad.
        country: Código del país (ISO 3166).
        temperature: Temperatura en Celsius.
        feels_like: Sensación térmica en Celsius.
        humidity: Humedad en porcentaje.
        wind_speed: Velocidad del viento en m/s.
        description: Descripción del clima.
        icon: Código del icono del clima.
        timestamp: Momento de la consulta.
    """

    city: str
    country: str
    temperature: float
    feels_like: float
    humidity: int
    wind_speed: float
    description: str
    icon: str
    timestamp: datetime = field(default_factory=datetime.now)

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> "Weather":
        """
        Crea una instancia de Weather desde la respuesta de la API.

        Args:
            data: Diccionario con respuesta de OpenWeatherMap.

        Returns:
            Instancia de Weather con los datos parseados.

        Example:
            >>> response = {"main": {"temp": 22.5, ...}, ...}
            >>> weather = Weather.from_api_response(response)
        """
        # TODO: Implementar parsing de respuesta API
        # La respuesta de OpenWeatherMap tiene esta estructura:
        # {
        #     "name": "Madrid",
        #     "sys": {"country": "ES"},
        #     "main": {
        #         "temp": 22.5,
        #         "feels_like": 21.8,
        #         "humidity": 45
        #     },
        #     "wind": {"speed": 3.5},
        #     "weather": [{"description": "cielo despejado", "icon": "01d"}]
        # }
        pass

    def get_icon_emoji(self) -> str:
        """
        Convierte el código de icono a emoji.

        Returns:
            Emoji correspondiente al clima.
        """
        # TODO: Implementar mapeo de iconos a emojis
        # Códigos comunes de OpenWeatherMap:
        # 01d/01n -> ☀️/🌙 (despejado)
        # 02d/02n -> ⛅ (pocas nubes)
        # 03d/03n -> ☁️ (nublado)
        # 04d/04n -> ☁️ (muy nublado)
        # 09d/09n -> 🌧️ (lluvia)
        # 10d/10n -> 🌦️ (lluvia con sol)
        # 11d/11n -> ⛈️ (tormenta)
        # 13d/13n -> ❄️ (nieve)
        # 50d/50n -> 🌫️ (niebla)
        pass

    def to_dict(self) -> dict[str, Any]:
        """
        Convierte Weather a diccionario para persistencia.

        Returns:
            Diccionario serializable a JSON.
        """
        # TODO: Implementar
        pass

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Weather":
        """
        Crea Weather desde diccionario (para cargar de JSON).

        Args:
            data: Diccionario con datos de Weather.

        Returns:
            Instancia de Weather.
        """
        # TODO: Implementar
        pass
