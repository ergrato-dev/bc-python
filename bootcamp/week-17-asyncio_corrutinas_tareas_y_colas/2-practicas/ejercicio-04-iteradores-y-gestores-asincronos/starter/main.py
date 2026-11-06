"""Ejercicio 04 · Iteradores y gestores asíncronos: async for, async with, debug y tests.

Ejecuta `uv run python main.py` después de cada paso.
"""

import asyncio
import time
from collections.abc import AsyncGenerator, AsyncIterator

LINES = ["etiqueta;valor", "Norte;12,5", "Sur;8", "basura", "Oriente;55,1"]


async def ticker(lines: list[str], interval: float) -> AsyncIterator[str]:
    """Un generador asíncrono: da una línea cada `interval` segundos, como una estación."""
    for line in lines:
        await asyncio.sleep(interval)
        yield line


print("Ejercicio 04 · Iteradores y gestores asíncronos")


# ============================================
# PASO 1: async for
# ============================================
# Descomenta las siguientes líneas:
# async def follow() -> None:
#     start = time.perf_counter()
#     async for line in ticker(LINES, 0.1):
#         print(f"  {time.perf_counter() - start:.1f} s · {line}")
#
#
# asyncio.run(follow())


# ============================================
# PASO 2: Comprensiones asíncronas
# ============================================
# Descomenta las siguientes líneas:
# async def only_data() -> list[str]:
#     return [line async for line in ticker(LINES, 0) if ";" in line][1:]
#
#
# print(f"datos: {asyncio.run(only_data())}")


# ============================================
# PASO 3: Salir antes y cerrar el generador
# ============================================
# Descomenta las siguientes líneas:
# async def watched(lines: list[str]) -> AsyncGenerator[str]:
#     print("  abro la conexión")
#     try:
#         for line in lines:
#             await asyncio.sleep(0)
#             yield line
#     finally:
#         print("  cierro la conexión")
#
#
# async def first_two() -> None:
#     stream = watched(LINES)
#     print(f"  primera: {await anext(stream)}")
#     print(f"  segunda: {await anext(stream)}")
#     await stream.aclose()
#
#
# asyncio.run(first_two())


# ============================================
# PASO 4: async with con una clase
# ============================================
# Descomenta las siguientes líneas:
# from typing import Self
#
#
# class Station:
#     def __init__(self, name: str) -> None:
#         self.name = name
#
#     async def __aenter__(self) -> Self:
#         await asyncio.sleep(0.1)  # Conectar también puede hacer esperar.
#         print(f"  conectada {self.name}")
#         return self
#
#     async def __aexit__(self, *problem: object) -> None:
#         await asyncio.sleep(0)
#         print(f"  desconectada {self.name} · ¿con error? {problem[0] is not None}")
#
#
# async def use_station() -> None:
#     async with Station("Norte") as station:
#         print(f"  leo de {station.name}")
#     try:
#         async with Station("Sur"):
#             raise ValueError("lectura imposible")
#     except ValueError as problem:
#         print(f"  fuera: {problem}")
#
#
# asyncio.run(use_station())


# ============================================
# PASO 5: asynccontextmanager
# ============================================
# Descomenta las siguientes líneas:
# from contextlib import asynccontextmanager
#
#
# @asynccontextmanager
# async def connected(name: str) -> AsyncIterator[str]:
#     await asyncio.sleep(0)
#     print(f"  conectada {name}")
#     try:
#         yield name
#     finally:
#         print(f"  desconectada {name}")
#
#
# async def use_connected() -> None:
#     async with connected("Oriente") as name, connected("Occidente") as other:
#         print(f"  leo de {name} y {other}")
#
#
# asyncio.run(use_connected())


# ============================================
# PASO 6: El modo debug encuentra lo que bloquea
# ============================================
# Descomenta las siguientes líneas:
# async def sneaky() -> None:
#     time.sleep(0.2)  # noqa: ASYNC251 (a propósito: el modo debug lo descubre)
#
#
# asyncio.run(sneaky(), debug=True)


# ============================================
# PASO 7: Probar una corrutina
# ============================================
# Descomenta las siguientes líneas:
# def test_ticker_gives_every_line() -> None:
#     async def collect() -> list[str]:
#         return [line async for line in ticker(LINES, 0)]
#
#     assert asyncio.run(collect()) == LINES
#
#
# def test_ticker_is_lazy() -> None:
#     async def first() -> str:
#         return await anext(ticker(["a", "b"], 0))
#
#     assert type(ticker([], 0)).__name__ == "async_generator"
#     assert asyncio.run(first()) == "a"
#
#
# test_ticker_gives_every_line()
# test_ticker_is_lazy()
# print("tests: 2 passed")
