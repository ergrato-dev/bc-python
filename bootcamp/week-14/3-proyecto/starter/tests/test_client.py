"""
Tests para el cliente de API.

Este módulo contiene tests para WeatherClient,
incluyendo mocking de requests.
"""

import pytest
from unittest.mock import Mock, patch


class TestWeatherClient:
    """Tests para WeatherClient."""

    def test_client_initialization(self):
        """Test inicialización del cliente."""
        # TODO: Implementar
        # from src.api.client import WeatherClient
        # client = WeatherClient()
        # assert client.base_url is not None
        pass

    @patch("src.api.client.requests.Session")
    def test_get_current_weather_success(
        self, mock_session, sample_weather_response
    ):
        """Test obtención exitosa de clima actual."""
        # TODO: Implementar
        # 1. Configurar mock para retornar sample_weather_response
        # 2. Llamar get_current_weather
        # 3. Verificar resultado
        pass

    @patch("src.api.client.requests.Session")
    def test_get_current_weather_city_not_found(self, mock_session):
        """Test manejo de ciudad no encontrada (404)."""
        # TODO: Implementar
        # 1. Configurar mock para retornar status 404
        # 2. Verificar que lanza CityNotFoundError
        pass

    @patch("src.api.client.requests.Session")
    def test_get_current_weather_invalid_api_key(self, mock_session):
        """Test manejo de API key inválida (401)."""
        # TODO: Implementar
        pass

    @patch("src.api.client.requests.Session")
    def test_get_current_weather_connection_error(self, mock_session):
        """Test manejo de error de conexión."""
        # TODO: Implementar
        # mock_session.return_value.get.side_effect = ConnectionError()
        pass

    @patch("src.api.client.requests.Session")
    def test_get_forecast_success(
        self, mock_session, sample_forecast_response
    ):
        """Test obtención exitosa de pronóstico."""
        # TODO: Implementar
        pass

    def test_handle_response_maps_errors_correctly(self):
        """Test que _handle_response mapea códigos a excepciones."""
        # TODO: Implementar
        pass


class TestAPIExceptions:
    """Tests para excepciones de API."""

    def test_city_not_found_error_message(self):
        """Test mensaje de CityNotFoundError."""
        from src.api.exceptions import CityNotFoundError

        error = CityNotFoundError("InvalidCity")
        assert "InvalidCity" in str(error)
        assert error.status_code == 404

    def test_invalid_api_key_error(self):
        """Test InvalidAPIKeyError."""
        from src.api.exceptions import InvalidAPIKeyError

        error = InvalidAPIKeyError()
        assert error.status_code == 401

    def test_connection_error_with_detail(self):
        """Test ConnectionError con detalle."""
        from src.api.exceptions import ConnectionError

        error = ConnectionError("timeout")
        assert "timeout" in str(error)
