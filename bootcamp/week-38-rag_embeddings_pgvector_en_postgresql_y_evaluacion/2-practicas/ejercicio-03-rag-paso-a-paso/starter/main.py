"""Ejercicio 03 · RAG paso a paso: buscar en un manual y responder con lo encontrado.

Ejecuta `uv run python main.py` después de cada paso y compara con el README.
"""

import hashlib
import json
import os
from pathlib import Path

import anthropic
import httpx2
import numpy as np
from anthropic.types import OutputConfigParam
from pydantic import BaseModel, Field
from sklearn.feature_extraction.text import TfidfVectorizer

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
            raise LookupError(
                "respuestas.json no tiene esta petición: ¿la has cambiado?"
            )
        status, answer = self.answers[fingerprint]
        return httpx2.Response(status, json=answer)


def make_client() -> anthropic.Anthropic:
    """Con CLAUDE_REAL=1, la API de verdad (y tu ANTHROPIC_API_KEY); si no, la grabación."""
    if os.environ.get("CLAUDE_REAL") == "1":
        return anthropic.Anthropic()
    transport = Replay(Path("respuestas.json"))
    return anthropic.Anthropic(
        api_key="grabacion",
        max_retries=0,
        http_client=httpx2.Client(transport=transport),
    )


client = make_client()
MANUAL = Path("manual.md").read_text(encoding="utf-8")
QUESTION = "¿Cada cuánto hay que cambiar el filtro de partículas?"

print("Ejercicio 03 · RAG paso a paso")

# ============================================
# PASO 1: Preguntar sin contexto
# ============================================
# Descomenta las siguientes líneas:
# response = client.messages.create(
#     model=MODEL, max_tokens=300, messages=[{"role": "user", "content": QUESTION}]
# )
# print(next(block.text for block in response.content if block.type == "text"))
# print(
#     f"tokens: {response.usage.input_tokens} de entrada y {response.usage.output_tokens} de salida"
# )

# ============================================
# PASO 2: Trocear el manual
# ============================================
# Descomenta las siguientes líneas:


# def split(text: str) -> list[str]:
#     """Un trozo por párrafo, con el título de su sección delante: «Sección: párrafo»."""
#     pieces = []
#     section = ""
#     for block in text.split("\n\n"):
#         block = block.strip()
#         if block.startswith("#"):
#             section = block.lstrip("# ")
#         elif block:
#             pieces.append(f"{section}: {block}")
#     return pieces


# pieces = split(MANUAL)
# sizes = [len(piece) for piece in pieces]
# print(f"{len(pieces)} trozos · de {min(sizes)} a {max(sizes)} caracteres")
# print("trozo 2:", pieces[2])

# ============================================
# PASO 3: Recuperar los trozos más parecidos
# ============================================
# Descomenta las siguientes líneas:
# vectorizer = TfidfVectorizer(strip_accents="unicode")
# matrix = vectorizer.fit_transform(pieces)


# def retrieve(question: str, k: int = 3) -> list[int]:
#     """Los números de los k trozos más parecidos a la pregunta, del más parecido al menos."""
#     scores = (matrix @ vectorizer.transform([question]).T).toarray().ravel()
#     best = np.argsort(-scores, kind="stable")[:k]
#     for number in best:
#         print(f"  [{number}] {scores[number]:.2f} · {pieces[number][:70]}…")
#     return [int(number) for number in best]


# found = retrieve(QUESTION)

# ============================================
# PASO 4: Aumentar el prompt y generar, con citas
# ============================================
# Descomenta las siguientes líneas:


# class Answer(BaseModel):
#     respuesta: str = Field(
#         description="La respuesta, en español y en 40 palabras o menos."
#     )
#     citas: list[int] = Field(
#         description="Los números de los fragmentos en que se apoya."
#     )


# SYSTEM = "\n".join(
#     [
#         "Respondes preguntas sobre el manual de mantenimiento de una red de estaciones.",
#         "Usa solo los fragmentos que van entre <fragmentos> y </fragmentos>.",
#         "En citas, pon el número (id) de cada fragmento en que te apoyas.",
#         "Si los fragmentos no responden a la pregunta, dilo así y deja citas vacía.",
#     ]
# )
# CONFIG: OutputConfigParam = {
#     "format": {"type": "json_schema", "schema": anthropic.transform_schema(Answer)},
#     "effort": "low",
# }


# def ask(question: str, numbers: list[int]) -> Answer:
#     """Pide la respuesta con los trozos `numbers` en el prompt, cada uno con su número."""
#     fragments = "\n".join(
#         f'<fragmento id="{n}">{pieces[n]}</fragmento>' for n in numbers
#     )
#     content = (
#         f"<fragmentos>\n{fragments}\n</fragmentos>\n<pregunta>{question}</pregunta>"
#     )
#     response = client.messages.create(
#         model=MODEL,
#         max_tokens=500,
#         system=SYSTEM,
#         messages=[{"role": "user", "content": content}],
#         output_config=CONFIG,
#     )
#     usage = response.usage
#     print(
#         f"  tokens: {usage.input_tokens} de entrada y {usage.output_tokens} de salida"
#     )
#     return Answer.model_validate_json(
#         next(b.text for b in response.content if b.type == "text")
#     )


# answer = ask(QUESTION, found)
# print(answer.respuesta)
# print("citas:", answer.citas)

# ============================================
# PASO 5: Comprobar las citas
# ============================================
# Descomenta las siguientes líneas:


# def check(answer: Answer, numbers: list[int]) -> None:
#     """Las citas deben ser de trozos que Claude recibió: si no, no pudo leerlos."""
#     invented = [number for number in answer.citas if number not in numbers]
#     if invented:
#         print("  cita trozos que no recibió:", invented)
#     else:
#         print("  todas las citas son de trozos que recibió")


# check(answer, found)
# OTHER = "¿Qué hago si el analizador de ozono da lecturas negativas?"
# numbers = retrieve(OTHER)
# other = ask(OTHER, numbers)
# print(other.respuesta)
# check(other, numbers)

# ============================================
# PASO 6: Lo que el manual no dice, y k
# ============================================
# Descomenta las siguientes líneas:
# PRICE = "¿Cuánto cuesta un analizador de ozono nuevo?"
# print(ask(PRICE, retrieve(PRICE)).respuesta)
# BOTH = "¿Qué pasa con los datos si hay un corte de energía largo?"
# for k in [1, 3]:
#     print(f"k = {k}:")
#     print(ask(BOTH, retrieve(BOTH, k)).respuesta)
