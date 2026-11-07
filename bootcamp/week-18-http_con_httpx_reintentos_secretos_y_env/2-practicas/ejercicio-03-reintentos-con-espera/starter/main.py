"""Ejercicio 03 · Reintentos con espera: qué reintentar, cuánto esperar y cuándo parar.

Ejecuta `uv run python main.py` después de cada paso. Los tiempos son de tu máquina:
compáralos con los del README por su orden de magnitud, no por el último decimal.
"""

import asyncio
import random
import time

import httpx

from servidor import start

BASE = start()
# Las respuestas que pueden salir bien si se repite la petición.
RETRY_STATUSES = frozenset({429, 500, 502, 503, 504})

print("Ejercicio 03 · Reintentos con espera")


# ============================================
# PASO 1: Un fallo pasajero
# ============================================
# Descomenta las siguientes líneas:
# async def passing_failure() -> None:
#     async with httpx.AsyncClient(base_url=BASE) as client:
#         for _ in range(3):
#             response = await client.get("/inestable?id=uno&fallos=2")
#             print(response.status_code, response.json())
#
#
# asyncio.run(passing_failure())


# ============================================
# PASO 2: Reintentar sin esperar
# ============================================
# Descomenta las siguientes líneas:
# async def naive(client: httpx.AsyncClient, path: str) -> httpx.Response:
#     for attempt in range(4):
#         response = await client.get(path)
#         print(f"  intento {attempt + 1}: {response.status_code}")
#         if response.status_code not in RETRY_STATUSES:
#             break
#     return response
#
#
# async def try_naive() -> None:
#     start_time = time.perf_counter()
#     async with httpx.AsyncClient(base_url=BASE) as client:
#         response = await naive(client, "/inestable?id=dos&fallos=2")
#     elapsed = time.perf_counter() - start_time
#     print(f"sin espera: {response.status_code} en {elapsed:.2f} s")
#
#
# asyncio.run(try_naive())


# ============================================
# PASO 3: Espera exponencial
# ============================================
# Descomenta las siguientes líneas:
# async def with_backoff(
#     client: httpx.AsyncClient, path: str, *, retries: int = 3, backoff: float = 0.2
# ) -> httpx.Response:
#     for attempt in range(retries + 1):
#         if attempt > 0:
#             delay = backoff * 2 ** (attempt - 1)
#             print(f"  espera {delay:.1f} s")
#             await asyncio.sleep(delay)
#         response = await client.get(path)
#         print(f"  intento {attempt + 1}: {response.status_code}")
#         if response.status_code not in RETRY_STATUSES:
#             break
#     return response
#
#
# async def try_backoff() -> None:
#     start_time = time.perf_counter()
#     async with httpx.AsyncClient(base_url=BASE) as client:
#         response = await with_backoff(client, "/inestable?id=tres&fallos=3")
#     elapsed = time.perf_counter() - start_time
#     print(f"con espera: {response.status_code} en {elapsed:.1f} s")
#
#
# asyncio.run(try_backoff())


# ============================================
# PASO 4: Qué se reintenta y qué no
# ============================================
# Descomenta las siguientes líneas:
# class FetchError(Exception):
#     """La petición no salió bien ni después de los reintentos."""
#
#
# async def fetch(
#     client: httpx.AsyncClient, url: str, *, retries: int = 3, backoff: float = 0.2
# ) -> httpx.Response:
#     failure = ""
#     for attempt in range(retries + 1):
#         if attempt > 0:
#             await asyncio.sleep(backoff * 2 ** (attempt - 1))
#         try:
#             response = await client.get(url)
#         except httpx.TransportError as problem:
#             failure = type(problem).__name__
#         else:
#             if response.status_code not in RETRY_STATUSES:
#                 return response
#             failure = str(response.status_code)
#     raise FetchError(f"{url}: {failure} tras {retries + 1} intentos")
#
#
# async def what_to_retry() -> None:
#     async with httpx.AsyncClient() as client:
#         for url in [f"{BASE}/estaciones/oeste", "http://127.0.0.1:9/estaciones"]:
#             start_time = time.perf_counter()
#             try:
#                 response = await fetch(client, url)
#                 result = str(response.status_code)
#             except FetchError as problem:
#                 result = f"FetchError: {problem}"
#             print(f"{result} · {time.perf_counter() - start_time:.1f} s")
#
#
# asyncio.run(what_to_retry())


# ============================================
# PASO 5: Variación aleatoria (jitter)
# ============================================
# Descomenta las siguientes líneas:
# random.seed(18)  # Para que tu salida sea igual que la del README.
# for attempt in [1, 2, 3]:
#     delay = 0.2 * 2 ** (attempt - 1)
#     jittered = sorted(round(random.uniform(0, delay), 2) for _ in range(5))
#     print(f"reintento {attempt}: todos a {delay:.1f} s · con jitter {jittered}")


# ============================================
# PASO 6: Retry-After
# ============================================
# Descomenta las siguientes líneas:
# async def polite(client: httpx.AsyncClient, path: str) -> httpx.Response:
#     for _ in range(4):
#         response = await client.get(path)
#         if response.status_code not in RETRY_STATUSES:
#             break
#         # Lo que pide el servidor, con un máximo: no te quedas esperando una hora.
#         wait = min(float(response.headers.get("Retry-After", "0.2")), 5.0)
#         print(f"  {response.status_code}: el servidor pide esperar {wait:g} s")
#         await asyncio.sleep(wait)
#     return response
#
#
# async def try_polite() -> None:
#     start_time = time.perf_counter()
#     async with httpx.AsyncClient(base_url=BASE) as client:
#         response = await polite(client, "/cuota?id=cuatro")
#     print(f"{response.status_code} en {time.perf_counter() - start_time:.1f} s")
#
#
# asyncio.run(try_polite())


# ============================================
# PASO 7: Un tope de tiempo total
# ============================================
# Descomenta las siguientes líneas:
# async def capped() -> None:
#     start_time = time.perf_counter()
#     try:
#         async with httpx.AsyncClient() as client, asyncio.timeout(1.0):
#             await fetch(client, f"{BASE}/inestable?id=cinco&fallos=10", retries=10)
#     except TimeoutError:
#         print(f"tiempo total agotado: {time.perf_counter() - start_time:.1f} s")
#
#
# asyncio.run(capped())


# ============================================
# PASO 8: Los reintentos que trae httpx
# ============================================
# Descomenta las siguientes líneas:
# async def transport_retries() -> None:
#     transport = httpx.AsyncHTTPTransport(retries=2)
#     async with httpx.AsyncClient(transport=transport) as client:
#         start_time = time.perf_counter()
#         try:
#             await client.get("http://127.0.0.1:9/estaciones")
#         except httpx.ConnectError:
#             elapsed = time.perf_counter() - start_time
#             print(f"sin servidor: ConnectError en {elapsed:.1f} s")
#         response = await client.get(f"{BASE}/inestable?id=seis&fallos=1")
#         print("un 503:", response.status_code, "sin reintentar")
#
#
# asyncio.run(transport_retries())
