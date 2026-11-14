"""Tests de la semana 37: leer las notas con Claude por la API.

Qué: comprueban core/llm.py (el esquema de la respuesta, el prompt, el reparto, las
peticiones, los tokens y el coste, las respuestas incompletas y las grabaciones) y el
comando `leer-notas`.
Para qué: ningún test sale a Internet ni necesita una clave. La API la sustituye
httpx2.MockTransport: una función que recibe la petición, que el test puede mirar, y
devuelve una respuesta con la forma exacta de la API de Messages.
Impacto: si un test llamara a la API de verdad, la CI fallaría sin clave y costaría dinero
en cada ejecución.
"""

import json
import random
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path

import anthropic
import httpx2
import pandas as pd
import pytest
from pydantic import ValidationError
from typer.testing import CliRunner

import observatorio.core
from observatorio import cli
from observatorio.core import llm
from observatorio.core.llm import (
    EFFORT,
    MAX_TOKENS,
    MODEL,
    PRICES,
    MissingAnswerError,
    Reading,
    Recording,
    Report,
    instructions,
    key,
    pick,
    read,
    schema,
    split,
)

runner = CliRunner()
CLASSES = ("averia", "calibracion", "limpieza")
Handler = Callable[[httpx2.Request], httpx2.Response]

# Por tipo, palabras que solo dicen ese tipo: el Claude falso de los tests las busca.
WORDS = {
    "averia": ["apagado", "roto", "quemado", "caído"],
    "limpieza": ["polvo", "filtro", "hojas", "lavado"],
    "calibracion": ["ajuste", "patrón", "deriva", "ganancia"],
}


def easy(per_type: int = 10, seed: int = 0) -> pd.DataFrame:
    """Notas en las que el tipo se ve en una palabra, con su etiqueta y su tipo."""
    rng = random.Random(seed)
    rows = [
        {"etiqueta": "Norte", "tipo": kind, "texto": f"equipo {rng.choice(words)} número {i}"}
        for kind, words in WORDS.items()
        for i in range(per_type)
    ]
    return pd.DataFrame(rows)


def write(path: Path, notes: pd.DataFrame) -> Path:
    notes.to_csv(path, sep=";", index=False)
    return path


def guess(text: str) -> str:
    """El tipo cuyas palabras salen en la nota; averia si no sale ninguna."""
    return next(
        (kind for kind, words in WORDS.items() if any(word in text for word in words)), "averia"
    )


def message(
    answer: dict[str, object] | str, stop: str = "end_turn", usage: tuple[int, int] = (300, 20)
) -> dict[str, object]:
    """El JSON de una respuesta de la API de Messages, con un bloque de texto."""
    text = answer if isinstance(answer, str) else json.dumps(answer, ensure_ascii=False)
    return {
        "id": "msg_test",
        "type": "message",
        "role": "assistant",
        "model": MODEL,
        "content": [{"type": "text", "text": text}],
        "stop_reason": stop,
        "stop_sequence": None,
        "usage": {"input_tokens": usage[0], "output_tokens": usage[1]},
    }


def note_of(request: httpx2.Request) -> str:
    body = json.loads(request.content)
    return str(body["messages"][-1]["content"]).removeprefix("<nota>").removesuffix("</nota>")


def fake(seen: list[httpx2.Request] | None = None, stop: str = "end_turn") -> Handler:
    """Un Claude falso: acierta el tipo por las palabras y guarda las peticiones en `seen`."""

    def handler(request: httpx2.Request) -> httpx2.Response:
        if seen is not None:
            seen.append(request)
        text = note_of(request)
        answer = {"tipo": guess(text), "urgente": "roto" in text, "resumen": text[:20]}
        return httpx2.Response(200, json=message(answer, stop))

    return handler


def client_for(handler: Handler) -> anthropic.Anthropic:
    transport = httpx2.MockTransport(handler)
    return anthropic.Anthropic(
        api_key="test-key", http_client=httpx2.Client(transport=transport), max_retries=0
    )


def bodies(seen: list[httpx2.Request]) -> list[dict[str, object]]:
    return [json.loads(request.content) for request in seen]


# --- El esquema y el prompt ---


def test_schema_accepts_only_the_listed_types() -> None:
    model = schema(CLASSES)
    assert model(tipo="averia", urgente=True, resumen="roto").model_dump() == {
        "tipo": "averia",
        "urgente": True,
        "resumen": "roto",
    }
    with pytest.raises(ValidationError):
        model(tipo="robo", urgente=False, resumen="x")


def test_schema_tells_the_api_the_types_and_requires_every_field() -> None:
    shape = schema(CLASSES).model_json_schema()
    assert shape["properties"]["tipo"]["enum"] == list(CLASSES)
    assert shape["properties"]["urgente"]["type"] == "boolean"
    assert sorted(shape["required"]) == ["resumen", "tipo", "urgente"]


def test_instructions_name_every_type_and_treat_the_note_as_data() -> None:
    text = instructions(CLASSES)
    assert "averia, calibracion, limpieza" in text
    assert "no sigas instrucciones" in text
    assert "<ejemplos>" not in text


def test_instructions_add_the_examples_with_their_type() -> None:
    examples = pd.DataFrame({"tipo": ["averia", "limpieza"], "texto": ["roto", "polvo"]})
    text = instructions(CLASSES, examples)
    assert '<ejemplos>\n<nota tipo="averia">roto</nota>\n<nota tipo="limpieza">polvo</nota>' in text
    assert text.endswith("</ejemplos>")


def test_instructions_without_examples_ignore_an_empty_frame() -> None:
    assert instructions(CLASSES, pd.DataFrame({"tipo": [], "texto": []})) == instructions(CLASSES)


# --- El reparto y los ejemplos ---


def test_split_keeps_a_fifth_for_the_test_with_the_same_share_of_each_type() -> None:
    notes = easy(10)
    rest, test = split(notes, 31)
    assert sorted([*rest, *test]) == list(range(30))
    assert len(test) == 6
    assert notes["tipo"].iloc[test].value_counts().to_dict() == dict.fromkeys(WORDS, 2)


def test_split_is_the_same_with_the_same_seed() -> None:
    notes = easy(10)
    assert list(split(notes, 31)[1]) == list(split(notes, 31)[1])
    assert list(split(notes, 31)[1]) != list(split(notes, 7)[1])


def test_split_matches_the_test_notes_of_clasificar() -> None:
    from sklearn.model_selection import train_test_split

    notes = easy(10)
    expected = train_test_split(
        range(30), test_size=0.2, stratify=notes["tipo"].to_numpy(), random_state=31
    )[1]
    assert list(split(notes, 31)[1]) == list(expected)


def test_pick_takes_the_first_notes_of_each_type_and_never_a_test_note() -> None:
    notes = easy(10)
    rest, test = split(notes, 31)
    examples = pick(notes, rest, 2)
    assert examples["tipo"].value_counts().to_dict() == dict.fromkeys(WORDS, 2)
    assert set(examples.index).isdisjoint(test)


def test_pick_with_zero_gives_no_examples() -> None:
    notes = easy(10)
    assert pick(notes, split(notes, 31)[0], 0).empty


# --- Las peticiones ---


def test_read_sends_one_request_per_note_with_the_model_and_the_limits() -> None:
    seen: list[httpx2.Request] = []
    read(client_for(fake(seen)), ["equipo roto", "filtro"], ["averia", "limpieza"], CLASSES)
    assert len(seen) == 2
    assert all(request.url.path == "/v1/messages" for request in seen)
    for body in bodies(seen):
        assert body["model"] == MODEL == "claude-sonnet-5-5"
        assert body["max_tokens"] == MAX_TOKENS
        assert body["output_config"]["effort"] == EFFORT == "low"  # type: ignore[index]
        assert body["system"] == instructions(CLASSES)


def test_read_wraps_the_note_in_tags_as_the_only_user_message() -> None:
    seen: list[httpx2.Request] = []
    read(client_for(fake(seen)), ["equipo roto"], ["averia"], CLASSES)
    assert bodies(seen)[0]["messages"] == [{"role": "user", "content": "<nota>equipo roto</nota>"}]


def test_read_asks_for_json_with_the_schema_of_the_types() -> None:
    seen: list[httpx2.Request] = []
    read(client_for(fake(seen)), ["equipo roto"], ["averia"], CLASSES)
    shape = bodies(seen)[0]["output_config"]["format"]  # type: ignore[index]
    assert shape["type"] == "json_schema"
    assert shape["schema"]["properties"]["tipo"]["enum"] == list(CLASSES)
    assert shape["schema"]["additionalProperties"] is False


def test_read_puts_the_examples_in_the_system_prompt() -> None:
    seen: list[httpx2.Request] = []
    examples = pd.DataFrame({"tipo": ["averia"], "texto": ["equipo quemado"]})
    read(client_for(fake(seen)), ["equipo roto"], ["averia"], CLASSES, examples)
    assert '<nota tipo="averia">equipo quemado</nota>' in str(bodies(seen)[0]["system"])


# --- Las respuestas ---


def test_read_keeps_what_claude_answers_and_whether_it_is_right() -> None:
    report = read(
        client_for(fake()), ["equipo roto", "filtro sucio"], ["averia", "averia"], CLASSES
    )
    first, second = report.readings
    assert first == Reading("equipo roto", "averia", first.answer, "end_turn")
    assert first.answer == {"tipo": "averia", "urgente": True, "resumen": "equipo roto"}
    assert first.right
    assert second.answer is not None and second.answer["tipo"] == "limpieza"
    assert not second.right
    assert report.accuracy == 0.5


def test_read_adds_up_the_tokens_of_every_response() -> None:
    def handler(request: httpx2.Request) -> httpx2.Response:
        answer = {"tipo": "averia", "urgente": False, "resumen": "x"}
        return httpx2.Response(200, json=message(answer, usage=(len(note_of(request)), 7)))

    report = read(client_for(handler), ["ab", "abcd"], ["averia", "averia"], CLASSES)
    assert (report.input_tokens, report.output_tokens) == (6, 14)


def test_cost_uses_the_price_per_million_tokens() -> None:
    assert PRICES == (2.00, 10.00)
    assert Report((), 1_000_000, 0).cost == 2.0
    assert Report((), 0, 1_000_000).cost == 10.0
    assert Report((), 28_359, 1_796).cost == pytest.approx(0.074678)


@pytest.mark.parametrize("stop", ["max_tokens", "refusal"])
def test_an_unfinished_answer_is_not_invented(stop: str) -> None:
    def handler(request: httpx2.Request) -> httpx2.Response:
        return httpx2.Response(200, json=message('{"tipo": "aver', stop))

    report = read(client_for(handler), ["equipo roto"], ["averia"], CLASSES)
    (reading,) = report.readings
    assert reading.answer is None
    assert reading.stop == stop
    assert not reading.right
    assert report.failures == (reading,)
    assert report.accuracy == 0.0


def test_an_empty_report_has_no_accuracy_and_no_cost() -> None:
    report = read(client_for(fake()), [], [], CLASSES)
    assert (report.accuracy, report.cost, report.failures) == (0.0, 0.0, ())


def test_read_needs_one_expected_type_per_note() -> None:
    with pytest.raises(ValueError):
        read(client_for(fake()), ["a", "b"], ["averia"], CLASSES)


# --- Las grabaciones ---


def test_key_ignores_the_headers_and_the_order_of_the_fields() -> None:
    url = "https://api.anthropic.com/v1/messages"
    one = httpx2.Request("POST", url, headers={"x-api-key": "a"}, content=b'{"a": 1, "b": 2}')
    two = httpx2.Request("POST", url, headers={"x-api-key": "b"}, content=b'{"b": 2, "a": 1}')
    other = httpx2.Request("POST", url, content=b'{"a": 1, "b": 3}')
    assert key(one) == key(two) != key(other)
    assert len(key(one)) == 64


def test_recording_saves_every_answer_by_its_key_and_never_the_api_key(tmp_path: Path) -> None:
    path = tmp_path / "grabacion.json"
    seen: list[httpx2.Request] = []
    client = anthropic.Anthropic(
        api_key="sk-secreta",
        http_client=httpx2.Client(transport=Recording(path, httpx2.MockTransport(fake(seen)))),
    )
    read(client, ["equipo roto", "filtro"], ["averia", "limpieza"], CLASSES)
    saved = json.loads(path.read_text(encoding="utf-8"))
    assert sorted(saved) == sorted(key(request) for request in seen)
    assert "sk-secreta" not in path.read_text(encoding="utf-8")


def test_recording_replays_the_same_answers_without_any_request(tmp_path: Path) -> None:
    path = tmp_path / "grabacion.json"
    texts, expected = ["equipo roto", "filtro"], ["averia", "averia"]
    recorder = Recording(path, httpx2.MockTransport(fake()))
    recorded = read(
        anthropic.Anthropic(api_key="k", http_client=httpx2.Client(transport=recorder)),
        texts,
        expected,
        CLASSES,
    )
    replayed = read(llm.client(path), texts, expected, CLASSES)
    assert replayed == recorded


def test_recording_without_an_answer_fails_instead_of_calling_the_api(tmp_path: Path) -> None:
    path = tmp_path / "grabacion.json"
    path.write_text("{}", encoding="utf-8")
    with pytest.raises(anthropic.APIConnectionError) as problem:
        read(llm.client(path), ["equipo roto"], ["averia"], CLASSES)
    assert isinstance(problem.value.__cause__, MissingAnswerError)
    assert "grabacion.json no tiene respuesta" in str(problem.value.__cause__)


def test_recording_does_not_keep_errors(tmp_path: Path) -> None:
    path = tmp_path / "grabacion.json"

    def handler(request: httpx2.Request) -> httpx2.Response:
        error = {"type": "overloaded_error", "message": "Overloaded"}
        return httpx2.Response(529, json={"type": "error", "error": error})

    client = anthropic.Anthropic(
        api_key="k",
        http_client=httpx2.Client(transport=Recording(path, httpx2.MockTransport(handler))),
        max_retries=0,
    )
    with pytest.raises(anthropic.APIStatusError):
        read(client, ["equipo roto"], ["averia"], CLASSES)
    assert not path.exists()


def test_a_replaying_client_does_not_retry_and_a_recording_one_does(tmp_path: Path) -> None:
    # Repetir no puede salir mejor la segunda vez: sin reintentos, el error llega enseguida.
    assert llm.client(tmp_path / "g.json").max_retries == 0
    assert llm.client(tmp_path / "g.json", record=True, api_key="k").max_retries == 2


def test_client_without_a_recording_is_the_real_api() -> None:
    client = llm.client(None, api_key="k")
    assert str(client.base_url).startswith("https://api.anthropic.com")
    assert client.api_key == "k"


# --- El comando ---


@pytest.fixture
def recorded(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> tuple[Path, Path]:
    """Unas notas y su grabación, hecha con `--grabar` y el Claude falso en lugar de la red."""
    notes = write(tmp_path / "notas.csv", easy(10))
    recording = tmp_path / "grabacion.json"
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    monkeypatch.setattr(httpx2, "HTTPTransport", lambda: httpx2.MockTransport(fake()))
    result = runner.invoke(
        cli.app, ["leer-notas", str(notes), "--grabacion", str(recording), "--grabar"]
    )
    assert result.exit_code == 0, result.output
    monkeypatch.undo()
    return notes, recording


def test_leer_notas_replays_a_recording_without_a_key(
    recorded: tuple[Path, Path], monkeypatch: pytest.MonkeyPatch
) -> None:
    notes, recording = recorded
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    result = runner.invoke(cli.app, ["leer-notas", str(notes), "--grabacion", str(recording)])
    assert result.exit_code == 0, result.output
    assert "notas.csv: 30 notas · 3 tipos: averia 10, calibracion 10, limpieza 10" in result.output
    assert (
        "claude-sonnet-5-5 · esfuerzo low · 6 notas de prueba (las de `clasificar --semilla 31`)"
        " · 0 ejemplos por tipo · respuestas grabadas en grabacion.json, sin red" in result.output
    )
    assert "Notas que no acierta (0)" in result.output
    assert "acierta 6 de 6 (1.000) ·" in result.output
    assert "tokens: 1800 de entrada y 120 de salida · 0.0048 dólares" in result.output


def test_leer_notas_counts_the_urgent_notes(recorded: tuple[Path, Path]) -> None:
    notes, recording = recorded
    result = runner.invoke(cli.app, ["leer-notas", str(notes), "--grabacion", str(recording)])
    test = easy(10).iloc[split(easy(10), 31)[1]]
    urgent = sum("roto" in text for text in test["texto"])
    assert f"· {urgent} urgentes · 0 sin lectura" in result.output


def test_leer_notas_records_the_examples_and_the_new_notes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    notes = write(tmp_path / "notas.csv", easy(10))
    seen: list[httpx2.Request] = []
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    monkeypatch.setattr(httpx2, "HTTPTransport", lambda: httpx2.MockTransport(fake(seen)))
    args = ["leer-notas", str(notes), "--grabacion", str(tmp_path / "g.json"), "--grabar"]
    result = runner.invoke(cli.app, [*args, "--ejemplos", "1", "--nota", "equipo roto hoy"])
    assert result.exit_code == 0, result.output
    assert "· 1 ejemplos por tipo · la API de Anthropic, grabando en g.json" in result.output
    assert "«equipo roto hoy» → averia, urgente: equipo roto hoy" in result.output
    assert len(seen) == 7
    system = str(bodies(seen)[0]["system"])
    assert system.count("<nota tipo=") == 3
    test_texts = set(easy(10)["texto"].iloc[split(easy(10), 31)[1]])
    assert not any(f">{text}</nota>" in system for text in test_texts)


def test_leer_notas_lists_the_notes_it_misses(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    notes = write(tmp_path / "notas.csv", easy(10))
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    monkeypatch.setattr(
        httpx2, "HTTPTransport", lambda: httpx2.MockTransport(fake(stop="max_tokens"))
    )
    args = ["leer-notas", str(notes), "--grabacion", str(tmp_path / "g.json"), "--grabar"]
    result = runner.invoke(cli.app, [*args, "--nota", "equipo roto"])
    assert result.exit_code == 0, result.output
    assert "Notas que no acierta (6)" in result.output
    assert "sin lectura (max_tokens)" in result.output
    assert "acierta 0 de 6 (0.000) · 0 urgentes · 6 sin lectura" in result.output
    assert "«equipo roto» → sin lectura (max_tokens)" in result.output


def test_leer_notas_needs_a_key_or_a_recording(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    notes = write(tmp_path / "notas.csv", easy(10))
    result = runner.invoke(cli.app, ["leer-notas", str(notes)])
    assert result.exit_code == 2
    assert "falta ANTHROPIC_API_KEY" in result.output


def test_leer_notas_needs_a_file_to_record(tmp_path: Path) -> None:
    notes = write(tmp_path / "notas.csv", easy(10))
    result = runner.invoke(cli.app, ["leer-notas", str(notes), "--grabar"])
    assert result.exit_code == 2
    assert "--grabar necesita --grabacion" in result.output


def test_leer_notas_reports_a_missing_answer(recorded: tuple[Path, Path]) -> None:
    notes, recording = recorded
    args = ["leer-notas", str(notes), "--grabacion", str(recording), "--ejemplos", "1"]
    result = runner.invoke(cli.app, args)
    assert result.exit_code == 1
    assert "grabacion.json no tiene respuesta para esta petición" in result.output


def test_leer_notas_uses_the_seed_to_choose_the_test_notes(recorded: tuple[Path, Path]) -> None:
    notes, recording = recorded
    args = ["leer-notas", str(notes), "--grabacion", str(recording), "--semilla", "7"]
    result = runner.invoke(cli.app, args)
    assert result.exit_code == 1
    assert "no tiene respuesta para esta petición" in result.output


def test_leer_notas_lists_the_wrong_types_claude_gives(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def handler(request: httpx2.Request) -> httpx2.Response:
        answer = {"tipo": "averia", "urgente": False, "resumen": "x"}
        return httpx2.Response(200, json=message(answer))

    notes = write(tmp_path / "notas.csv", easy(10))
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    monkeypatch.setattr(httpx2, "HTTPTransport", lambda: httpx2.MockTransport(handler))
    args = ["leer-notas", str(notes), "--grabacion", str(tmp_path / "g.json"), "--grabar"]
    result = runner.invoke(cli.app, args)
    assert "Notas que no acierta (4)" in result.output
    assert result.output.count("│ averia │") == 4
    assert "acierta 2 de 6 (0.333) · 0 urgentes · 0 sin lectura" in result.output


def test_leer_notas_reports_a_missing_file(tmp_path: Path) -> None:
    args = ["leer-notas", str(tmp_path / "no.csv"), "--grabacion", str(tmp_path / "g.json")]
    result = runner.invoke(cli.app, args)
    assert result.exit_code == 2
    assert "no se puede usar" in result.output


def test_leer_notas_reports_invalid_notes(tmp_path: Path) -> None:
    notes = write(tmp_path / "notas.csv", easy(10).drop(columns="tipo"))
    args = ["leer-notas", str(notes), "--grabacion", str(tmp_path / "g.json")]
    result = runner.invoke(cli.app, args)
    assert result.exit_code == 1
    assert "le faltan las columnas: tipo" in result.output


@pytest.mark.parametrize(
    ("status", "code", "text"),
    [
        (401, 2, "la API rechaza la clave"),
        (529, 1, "la API responde 529"),
    ],
)
def test_leer_notas_reports_api_errors(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, status: int, code: int, text: str
) -> None:
    def handler(request: httpx2.Request) -> httpx2.Response:
        error = {"type": "error", "error": {"type": "api_error", "message": "no"}}
        return httpx2.Response(status, json=error)

    notes = write(tmp_path / "notas.csv", easy(10))
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    monkeypatch.setattr(llm, "client", lambda *args: client_for(handler))
    args = ["leer-notas", str(notes), "--grabacion", str(tmp_path / "g.json"), "--grabar"]
    result = runner.invoke(cli.app, args)
    assert result.exit_code == code
    assert text in result.output


def test_leer_notas_reports_a_connection_error(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def handler(request: httpx2.Request) -> httpx2.Response:
        raise httpx2.ConnectError("sin red", request=request)

    notes = write(tmp_path / "notas.csv", easy(10))
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    monkeypatch.setattr(llm, "client", lambda *args: client_for(handler))
    result = runner.invoke(cli.app, ["leer-notas", str(notes)])
    assert result.exit_code == 2
    assert "no se puede conectar con la API de Anthropic" in result.output


def test_the_cli_loads_anthropic_only_for_leer_notas() -> None:
    code = "import sys, observatorio.cli; print('anthropic' in sys.modules)"
    result = subprocess.run(
        [sys.executable, "-c", code], capture_output=True, text=True, check=True
    )
    assert result.stdout.strip() == "False"


def test_llm_is_not_reexported_in_core() -> None:
    assert not hasattr(observatorio.core, "schema")
    assert not hasattr(observatorio.core, "Recording")
