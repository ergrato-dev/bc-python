"""
Fixtures compartidas para tests.

Este módulo contiene fixtures de pytest que se usan
en múltiples archivos de test.
"""

import pytest
from datetime import datetime
from typing import Any


# ============================================
# DATOS DE PRUEBA - RESPUESTAS DE API
# ============================================

@pytest.fixture
def sample_weather_response() -> dict[str, Any]:
    """
    Fixture con respuesta de ejemplo de /weather.

    Returns:
        Diccionario simulando respuesta de OpenWeatherMap.
    """
    return {
        "coord": {"lon": -3.7026, "lat": 40.4165},
        "weather": [
            {
                "id": 800,
                "main": "Clear",
                "description": "cielo claro",
                "icon": "01d",
            }
        ],
        "base": "stations",
        "main": {
            "temp": 22.5,
            "feels_like": 21.8,
            "temp_min": 20.0,
            "temp_max": 25.0,
            "pressure": 1015,
            "humidity": 45,
        },
        "visibility": 10000,
        "wind": {"speed": 3.5, "deg": 180},
        "clouds": {"all": 0},
        "dt": 1704200400,
        "sys": {
            "type": 2,
            "id": 2007545,
            "country": "ES",
            "sunrise": 1704181234,
            "sunset": 1704214567,
        },
        "timezone": 3600,
        "id": 3117735,
        "name": "Madrid",
        "cod": 200,
    }


@pytest.fixture
def sample_forecast_response() -> dict[str, Any]:
    """
    Fixture con respuesta de ejemplo de /forecast.

    Returns:
        Diccionario simulando respuesta de pronóstico.
    """
    # Crear lista de pronósticos (cada 3 horas, 5 días)
    forecast_list = []

    # Base timestamp (2026-01-02 00:00:00)
    base_ts = 1735776000

    for i in range(40):  # 40 items = 5 días x 8 items/día
        forecast_list.append({
            "dt": base_ts + (i * 3 * 3600),
            "main": {
                "temp": 18.0 + (i % 8) * 2,  # Varía durante el día
                "feels_like": 17.0 + (i % 8) * 2,
                "humidity": 50 + (i % 5) * 5,
            },
            "weather": [
                {
                    "id": 800,
                    "main": "Clear",
                    "description": "cielo claro",
                    "icon": "01d" if (i % 8) < 4 else "01n",
                }
            ],
            "wind": {"speed": 2.5 + (i % 3)},
            "dt_txt": f"2026-01-{2 + i // 8:02d} {(i % 8) * 3:02d}:00:00",
        })

    return {
        "cod": "200",
        "message": 0,
        "cnt": 40,
        "list": forecast_list,
        "city": {
            "id": 3117735,
            "name": "Madrid",
            "coord": {"lat": 40.4165, "lon": -3.7026},
            "country": "ES",
            "population": 3255944,
            "timezone": 3600,
            "sunrise": 1704181234,
            "sunset": 1704214567,
        },
    }


# ============================================
# FIXTURES DE MODELOS
# ============================================

@pytest.fixture
def sample_weather():
    """
    Fixture con objeto Weather de prueba.

    Returns:
        Objeto Weather para tests.
    """
    from src.models.weather import Weather

    return Weather(
        city="Madrid",
        country="ES",
        temperature=22.5,
        feels_like=21.8,
        humidity=45,
        wind_speed=3.5,
        description="cielo claro",
        icon="01d",
        timestamp=datetime(2026, 1, 2, 15, 30),
    )


@pytest.fixture
def sample_cities() -> list[str]:
    """
    Fixture con lista de ciudades de prueba.

    Returns:
        Lista de ciudades.
    """
    return ["Madrid", "Barcelona", "London,UK", "Paris,FR", "Tokyo,JP"]


# ============================================
# FIXTURES DE STORAGE (MOCK)
# ============================================

@pytest.fixture
def temp_storage(tmp_path):
    """
    Fixture que crea un JsonStorage temporal.

    Args:
        tmp_path: Fixture de pytest para directorio temporal.

    Returns:
        JsonStorage con directorio temporal.
    """
    from src.storage.json_storage import JsonStorage

    return JsonStorage("test.json", str(tmp_path))


@pytest.fixture
def mock_favorites_storage():
    """
    Fixture con storage mock para favoritos.

    Returns:
        Mock de storage con datos precargados.
    """

    class MockStorage:
        def __init__(self):
            self.data = ["Madrid", "Barcelona"]

        def load(self) -> list:
            return self.data.copy()

        def save(self, data: list) -> None:
            self.data = data.copy()

    return MockStorage()


@pytest.fixture
def mock_history_storage():
    """
    Fixture con storage mock para historial.

    Returns:
        Mock de storage vacío.
    """

    class MockStorage:
        def __init__(self):
            self.data = []

        def load(self) -> list:
            return self.data.copy()

        def save(self, data: list) -> None:
            self.data = data.copy()

    return MockStorage()


# ============================================
# FIXTURES DE CLIENTE API (MOCK)
# ============================================

@pytest.fixture
def mock_weather_client(sample_weather_response, sample_forecast_response):
    """
    Fixture con cliente de API mock.

    Returns:
        Mock de WeatherClient que retorna datos de prueba.
    """

    class MockClient:
        def __init__(self):
            self.weather_response = sample_weather_response
            self.forecast_response = sample_forecast_response

        def get_current_weather(self, city: str) -> dict:
            if city.lower() == "invalid":
                from src.api.exceptions import CityNotFoundError

                raise CityNotFoundError(city)
            return self.weather_response

        def get_forecast(self, city: str) -> dict:
            if city.lower() == "invalid":
                from src.api.exceptions import CityNotFoundError

                raise CityNotFoundError(city)
            return self.forecast_response

    return MockClient()
