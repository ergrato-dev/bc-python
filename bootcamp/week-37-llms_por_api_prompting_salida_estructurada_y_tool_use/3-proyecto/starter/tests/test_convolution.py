"""Tests de la semana 35: una red convolucional que pronostica el siguiente valor.

Qué: comprueban core/convolution.py (las ventanas, la red, congelar, el entrenamiento con
mini-lotes y parada temprana, el pronóstico por tiempo, y guardar y cargar los pesos) y el
comando `pronosticar`.
Para qué: casi todo lo que puede salir mal al entrenar no da ningún error: barajar antes de
repartir (la red ve el futuro), quedarse con la última época en lugar de la mejor, olvidar
congelar, o cargar un archivo de pesos que ejecuta código. Solo un test lo detecta.
Impacto: convolution.py no se reexporta en core: la CLI arranca sin cargar PyTorch.
"""

import pickle
from dataclasses import FrozenInstanceError
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import torch
from test_validation import frame_of, noise, signal, write
from torch import nn
from torch.utils.data import DataLoader, TensorDataset
from typer.testing import CliRunner

import observatorio.core
from observatorio import cli
from observatorio.core import convolution
from observatorio.core.convolution import (
    BATCH,
    CHANNELS,
    EPOCHS,
    KERNEL,
    MINIMUM,
    PATIENCE,
    RATE,
    WINDOW,
    Forecast,
    cnn,
    count,
    fit,
    forecast,
    freeze,
    load,
    save,
    windows,
)
from observatorio.core.learning import SEED

runner = CliRunner()


def wave(size: int = 200, label: str = "Norte") -> pd.DataFrame:
    """Un valor que sube y baja cada 12 posiciones, con poco ruido: los anteriores dicen
    cuál viene después."""
    rng = np.random.default_rng(5)
    values = 40 + 30 * np.sin(2 * np.pi * np.arange(size) / 12) + rng.normal(0, 2, size)
    return frame_of([(label, float(round(value, 1))) for value in values])


def parts(size: int = 100) -> tuple[tuple[torch.Tensor, torch.Tensor], ...]:
    """Las ventanas de una onda escalada: 80 para entrenar y el resto para validar."""
    values = wave(size)["valor"].to_numpy()
    x, y = windows((values - values.mean()) / values.std(), WINDOW)
    return (x[:80], y[:80]), (x[80:], y[80:])


def by_hand(
    model: nn.Module,
    train: tuple[torch.Tensor, torch.Tensor],
    validation: tuple[torch.Tensor, torch.Tensor],
    epochs: int,
) -> list[float]:
    """El bucle de la teoría 03, por mini-lotes y midiendo la validación, sin parar."""
    optimizer = torch.optim.Adam(model.parameters(), lr=RATE)
    loader = DataLoader(TensorDataset(*train), batch_size=BATCH, shuffle=True)
    losses = []
    for _ in range(epochs):
        for x, y in loader:
            optimizer.zero_grad()
            ((model(x) - y) ** 2).mean().backward()
            optimizer.step()
        with torch.no_grad():
            losses.append(((model(validation[0]) - validation[1]) ** 2).mean().item())
    return losses


def validation_loss(model: nn.Module, validation: tuple[torch.Tensor, torch.Tensor]) -> float:
    with torch.no_grad():
        return float(nn.MSELoss()(model(validation[0]), validation[1]).item())


def filters(model: nn.Sequential) -> torch.Tensor:
    """Los pesos de la capa convolucional, copiados."""
    layer = model[0]
    assert isinstance(layer, nn.Conv1d)
    return layer.weight.detach().clone()


def two_labels() -> pd.DataFrame:
    """Norte y Sur turnándose: 60 de cada una."""
    rows = [("Norte" if position % 2 else "Sur", float(position % 70)) for position in range(120)]
    return frame_of(rows)


# --- Forecast ---


def outcome(mae: float, baseline: float) -> Forecast:
    return Forecast(41, 41, (70, 15, 15), (1.0, 0.5), 1, mae, baseline)


def test_improves_when_the_network_errs_less_than_the_baseline() -> None:
    assert outcome(1.0, 2.0).improves


def test_a_tie_does_not_improve() -> None:
    assert not outcome(2.0, 2.0).improves


def test_forecast_is_frozen() -> None:
    with pytest.raises(FrozenInstanceError):
        outcome(1.0, 2.0).mae = 0.0  # type: ignore[misc]


# --- windows ---


def test_windows_shapes() -> None:
    x, y = windows(np.arange(10.0), 3)
    assert x.shape == (7, 1, 3)
    assert y.shape == (7, 1)


def test_windows_are_the_values_before_the_target() -> None:
    x, y = windows(np.arange(10.0), 3)
    assert x[0, 0].tolist() == [0.0, 1.0, 2.0]
    assert y[0].item() == 3.0
    assert x[-1, 0].tolist() == [6.0, 7.0, 8.0]
    assert y[-1].item() == 9.0


def test_windows_are_float32() -> None:
    x, y = windows(np.arange(10.0), 3)
    assert x.dtype == y.dtype == torch.float32


# --- cnn, freeze y count ---


def test_cnn_is_a_convolution_a_relu_a_flatten_and_a_line() -> None:
    layers = [type(layer) for layer in cnn(WINDOW)]
    assert layers == [nn.Conv1d, nn.ReLU, nn.Flatten, nn.Linear]


def test_cnn_filters() -> None:
    convolution_layer = cnn(WINDOW)[0]
    assert isinstance(convolution_layer, nn.Conv1d)
    assert convolution_layer.in_channels == 1
    assert convolution_layer.out_channels == CHANNELS
    assert convolution_layer.kernel_size == (KERNEL,)


@pytest.mark.parametrize(
    ("size", "channels", "expected"),
    [(8, 4, (4 * 3 + 4) + (4 * 6 + 1)), (5, 2, (2 * 3 + 2) + (2 * 3 + 1))],
)
def test_cnn_parameters(size: int, channels: int, expected: int) -> None:
    assert count(cnn(size, channels)) == expected


def test_cnn_predicts_one_value_per_window() -> None:
    assert cnn(WINDOW)(torch.zeros(5, 1, WINDOW)).shape == (5, 1)


def test_defaults() -> None:
    assert (WINDOW, CHANNELS, KERNEL) == (8, 4, 3)
    assert (EPOCHS, RATE, BATCH, PATIENCE, MINIMUM) == (100, 0.01, 32, 10, 20)


def test_freeze_stops_the_filters_only() -> None:
    model = cnn(WINDOW)
    freeze(model)
    assert [p.requires_grad for p in model[0].parameters()] == [False, False]
    assert [p.requires_grad for p in model[3].parameters()] == [True, True]


def test_count_trainable_after_freezing() -> None:
    model = cnn(WINDOW)
    freeze(model)
    assert (count(model), count(model, trainable=True)) == (41, 25)


# --- fit ---


def test_fit_is_the_loop_by_hand() -> None:
    train, validation = parts()
    torch.manual_seed(0)
    model = cnn(WINDOW)
    torch.manual_seed(0)
    twin = cnn(WINDOW)
    torch.manual_seed(1)
    losses, _ = fit(model, train, validation, epochs=15, patience=15)
    torch.manual_seed(1)
    assert losses == pytest.approx(by_hand(twin, train, validation, 15))


def test_fit_one_loss_per_epoch_without_stopping() -> None:
    train, validation = parts()
    losses, _ = fit(cnn(WINDOW), train, validation, epochs=12, patience=100)
    assert len(losses) == 12


def test_fit_best_is_the_lowest_loss() -> None:
    train, validation = parts()
    losses, best = fit(cnn(WINDOW), train, validation, epochs=30, patience=100)
    assert losses[best] == min(losses)


def test_fit_stops_after_patience_epochs_without_improving() -> None:
    values = noise(200)["valor"].to_numpy()
    x, y = windows((values - values.mean()) / values.std(), WINDOW)
    torch.manual_seed(SEED)
    losses, best = fit(cnn(WINDOW), (x[:150], y[:150]), (x[150:], y[150:]), patience=3)
    assert len(losses) < EPOCHS
    assert len(losses) == best + 3 + 1


def test_fit_returns_the_model_at_its_best_epoch() -> None:
    train, validation = parts()
    model = cnn(WINDOW)
    losses, best = fit(model, train, validation, epochs=40, patience=5)
    assert validation_loss(model, validation) == pytest.approx(losses[best])


def test_fit_learns_a_wave() -> None:
    train, validation = parts()
    torch.manual_seed(SEED)
    losses, best = fit(cnn(WINDOW), train, validation)
    assert losses[best] < 0.2


def test_fit_does_not_change_frozen_filters() -> None:
    train, validation = parts()
    model = cnn(WINDOW)
    freeze(model)
    before = filters(model)
    fit(model, train, validation, epochs=5)
    assert torch.equal(filters(model), before)


# --- forecast ---


def test_forecast_splits_by_time() -> None:
    # 120 valores, ventanas de 8: 112 ventanas; 78 entrenan, 17 validan y 17 son la prueba.
    result, _ = forecast(noise(), epochs=1)
    assert result.sizes == (78, 17, 17)


def test_forecast_learns_a_wave() -> None:
    result, _ = forecast(wave())
    assert result.improves
    assert result.mae < result.baseline / 3


def test_forecast_does_not_find_what_is_not_there() -> None:
    result, _ = forecast(noise(400))
    assert result.mae == pytest.approx(result.baseline, abs=2)


def test_forecast_baseline_is_the_mean_of_what_training_sees() -> None:
    # Un valor que crece: con otro reparto, o con la media de toda la serie, sería otra.
    frame = frame_of([("Norte", float(position % 80)) for position in range(120)])
    values = frame["valor"].to_numpy()
    center = values[: 78 + WINDOW].mean()
    expected = np.abs(values[WINDOW + 95 :] - center).mean()
    result, _ = forecast(frame, epochs=1)
    assert result.baseline == pytest.approx(expected, rel=1e-5)


def test_forecast_scales_the_value() -> None:
    frame = wave()
    frame["valor"] += 1000
    result, _ = forecast(frame, epochs=1)
    assert result.losses[0] < 3


def test_forecast_stops_early() -> None:
    result, _ = forecast(noise(400), patience=3)
    assert len(result.losses) == result.best + 3 + 1


def test_forecast_counts_the_parameters() -> None:
    result, _ = forecast(wave(), window=5, epochs=1)
    assert result.parameters == result.trainable == (4 * 3 + 4) + (4 * 3 + 1)


def test_forecast_follows_the_order_of_arrival() -> None:
    frame = wave()
    shuffled = frame.sample(frac=1, random_state=0)
    assert forecast(shuffled, epochs=3)[0] == forecast(frame, epochs=3)[0]


def test_forecast_drops_the_measures_without_value() -> None:
    frame = wave()
    frame.loc[[0, 1, 2], "valor"] = None
    result, _ = forecast(frame, epochs=3)
    assert sum(result.sizes) == 200 - 3 - WINDOW
    assert np.isfinite(result.mae)


def test_forecast_of_one_label() -> None:
    result, _ = forecast(two_labels(), label="Norte", epochs=1)
    assert sum(result.sizes) == 60 - WINDOW


def test_forecast_of_an_unknown_label() -> None:
    with pytest.raises(ValueError, match=r"al menos 28 valores para ventanas de 8, y hay 0"):
        forecast(two_labels(), label="Este")


def test_forecast_needs_enough_values() -> None:
    frame = wave(WINDOW + MINIMUM - 1)
    with pytest.raises(ValueError, match=r"al menos 28 valores para ventanas de 8, y hay 27"):
        forecast(frame)
    forecast(wave(WINDOW + MINIMUM), epochs=1)


def test_forecast_uses_the_seed() -> None:
    first, _ = forecast(noise(), epochs=5)
    assert first == forecast(noise(), epochs=5)[0]
    assert first != forecast(noise(), epochs=5, seed=7)[0]


def test_forecast_seed_fixes_the_initial_weights() -> None:
    torch.manual_seed(123)
    first, _ = forecast(wave(), epochs=3)
    torch.manual_seed(456)
    assert forecast(wave(), epochs=3)[0] == first


def test_forecast_returns_the_trained_model() -> None:
    _, model = forecast(wave(), epochs=3)
    assert count(model) == 41


def test_forecast_from_a_network_freezes_its_filters() -> None:
    start = cnn(WINDOW)
    before = filters(start)
    result, model = forecast(wave(), start=start, epochs=5)
    assert model is start
    assert result.trainable == 25
    assert torch.equal(filters(model), before)


def test_forecast_names_the_missing_columns() -> None:
    with pytest.raises(ValueError, match="faltan las columnas nivel"):
        forecast(wave().drop(columns=["nivel"]))


# --- save y load ---


def test_save_and_load(tmp_path: Path) -> None:
    model = cnn(5)
    save(model, 5, tmp_path / "pesos.pt")
    loaded, window = load(tmp_path / "pesos.pt")
    assert window == 5
    for mine, theirs in zip(model.parameters(), loaded.parameters(), strict=True):
        assert torch.equal(mine, theirs)


def test_load_rejects_what_is_not_only_weights(tmp_path: Path) -> None:
    # Un modelo entero se guarda con pickle, que al cargar puede ejecutar código.
    torch.save(cnn(WINDOW), tmp_path / "modelo.pt")
    with pytest.raises(pickle.UnpicklingError):
        load(tmp_path / "modelo.pt")


def test_save_where_it_cannot(tmp_path: Path) -> None:
    with pytest.raises(OSError):
        save(cnn(WINDOW), WINDOW, tmp_path / "no" / "pesos.pt")


# --- el comando pronosticar ---


def run(tmp_path: Path, frame: pd.DataFrame, *options: str) -> tuple[int, str]:
    result = runner.invoke(cli.app, ["pronosticar", str(write(tmp_path, frame)), *options])
    return result.exit_code, result.output


def test_pronosticar_prints_the_data_the_series_the_network_and_the_verdict(
    tmp_path: Path,
) -> None:
    code, output = run(tmp_path, wave())
    assert code == 0
    assert "instantanea.csv: 200 medidas · sha256: " in output
    assert "serie de todas las etiquetas · ventanas de 8 valores" in output
    assert "134 para entrenar, 29 para validar, 29 para prueba" in output
    assert "red convolucional, desde cero · 41 parámetros, 41 entrenables" in output
    assert "Pérdida en validación (MSE del valor escalado)" in output
    assert "se queda con la " in output
    assert "la red mejora la referencia" in output


def test_pronosticar_says_where_it_stopped(tmp_path: Path) -> None:
    _, output = run(tmp_path, noise(400), "--paciencia", "2")
    assert "paró en la época " in output


def test_pronosticar_says_when_it_trained_every_epoch(tmp_path: Path) -> None:
    _, output = run(tmp_path, wave(), "--epocas", "3")
    assert "entrenó 3 épocas" in output


def test_pronosticar_shows_six_epochs_at_most(tmp_path: Path) -> None:
    _, output = run(tmp_path, wave(), "--epocas", "13", "--paciencia", "20")
    rows = [line.split("│")[1].strip() for line in output.splitlines() if line.startswith("│")]
    assert rows == ["1", "4", "7", "10", "13"]


def test_pronosticar_says_when_it_does_not_improve(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def tie(*args: object) -> tuple[Forecast, nn.Sequential]:
        return outcome(2.0, 2.0), cnn(WINDOW)

    monkeypatch.setattr(convolution, "forecast", tie)
    _, output = run(tmp_path, wave())
    assert "red 2.000 · referencia 2.000: la red no mejora la referencia" in output


def test_pronosticar_passes_its_options_to_forecast(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    calls: list[tuple[object, ...]] = []

    def spy(*args: object) -> tuple[Forecast, nn.Sequential]:
        calls.append(args[1:])
        return outcome(1.0, 2.0), cnn(WINDOW)

    monkeypatch.setattr(convolution, "forecast", spy)
    options = ["--etiqueta", "Norte", "--ventana", "5", "--epocas", "40", "--paciencia", "4"]
    run(tmp_path, wave(), *options, "--semilla", "7")
    assert calls == [(5, 40, 4, 7, "Norte", None)]


def test_pronosticar_of_one_label(tmp_path: Path) -> None:
    _, output = run(tmp_path, two_labels(), "--etiqueta", "Norte", "--epocas", "1")
    assert "serie de Norte" in output


def test_pronosticar_saves_and_starts_from_the_weights(tmp_path: Path) -> None:
    weights = tmp_path / "pesos.pt"
    _, output = run(tmp_path, wave(), "--ventana", "5", "--epocas", "3", "--guardar", str(weights))
    assert f"pesos guardados en {weights}" in output
    code, output = run(tmp_path, wave(), "--epocas", "3", "--desde", str(weights))
    assert code == 0
    assert "ventanas de 5 valores" in output
    assert "filtros congelados de pesos.pt · 29 parámetros, 13 entrenables" in output


def test_pronosticar_checks_the_digest(tmp_path: Path) -> None:
    code, output = run(tmp_path, wave(), "--huella", "0000")
    assert code == 1
    assert "no 0000" in output


def test_pronosticar_with_too_few_values(tmp_path: Path) -> None:
    code, output = run(tmp_path, wave(20))
    assert code == 1
    assert "hacen falta al menos 28 valores" in output


def test_pronosticar_without_the_file(tmp_path: Path) -> None:
    result = runner.invoke(cli.app, ["pronosticar", str(tmp_path / "no.csv")])
    assert result.exit_code == 2
    assert "no se puede usar" in result.output


def test_pronosticar_from_a_file_that_is_not_weights(tmp_path: Path) -> None:
    torch.save(cnn(WINDOW), tmp_path / "modelo.pt")
    code, output = run(tmp_path, wave(), "--desde", str(tmp_path / "modelo.pt"))
    assert code == 2
    assert "no es un archivo de pesos" in output


def test_pronosticar_saving_where_it_cannot(tmp_path: Path) -> None:
    code, output = run(tmp_path, wave(), "--epocas", "1", "--guardar", str(tmp_path / "no" / "p"))
    assert code == 2
    assert "no se puede usar" in output


@pytest.mark.parametrize(
    ("option", "value"), [("--ventana", "2"), ("--epocas", "0"), ("--paciencia", "0")]
)
def test_pronosticar_rejects_options_out_of_range(tmp_path: Path, option: str, value: str) -> None:
    code, output = run(tmp_path, signal(), option, value)
    assert code == 2
    assert "not in the range" in output


def test_convolution_is_not_reexported_in_core() -> None:
    assert "convolution" not in observatorio.core.__all__
    assert not hasattr(observatorio.core, "forecast")
