"""Ejercicio 02 · Cuerpos y respuestas con Pydantic.

Los datos que llegan en el cuerpo de un POST se validan con un modelo de Pydantic,
y lo que sale se filtra con otro. Todo se prueba con TestClient, sin servidor.
"""

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query, Response, status
from fastapi.testclient import TestClient
from pydantic import BaseModel, ConfigDict, Field

print("Ejercicio 02 · Cuerpos y respuestas con Pydantic")

app = FastAPI()
client = TestClient(app)

# Lo que la API va guardando, en memoria: se pierde al terminar el programa.
SAVED: list[dict[str, object]] = []


# ============================================
# PASO 1: Un cuerpo con un modelo
# ============================================
# Descomenta las siguientes líneas:
# class ReadingIn(BaseModel):
#     label: str
#     value: float | None
#
#
# @app.post("/readings", status_code=status.HTTP_201_CREATED)
# def post_reading(reading: ReadingIn) -> dict[str, object]:
#     # Un parámetro con un modelo de Pydantic es el cuerpo JSON de la petición.
#     print("  la función recibe:", repr(reading))
#     SAVED.append({"id": len(SAVED) + 1, **reading.model_dump(), "author": "ana@example.com"})
#     return SAVED[-1]
#
#
# print("\n--- Paso 1: POST /readings ---")
# response = client.post("/readings", json={"label": "Norte", "value": 12.5})
# print("estado:", response.status_code, "· cuerpo:", response.json())
# response = client.post("/readings", json={"label": "Sur", "value": "30"})
# print("estado:", response.status_code, "· cuerpo:", response.json())


# ============================================
# PASO 2: Lo que no es válido: 422
# ============================================
# Descomenta las siguientes líneas:
# print("\n--- Paso 2: cuerpos no válidos ---")
# bad_bodies = [
#     {"label": "Norte"},
#     {"label": "Norte", "value": "mucho"},
#     {"label": ["Norte"], "value": 1},
#     "Norte;12,5",
# ]
# for body in bad_bodies:
#     response = client.post("/readings", json=body)
#     print(f"{body!r:<38} -> {response.status_code}")
#     for error in response.json()["detail"]:
#         print(f"    {error['loc']}: {error['msg']}")
# print("guardadas:", len(SAVED), "(ninguna de las no válidas)")


# ============================================
# PASO 3: Reglas en el modelo
# ============================================
# Descomenta las siguientes líneas:
# class StrictReadingIn(BaseModel):
#     # extra="forbid": una clave que el modelo no conoce es un error, no se ignora.
#     model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
#
#     label: Annotated[str, Field(min_length=1, max_length=20)]
#     value: Annotated[float | None, Field(ge=-50, le=150)]
#
#
# @app.post("/strict-readings", status_code=status.HTTP_201_CREATED)
# def post_strict_reading(reading: StrictReadingIn) -> StrictReadingIn:
#     return reading
#
#
# print("\n--- Paso 3: reglas ---")
# bodies = [
#     {"label": "  Norte  ", "value": 12.5},
#     {"label": "", "value": 12.5},
#     {"label": "Norte", "value": 200},
#     {"label": "Norte", "value": 1, "unit": "°C"},
# ]
# for body in bodies:
#     response = client.post("/strict-readings", json=body)
#     detail = response.json()
#     message = detail if response.status_code == 201 else detail["detail"][0]["msg"]
#     print(f"{body!r:<46} -> {response.status_code} {message}")


# ============================================
# PASO 4: Lo que sale: el modelo de respuesta
# ============================================
# Descomenta las siguientes líneas:
# class ReadingOut(BaseModel):
#     id: int
#     label: str
#     value: float | None
#
#
# @app.get("/readings")
# def get_readings(
#     limit: Annotated[int, Query(ge=1, le=100)] = 10,
# ) -> list[ReadingOut]:
#     # SAVED lleva "author", con un correo: el tipo de retorno lo filtra al responder.
#     return [ReadingOut.model_validate(item) for item in SAVED[:limit]]
#
#
# print("\n--- Paso 4: GET /readings ---")
# print("guardado:", SAVED[0])
# print("respuesta:", client.get("/readings").json())
# print("limit=0 ->", client.get("/readings?limit=0").status_code)


# ============================================
# PASO 5: Códigos y cabeceras
# ============================================
# Descomenta las siguientes líneas:
# @app.post("/places", status_code=status.HTTP_201_CREATED)
# def post_place(place: ReadingIn, response: Response) -> dict[str, int]:
#     SAVED.append({"id": len(SAVED) + 1, **place.model_dump()})
#     # Location: dónde está lo que acabas de crear. Lo lee quien llama.
#     response.headers["Location"] = f"/readings/{len(SAVED)}"
#     return {"id": len(SAVED)}
#
#
# @app.delete("/readings/{reading_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_reading(reading_id: int) -> None:
#     for item in SAVED:
#         if item["id"] == reading_id:
#             SAVED.remove(item)
#             return
#     raise HTTPException(status.HTTP_404_NOT_FOUND, f"no existe la medida {reading_id}")
#
#
# print("\n--- Paso 5: códigos y cabeceras ---")
# response = client.post("/places", json={"label": "Este", "value": None})
# print("POST /places      ->", response.status_code, response.headers["location"])
# response = client.delete("/readings/1")
# print("DELETE /readings/1 ->", response.status_code, repr(response.content))
# response = client.delete("/readings/1")
# print("DELETE /readings/1 ->", response.status_code, response.json())


# ============================================
# PASO 6: Fechas y dataclasses
# ============================================
# Descomenta las siguientes líneas:
# @dataclass(frozen=True)
# class Summary:
#     readings: int
#     mean: float | None
#     at: datetime
#
#
# @app.get("/summary")
# def get_summary() -> Summary:
#     # Una dataclass también vale como respuesta; la fecha sale en ISO 8601.
#     values = [item["value"] for item in SAVED if isinstance(item["value"], float)]
#     mean = sum(values) / len(values) if values else None
#     return Summary(len(SAVED), mean, datetime(2026, 11, 8, 10, 30, tzinfo=UTC))
#
#
# print("\n--- Paso 6: GET /summary ---")
# print(client.get("/summary").text)
