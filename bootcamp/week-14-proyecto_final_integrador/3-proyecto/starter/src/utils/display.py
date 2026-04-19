"""
Display - Formateo de salida para la CLI.

Este módulo contiene funciones para formatear y mostrar
los datos meteorológicos de manera atractiva.
"""


class WeatherDisplay:
    """
    Formateador de datos meteorológicos para consola.

    Proporciona métodos para mostrar clima actual,
    pronósticos y otros datos de forma atractiva.
    """

    # Caracteres para líneas
    LINE_CHAR = "━"
    LINE_WIDTH = 40

    @classmethod
    def print_current_weather(cls, weather: "Weather") -> None:
        """
        Muestra el clima actual formateado.

        Args:
            weather: Objeto Weather a mostrar.

        Output:
            🌤️ Clima actual en Madrid, ES
            ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            🌡️  Temperatura: 22.5°C (sensación: 21.8°C)
            💧 Humedad: 45%
            💨 Viento: 3.5 m/s
            ☁️  Condición: Cielo despejado
        """
        # TODO: Implementar formateo
        pass

    @classmethod
    def print_forecast(cls, forecast: "Forecast") -> None:
        """
        Muestra el pronóstico formateado.

        Args:
            forecast: Objeto Forecast a mostrar.

        Output:
            📊 Pronóstico 5 días - Madrid, ES
            ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

            📅 Lunes 03/01
               🌡️ 18°C - 24°C | ☀️ Soleado
            ...
        """
        # TODO: Implementar formateo
        pass

    @classmethod
    def print_favorites(cls, favorites: list[str]) -> None:
        """
        Muestra la lista de favoritos.

        Args:
            favorites: Lista de ciudades favoritas.
        """
        # TODO: Implementar
        pass

    @classmethod
    def print_history(cls, entries: list["HistoryEntry"]) -> None:
        """
        Muestra el historial de búsquedas.

        Args:
            entries: Lista de entradas del historial.
        """
        # TODO: Implementar
        pass

    @classmethod
    def print_error(cls, message: str, suggestion: str | None = None) -> None:
        """
        Muestra un mensaje de error.

        Args:
            message: Mensaje de error.
            suggestion: Sugerencia opcional para el usuario.

        Output:
            ❌ Error: Ciudad no encontrada.
            💡 Sugerencia: Verifica el nombre...
        """
        # TODO: Implementar
        pass

    @classmethod
    def print_success(cls, message: str) -> None:
        """
        Muestra un mensaje de éxito.

        Args:
            message: Mensaje a mostrar.
        """
        # TODO: Implementar
        pass

    @classmethod
    def _print_line(cls, width: int | None = None) -> None:
        """Imprime una línea separadora."""
        w = width or cls.LINE_WIDTH
        print(cls.LINE_CHAR * w)


# Type hints for forward references (evita imports circulares)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.weather import Weather
    from src.models.forecast import Forecast
    from src.services.history_service import HistoryEntry
