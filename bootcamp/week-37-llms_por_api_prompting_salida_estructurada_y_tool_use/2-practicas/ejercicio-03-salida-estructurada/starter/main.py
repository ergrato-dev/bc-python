"""Ejercicio 03 · Salida estructurada: JSON que se puede leer siempre.

Ejecuta `uv run python main.py` después de cada paso y compara con el README.
"""

import hashlib
import json
import os
from pathlib import Path
from typing import Literal

import anthropic
import httpx2
from pydantic import BaseModel, Field, ValidationError

MODEL = "claude-sonnet-5-5"


class Replay(httpx2.BaseTransport):
    """Repite las respuestas de respuestas.json sin salir a Internet: no hace falta clave.

    Cada respuesta está guardada con la huella de su petición (el cuerpo JSON). Si cambias
    una petición, la huella cambia y no hay respuesta: pruébala con tu clave (README)."""

    def __init__(self, path: Path) -> None:
        self.answers = json.loads(path.read_text(encoding="utf-8"))

    def handle_request(self, request: httpx2.Request) -> httpx2.Response:
        body = json.dumps(json.loads(request.content), sort_keys=True)
        fingerprint = hashlib.sha256(body.encode()).hexdigest()
        if fingerprint not in self.answers:
            raise LookupError("respuestas.json no tiene esta petición: ¿la has cambiado?")
        status, answer = self.answers[fingerprint]
        return httpx2.Response(status, json=answer)


def make_client() -> anthropic.Anthropic:
    """Con CLAUDE_REAL=1, la API de verdad (y tu ANTHROPIC_API_KEY); si no, la grabación."""
    if os.environ.get("CLAUDE_REAL") == "1":
        return anthropic.Anthropic()
    transport = Replay(Path("respuestas.json"))
    return anthropic.Anthropic(
        api_key="grabacion", max_retries=0, http_client=httpx2.Client(transport=transport)
    )


client = make_client()

print("Ejercicio 03 · Salida estructurada")

NOTES = [
    "El sensor de Norte dejó de enviar lecturas, la limpieza no lo arregló.",
    "En Centro se cambió el filtro sucio, sin avería, queda limpio.",
    "La estación Centro tenía deriva y se corrigió el cero, queda calibrado.",
    "La estación Sur tiene la placa quemada, se pidió un repuesto.",
]
SYSTEM = (
    "Clasificas notas de mantenimiento de una red de sensores: averia, limpieza o calibracion."
    " Fíjate en lo que se hizo, no en lo que se menciona de pasada."
)

# ============================================
# PASO 1: Pedir JSON en el prompt
# ============================================
# Descomenta las siguientes líneas:
# ASK_JSON = SYSTEM + (
#     ' Responde solo con un JSON: {"tipo": ..., "urgente": true o false, "resumen": ...}.'
# )
# for note in NOTES:
#     response = client.messages.create(
#         model=MODEL, max_tokens=300, system=ASK_JSON, messages=[{"role": "user", "content": note}]
#     )
#     text = response.content[0].text
#     try:
#         print(json.loads(text))
#     except json.JSONDecodeError as error:
#         print(f"no es JSON ({error.msg}): {text!r}")

# ============================================
# PASO 2: Un esquema JSON en output_config
# ============================================
# Descomenta las siguientes líneas:
# SCHEMA = {
#     "type": "object",
#     "properties": {
#         "tipo": {"type": "string", "enum": ["averia", "limpieza", "calibracion"]},
#         "urgente": {"type": "boolean"},
#         "resumen": {"type": "string"},
#     },
#     "required": ["tipo", "urgente", "resumen"],
#     "additionalProperties": False,
# }
# for note in NOTES:
#     response = client.messages.create(
#         model=MODEL,
#         max_tokens=300,
#         system=SYSTEM,
#         messages=[{"role": "user", "content": note}],
#         output_config={"format": {"type": "json_schema", "schema": SCHEMA}},
#     )
#     print(json.loads(response.content[0].text))


# ============================================
# PASO 3: El esquema con Pydantic
# ============================================
# Descomenta las siguientes líneas:
# class Reading(BaseModel):
#     tipo: Literal["averia", "limpieza", "calibracion"]
#     urgente: bool
#     resumen: str


# response = client.messages.parse(
#     model=MODEL,
#     max_tokens=300,
#     system=SYSTEM,
#     messages=[{"role": "user", "content": NOTES[3]}],
#     output_format=Reading,
# )
# reading = response.parsed_output
# print(repr(reading))
# print(f"{reading.tipo.upper()} · urgente: {'sí' if reading.urgente else 'no'} · {reading.resumen}")


# ============================================
# PASO 4: Extraer más de una nota larga
# ============================================
# Descomenta las siguientes líneas:
# class Maintenance(BaseModel):
#     tipo: Literal["averia", "limpieza", "calibracion"]
#     equipo: str | None = Field(description="El equipo que se tocó, si la nota lo dice.")
#     acciones: list[str] = Field(description="Lo que se hizo, una acción por elemento.")
#     urgencia: Literal["baja", "media", "alta"]
#     repuesto: bool = Field(description="Si hace falta pedir una pieza.")


# LONG = (
#     "Llegué a Oeste a las 9. El analizador de ozono no respondía: reinicié el equipo y"
#     " revisé el cableado, que estaba bien. La fuente de alimentación está quemada; hasta"
#     " que llegue la nueva, la estación no mide ozono."
# )
# SHORT = "Revisión de rutina en Este, todo normal."
# for note in [LONG, SHORT]:
#     response = client.messages.parse(
#         model=MODEL,
#         max_tokens=500,
#         system=SYSTEM,
#         messages=[{"role": "user", "content": note}],
#         output_format=Maintenance,
#     )
#     print(response.parsed_output.model_dump())


# ============================================
# PASO 5: Lo que el esquema no garantiza
# ============================================
# Descomenta las siguientes líneas:
# class Short(BaseModel):
#     tipo: Literal["averia", "limpieza", "calibracion"]
#     resumen: str = Field(max_length=40)


# La API no admite maxLength: el SDK lo pasa a la descripción, como una petición.
# print(anthropic.transform_schema(Short)["properties"]["resumen"])
# try:
#     client.messages.parse(
#         model=MODEL,
#         max_tokens=300,
#         system=SYSTEM,
#         messages=[{"role": "user", "content": LONG}],
#         output_format=Short,
#     )
# except ValidationError as error:
#     problem = error.errors()[0]
#     print(f"ValidationError en {problem['loc']}: {problem['msg']}")

# ============================================
# PASO 6: Mirar stop_reason antes de leer
# ============================================
# Descomenta las siguientes líneas:
# response = client.messages.create(
#     model=MODEL,
#     max_tokens=30,
#     system=SYSTEM,
#     messages=[{"role": "user", "content": LONG}],
#     output_config={
#         "format": {"type": "json_schema", "schema": anthropic.transform_schema(Maintenance)}
#     },
# )
# print(f"stop_reason: {response.stop_reason}")
# if response.stop_reason == "end_turn":
#     print(Maintenance.model_validate_json(response.content[0].text))
# else:
#     print(f"respuesta cortada, no se lee: {response.content[0].text!r}")
