"""Ejercicio 02 · Cliente asíncrono y concurrencia: AsyncClient, TaskGroup, límites y pruebas.

Ejecuta `uv run python main.py` después de cada paso. Los tiempos son de tu máquina:
compáralos con los del README por su orden de magnitud, no por el último decimal.
"""

import asyncio
import time

import httpx

from servidor import start

BASE = start()
# Seis peticiones que tardan 0,3 s cada una en contestar.
SLOW = [f"/lenta?s=0.3&n={n}" for n in range(6)]

print("Ejercicio 02 · Cliente asíncrono y concurrencia")


# ============================================
# PASO 1: AsyncClient
# ============================================
# Descomenta las siguientes líneas:
# async def first() -> None:
#     async with httpx.AsyncClient(base_url=BASE) as client:
#         response = await client.get("/estaciones/norte")
#         print(response.status_code, response.json())
#
#
# asyncio.run(first())


# ============================================
# PASO 2: Una detrás de otra
# ============================================
# Descomenta las siguientes líneas:
# async def one_by_one() -> None:
#     start_time = time.perf_counter()
#     async with httpx.AsyncClient(base_url=BASE) as client:
#         for path in SLOW:
#             await client.get(path)
#     print(f"una detrás de otra: {time.perf_counter() - start_time:.1f} s")
#
#
# asyncio.run(one_by_one())


# ============================================
# PASO 3: Todas a la vez, con TaskGroup
# ============================================
# Descomenta las siguientes líneas:
# async def all_at_once() -> None:
#     start_time = time.perf_counter()
#     async with httpx.AsyncClient(base_url=BASE) as client, asyncio.TaskGroup() as group:
#         tasks = [group.create_task(client.get(path)) for path in SLOW]
#     codes = [task.result().status_code for task in tasks]
#     print(f"todas a la vez: {time.perf_counter() - start_time:.1f} s · {codes}")
#
#
# asyncio.run(all_at_once())


# ============================================
# PASO 4: Como mucho dos a la vez
# ============================================
# Descomenta las siguientes líneas:
# async def two_at_a_time() -> None:
#     semaphore = asyncio.Semaphore(2)
#     start_time = time.perf_counter()
#
#     async def get(client: httpx.AsyncClient, path: str) -> httpx.Response:
#         async with semaphore:
#             return await client.get(path)
#
#     async with httpx.AsyncClient(base_url=BASE) as client, asyncio.TaskGroup() as group:
#         for path in SLOW:
#             group.create_task(get(client, path))
#     print(f"dos a la vez, con Semaphore: {time.perf_counter() - start_time:.1f} s")
#
#
# asyncio.run(two_at_a_time())


# ============================================
# PASO 5: El límite del cliente, con Limits
# ============================================
# Descomenta las siguientes líneas:
# async def limited_client() -> None:
#     limits = httpx.Limits(max_connections=2)
#     start_time = time.perf_counter()
#     client = httpx.AsyncClient(base_url=BASE, limits=limits)
#     async with client, asyncio.TaskGroup() as group:
#         for path in SLOW:
#             group.create_task(client.get(path))
#     print(f"dos a la vez, con Limits: {time.perf_counter() - start_time:.1f} s")
#
#
# asyncio.run(limited_client())


# ============================================
# PASO 6: Un error en el grupo
# ============================================
# Descomenta las siguientes líneas:
# async def checked(client: httpx.AsyncClient, path: str) -> int:
#     response = await client.get(path)
#     response.raise_for_status()
#     return response.status_code
#
#
# async def with_an_error() -> None:
#     paths = ["/lenta?s=0.3", "/estaciones/oeste", "/estaciones/sur"]
#     try:
#         client = httpx.AsyncClient(base_url=BASE)
#         async with client, asyncio.TaskGroup() as group:
#             for path in paths:
#                 group.create_task(checked(client, path))
#     except* httpx.HTTPStatusError as group_error:
#         for problem in group_error.exceptions:
#             print("falló:", str(problem).splitlines()[0])
#
#
# asyncio.run(with_an_error())


# ============================================
# PASO 7: Un plazo para todo
# ============================================
# Descomenta las siguientes líneas:
# async def deadline() -> None:
#     start_time = time.perf_counter()
#     try:
#         client = httpx.AsyncClient(base_url=BASE, timeout=10.0)
#         async with client, asyncio.timeout(0.5), asyncio.TaskGroup() as group:
#             for path in ["/lenta?s=0.2", "/lenta?s=2", "/lenta?s=3"]:
#                 group.create_task(client.get(path))
#     except TimeoutError:
#         print(f"plazo total agotado: {time.perf_counter() - start_time:.1f} s")
#
#
# asyncio.run(deadline())


# ============================================
# PASO 8: Sin servidor, con MockTransport
# ============================================
# Descomenta las siguientes líneas:
# seen: list[str] = []
#
#
# def handler(request: httpx.Request) -> httpx.Response:
#     seen.append(request.url.path)
#     if request.url.path == "/estaciones/norte":
#         return httpx.Response(200, json={"label": "Norte", "value": 99.9})
#     return httpx.Response(503)
#
#
# async def mocked() -> None:
#     transport = httpx.MockTransport(handler)
#     client = httpx.AsyncClient(base_url="http://falso.test", transport=transport)
#     async with client:
#         norte = await client.get("/estaciones/norte")
#         sur = await client.get("/estaciones/sur")
#     print(norte.status_code, norte.json(), "·", sur.status_code)
#     print("peticiones:", seen)
#
#
# asyncio.run(mocked())
