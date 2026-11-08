"""Ejercicio 01 · Tu primera API con FastAPI.

Cada paso añade rutas a la aplicación `app` y las prueba con TestClient, que habla con
ella sin red ni servidor. El último paso la sirve de verdad con uvicorn, en un hilo.
"""

import threading
import time

import httpx2
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

print("Ejercicio 01 · Tu primera API")

app = FastAPI(title="Estaciones")
client = TestClient(app)

# Los datos de las estaciones: en el ejercicio 04 vivirán en PostgreSQL.
STATIONS = {1: "Norte", 2: "Sur", 3: "Este"}
READINGS = [("Norte", 12.5), ("Sur", 30.0), ("Norte", 7.5), ("Este", 55.1), ("Sur", 41.0)]


# ============================================
# PASO 1: Una ruta
# ============================================
# Descomenta las siguientes líneas:
# @app.get("/")
# def home() -> dict[str, str]:
#     return {"mensaje": "hola desde FastAPI"}
#
#
# response = client.get("/")
# print("\n--- Paso 1: GET / ---")
# print("estado:", response.status_code)
# print("tipo:", response.headers["content-type"])
# print("cuerpo:", response.text)
# print("como Python:", response.json())


# ============================================
# PASO 2: Parámetros de ruta, con tipo
# ============================================
# Descomenta las siguientes líneas:
# @app.get("/stations/{station_id}")
# def get_station(station_id: int) -> dict[str, object]:
#     # station_id llega ya convertido a int: FastAPI lo lee de la anotación.
#     return {"id": station_id, "name": STATIONS.get(station_id), "type": type(station_id).__name__}
#
#
# print("\n--- Paso 2: /stations/{station_id} ---")
# print("/stations/2 ->", client.get("/stations/2").json())
# response = client.get("/stations/dos")
# print("/stations/dos ->", response.status_code)
# for error in response.json()["detail"]:
#     print("  ", error["loc"], error["msg"])


# ============================================
# PASO 3: Parámetros de consulta
# ============================================
# Descomenta las siguientes líneas:
# @app.get("/readings")
# def get_readings(minimum: float = 0.0, limit: int = 10, label: str | None = None) -> list[float]:
#     # Lo que no está en la ruta es de la consulta: /readings?minimum=10&limit=2.
#     values = [value for name, value in READINGS if label is None or name == label]
#     return [value for value in values if value >= minimum][:limit]
#
#
# print("\n--- Paso 3: /readings?... ---")
# print("sin parámetros       ->", client.get("/readings").json())
# print("minimum=10&limit=2   ->", client.get("/readings?minimum=10&limit=2").json())
# print("label=Sur            ->", client.get("/readings", params={"label": "Sur"}).json())
# response = client.get("/readings", params={"limit": "muchos"})
# print("limit=muchos         ->", response.status_code, response.json()["detail"][0]["loc"])


# ============================================
# PASO 4: Errores con HTTPException
# ============================================
# Descomenta las siguientes líneas:
# @app.get("/stations/{station_id}/name")
# def get_station_name(station_id: int) -> str:
#     if station_id not in STATIONS:
#         # raise, no return: corta la función y FastAPI responde con este código.
#         raise HTTPException(status_code=404, detail=f"no existe la estación {station_id}")
#     return STATIONS[station_id]
#
#
# print("\n--- Paso 4: errores ---")
# for path in ["/stations/1/name", "/stations/9/name", "/nada"]:
#     response = client.get(path)
#     print(f"GET {path:<17} -> {response.status_code} {response.json()}")
# response = client.post("/stations/1/name")
# print(f"POST /stations/1/name -> {response.status_code} {response.json()}")


# ============================================
# PASO 5: La documentación que FastAPI escribe solo
# ============================================
# Descomenta las siguientes líneas:
# schema = client.get("/openapi.json").json()
# print("\n--- Paso 5: /openapi.json ---")
# print("título:", schema["info"]["title"], "· versión:", schema["info"]["version"])
# for path, methods in schema["paths"].items():
#     for method, operation in methods.items():
#         names = [parameter["name"] for parameter in operation.get("parameters", [])]
#         print(f"  {method.upper():<4} {path:<28} parámetros: {names}")
# response = client.get("/docs")
# print("/docs ->", response.status_code, response.headers["content-type"])


# ============================================
# PASO 6: Un servidor de verdad
# ============================================
# Descomenta las siguientes líneas:
# # log_level="warning": sin las líneas INFO de cada petición, que irían mezcladas con las tuyas.
# config = uvicorn.Config(app, host="127.0.0.1", port=8001, log_level="warning")
# server = uvicorn.Server(config)
# thread = threading.Thread(target=server.run)
# print("\n--- Paso 6: uvicorn en 127.0.0.1:8001 ---")
# thread.start()
# while not server.started:
#     time.sleep(0.05)
# # Ahora sí hay red: httpx2 abre una conexión TCP con el puerto 8001.
# with httpx2.Client(base_url="http://127.0.0.1:8001") as http:
#     print("GET /           ->", http.get("/").json())
#     print("GET /stations/3 ->", http.get("/stations/3").json())
# server.should_exit = True
# thread.join()
# print("servidor parado")
