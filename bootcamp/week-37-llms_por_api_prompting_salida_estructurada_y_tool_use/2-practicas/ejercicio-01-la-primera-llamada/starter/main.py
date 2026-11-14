"""Ejercicio 01 · La primera llamada a Claude.

Ejecuta `uv run python main.py` después de cada paso y compara con el README.
"""

import hashlib
import json
import os
from pathlib import Path

import anthropic
import httpx2

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

print("Ejercicio 01 · La primera llamada a Claude")
print(
    f"modelo {MODEL} · {'API de verdad' if os.environ.get('CLAUDE_REAL') == '1' else 'respuestas grabadas'}"
)

QUESTION = "En una frase: ¿qué es un sensor de calidad del aire?"

# ============================================
# PASO 1: Una pregunta, una respuesta
# ============================================
# Descomenta las siguientes líneas:
# Un mensaje del usuario y el máximo de tokens que puede escribir Claude.
# response = client.messages.create(
#     model=MODEL,
#     max_tokens=300,
#     messages=[{"role": "user", "content": QUESTION}],
# )
# La respuesta es una lista de bloques: aquí, uno de texto.
# print(response.content[0].text)

# ============================================
# PASO 2: Lo que trae la respuesta
# ============================================
# Descomenta las siguientes líneas:
# print(f"id {response.id} · modelo {response.model}")
# print(f"bloques: {[block.type for block in response.content]}")
# print(f"stop_reason: {response.stop_reason}")
# print(
#     f"tokens: {response.usage.input_tokens} de entrada, {response.usage.output_tokens} de salida"
# )

# ============================================
# PASO 3: El prompt de sistema
# ============================================
# Descomenta las siguientes líneas:
# El sistema dice quién responde, a quién y cómo; el mensaje, qué se pregunta.
# SYSTEM = "Respondes a técnicos de campo de una red de sensores. Como mucho 15 palabras."
# short = client.messages.create(
#     model=MODEL,
#     max_tokens=300,
#     system=SYSTEM,
#     messages=[{"role": "user", "content": QUESTION}],
# )
# print(short.content[0].text)
# print(f"tokens: {short.usage.input_tokens} de entrada, {short.usage.output_tokens} de salida")

# ============================================
# PASO 4: La API no recuerda nada
# ============================================
# Descomenta las siguientes líneas:
# FOLLOW_UP = "¿Y cada cuánto se calibra?"
# alone = client.messages.create(
#     model=MODEL, max_tokens=300, system=SYSTEM, messages=[{"role": "user", "content": FOLLOW_UP}]
# )
# print(f"sin historia: {alone.content[0].text}")
# La conversación entera viaja en cada petición: tus mensajes y los de Claude.
# history = [
#     {"role": "user", "content": QUESTION},
#     {"role": "assistant", "content": short.content[0].text},
#     {"role": "user", "content": FOLLOW_UP},
# ]
# together = client.messages.create(model=MODEL, max_tokens=300, system=SYSTEM, messages=history)
# print(f"con historia: {together.content[0].text}")
# print(
#     f"tokens de entrada: {alone.usage.input_tokens} sin historia, {together.usage.input_tokens} con historia"
# )

# ============================================
# PASO 5: Cuando se acaba max_tokens
# ============================================
# Descomenta las siguientes líneas:
# cut = client.messages.create(
#     model=MODEL, max_tokens=20, messages=[{"role": "user", "content": QUESTION}]
# )
# print(f"stop_reason: {cut.stop_reason} · {cut.usage.output_tokens} tokens de salida")
# print(f"texto: {cut.content[0].text}")

# ============================================
# PASO 6: Lo que cuesta
# ============================================
# Descomenta las siguientes líneas:
# Dólares por millón de tokens (entrada, salida), del 2026-11-13.
# PRICES = {
#     "claude-haiku-5-5": (0.10, 0.50),
#     "claude-sonnet-5-5": (2.00, 10.00),
#     "claude-opus-5-5": (4.00, 20.00),
# }
# used = response.usage
# for name, (inp, outp) in PRICES.items():
#     one = (used.input_tokens * inp + used.output_tokens * outp) / 1_000_000
#     print(
#         f"{name:>18} · una respuesta como la del paso 1: {one:.6f} $ · mil al día, 30 días: {one * 1000 * 30:.2f} $"
#     )

# ============================================
# PASO 7: Cuando algo falla
# ============================================
# Descomenta las siguientes líneas:
# try:
#     client.messages.create(
#         model="claude-sonnet-9", max_tokens=300, messages=[{"role": "user", "content": QUESTION}]
#     )
# except anthropic.NotFoundError as error:
#     print(f"NotFoundError {error.status_code}: {error.body['error']['message']}")
# try:
#     client.messages.create(model=MODEL, max_tokens=300, messages=[])
# except anthropic.BadRequestError as error:
#     print(f"BadRequestError {error.status_code}: {error.body['error']['message']}")
