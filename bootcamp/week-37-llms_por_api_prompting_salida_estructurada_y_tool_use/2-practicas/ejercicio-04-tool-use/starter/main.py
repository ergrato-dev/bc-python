"""Ejercicio 04 · Tool use: Claude consulta los datos con tus funciones.

Ejecuta `uv run python main.py` después de cada paso y compara con el README.
"""

import hashlib
import json
import os
import statistics
from pathlib import Path

import anthropic
import httpx2
from anthropic import beta_tool

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

print("Ejercicio 04 · Tool use")

# Unas medidas de PM2.5 (µg/m³) y unas notas por estación: los datos que Claude no tiene.
READINGS = {
    "Norte": [38.0, 41.5, 44.0, 52.5],
    "Sur": [55.0, 61.0, 58.5, 49.5],
    "Centro": [30.5, 33.0, 29.0, 35.5],
    "Este": [22.0, 25.5, 24.0, 21.5],
    "Oeste": [40.0, 39.5, 43.0, 41.5],
}
NOTES = {
    "Norte": ["Se lavó la carcasa del equipo, queda limpio."],
    "Sur": ["La placa está quemada, se pidió un repuesto.", "Se recalibró con gas de referencia."],
    "Centro": ["Se cambió el filtro sucio."],
    "Este": [],
    "Oeste": ["Se ajustó la ganancia del sensor."],
}


def statistics_of(label: str) -> dict[str, object]:
    """Lo que hace la herramienta `estadisticas`: n, media, mínimo y máximo de una estación."""
    if label not in READINGS:
        raise KeyError(f"no hay estación {label}; las estaciones son {', '.join(READINGS)}")
    values = READINGS[label]
    return {
        "etiqueta": label,
        "n": len(values),
        "media": round(statistics.mean(values), 2),
        "minimo": min(values),
        "maximo": max(values),
    }


def notes_of(label: str) -> list[str]:
    """Lo que hace la herramienta `notas`: las notas de mantenimiento de una estación."""
    if label not in NOTES:
        raise KeyError(f"no hay estación {label}; las estaciones son {', '.join(NOTES)}")
    return NOTES[label]


def label_schema(text: str) -> dict[str, object]:
    return {
        "type": "object",
        "properties": {"etiqueta": {"type": "string", "description": text}},
        "required": ["etiqueta"],
        "additionalProperties": False,
    }


TOOLS = [
    {
        "name": "estadisticas",
        "description": "Número de medidas, media, mínimo y máximo de PM2.5 (µg/m³) de una estación.",
        "input_schema": label_schema("La etiqueta de la estación, por ejemplo Norte."),
        "strict": True,
    },
    {
        "name": "notas",
        "description": "Las notas de mantenimiento de una estación, de la más antigua a la más nueva.",
        "input_schema": label_schema("La etiqueta de la estación, por ejemplo Norte."),
        "strict": True,
    },
]
FUNCTIONS = {"estadisticas": statistics_of, "notas": notes_of}
SYSTEM = "Respondes sobre las estaciones de un observatorio de calidad del aire. Usa las herramientas para los datos; no los inventes."

# ============================================
# PASO 1: Claude pide una herramienta
# ============================================
# Descomenta las siguientes líneas:
# question = [{"role": "user", "content": "¿Cuál es la media de PM2.5 en Norte?"}]
# response = client.messages.create(
#     model=MODEL, max_tokens=1000, system=SYSTEM, tools=TOOLS, messages=question
# )
# print(f"stop_reason: {response.stop_reason}")
# for block in response.content:
#     if block.type == "text":
#         print(f"texto: {block.text}")
#     elif block.type == "tool_use":
#         print(f"tool_use: {block.name}({block.input}) · id {block.id}")

# ============================================
# PASO 2: Tú ejecutas la herramienta y devuelves el resultado
# ============================================
# Descomenta las siguientes líneas:
# call = next(block for block in response.content if block.type == "tool_use")
# result = FUNCTIONS[call.name](call.input["etiqueta"])
# print(f"resultado: {result}")
# messages = [
#     *question,
#     {"role": "assistant", "content": response.content},
#     {
#         "role": "user",
#         "content": [
#             {"type": "tool_result", "tool_use_id": call.id, "content": json.dumps(result)}
#         ],
#     },
# ]
# final = client.messages.create(
#     model=MODEL, max_tokens=1000, system=SYSTEM, tools=TOOLS, messages=messages
# )
# print(f"stop_reason: {final.stop_reason}")
# print(final.content[0].text)


# ============================================
# PASO 3: El bucle
# ============================================
# Descomenta las siguientes líneas:
# def run(text: str, turns: int = 5) -> None:
#     """Pregunta, ejecuta las herramientas que pida Claude y repite hasta que conteste."""
#     messages: list[dict[str, object]] = [{"role": "user", "content": text}]
#     used = 0
#     for turn in range(1, turns + 1):
#         response = client.messages.create(
#             model=MODEL, max_tokens=1000, system=SYSTEM, tools=TOOLS, messages=messages
#         )
#         used += response.usage.input_tokens + response.usage.output_tokens
#         if response.stop_reason != "tool_use":
#             print(f"vuelta {turn}: {response.content[-1].text}")
#             print(f"{turn} vueltas · {used} tokens")
#             return
#         messages.append({"role": "assistant", "content": response.content})
#         results = []
#         for block in response.content:
#             if block.type != "tool_use":
#                 continue
#             try:
#                 output, failed = json.dumps(FUNCTIONS[block.name](block.input["etiqueta"])), False
#             except KeyError as error:
#                 output, failed = str(error.args[0]), True
#             print(
#                 f"vuelta {turn}: {block.name}({block.input['etiqueta']}){' → error' if failed else ''}"
#             )
#             results.append(
#                 {
#                     "type": "tool_result",
#                     "tool_use_id": block.id,
#                     "content": output,
#                     "is_error": failed,
#                 }
#             )
        # Todos los resultados de una vuelta, en un solo mensaje.
#         messages.append({"role": "user", "content": results})
#     print(f"sin respuesta: límite de vueltas ({turns}) · {used} tokens")


# run("¿Qué estación tiene la media de PM2.5 más alta, y qué dicen sus notas de mantenimiento?")

# ============================================
# PASO 4: Cuando la herramienta falla
# ============================================
# Descomenta las siguientes líneas:
# run("¿Cuál es la media de PM2.5 en Sureste?")

# ============================================
# PASO 5: Un límite de vueltas
# ============================================
# Descomenta las siguientes líneas:
# run(
#     "¿Qué estación tiene la media de PM2.5 más alta, y qué dicen sus notas de mantenimiento?",
#     turns=1,
# )


# ============================================
# PASO 6: El tool runner del SDK
# ============================================
# Descomenta las siguientes líneas:
# @beta_tool
# def estadisticas(etiqueta: str) -> str:
#     """Número de medidas, media, mínimo y máximo de PM2.5 (µg/m³) de una estación.

#     Args:
#         etiqueta: La etiqueta de la estación, por ejemplo Norte.
#     """
#     return json.dumps(statistics_of(etiqueta))


# runner = client.beta.messages.tool_runner(
#     model=MODEL,
#     max_tokens=1000,
#     system=SYSTEM,
#     tools=[estadisticas],
#     messages=[{"role": "user", "content": "¿Cuál es la media de PM2.5 en Sur?"}],
# )
# for message in runner:
#     print(f"{message.stop_reason}: {[block.type for block in message.content]}")
# print(message.content[-1].text)
