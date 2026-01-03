"""
Tests para modelos de datos.

Este módulo contiene tests para Weather y Forecast.
"""

import pytest
from datetime import datetime, date


class TestWeather:
    """Tests para el modelo Weather."""

    def test_weather_creation(self, sample_weather):
        """Test creación básica de Weather."""
        # TODO: Implementar
        # assert sample_weather.city == "Madrid"
        # assert sample_weather.temperature == 22.5
        pass

    def test_weather_from_api_response(self, sample_weather_response):
        """Test creación desde respuesta de API."""
        # TODO: Implementar
        # from src.models.weather import Weather
        # weather = Weather.from_api_response(sample_weather_response)
        # assert weather.city == "Madrid"
        # assert weather.country == "ES"
        # assert weather.temperature == 22.5
        pass

    def test_weather_icon_emoji_sunny(self):
        """Test conversión de icono a emoji (soleado)."""
        # TODO: Implementar
        pass

    def test_weather_icon_emoji_rainy(self):
        """Test conversión de icono a emoji (lluvia)."""
        # TODO: Implementar
        pass

    def test_weather_to_dict(self, sample_weather):
        """Test serialización a diccionario."""
        # TODO: Implementar
        pass

    def test_weather_from_dict_roundtrip(self, sample_weather):
        """Test que to_dict y from_dict son inversos."""
        # TODO: Implementar
        # data = sample_weather.to_dict()
        # restored = Weather.from_dict(data)
        # assert restored.city == sample_weather.city
        pass


class TestForecast:
    """Tests para el modelo Forecast."""

    def test_forecast_from_api_response(self, sample_forecast_response):
        """Test creación desde respuesta de API."""
        # TODO: Implementar
        # from src.models.forecast import Forecast
        # forecast = Forecast.from_api_response(sample_forecast_response)
        # assert forecast.city == "Madrid"
        # assert len(forecast.days) == 5
        pass

    def test_forecast_aggregates_temperatures(self, sample_forecast_response):
        """Test que calcula correctamente min/max por día."""
        # TODO: Implementar
        pass

    def test_forecast_get_days_with_limit(self, sample_forecast_response):
        """Test limitación de días."""
        # TODO: Implementar
        # forecast = Forecast.from_api_response(sample_forecast_response)
        # days = forecast.get_days(limit=3)
        # assert len(days) == 3
        pass


class TestDailyForecast:
    """Tests para DailyForecast."""

    def test_daily_forecast_creation(self):
        """Test creación de pronóstico diario."""
        # TODO: Implementar
        pass

    def test_daily_forecast_format_date(self):
        """Test formateo de fecha."""
        # TODO: Implementar
        pass
