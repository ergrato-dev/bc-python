"""Ejercicio 04: validadores y JSON.

Descomenta cada PASO cuando el README te lo pida y ejecuta:
    uv run python validators_lab.py
    uv run --with mypy==2.4.1 mypy --strict validators_lab.py
"""

import json
from dataclasses import dataclass
from typing import Self

from pydantic import (
    BaseModel,
    TypeAdapter,
    ValidationError,
    field_validator,
    model_validator,
)

print("Ejercicio 04 · Validadores y JSON")

# ============================================
# PASO 1: field_validator después del tipo
# ============================================
# Descomenta las siguientes líneas:
# class Reading(BaseModel):
#     label: str
#     value: float | None
#
#     @field_validator("label")
#     @classmethod
#     def clean_label(cls, label: str) -> str:
#         if any(char.isdigit() for char in label):
#             raise ValueError("la etiqueta no lleva números")
#         return label.strip().title()
#
#
# print("Normalizada:", Reading.model_validate({"label": "  zona norte ", "value": 12.5}))
# try:
#     Reading.model_validate({"label": "Norte2", "value": 12.5})
# except ValidationError as error:
#     print("Rechazada:", error.errors()[0]["msg"])

# ============================================
# PASO 2: field_validator antes del tipo
# ============================================
# Descomenta las siguientes líneas:
# class CommaReading(BaseModel):
#     label: str
#     value: float | None
#
#     @field_validator("value", mode="before")
#     @classmethod
#     def parse_comma(cls, value: object) -> object:
#         if isinstance(value, str):
#             text = value.strip()
#             return None if text == "NA" else text.replace(",", ".")
#         return value
#
#
# for raw in ["12,5", "NA", 8, "doce"]:
#     try:
#         print(f"{raw!r}:", CommaReading.model_validate({"label": "Norte", "value": raw}).value)
#     except ValidationError as error:
#         print(f"{raw!r}:", error.errors()[0]["msg"])

# ============================================
# PASO 3: model_validator compara campos
# ============================================
# Descomenta las siguientes líneas:
# class Thresholds(BaseModel):
#     low: float
#     high: float
#
#     @model_validator(mode="after")
#     def check_order(self) -> Self:
#         if self.low >= self.high:
#             raise ValueError(f"low ({self.low}) debe ser menor que high ({self.high})")
#         return self
#
#
# print("Válidos:", Thresholds(low=10, high=50))
# try:
#     Thresholds(low=50, high=10)
# except ValidationError as error:
#     print("Imposibles:", error.errors()[0]["loc"], error.errors()[0]["msg"])

# ============================================
# PASO 4: de modelo a JSON y vuelta
# ============================================
# Descomenta las siguientes líneas:
# missing = CommaReading(label="Sur", value=None)
# print("model_dump:", missing.model_dump())
# print("Sin los None:", missing.model_dump(exclude_none=True))
# text = CommaReading(label="Norte", value=12.5).model_dump_json()
# print("model_dump_json:", text)
# print("Y de vuelta:", CommaReading.model_validate_json(text))
# try:
#     CommaReading.model_validate_json('{"label": "Norte", "value": 12.5')
# except ValidationError as error:
#     print("JSON roto:", error.errors()[0]["type"], "·", error.errors()[0]["msg"])
# schema = Thresholds.model_json_schema()
# print("Esquema JSON:", json.dumps(schema["properties"], ensure_ascii=False))

# ============================================
# PASO 5: TypeAdapter para lo que no es un BaseModel
# ============================================
# Descomenta las siguientes líneas:
# readings = TypeAdapter(list[CommaReading])
# items = readings.validate_json('[{"label": "Norte", "value": "12,5"}, {"label": "Sur", "value": null}]')
# print("Lista validada:", items)
# try:
#     readings.validate_json('[{"label": "Norte", "value": 1}, {"label": "Sur"}]')
# except ValidationError as error:
#     print("Falla la medida", error.errors()[0]["loc"])
#
#
# @dataclass(frozen=True)
# class Scale:
#     unit: str
#     low: float
#     high: float
#
#     def __post_init__(self) -> None:
#         if self.low >= self.high:
#             raise ValueError("umbrales imposibles")
#
#
# scales = TypeAdapter(Scale)
# print("Una dataclass:", scales.validate_json('{"unit": "ppm", "low": "10", "high": 50}'))
# try:
#     scales.validate_json('{"unit": "ppm", "low": 50, "high": 10}')
# except ValidationError as error:
#     print("Su __post_init__ también:", error.errors()[0]["msg"])
