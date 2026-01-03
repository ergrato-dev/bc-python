"""Paquete API - Cliente HTTP para OpenWeatherMap."""

from src.api.client import WeatherClient
from src.api.exceptions import (
    APIError,
    CityNotFoundError,
    ConnectionError,
    InvalidAPIKeyError,
)

__all__ = [
    "WeatherClient",
    "APIError",
    "CityNotFoundError",
    "ConnectionError",
    "InvalidAPIKeyError",
]
