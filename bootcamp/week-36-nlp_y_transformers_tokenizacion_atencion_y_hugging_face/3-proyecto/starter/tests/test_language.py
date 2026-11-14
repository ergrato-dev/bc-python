"""Tests de la semana 36: clasificar las notas de texto libre.

Qué: comprueban core/language.py (leer y validar las notas, el tokenizador BPE, el
Transformer, el reparto, TF-IDF, la referencia y las predicciones) y el comando `clasificar`.
Para qué: en NLP casi nada da error: un tokenizador entrenado con las notas de prueba, una
máscara que deja mirar el relleno o una referencia mal calculada solo cambian unos números.
Solo un test lo detecta.
Impacto: language.py no se reexporta en core: la CLI arranca sin cargar PyTorch ni tokenizers.
"""

import random
import subprocess
import sys
from dataclasses import FrozenInstanceError
from pathlib import Path

import pandas as pd
import pytest
import torch
from tokenizers import Tokenizer
from torch import nn
from typer.testing import CliRunner

import observatorio.core
from observatorio import cli
from observatorio.core import language
from observatorio.core.convolution import count, fit
from observatorio.core.language import (
    BAG,
    BASELINE,
    LENGTH,
    MINIMUM,
    PAD,
    TRANSFORMER,
    UNKNOWN,
    Classification,
    Encoder,
    classify,
    encode,
    pieces,
    predict,
    read_notes,
    tokenizer,
)

runner = CliRunner()
Trained = tuple[Classification, Encoder, Tokenizer]

# Por tipo, palabras que solo dicen ese tipo; todas las notas comparten el resto.
WORDS = {
    "averia": ["apagado", "roto", "quemado", "caído"],
    "limpieza": ["polvo", "filtro", "hojas", "lavado"],
    "calibracion": ["ajuste", "patrón", "deriva", "ganancia"],
}


def easy(per_type: int = 20, seed: int = 0) -> pd.DataFrame:
    """Notas en las que el tipo se ve en dos palabras: los dos modelos deberían acertarlo."""
    rng = random.Random(seed)
    rows = [
        ("Norte", kind, f"El equipo de Norte está {' y '.join(rng.sample(words, 2))} hoy")
        for _ in range(per_type)
        for kind, words in WORDS.items()
    ]
    return pd.DataFrame(rows, columns=["etiqueta", "tipo", "texto"])


def write(tmp_path: Path, notes: pd.DataFrame | str) -> Path:
    path = tmp_path / "notas.csv"
    if isinstance(notes, str):
        path.write_text(notes, encoding="utf-8")
    else:
        notes.to_csv(path, sep=";", index=False, lineterminator="\n")
    return path


def outcome(**accuracy: float) -> Classification:
    return Classification(
        ("averia", "calibracion", "limpieza"),
        (9, 3, 3),
        60,
        100,
        (0.9, 0.5, 0.7),
        1,
        accuracy or {BASELINE: 0.5},
    )


# --- read_notes ---


def test_read_notes_reads_the_three_columns(tmp_path: Path) -> None:
    notes = read_notes(write(tmp_path, easy(5)))
    assert list(notes.columns) == ["etiqueta", "tipo", "texto"]
    assert len(notes) == 15


def test_read_notes_strips_the_text_and_the_type(tmp_path: Path) -> None:
    rows = "".join(f"Sur; {kind} ;  nota {i}  \n" for i in range(5) for kind in "ab")
    notes = read_notes(write(tmp_path, "etiqueta;tipo;texto\n" + rows))
    assert notes["texto"].iloc[0] == "nota 0"
    assert set(notes["tipo"]) == {"a", "b"}


def test_read_notes_keeps_na_as_text(tmp_path: Path) -> None:
    rows = "".join(f"Sur;{kind};NA\n" for _ in range(5) for kind in "ab")
    notes = read_notes(write(tmp_path, "etiqueta;tipo;texto\n" + rows))
    assert (notes["texto"] == "NA").all()


def test_read_notes_keeps_the_accents(tmp_path: Path) -> None:
    notes = read_notes(write(tmp_path, easy(5)))
    assert "calibracion" in set(notes["tipo"])
    assert notes["texto"].str.contains("está").all()


def test_read_notes_says_which_columns_are_missing(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="le faltan las columnas: tipo, texto"):
        read_notes(write(tmp_path, "etiqueta;nota\nSur;hola\n"))


@pytest.mark.parametrize("row", ["Sur;b;   ", "Sur;;una nota"])
def test_read_notes_says_which_line_is_empty(tmp_path: Path, row: str) -> None:
    rows = "".join(f"Sur;{kind};nota\n" for _ in range(5) for kind in "ab")
    with pytest.raises(ValueError, match="la línea 12 no tiene texto o tipo"):
        read_notes(write(tmp_path, f"etiqueta;tipo;texto\n{rows}{row}\n"))


def test_read_notes_needs_two_types(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="al menos dos tipos"):
        read_notes(write(tmp_path, "etiqueta;tipo;texto\n" + "Sur;a;nota\n" * 10))


def test_read_notes_needs_enough_notes_of_each_type(tmp_path: Path) -> None:
    rows = "Sur;a;nota\n" * 10 + "Sur;b;nota\n" * (MINIMUM - 1)
    with pytest.raises(ValueError, match=f"el tipo b tiene {MINIMUM - 1} notas"):
        read_notes(write(tmp_path, "etiqueta;tipo;texto\n" + rows))


def test_read_notes_accepts_the_minimum(tmp_path: Path) -> None:
    rows = "Sur;a;nota\n" * MINIMUM + "Sur;b;nota\n" * MINIMUM
    assert len(read_notes(write(tmp_path, "etiqueta;tipo;texto\n" + rows))) == 2 * MINIMUM


def test_read_notes_without_the_file(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        read_notes(tmp_path / "no.csv")


# --- tokenizer, encode y pieces ---


TEXTS = ["el filtro sucio", "el filtro limpio", "filtro y sensor"] * 20


def test_tokenizer_ignores_case_and_accents() -> None:
    model = tokenizer(TEXTS + ["calibracion"] * 5, 100)
    assert pieces(model, "Calibración") == pieces(model, "calibracion")


def test_tokenizer_starts_with_padding_and_unknown() -> None:
    model = tokenizer(TEXTS, 100)
    assert model.token_to_id(PAD) == 0
    assert model.token_to_id(UNKNOWN) == 1


def test_tokenizer_stops_at_its_size() -> None:
    assert tokenizer(TEXTS * 3 + [" ".join(map(str, range(500)))], 60).get_vocab_size() == 60


def test_frequent_words_become_one_piece() -> None:
    assert pieces(tokenizer(TEXTS, 100), "filtro") == ["filtro"]


def test_rare_words_are_split_into_smaller_pieces() -> None:
    split = pieces(tokenizer(TEXTS, 100), "sensorfiltro")
    assert len(split) > 1
    assert "".join(split) == "sensorfiltro"


def test_pieces_never_cross_two_words_and_split_punctuation() -> None:
    model = tokenizer([*TEXTS, "el filtro, sucio."], 100)
    assert pieces(model, "filtro, sucio.") == ["filtro", ",", "sucio", "."]


def test_unseen_characters_are_unknown() -> None:
    assert pieces(tokenizer(TEXTS, 100), "ж") == [UNKNOWN]


def test_encode_pads_every_text_to_the_same_length() -> None:
    model = tokenizer(TEXTS, 100)
    ids = encode(model, ["filtro", "el filtro sucio"])
    assert ids.shape == (2, LENGTH)
    assert ids.dtype == torch.int64
    assert ids[0, 0] != 0
    assert (ids[0, 1:] == 0).all()
    assert (ids[1, 3:] == 0).all()


def test_encode_cuts_long_texts() -> None:
    ids = encode(tokenizer(TEXTS, 100), ["filtro " * (LENGTH + 10)])
    assert ids.shape == (1, LENGTH)
    assert (ids != 0).all()


# --- Encoder ---


def ids_of(*rows: list[int]) -> torch.Tensor:
    return torch.tensor([row + [0] * (LENGTH - len(row)) for row in rows])


def test_encoder_gives_a_score_per_type() -> None:
    assert Encoder(50, 3)(ids_of([2, 3], [4, 5, 6])).shape == (2, 3)


def test_encoder_parameters() -> None:
    # Embeddings 200 x 16 y 48 x 16, atención 3 x 16 x 16 + 3 x 16 y 16 x 16 + 16,
    # la red de cada pieza 16 x 32 + 32 y 32 x 16 + 16, dos normalizaciones de 2 x 16,
    # y la salida 16 x 3 + 3.
    assert count(Encoder(200, 3)) == 6243


def test_encoder_padding_is_a_vector_of_zeros() -> None:
    assert (Encoder(50, 3).tokens.weight[0] == 0).all()


def test_encoder_does_not_look_at_the_padding() -> None:
    torch.manual_seed(0)
    model = Encoder(50, 3).eval()
    ids = ids_of([2, 3, 4])
    with torch.no_grad():
        assert torch.allclose(model(ids), model(ids[:, :5]), atol=1e-6)


def test_encoder_cares_about_the_order() -> None:
    torch.manual_seed(0)
    model = Encoder(50, 3).eval()
    with torch.no_grad():
        assert not torch.allclose(model(ids_of([2, 3, 4])), model(ids_of([4, 3, 2])))


def test_fit_trains_a_classifier_with_cross_entropy() -> None:
    torch.manual_seed(0)
    ids, y = ids_of(*[[2, 3]] * 8, *[[4, 5]] * 8), torch.tensor([0] * 8 + [1] * 8)
    model = Encoder(10, 2)
    losses, best = fit(model, (ids, y), (ids, y), 30, 30, nn.CrossEntropyLoss())
    assert losses[best] < losses[0]
    model.eval()
    assert (model(ids).argmax(dim=1) == y).all()


# --- Classification ---


def test_the_winner_is_the_most_accurate() -> None:
    assert outcome(**{BASELINE: 0.3, BAG: 0.8, TRANSFORMER: 0.9}).winner == TRANSFORMER


def test_in_a_tie_the_first_wins() -> None:
    result = outcome(**{BASELINE: 0.3, BAG: 0.9, TRANSFORMER: 0.9})
    assert result.winner == BAG
    assert result.improves


def test_a_tie_with_the_baseline_does_not_improve() -> None:
    result = outcome(**{BASELINE: 0.5, BAG: 0.5, TRANSFORMER: 0.4})
    assert result.winner == BASELINE
    assert not result.improves


def test_classification_is_frozen() -> None:
    with pytest.raises(FrozenInstanceError):
        outcome().best = 2  # type: ignore[misc]


# --- classify ---


@pytest.fixture(scope="module")
def trained() -> Trained:
    return classify(easy(), size=60, epochs=60)


def test_classify_splits_by_type(trained: Trained) -> None:
    result, _, _ = trained
    assert result.sizes == (36, 12, 12)
    assert result.classes == ("averia", "calibracion", "limpieza")


def test_classify_measures_the_three_models(
    trained: Trained,
) -> None:
    result, _, _ = trained
    assert list(result.accuracy) == [BASELINE, BAG, TRANSFORMER]
    assert result.accuracy[BASELINE] == pytest.approx(1 / 3)
    assert result.accuracy[BAG] == 1.0
    assert result.accuracy[TRANSFORMER] == 1.0
    assert result.improves


def test_classify_reports_the_network(trained: Trained) -> None:
    result, model, vocabulary = trained
    assert result.vocabulary == 60 == vocabulary.get_vocab_size()
    assert result.parameters == count(model)
    assert result.losses[result.best] == min(result.losses)


def test_classify_returns_the_best_epoch_not_the_last() -> None:
    result, _, _ = classify(easy(), size=60, epochs=40, patience=40)
    assert len(result.losses) == 40
    assert result.losses[result.best] == min(result.losses)


def test_classify_stops_after_patience() -> None:
    result, _, _ = classify(easy(), size=60, epochs=100, patience=1)
    assert len(result.losses) <= result.best + 2


def test_classify_honors_the_epochs() -> None:
    result, _, _ = classify(easy(), size=60, epochs=2)
    assert len(result.losses) == 2


def test_classify_counts_hits_exactly() -> None:
    # Una época no basta para acertar todo: un acierto de 1/3, 5/12... sin redondeos.
    result, _, _ = classify(easy(), size=60, epochs=1)
    assert 0 < result.accuracy[TRANSFORMER] < 1
    assert result.accuracy[TRANSFORMER] in {hits / 12 for hits in range(13)}


def test_the_baseline_is_the_most_frequent_type_in_training() -> None:
    notes = pd.concat([easy(20), easy(20).query("tipo == 'averia'")], ignore_index=True)
    result, _, _ = classify(notes, size=60, epochs=1)
    # 40 de 80 notas son averia: la mitad de la prueba.
    assert result.accuracy[BASELINE] == 0.5


def test_classify_trains_the_tokenizer_only_with_the_training_notes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    seen: list[list[str]] = []
    real = language.tokenizer

    def spy(texts: list[str], size: int) -> Tokenizer:
        seen.append(texts)
        return real(texts, size)

    monkeypatch.setattr(language, "tokenizer", spy)
    notes = easy()
    notes["texto"] = [f"{text} {i}" for i, text in enumerate(notes["texto"])]
    result, _, _ = classify(notes, size=60, epochs=1)
    assert len(seen[0]) == result.sizes[0]
    assert set(seen[0]) < set(notes["texto"])


def test_classify_is_reproducible_with_the_seed() -> None:
    first, _, _ = classify(easy(), size=60, epochs=3, seed=4)
    again, _, _ = classify(easy(), size=60, epochs=3, seed=4)
    other, _, _ = classify(easy(), size=60, epochs=3, seed=5)
    assert first == again
    assert first.losses != other.losses


# --- predict ---


def test_predict_gives_the_type_and_its_probability(
    trained: Trained,
) -> None:
    result, model, vocabulary = trained
    texts = ["El equipo de Norte está roto y quemado", "El equipo de Norte está con polvo y hojas"]
    predictions = predict(model, vocabulary, result.classes, texts)
    assert [kind for kind, _ in predictions] == ["averia", "limpieza"]
    assert all(0.5 < chance <= 1 for _, chance in predictions)


def test_predict_without_texts(trained: Trained) -> None:
    result, model, vocabulary = trained
    assert predict(model, vocabulary, result.classes, []) == []


# --- el comando clasificar ---


def run(tmp_path: Path, notes: pd.DataFrame | str, *options: str) -> tuple[int, str]:
    result = runner.invoke(cli.app, ["clasificar", str(write(tmp_path, notes)), *options])
    return result.exit_code, result.output


def test_clasificar_prints_the_notes_the_split_the_network_and_the_verdict(
    tmp_path: Path,
) -> None:
    code, output = run(tmp_path, easy(), "--vocabulario", "60", "--epocas", "60")
    assert code == 0
    assert "notas.csv: 60 notas · 3 tipos: averia 20, calibracion 20, limpieza 20" in output
    assert "36 para entrenar, 12 para validar, 12 para prueba" in output
    assert "tokenizador BPE de 60 piezas" in output
    assert "«El equipo de Norte está " in output
    assert "→ el · equipo · de · norte · esta · " in output
    assert "1 capa, 2 cabezas de atención, vectores de 16 · " in output
    assert "Pérdida en validación (entropía cruzada)" in output
    assert "│ tf-idf      │   1.000 │" in output
    assert "gana tf-idf: acierta más que la referencia" in output


def test_clasificar_says_where_it_stopped(tmp_path: Path) -> None:
    _, output = run(tmp_path, easy(), "--vocabulario", "60", "--paciencia", "1")
    assert "paró en la época " in output


def test_clasificar_says_when_it_trained_every_epoch(tmp_path: Path) -> None:
    _, output = run(tmp_path, easy(), "--vocabulario", "60", "--epocas", "3")
    assert "entrenó 3 épocas" in output


def test_clasificar_shows_six_epochs_at_most(tmp_path: Path) -> None:
    options = ["--vocabulario", "60", "--epocas", "13", "--paciencia", "20"]
    _, output = run(tmp_path, easy(), *options)
    table = output.split("Pérdida en validación")[1].split("Acierto")[0]
    rows = [line.split("│")[1].strip() for line in table.splitlines() if line.startswith("│")]
    assert rows == ["1", "4", "7", "10", "13"]


def test_clasificar_says_when_no_model_improves(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def tie(*args: object) -> Trained:
        return outcome(**{BASELINE: 0.5, BAG: 0.5}), Encoder(10, 2), language.tokenizer(TEXTS, 60)

    monkeypatch.setattr(language, "classify", tie)
    _, output = run(tmp_path, easy(5))
    assert "ningún modelo acierta más que la referencia" in output


def test_clasificar_passes_its_options_to_classify(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    calls: list[tuple[object, ...]] = []

    def spy(*args: object) -> Trained:
        calls.append(args[1:])
        return outcome(), Encoder(10, 2), language.tokenizer(TEXTS, 60)

    monkeypatch.setattr(language, "classify", spy)
    options = ["--vocabulario", "80", "--epocas", "40", "--paciencia", "4", "--semilla", "7"]
    run(tmp_path, easy(5), *options)
    assert calls == [(80, 40, 4, 7)]


def test_clasificar_classifies_new_notes(tmp_path: Path) -> None:
    options = ["--vocabulario", "60", "--epocas", "60"]
    notes = ["--nota", "El equipo de Norte está roto y caído", "--nota", "[b]filtro[/b] y polvo"]
    _, output = run(tmp_path, easy(), *options, *notes)
    assert "«El equipo de Norte está roto y caído» → averia (transformer, " in output
    assert "«[b]filtro[/b] y polvo» → limpieza (transformer, " in output


def test_clasificar_shows_brackets_as_text(tmp_path: Path) -> None:
    notes = easy()
    notes.loc[0, "texto"] = "[b]roto[/b] y apagado"
    _, output = run(tmp_path, notes, "--vocabulario", "60", "--epocas", "1")
    assert "«[b]roto[/b] y apagado» → [ · b · ] · " in output


def test_clasificar_with_wrong_columns(tmp_path: Path) -> None:
    code, output = run(tmp_path, "etiqueta;nota\nSur;hola\n")
    assert code == 1
    assert "le faltan las columnas" in output


def test_clasificar_without_the_file(tmp_path: Path) -> None:
    result = runner.invoke(cli.app, ["clasificar", str(tmp_path / "no.csv")])
    assert result.exit_code == 2
    assert "no se puede usar" in result.output


@pytest.mark.parametrize(
    ("option", "value"),
    [("--vocabulario", "49"), ("--vocabulario", "5001"), ("--epocas", "0"), ("--paciencia", "0")],
)
def test_clasificar_rejects_options_out_of_range(tmp_path: Path, option: str, value: str) -> None:
    code, output = run(tmp_path, easy(5), option, value)
    assert code == 2
    assert "not in the range" in output


def test_language_is_not_reexported_in_core() -> None:
    assert "language" not in observatorio.core.__all__
    assert not hasattr(observatorio.core, "read_notes")


def test_the_cli_loads_tokenizers_only_for_clasificar() -> None:
    code = "import sys, observatorio.cli; print('tokenizers' in sys.modules)"
    result = subprocess.run(
        [sys.executable, "-c", code], check=False, capture_output=True, text=True
    )
    assert result.stdout == "False\n"
