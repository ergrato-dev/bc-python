"""
Tests para servicios.

Este módulo contiene tests para WeatherService,
FavoritesService y HistoryService.
"""

import pytest
from datetime import datetime


class TestWeatherService:
    """Tests para WeatherService."""

    def test_service_initialization(self, mock_weather_client):
        """Test inicialización del servicio."""
        # TODO: Implementar
        # from src.services.weather_service import WeatherService
        # service = WeatherService(client=mock_weather_client)
        # assert service.client is not None
        pass

    def test_get_current_weather_returns_weather_model(
        self, mock_weather_client
    ):
        """Test que retorna modelo Weather."""
        # TODO: Implementar
        # service = WeatherService(client=mock_weather_client)
        # weather = service.get_current_weather("Madrid")
        # assert isinstance(weather, Weather)
        pass

    def test_get_forecast_returns_forecast_model(self, mock_weather_client):
        """Test que retorna modelo Forecast."""
        # TODO: Implementar
        pass

    def test_get_weather_for_cities(self, mock_weather_client, sample_cities):
        """Test obtención de clima para múltiples ciudades."""
        # TODO: Implementar
        pass

    def test_get_weather_handles_errors_gracefully(self, mock_weather_client):
        """Test que maneja errores sin propagar."""
        # TODO: Implementar
        # Para get_weather_for_cities, debería omitir ciudades con error
        pass


class TestFavoritesService:
    """Tests para FavoritesService."""

    def test_add_favorite(self, mock_favorites_storage):
        """Test añadir ciudad a favoritos."""
        # TODO: Implementar
        # from src.services.favorites_service import FavoritesService
        # service = FavoritesService(storage=mock_favorites_storage)
        # result = service.add("London")
        # assert result is True
        # assert "London" in service.list_all()
        pass

    def test_add_duplicate_favorite_returns_false(self, mock_favorites_storage):
        """Test que no añade duplicados."""
        # TODO: Implementar
        # result = service.add("Madrid")  # Ya existe en mock
        # assert result is False
        pass

    def test_remove_favorite(self, mock_favorites_storage):
        """Test eliminar ciudad de favoritos."""
        # TODO: Implementar
        pass

    def test_remove_nonexistent_returns_false(self, mock_favorites_storage):
        """Test eliminar ciudad que no existe."""
        # TODO: Implementar
        pass

    def test_list_all_returns_copy(self, mock_favorites_storage):
        """Test que list_all retorna copia."""
        # TODO: Implementar
        # favorites = service.list_all()
        # favorites.append("Test")  # Modificar copia
        # assert "Test" not in service.list_all()
        pass

    def test_exists(self, mock_favorites_storage):
        """Test verificación de existencia."""
        # TODO: Implementar
        pass

    def test_clear(self, mock_favorites_storage):
        """Test limpiar favoritos."""
        # TODO: Implementar
        pass

    def test_favorites_are_normalized(self, mock_favorites_storage):
        """Test que los nombres se normalizan."""
        # TODO: Implementar
        # service.add("london")  # minúsculas
        # assert "London" in service.list_all()  # capitalizado
        pass


class TestHistoryService:
    """Tests para HistoryService."""

    def test_add_entry(self, mock_history_storage, sample_weather):
        """Test añadir entrada al historial."""
        # TODO: Implementar
        # from src.services.history_service import HistoryService
        # service = HistoryService(storage=mock_history_storage)
        # service.add(sample_weather)
        # assert service.count() == 1
        pass

    def test_get_recent_returns_in_order(self, mock_history_storage):
        """Test que retorna entradas ordenadas."""
        # TODO: Implementar
        pass

    def test_get_recent_respects_limit(self, mock_history_storage):
        """Test que respeta el límite."""
        # TODO: Implementar
        pass

    def test_history_truncates_at_max_entries(self, mock_history_storage):
        """Test que trunca al máximo configurado."""
        # TODO: Implementar
        pass

    def test_clear_history(self, mock_history_storage, sample_weather):
        """Test limpiar historial."""
        # TODO: Implementar
        pass
