"""Ejercicio 04 · Evaluar un RAG: la búsqueda y las respuestas, con números.

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
PRICES = (2.00, 10.00)  # dólares por millón de tokens de entrada y de salida


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


def split(text: str, by_section: bool = False) -> list[str]:
    """Un trozo por párrafo (o por sección), con el título de su sección delante."""
    pieces: list[str] = []
    section = ""
    for block in text.split("\n\n"):
        block = block.strip()
        if block.startswith("#"):
            section = block.lstrip("# ")
        elif block and by_section and pieces and pieces[-1].startswith(f"{section}:"):
            pieces[-1] += " " + block
        elif block:
            pieces.append(f"{section}: {block}")
    return pieces


def ranking(pieces: list[str], question: str) -> list[int]:
    """Los números de todos los trozos, del más parecido a la pregunta al menos (TF-IDF)."""
    vectorizer = TfidfVectorizer(strip_accents="unicode")
    matrix = vectorizer.fit_transform(pieces)
    scores = (matrix @ vectorizer.transform([question]).T).toarray().ravel()
    return [int(number) for number in np.argsort(-scores, kind="stable")]


# Cada pregunta, con una frase que solo está en el trozo que la responde y el dato que
# debe traer la respuesta. Escribirlas a mano es la parte cara de evaluar: y la que más vale.
QUESTIONS = [
    ("¿Cada cuánto se visita una estación?", "una vez al mes", "una vez al mes"),
    ("¿Cuándo hay que cambiar el filtro antes de tiempo?", "50 Pa", "50 Pa"),
    ("¿Cómo compruebo que no hay fugas?", "prueba de fugas", "tapa la entrada"),
    ("¿Con qué se limpia la toma de aire?", "cepillo suave", "cepillo"),
    (
        "¿Cada cuánto se calibra el analizador de ozono?",
        "cada tres meses",
        "tres meses",
    ),
    ("¿Qué significa que el ozono salga negativo?", "lecturas negativas", "cero"),
    ("¿Dónde se calibra el sensor de partículas?", "una vez al año", "laboratorio"),
    ("¿Cuánto aguanta la estación sin corriente?", "cuatro horas", "cuatro horas"),
    ("¿Qué datos no valen después de un apagón?", "30 minutos", "30 minutos"),
    ("¿Cuánto tarda en llegar un repuesto?", "una semana", "una semana"),
    ("¿Qué pasa si una estación deja de transmitir?", "tarjeta de memoria", "tarjeta"),
    ("¿Cómo se llevan las botellas de gas?", "posición vertical", "vertical"),
]

print("Ejercicio 04 · Evaluar un RAG")

# ============================================
# PASO 1: Un conjunto de preguntas etiquetadas
# ============================================
# Descomenta las siguientes líneas:
# pieces = split(MANUAL)


# def relevant(pieces: list[str], phrase: str) -> int:
#     """El número del único trozo que contiene la frase: el que responde la pregunta."""
#     [number] = [n for n, piece in enumerate(pieces) if phrase in piece]
#     return number


# labels = [relevant(pieces, phrase) for _, phrase, _ in QUESTIONS]
# print(
#     f"{len(QUESTIONS)} preguntas · {len(pieces)} trozos · trozos que responden: {labels}"
# )

# ============================================
# PASO 2: ¿Está el trozo bueno entre los k primeros?
# ============================================
# Descomenta las siguientes líneas:


# def positions(pieces: list[str], labels: list[int]) -> list[int]:
#     """En qué puesto sale el trozo que responde cada pregunta: 1, el primero."""
#     return [
#         ranking(pieces, question).index(label) + 1
#         for (question, _, _), label in zip(QUESTIONS, labels, strict=True)
#     ]


# places = positions(pieces, labels)
# print("puestos:", places)
# for k in [1, 3, 5]:
#     hits = sum(place <= k for place in places)
#     print(f"recall@{k}: {hits / len(places):.2f} ({hits} de {len(places)})")

# ============================================
# PASO 3: El rango recíproco medio (MRR)
# ============================================
# Descomenta las siguientes líneas:


# def mrr(places: list[int]) -> float:
#     """La media de 1/puesto: 1 si el bueno sale siempre primero; 0,5 si sale segundo."""
#     return float(np.mean([1 / place for place in places]))


# print(f"MRR: {mrr(places):.2f}")
# for (question, _, _), place in zip(QUESTIONS, places, strict=True):
#     if place > 3:
#         print(f"  puesto {place}: {question}")

# ============================================
# PASO 4: Otro troceo, otros números
# ============================================
# Descomenta las siguientes líneas:
# sections = split(MANUAL, by_section=True)
# section_labels = [relevant(sections, phrase) for _, phrase, _ in QUESTIONS]
# for name, chunks, chunk_labels in [
#     ("párrafos", pieces, labels),
#     ("secciones", sections, section_labels),
# ]:
#     places = positions(chunks, chunk_labels)
#     size = np.mean([len(chunk) for chunk in chunks])
#     print(
#         f"{name:>9}: {len(chunks)} trozos de {size:.0f} caracteres · recall@1"
#         f" {np.mean([p <= 1 for p in places]):.2f} · recall@3 {np.mean([p <= 3 for p in places]):.2f}"
#         f" · MRR {mrr(places):.2f}"
#     )

# ============================================
# PASO 5: Las respuestas, con comprobaciones
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
# tokens = [0, 0]


# def fragments(numbers: list[int]) -> str:
#     rows = "\n".join(f'<fragmento id="{n}">{pieces[n]}</fragmento>' for n in numbers)
#     return f"<fragmentos>\n{rows}\n</fragmentos>"


# def ask(system: str, content: str, model: type[BaseModel]) -> BaseModel:
#     """Una petición con salida estructurada; suma sus tokens a `tokens`."""
#     config: OutputConfigParam = {
#         "format": {"type": "json_schema", "schema": anthropic.transform_schema(model)},
#         "effort": "low",
#     }
#     response = client.messages.create(
#         model=MODEL,
#         max_tokens=500,
#         system=system,
#         messages=[{"role": "user", "content": content}],
#         output_config=config,
#     )
#     tokens[0] += response.usage.input_tokens
#     tokens[1] += response.usage.output_tokens
#     return model.model_validate_json(
#         next(b.text for b in response.content if b.type == "text")
#     )


# answers = []
# print("cita válida · cita el bueno · trae el dato · pregunta")
# CHOSEN = [
#     1,
#     3,
#     4,
#     5,
#     7,
# ]  # cinco preguntas: las tres primeras, bien recuperadas; las otras dos, no
# for number in CHOSEN:
#     (question, _, fact), label = QUESTIONS[number], labels[number]
#     given = ranking(pieces, question)[:3]
#     content = f"{fragments(given)}\n<pregunta>{question}</pregunta>"
#     answer = ask(SYSTEM, content, Answer)
#     assert isinstance(answer, Answer)
#     answers.append((question, given, answer))
#     checks = [
#         all(number in given for number in answer.citas),
#         label in answer.citas,
#         fact in answer.respuesta,
#     ]
#     print(
#         "  " + "  ·  ".join("sí" if check else "no" for check in checks), "·", question
#     )

# ============================================
# PASO 6: Claude como juez
# ============================================
# Descomenta las siguientes líneas:


# class Verdict(BaseModel):
#     fiel: bool = Field(
#         description="Si todo lo que dice la respuesta está en los fragmentos."
#     )
#     motivo: str = Field(description="Por qué, en 20 palabras o menos.")


# JUDGE = "\n".join(
#     [
#         "Revisas respuestas de un asistente que solo debe usar los fragmentos que recibe.",
#         "Una respuesta es fiel si todo lo que afirma está en los fragmentos.",
#         "Una respuesta incompleta puede ser fiel; una que añade algo que no está, no.",
#     ]
# )
# for question, given, answer in answers:
#     content = (
#         f"{fragments(given)}\n<pregunta>{question}</pregunta>\n"
#         f"<respuesta>{answer.respuesta}</respuesta>"
#     )
#     verdict = ask(JUDGE, content, Verdict)
#     assert isinstance(verdict, Verdict)
#     print(f"{'fiel' if verdict.fiel else 'NO fiel'} · {question} · {verdict.motivo}")
# cost = (tokens[0] * PRICES[0] + tokens[1] * PRICES[1]) / 1_000_000
# print(
#     f"evaluar 5 respuestas: {tokens[0]} tokens de entrada y {tokens[1]} de salida · {cost:.4f} $"
# )
