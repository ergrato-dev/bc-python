"""
Fixtures compartidas para tests de mocking y coverage.
"""
import pytest
from src.weather_service import WeatherService
from src.notification import NotificationService


@pytest.fixture
def weather_service() -> WeatherService:
    """Provee una instancia del servicio de clima."""
    return WeatherService(api_key="test-api-key-12345")


@pytest.fixture
def notification_service() -> NotificationService:
    """Provee una instancia del servicio de notificaciones."""
    return NotificationService(
        smtp_host="localhost",
        smtp_port=587,
        sms_api_key="test-sms-key",
    )


@pytest.fixture
def mock_weather_response() -> dict:
    """Respuesta simulada de la API de clima."""
    return {
        "main": {
            "temp": 22.5,
            "humidity": 65,
        },
        "weather": [
            {
                "description": "partly cloudy",
            }
        ],
        "wind": {
            "speed": 12.3,
        },
    }


@pytest.fixture
def mock_forecast_response() -> dict:
    """Respuesta simulada del pronóstico."""
    return {
        "forecast": [
            {"day": "Monday", "temp": 20, "description": "sunny"},
            {"day": "Tuesday", "temp": 18, "description": "cloudy"},
            {"day": "Wednesday", "temp": 22, "description": "sunny"},
        ]
    }
