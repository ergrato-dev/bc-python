"""Ejercicio 03: modelos de Pydantic.

Descomenta cada PASO cuando el README te lo pida y ejecuta:
    uv run python models_lab.py
    uv run --with mypy==2.4.1 mypy --strict models_lab.py
"""

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, ValidationError

print("Ejercicio 03 · Modelos de Pydantic")

# ============================================
# PASO 1: un modelo valida y convierte
# ============================================
# Descomenta las siguientes líneas:
# class Reading(BaseModel):
#     label: str
#     value: float | None
#
#
# reading = Reading(label="Norte", value=12.5)
# print("Con el constructor:", reading)
# print("repr:", repr(reading))
# print("Un texto con un número:", Reading.model_validate({"label": "Sur", "value": "8.0"}))
# print("Un entero:", Reading.model_validate({"label": "Sur", "value": 8}))
# print("Un booleano:", Reading.model_validate({"label": "Sur", "value": True}))

# ============================================
# PASO 2: ValidationError dice qué falla y dónde
# ============================================
# Descomenta las siguientes líneas:
# try:
#     Reading.model_validate({"label": 5, "value": "doce"})
# except ValidationError as error:
#     print("Errores:", error.error_count())
#     print(error)
#     for problem in error.errors():
#         print("  ", problem["loc"], problem["type"], "·", problem["msg"])

# ============================================
# PASO 3: modo estricto
# ============================================
# Descomenta las siguientes líneas:
# class StrictReading(BaseModel):
#     model_config = ConfigDict(strict=True)
#
#     label: str
#     value: float | None
#
#
# print("Un entero sigue valiendo:", StrictReading.model_validate({"label": "N", "value": 3}))
# for raw in ["8.0", True]:
#     try:
#         StrictReading.model_validate({"label": "N", "value": raw})
#     except ValidationError as error:
#         print(f"{raw!r} en estricto:", error.errors()[0]["msg"])

# ============================================
# PASO 4: restricciones con Field y claves de más
# ============================================
# Descomenta las siguientes líneas:
# class Station(BaseModel):
#     model_config = ConfigDict(extra="forbid", frozen=True)
#
#     name: Annotated[str, Field(min_length=1, max_length=20)]
#     altitude: Annotated[float, Field(ge=0)] = 0.0
#     tags: list[str] = Field(default_factory=list)
#     readings: list[Reading] = []
#
#
# print("Con los valores por defecto:", Station(name="Norte"))
# try:
#     Station.model_validate({"name": "", "altitude": -5, "zone": "centro"})
# except ValidationError as error:
#     print(error)

# ============================================
# PASO 5: modelos anidados, frozen y model_copy
# ============================================
# Descomenta las siguientes líneas:
# raw = {"name": "Norte", "readings": [{"label": "N1", "value": "12.5"}, {"label": "N2", "value": None}]}
# station = Station.model_validate(raw)
# print("Anidado:", station.readings)
# print("Cada medida es un Reading:", type(station.readings[0]).__name__)
# try:
#     station.name = "Sur"  # type: ignore[misc]
# except ValidationError as error:
#     print("frozen:", error.errors()[0]["msg"])
# moved = station.model_copy(update={"altitude": -100})
# print("model_copy no valida:", moved.altitude)
# print("model_validate sí:", Station.model_validate(moved.model_dump() | {"altitude": 2600}).altitude)
