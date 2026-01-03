"""
Tests para WeatherService usando mocking.

Ejercicio: Descomenta cada sección paso a paso.
"""
import pytest
from unittest.mock import patch, Mock, MagicMock
import requests

from src.weather_service import WeatherService, WeatherServiceError, WeatherData


# ============================================
# PASO 2: Mock Básico con @patch
# ============================================
print("--- Paso 2: Mock básico ---")

# @patch reemplaza temporalmente un objeto durante el test.
# El path debe ser donde se USA el objeto, no donde se DEFINE.
# Como weather_service.py hace `import requests`, parcheamos
# "src.weather_service.requests.get"

# Descomenta las siguientes líneas:
# @patch("src.weather_service.requests.get")
# def test_get_weather_returns_weather_data(mock_get, weather_service, mock_weather_response):
#     """Test que get_weather retorna WeatherData correctamente."""
#     # Configurar el mock
#     mock_response = Mock()
#     mock_response.json.return_value = mock_weather_response
#     mock_response.raise_for_status = Mock()  # No hace nada
#     mock_get.return_value = mock_response
#
#     # Ejecutar
#     result = weather_service.get_weather("London")
#
#     # Verificar
#     assert isinstance(result, WeatherData)
#     assert result.city == "London"
#     assert result.temperature == 22.5
#     assert result.humidity == 65
#     assert result.description == "partly cloudy"


# @patch("src.weather_service.requests.get")
# def test_get_weather_uses_correct_url(mock_get, weather_service, mock_weather_response):
#     """Test que se llama a la URL correcta."""
#     mock_response = Mock()
#     mock_response.json.return_value = mock_weather_response
#     mock_response.raise_for_status = Mock()
#     mock_get.return_value = mock_response
#
#     weather_service.get_weather("Paris")
#
#     # Verificar que se llamó con los parámetros correctos
#     mock_get.assert_called_once_with(
#         "https://api.weather.example.com/v1/current",
#         params={"city": "Paris", "key": "test-api-key-12345"},
#         timeout=10,
#     )


# ============================================
# PASO 3: Verificar Llamadas al Mock
# ============================================
print("--- Paso 3: Verificar llamadas ---")

# Podemos verificar cómo se llamó al mock:
# - assert_called() - Fue llamado al menos una vez
# - assert_called_once() - Fue llamado exactamente una vez
# - assert_called_with(...) - Última llamada con estos args
# - assert_called_once_with(...) - Una vez con estos args
# - call_count - Número de veces llamado

# Descomenta las siguientes líneas:
# @patch("src.weather_service.requests.get")
# def test_get_forecast_calls_api(mock_get, weather_service, mock_forecast_response):
#     """Test que get_forecast llama a la API correctamente."""
#     mock_response = Mock()
#     mock_response.json.return_value = mock_forecast_response
#     mock_response.raise_for_status = Mock()
#     mock_get.return_value = mock_response
#
#     result = weather_service.get_forecast("Tokyo", days=3)
#
#     # Verificar llamada
#     assert mock_get.called
#     assert mock_get.call_count == 1
#
#     # Verificar que retorna los datos del forecast
#     assert len(result) == 3
#     assert result[0]["day"] == "Monday"


# @patch("src.weather_service.requests.get")
# def test_is_available_returns_true_when_healthy(mock_get, weather_service):
#     """Test que is_available retorna True si el servicio responde."""
#     mock_response = Mock()
#     mock_response.status_code = 200
#     mock_get.return_value = mock_response
#
#     result = weather_service.is_available()
#
#     assert result is True
#     mock_get.assert_called_once()


# ============================================
# PASO 4: Simular Errores con side_effect
# ============================================
print("--- Paso 4: Simular errores ---")

# side_effect permite:
# - Lanzar excepciones
# - Retornar diferentes valores en llamadas sucesivas
# - Ejecutar una función personalizada

# Descomenta las siguientes líneas:
# @patch("src.weather_service.requests.get")
# def test_get_weather_handles_connection_error(mock_get, weather_service):
#     """Test que maneja errores de conexión."""
#     mock_get.side_effect = requests.ConnectionError("Network unavailable")
#
#     with pytest.raises(WeatherServiceError) as exc_info:
#         weather_service.get_weather("London")
#
#     assert "Connection error" in str(exc_info.value)


# @patch("src.weather_service.requests.get")
# def test_get_weather_handles_timeout(mock_get, weather_service):
#     """Test que maneja timeouts."""
#     mock_get.side_effect = requests.Timeout("Request timed out")
#
#     with pytest.raises(WeatherServiceError) as exc_info:
#         weather_service.get_weather("London")
#
#     assert "timeout" in str(exc_info.value).lower()


# @patch("src.weather_service.requests.get")
# def test_get_weather_handles_http_error(mock_get, weather_service):
#     """Test que maneja errores HTTP (404, 500, etc.)."""
#     mock_response = Mock()
#     mock_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")
#     mock_get.return_value = mock_response
#
#     with pytest.raises(WeatherServiceError) as exc_info:
#         weather_service.get_weather("NonexistentCity")
#
#     assert "HTTP error" in str(exc_info.value)


# @patch("src.weather_service.requests.get")
# def test_get_weather_handles_invalid_json(mock_get, weather_service):
#     """Test que maneja respuestas JSON inválidas."""
#     mock_response = Mock()
#     mock_response.raise_for_status = Mock()
#     # Respuesta con formato incorrecto (falta "main")
#     mock_response.json.return_value = {"invalid": "format"}
#     mock_get.return_value = mock_response
#
#     with pytest.raises(WeatherServiceError) as exc_info:
#         weather_service.get_weather("London")
#
#     assert "Invalid response" in str(exc_info.value)


# @patch("src.weather_service.requests.get")
# def test_is_available_returns_false_on_error(mock_get, weather_service):
#     """Test que is_available retorna False si hay error."""
#     mock_get.side_effect = requests.ConnectionError()
#
#     result = weather_service.is_available()
#
#     assert result is False


# ============================================
# PASO 5: Tests para WeatherData
# ============================================
print("--- Paso 5: Tests de WeatherData ---")

# También debemos testear la clase WeatherData

# Descomenta las siguientes líneas:
# class TestWeatherData:
#     """Tests para la clase WeatherData."""
#
#     def test_is_hot_above_30(self):
#         """Test que is_hot es True cuando temp > 30."""
#         weather = WeatherData(
#             city="Desert",
#             temperature=35.0,
#             humidity=20,
#             description="sunny",
#             wind_speed=5.0,
#         )
#         assert weather.is_hot is True
#
#     def test_is_hot_at_30(self):
#         """Test que is_hot es False cuando temp = 30."""
#         weather = WeatherData(
#             city="City",
#             temperature=30.0,
#             humidity=50,
#             description="warm",
#             wind_speed=10.0,
#         )
#         assert weather.is_hot is False
#
#     def test_is_cold_below_10(self):
#         """Test que is_cold es True cuando temp < 10."""
#         weather = WeatherData(
#             city="Arctic",
#             temperature=5.0,
#             humidity=80,
#             description="freezing",
#             wind_speed=20.0,
#         )
#         assert weather.is_cold is True
#
#     def test_is_cold_at_10(self):
#         """Test que is_cold es False cuando temp = 10."""
#         weather = WeatherData(
#             city="City",
#             temperature=10.0,
#             humidity=60,
#             description="cool",
#             wind_speed=8.0,
#         )
#         assert weather.is_cold is False
#
#     def test_get_summary(self):
#         """Test que get_summary retorna formato correcto."""
#         weather = WeatherData(
#             city="London",
#             temperature=18.5,
#             humidity=70,
#             description="cloudy",
#             wind_speed=15.0,
#         )
#         summary = weather.get_summary()
#
#         assert summary == "London: 18.5°C, cloudy"


# ============================================
# PASO 6: Test de Validación de Parámetros
# ============================================
print("--- Paso 6: Validación de parámetros ---")

# Descomenta las siguientes líneas:
# def test_get_forecast_validates_days(weather_service):
#     """Test que get_forecast valida el rango de días."""
#     with pytest.raises(ValueError, match="Days must be between 1 and 7"):
#         weather_service.get_forecast("London", days=0)
#
#     with pytest.raises(ValueError, match="Days must be between 1 and 7"):
#         weather_service.get_forecast("London", days=8)
