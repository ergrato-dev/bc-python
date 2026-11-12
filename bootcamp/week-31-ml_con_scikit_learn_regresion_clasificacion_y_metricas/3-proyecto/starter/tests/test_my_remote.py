# Tus tests de la semana 18: sustituye este ejemplo por al menos 6 tests tuyos (paso 14).
# Con medidas de tu dominio y httpx.MockTransport, sin red: get_text con éxito, con un
# error que no se reintenta y con reintentos; download y el archivo guardado; Settings
# con monkeypatch.setenv; y el comando descargar con CliRunner.
import asyncio

import httpx
import pytest

from observatorio.core import FetchError, get_text, make_client


def test_example_a_404_is_a_fetch_error() -> None:
    async def main() -> str:
        transport = httpx.MockTransport(lambda request: httpx.Response(404))
        async with make_client(transport=transport) as client:
            return await get_text(client, "http://estaciones.test/falta.json")

    with pytest.raises(FetchError, match="respondió 404"):
        asyncio.run(main())
