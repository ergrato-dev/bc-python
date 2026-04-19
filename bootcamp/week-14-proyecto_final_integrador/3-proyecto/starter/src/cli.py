"""
CLI - Interfaz de Línea de Comandos.

Este módulo define todos los comandos disponibles:
- weather: Consultar clima actual
- forecast: Ver pronóstico 5 días
- favorites: Gestionar ciudades favoritas
- history: Ver historial de búsquedas
"""

import argparse
import sys
from typing import Sequence

from src.services.weather_service import WeatherService
from src.services.favorites_service import FavoritesService
from src.services.history_service import HistoryService
from src.utils.display import WeatherDisplay


def create_parser() -> argparse.ArgumentParser:
    """
    Crea el parser de argumentos CLI.

    Returns:
        ArgumentParser configurado con todos los comandos.
    """
    # TODO: Implementar parser principal
    # 1. Crear parser con descripción
    # 2. Agregar subparsers para comandos
    pass


def add_weather_command(subparsers: argparse._SubParsersAction) -> None:
    """
    Añade el comando 'weather' para clima actual.

    Args:
        subparsers: Subparsers del parser principal.
    """
    # TODO: Implementar comando weather
    # weather <city> - Muestra clima actual
    pass


def add_forecast_command(subparsers: argparse._SubParsersAction) -> None:
    """
    Añade el comando 'forecast' para pronóstico.

    Args:
        subparsers: Subparsers del parser principal.
    """
    # TODO: Implementar comando forecast
    # forecast <city> [--days N] - Muestra pronóstico
    pass


def add_favorites_command(subparsers: argparse._SubParsersAction) -> None:
    """
    Añade el comando 'favorites' para gestionar favoritos.

    Args:
        subparsers: Subparsers del parser principal.
    """
    # TODO: Implementar comando favorites con subcomandos
    # favorites add <city>
    # favorites remove <city>
    # favorites list
    # favorites weather
    pass


def add_history_command(subparsers: argparse._SubParsersAction) -> None:
    """
    Añade el comando 'history' para ver historial.

    Args:
        subparsers: Subparsers del parser principal.
    """
    # TODO: Implementar comando history
    # history [--limit N]
    # history clear
    pass


def handle_weather(args: argparse.Namespace) -> int:
    """
    Maneja el comando 'weather'.

    Args:
        args: Argumentos parseados.

    Returns:
        Código de salida.
    """
    # TODO: Implementar handler
    # 1. Crear servicio de clima
    # 2. Obtener clima de la ciudad
    # 3. Mostrar resultado formateado
    # 4. Guardar en historial
    # 5. Manejar errores
    pass


def handle_forecast(args: argparse.Namespace) -> int:
    """
    Maneja el comando 'forecast'.

    Args:
        args: Argumentos parseados.

    Returns:
        Código de salida.
    """
    # TODO: Implementar handler
    pass


def handle_favorites(args: argparse.Namespace) -> int:
    """
    Maneja el comando 'favorites'.

    Args:
        args: Argumentos parseados.

    Returns:
        Código de salida.
    """
    # TODO: Implementar handler según acción
    # add, remove, list, weather
    pass


def handle_history(args: argparse.Namespace) -> int:
    """
    Maneja el comando 'history'.

    Args:
        args: Argumentos parseados.

    Returns:
        Código de salida.
    """
    # TODO: Implementar handler
    pass


def main(argv: Sequence[str] | None = None) -> int:
    """
    Punto de entrada principal de la CLI.

    Args:
        argv: Argumentos de línea de comandos (None usa sys.argv).

    Returns:
        Código de salida (0 = éxito, 1 = error).
    """
    # TODO: Implementar
    # 1. Crear parser
    # 2. Parsear argumentos
    # 3. Ejecutar comando correspondiente
    pass


if __name__ == "__main__":
    sys.exit(main())
