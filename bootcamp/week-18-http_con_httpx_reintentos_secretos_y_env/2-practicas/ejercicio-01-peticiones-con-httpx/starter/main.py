"""Ejercicio 01 · Peticiones con httpx: respuesta, consulta, errores, plazos y clientes.

Ejecuta `uv run python main.py` después de cada paso. Las peticiones van a un servidor
de prueba que arranca en tu máquina (servidor.py): no hace falta Internet.
"""

import time

import httpx

from servidor import start

BASE = start()

print("Ejercicio 01 · Peticiones con httpx")


# ============================================
# PASO 1: Una petición GET
# ============================================
# Descomenta las siguientes líneas:
# response = httpx.get(f"{BASE}/estaciones")
# print(response.status_code, response.reason_phrase)
# print(response.headers["content-type"])
# print(response.text)


# ============================================
# PASO 2: El cuerpo, como datos
# ============================================
# Descomenta las siguientes líneas:
# items = httpx.get(f"{BASE}/estaciones").json()
# print(type(items).__name__, len(items))
# for item in items:
#     value = "sin dato" if item["value"] is None else item["value"]
#     print(f"  {item['label']}: {value}")


# ============================================
# PASO 3: La consulta, con params
# ============================================
# Descomenta las siguientes líneas:
# response = httpx.get(f"{BASE}/eco", params={"dia": "6 de noviembre", "unidad": "°C"})
# print(response.url)
# print(response.json()["query"])


# ============================================
# PASO 4: Una respuesta que dice error
# ============================================
# Descomenta las siguientes líneas:
# response = httpx.get(f"{BASE}/estaciones/oeste")
# print(response.status_code, response.reason_phrase, "· is_error:", response.is_error)
# try:
#     response.raise_for_status()
# except httpx.HTTPStatusError as problem:
#     print(type(problem).__name__, "·", str(problem).splitlines()[0])


# ============================================
# PASO 5: Sin respuesta
# ============================================
# Descomenta las siguientes líneas:
# for url in ["http://127.0.0.1:9/estaciones", "127.0.0.1:9/estaciones"]:
#     try:
#         httpx.get(url)
#     except httpx.TransportError as problem:
#         print(f"{type(problem).__name__}: {problem}")


# ============================================
# PASO 6: Un plazo
# ============================================
# Descomenta las siguientes líneas:
# start_time = time.perf_counter()
# try:
#     httpx.get(f"{BASE}/lenta?s=2", timeout=0.5)
# except httpx.TimeoutException as problem:
#     elapsed = time.perf_counter() - start_time
#     print(f"{type(problem).__name__}: {problem} · {elapsed:.1f} s")


# ============================================
# PASO 7: Un cliente reutiliza las conexiones
# ============================================
# Descomenta las siguientes líneas:
# def connections() -> int:
#     count: int = httpx.get(f"{BASE}/conexiones").json()["conexiones"]
#     return count
#
#
# before = connections()
# for _ in range(5):
#     httpx.get(f"{BASE}/estaciones")
# print("5 peticiones sueltas · conexiones nuevas:", connections() - before - 1)
#
# before = connections()
# with httpx.Client(base_url=BASE) as client:
#     for _ in range(5):
#         client.get("/estaciones")
# print("5 peticiones con un cliente · conexiones nuevas:", connections() - before - 1)


# ============================================
# PASO 8: Cabeceras, POST y redirecciones
# ============================================
# Descomenta las siguientes líneas:
# with httpx.Client(base_url=BASE, headers={"User-Agent": "ejercicio/1.0"}) as client:
#     echo = client.post("/eco", json={"label": "Norte", "value": 12.5}).json()
#     print(echo["method"], "·", echo["user-agent"], "·", echo["body"])
#     moved = client.get("/mover")
#     print(moved.status_code, "→", moved.headers["location"])
#     followed = client.get("/mover", follow_redirects=True)
#     print(followed.status_code, followed.url.path, len(followed.json()), "medidas")
