import io
from datetime import UTC, datetime
from unittest.mock import Mock, create_autospec, patch
from urllib.error import URLError

import pytest

import weather
from weather import ReadingError, fetch_reading, stamp


def response(text: str) -> io.BytesIO:
    """Una respuesta falsa: BytesIO se lee como un archivo y vale en un with, como la real."""
    return io.BytesIO(text.encode())


# ============================================
# PASO 1: Un Mock apunta cada llamada y devuelve lo que le digas
# ============================================
# Descomenta las siguientes líneas:
# def test_a_mock_records_its_calls() -> None:
#     fake = Mock(return_value=12.5)
#     assert fake("Norte") == 12.5
#     fake.assert_called_once_with("Norte")
#     assert isinstance(fake.anything.at_all(), Mock)


# ============================================
# PASO 2: patch cambia urlopen por un Mock mientras dura el with
# ============================================
# Descomenta las siguientes líneas:
# def test_fetch_reading_with_a_fake_service() -> None:
#     with patch("weather.urlopen", return_value=response('{"value": "12.5"}')) as fake:
#         assert fetch_reading("Norte") == 12.5
#     fake.assert_called_once_with("http://observatorio.invalid/api/Norte", timeout=5)


# ============================================
# PASO 3: El parche en el sitio equivocado no llega a weather
# ============================================
# Descomenta las siguientes líneas:
# def test_patching_the_wrong_name_does_nothing() -> None:
#     with (
#         patch("urllib.request.urlopen", return_value=response('{"value": 1}')),
#         pytest.raises(ReadingError),
#     ):
#         fetch_reading("Norte")


# ============================================
# PASO 4: side_effect lanza una excepción en lugar de devolver
# ============================================
# Descomenta las siguientes líneas:
# def test_fetch_reading_when_the_service_is_down() -> None:
#     with (
#         patch("weather.urlopen", side_effect=URLError("sin red")),
#         pytest.raises(ReadingError, match="sin respuesta de Norte") as caught,
#     ):
#         fetch_reading("Norte")
#     assert isinstance(caught.value.__cause__, URLError)


# ============================================
# PASO 5: Congelar la hora
# ============================================
# Descomenta las siguientes líneas:
# def test_stamp_uses_the_current_time() -> None:
#     with patch("weather.datetime") as fake:
#         fake.now.return_value = datetime(2026, 11, 6, 8, 30, tzinfo=UTC)
#         assert stamp(12.5) == "12.5 a las 08:30"
#     fake.now.assert_called_once_with(UTC)


# ============================================
# PASO 6: autospec: el doble tiene la firma del original
# ============================================
# Descomenta las siguientes líneas:
# def test_autospec_checks_the_arguments() -> None:
#     loose = Mock(return_value=12.5)
#     assert loose("Norte", "Sur", 3) == 12.5
#     strict = create_autospec(fetch_reading, return_value=12.5)
#     with pytest.raises(TypeError):
#         strict("Norte", "Sur", 3)


# ============================================
# PASO 7: Lo mismo que el paso 2, con monkeypatch y una función normal
# ============================================
# Descomenta las siguientes líneas:
# def test_fetch_reading_with_monkeypatch(monkeypatch: pytest.MonkeyPatch) -> None:
#     calls: list[str] = []
#
#     def fake_urlopen(url: str, timeout: float) -> io.BytesIO:
#         calls.append(url)
#         return response('{"value": 8}')
#
#     monkeypatch.setattr(weather, "urlopen", fake_urlopen)
#     assert fetch_reading("Sur") == 8.0
#     assert calls == ["http://observatorio.invalid/api/Sur"]
