"""Tests de la semana 34: una red neuronal pequeña en PyTorch, entrenada a mano.

Qué: comprueban core/neural.py (el resultado del entrenamiento, los tensores, la red, el
bucle de entrenamiento y learn, que reparte, prepara, entrena y mide) y el comando `red`.
Para qué: un bucle de entrenamiento tiene cuatro pasos y olvidar uno no da ningún error:
sin poner los gradientes a cero, sin escalar el valor o sin semilla, la red entrena igual,
pero peor o distinta cada vez. Solo un test que compara con un bucle conocido lo detecta.
Impacto: neural.py no se reexporta en core: la CLI arranca sin cargar PyTorch.
"""

import hashlib
import re
import subprocess
import sys
from dataclasses import FrozenInstanceError
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import torch
from test_ensembles import bump
from test_validation import frame_of, noise, signal, write
from torch import nn
from typer.testing import CliRunner

import observatorio.core
from observatorio import cli
from observatorio.core import neural
from observatorio.core.learning import SEED, split
from observatorio.core.neural import EPOCHS, HIDDEN, RATE, Training, learn, mlp, tensor, train

runner = CliRunner()


def line(size: int = 50) -> tuple[torch.Tensor, torch.Tensor]:
    """y = 2x + 1 con x entre -1 y 1: una sola neurona lineal puede aprenderla entera."""
    x = torch.linspace(-1, 1, size).reshape(-1, 1)
    return x, 2 * x + 1


def by_hand(model: nn.Module, x: torch.Tensor, y: torch.Tensor, epochs: int) -> list[float]:
    """El bucle de la teoría 03, paso a paso, para comparar con train."""
    optimizer = torch.optim.Adam(model.parameters(), lr=RATE)
    losses = []
    for _ in range(epochs):
        optimizer.zero_grad()
        loss = ((model(x) - y) ** 2).mean()
        loss.backward()
        optimizer.step()
        losses.append(loss.item())
    return losses


def linears(model: nn.Module) -> list[nn.Linear]:
    """Las capas lineales de la red, en orden."""
    return [layer for layer in model.modules() if isinstance(layer, nn.Linear)]


def many_labels(size: int = 400) -> pd.DataFrame:
    """Cuarenta etiquetas: con el one-hot, casi todo ceros."""
    rng = np.random.default_rng(4)
    rows = [(f"E{position % 40:02d}", float(rng.uniform(0, 80))) for position in range(size)]
    return frame_of(rows)


# --- Training ---


def test_learned_when_the_last_loss_is_lower() -> None:
    assert Training(1, (1.0, 0.5, 0.2), 1.0, 2.0).learned


@pytest.mark.parametrize("losses", [(1.0, 1.0), (1.0, 0.5, 1.5)])
def test_not_learned_when_the_last_loss_is_not_lower(losses: tuple[float, ...]) -> None:
    assert not Training(1, losses, 1.0, 2.0).learned


def test_improves_when_the_network_errs_less_than_the_baseline() -> None:
    assert Training(1, (1.0,), 1.0, 2.0).improves
    assert not Training(1, (1.0,), 3.0, 2.0).improves


def test_a_tie_does_not_improve() -> None:
    assert not Training(1, (1.0,), 2.0, 2.0).improves


def test_training_is_frozen() -> None:
    training = Training(1, (1.0,), 1.0, 2.0)
    with pytest.raises(FrozenInstanceError):
        training.mae = 0.0  # type: ignore[misc]


# --- tensor y mlp ---


def test_tensor_is_float32() -> None:
    result = tensor(pd.DataFrame({"a": [1, 2], "b": [3, 4]}))
    assert result.dtype == torch.float32
    assert result.tolist() == [[1.0, 3.0], [2.0, 4.0]]


def test_tensor_of_a_column_has_one_dimension() -> None:
    assert tensor(pd.Series([1.5, 2.5])).shape == (2,)


def test_mlp_is_a_line_a_relu_and_a_line() -> None:
    layers = list(mlp(4))
    assert [type(layer) for layer in layers] == [nn.Linear, nn.ReLU, nn.Linear]


def test_mlp_goes_from_the_inputs_to_one_value() -> None:
    sizes = [(layer.in_features, layer.out_features) for layer in linears(mlp(4, 8))]
    assert sizes == [(4, 8), (8, 1)]


def test_mlp_hidden_layer_by_default() -> None:
    assert linears(mlp(4))[0].out_features == HIDDEN == 16


def test_mlp_predicts_one_value_per_row() -> None:
    assert mlp(4)(torch.zeros(7, 4)).shape == (7, 1)


def test_defaults() -> None:
    assert (EPOCHS, RATE) == (300, 0.01)


# --- train ---


def test_train_returns_one_loss_per_epoch() -> None:
    x, y = line()
    assert len(train(nn.Linear(1, 1), x, y, 25, RATE)) == 25


def test_train_starts_with_the_mean_squared_error_of_the_untrained_model() -> None:
    torch.manual_seed(0)
    model, (x, y) = nn.Linear(1, 1), line()
    with torch.no_grad():
        expected = float(((model(x) - y) ** 2).mean())
    assert train(model, x, y, 1, RATE)[0] == pytest.approx(expected)


def test_train_is_the_loop_by_hand() -> None:
    x, y = line()
    torch.manual_seed(0)
    model = nn.Linear(1, 1)
    torch.manual_seed(0)
    expected = by_hand(nn.Linear(1, 1), x, y, 100)
    assert train(model, x, y, 100, RATE) == pytest.approx(expected)


def test_train_learns_a_line() -> None:
    torch.manual_seed(0)
    model, (x, y) = nn.Linear(1, 1), line()
    losses = train(model, x, y, 2000, 0.05)
    assert losses[-1] < 1e-4
    assert model.weight.item() == pytest.approx(2.0, abs=0.01)
    assert model.bias.item() == pytest.approx(1.0, abs=0.01)


def test_train_uses_the_rate() -> None:
    x, y = line()
    torch.manual_seed(0)
    slow = train(nn.Linear(1, 1), x, y, 50, 0.001)
    torch.manual_seed(0)
    fast = train(nn.Linear(1, 1), x, y, 50, 0.05)
    assert slow[0] == fast[0]
    assert fast[-1] < slow[-1]


def test_train_changes_the_weights_of_the_model() -> None:
    torch.manual_seed(0)
    model, (x, y) = mlp(1, 4), line()
    before = [parameter.clone() for parameter in model.parameters()]
    train(model, x, y, 5, RATE)
    after = list(model.parameters())
    assert all(not torch.equal(old, new) for old, new in zip(before, after, strict=True))


# --- learn ---


def test_learn_counts_the_parameters() -> None:
    # Tres etiquetas y la posición son 4 entradas: (4 + 1) x 16 + (16 + 1).
    assert learn(signal(), epochs=1).parameters == 97


def test_learn_uses_the_hidden_neurons() -> None:
    assert learn(signal(), hidden=4, epochs=1).parameters == (4 + 1) * 4 + (4 + 1)


def test_learn_one_loss_per_epoch() -> None:
    assert len(learn(signal(), epochs=50).losses) == 50


def test_learn_scales_the_value() -> None:
    # Escalado, el valor tiene media 0 y desviación 1: la primera pérdida ronda 1.
    assert learn(signal(), epochs=1).losses[0] < 3


def test_learn_when_the_label_decides_the_value() -> None:
    training = learn(signal())
    assert training.learned
    assert training.improves
    assert training.mae < 3


def test_learn_draws_what_a_line_cannot() -> None:
    training = learn(bump())
    assert training.mae < training.baseline / 2


def test_learn_memorizes_noise_but_does_not_generalize() -> None:
    training = learn(noise())
    assert training.losses[-1] < 0.9 * training.losses[0]
    assert training.mae == pytest.approx(training.baseline, abs=1)


@pytest.mark.parametrize("seed", [SEED, 7])
def test_learn_baseline_is_the_mean_of_the_training_values(seed: int) -> None:
    train_rows, test_rows = split(signal(), seed=seed)
    expected = (test_rows["valor"] - train_rows["valor"].mean()).abs().mean()
    assert learn(signal(), epochs=1, seed=seed).baseline == pytest.approx(expected, rel=1e-5)


def test_learn_uses_the_seed_for_the_split_and_the_weights() -> None:
    first = learn(noise(), epochs=20)
    assert first == learn(noise(), epochs=20)
    assert first != learn(noise(), epochs=20, seed=7)


def test_learn_seed_fixes_the_initial_weights() -> None:
    torch.manual_seed(123)
    first = learn(signal(), epochs=5)
    torch.manual_seed(456)
    assert learn(signal(), epochs=5) == first


def test_learn_with_many_labels() -> None:
    training = learn(many_labels(), epochs=5)
    assert training.parameters == (41 + 1) * 16 + (16 + 1)


def test_learn_drops_the_measures_without_value() -> None:
    frame = signal()
    frame.loc[[0, 1, 2], "valor"] = None
    assert np.isfinite(learn(frame, epochs=5).mae)


def test_learn_names_the_missing_columns() -> None:
    with pytest.raises(ValueError, match="faltan las columnas nivel"):
        learn(signal().drop(columns=["nivel"]))


# --- el comando red ---


def test_red_prints_the_data_the_network_and_the_verdict(tmp_path: Path) -> None:
    path = write(tmp_path, signal())
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    result = runner.invoke(cli.app, ["red", str(path)])
    assert result.exit_code == 0, result.output
    expected = learn(signal())
    assert f"instantanea.csv: 120 medidas · sha256: {digest}" in result.output
    assert "red de 16 neuronas ocultas y 97 parámetros · 300 épocas · ritmo 0.01" in result.output
    assert "Pérdida en entrenamiento (MSE del valor escalado)" in result.output
    assert (
        f"regresión del valor · MAE en prueba: red {expected.mae:.3f}"
        f" · referencia {expected.baseline:.3f}: la red mejora la referencia"
    ) in result.output


def test_red_shows_six_epochs_and_their_losses(tmp_path: Path) -> None:
    result = runner.invoke(cli.app, ["red", str(write(tmp_path, signal()))])
    losses = learn(signal()).losses
    shown = re.findall(r"│ +(\d+) │ +([\d.]+) │", result.output)
    assert shown == [
        (str(epoch), f"{losses[epoch - 1]:.4f}") for epoch in (1, 61, 121, 181, 241, 300)
    ]


def test_red_shows_every_epoch_when_there_are_few(tmp_path: Path) -> None:
    result = runner.invoke(cli.app, ["red", str(write(tmp_path, signal())), "--epocas", "3"])
    assert [epoch for epoch, _ in re.findall(r"│ +(\d+) │ +([\d.]+) │", result.output)] == [
        "1",
        "2",
        "3",
    ]


def test_red_says_when_it_does_not_improve(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    def fake(frame: pd.DataFrame, hidden: int, epochs: int, rate: float, seed: int) -> Training:
        return Training(5, (1.0, 0.5), 3.0, 2.0)

    monkeypatch.setattr(neural, "learn", fake)
    result = runner.invoke(cli.app, ["red", str(write(tmp_path, signal()))])
    assert "red 3.000 · referencia 2.000: la red no mejora la referencia" in result.output
    assert "la pérdida no bajó" not in result.output


def test_red_says_when_the_loss_did_not_go_down(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def fake(frame: pd.DataFrame, hidden: int, epochs: int, rate: float, seed: int) -> Training:
        return Training(5, (1.0, 1.5), 3.0, 2.0)

    monkeypatch.setattr(neural, "learn", fake)
    result = runner.invoke(cli.app, ["red", str(write(tmp_path, signal()))])
    assert "la pérdida no bajó: prueba otro --ritmo o más --epocas" in result.output


def test_red_passes_its_options_to_learn(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[tuple[int, int, float, int]] = []

    def spy(frame: pd.DataFrame, hidden: int, epochs: int, rate: float, seed: int) -> Training:
        calls.append((hidden, epochs, rate, seed))
        return Training(5, (1.0, 0.5), 1.0, 2.0)

    monkeypatch.setattr(neural, "learn", spy)
    path = str(write(tmp_path, signal()))
    options = ["--oculta", "8", "--epocas", "40", "--ritmo", "0.05", "--semilla", "7"]
    runner.invoke(cli.app, ["red", path, *options])
    assert calls == [(8, 40, 0.05, 7)]


def test_red_checks_the_digest(tmp_path: Path) -> None:
    result = runner.invoke(cli.app, ["red", str(write(tmp_path, signal())), "--huella", "0000"])
    assert result.exit_code == 1
    assert "no 0000" in result.output


def test_red_without_the_level_column(tmp_path: Path) -> None:
    path = write(tmp_path, signal().drop(columns=["nivel"]))
    result = runner.invoke(cli.app, ["red", str(path)])
    assert result.exit_code == 1
    assert "faltan las columnas nivel" in result.output


def test_red_without_the_file(tmp_path: Path) -> None:
    result = runner.invoke(cli.app, ["red", str(tmp_path / "no.csv")])
    assert result.exit_code == 2
    assert "no se puede leer" in result.output


@pytest.mark.parametrize(
    ("option", "value"), [("--oculta", "0"), ("--epocas", "0"), ("--ritmo", "0")]
)
def test_red_rejects_options_out_of_range(tmp_path: Path, option: str, value: str) -> None:
    result = runner.invoke(cli.app, ["red", str(write(tmp_path, signal())), option, value])
    assert result.exit_code == 2
    assert "not in the range" in result.output


def test_neural_is_not_reexported_in_core() -> None:
    assert "neural" not in observatorio.core.__all__
    assert not hasattr(observatorio.core, "learn")


def test_the_cli_loads_torch_only_for_red() -> None:
    code = "import sys, observatorio.cli; print('torch' in sys.modules)"
    result = subprocess.run(
        [sys.executable, "-c", code], check=False, capture_output=True, text=True
    )
    assert result.stdout == "False\n"
