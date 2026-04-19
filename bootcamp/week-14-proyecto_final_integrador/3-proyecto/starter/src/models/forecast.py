"""
Modelo Forecast - Datos del pronóstico.

Este módulo define las estructuras de datos para
representar el pronóstico meteorológico.
"""

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Any


@dataclass
class DailyForecast:
    """
    Pronóstico para un día específico.

    Attributes:
        date: Fecha del pronóstico.
        temp_min: Temperatura mínima.
        temp_max: Temperatura máxima.
        description: Descripción del clima.
        icon: Código del icono.
        humidity: Humedad promedio.
        wind_speed: Velocidad del viento promedio.
    """

    date: date
    temp_min: float
    temp_max: float
    description: str
    icon: str
    humidity: int = 0
    wind_speed: float = 0.0

    def get_icon_emoji(self) -> str:
        """
        Convierte el código de icono a emoji.

        Returns:
            Emoji correspondiente al clima.
        """
        # TODO: Implementar (similar a Weather)
        pass

    def format_date(self) -> str:
        """
        Formatea la fecha para mostrar.

        Returns:
            Fecha formateada (ej: "Lunes 03/01").
        """
        # TODO: Implementar
        # Usar locale español para nombres de días
        pass


@dataclass
class Forecast:
    """
    Pronóstico completo de una ciudad.

    Attributes:
        city: Nombre de la ciudad.
        country: Código del país.
        days: Lista de pronósticos diarios.
        timestamp: Momento de la consulta.
    """

    city: str
    country: str
    days: list[DailyForecast] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> "Forecast":
        """
        Crea una instancia de Forecast desde la respuesta de la API.

        La API de OpenWeatherMap retorna pronósticos cada 3 horas.
        Este método agrupa los datos por día y calcula min/max.

        Args:
            data: Diccionario con respuesta de OpenWeatherMap.

        Returns:
            Instancia de Forecast con datos agregados por día.

        Example:
            >>> response = {"city": {"name": "Madrid"}, "list": [...]}
            >>> forecast = Forecast.from_api_response(response)
            >>> len(forecast.days)  # 5 días
            5
        """
        # TODO: Implementar parsing y agregación
        # La respuesta tiene esta estructura:
        # {
        #     "city": {"name": "Madrid", "country": "ES"},
        #     "list": [
        #         {
        #             "dt": 1704200400,  # Unix timestamp
        #             "main": {"temp": 22.0, "humidity": 45},
        #             "weather": [{"description": "...", "icon": "01d"}],
        #             "wind": {"speed": 3.5}
        #         },
        #         ...  # 40 elementos (cada 3 horas por 5 días)
        #     ]
        # }
        #
        # Pasos sugeridos:
        # 1. Agrupar elementos por fecha
        # 2. Para cada día, calcular temp_min y temp_max
        # 3. Usar la descripción/icon más frecuente del día
        # 4. Promediar humidity y wind_speed
        pass

    def get_days(self, limit: int = 5) -> list[DailyForecast]:
        """
        Obtiene los pronósticos diarios con límite.

        Args:
            limit: Número máximo de días a retornar.

        Returns:
            Lista de pronósticos diarios.
        """
        # TODO: Implementar
        pass
