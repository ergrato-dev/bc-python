"""Tests de la semana 33: grupos de etiquetas con KMeans.

Qué: comprueban core/clustering.py (el perfil de cada etiqueta, los grupos, su numeración y
la silueta) y el comando `agrupar`.
Para qué: KMeans siempre devuelve k grupos, también si no hay ninguno. Sin escalar, decide
la columna con los números más grandes; sin numerar los grupos de forma fija, el mismo
reparto sale con otros números; y sin la silueta, nadie sabe si los grupos se solapan.
Impacto: clustering.py no se reexporta en core: la CLI arranca sin cargar scikit-learn.
"""

import hashlib
import re
from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from test_validation import frame_of, noise, write
from typer.testing import CliRunner

import observatorio.core
from observatorio import cli
from observatorio.core.clustering import SEPARATED, Clustering, cluster, profiles

runner = CliRunner()


def spread(spec: dict[str, tuple[float, float]]) -> list[tuple[str, float]]:
    """Tres medidas por etiqueta: su centro y el centro más y menos una distancia. La
    media y la mediana son el centro; la desviación, la distancia."""
    rows = []
    for label, (center, distance) in spec.items():
        rows += [(label, center - distance), (label, center), (label, center + distance)]
    return rows


def two_groups() -> list[tuple[str, float]]:
    """Norte y Oeste, limpios; Centro y Sur, sucios. La misma dispersión en todas."""
    return spread(
        {"Norte": (10.0, 2.0), "Centro": (60.0, 2.0), "Oeste": (11.0, 2.0), "Sur": (61.0, 2.0)}
    )


# --- Clustering ---


def test_separated_from_the_threshold() -> None:
    assert Clustering({}, SEPARATED).separated
    assert not Clustering({}, SEPARATED - 0.01).separated
    assert SEPARATED == 0.5


def test_clustering_is_frozen() -> None:
    with pytest.raises(FrozenInstanceError):
        Clustering({}, 0.5).silhouette = 1.0  # type: ignore[misc]


# --- profiles ---


def test_profiles_one_row_per_label_in_alphabetical_order() -> None:
    table = profiles(frame_of(two_groups()))
    assert table.index.tolist() == ["Centro", "Norte", "Oeste", "Sur"]
    assert table.columns.tolist() == ["media", "mediana", "desviacion"]


def test_profiles_mean_median_and_deviation() -> None:
    rows = [("Norte", 1.0), ("Norte", 2.0), ("Norte", 9.0), ("Sur", 4.0), ("Sur", 4.0)]
    table = profiles(frame_of(rows))
    assert list(table.loc["Norte"]) == pytest.approx([4.0, 2.0, 4.358898943540674])
    assert list(table.loc["Sur"]) == pytest.approx([4.0, 4.0, 0.0])


def test_profiles_deviation_of_a_single_measure_is_zero() -> None:
    rows = [("Norte", 1.0), ("Norte", 3.0), ("Sur", 50.0), ("Sur", 52.0), ("Este", 7.0)]
    assert profiles(frame_of(rows)).loc["Este", "desviacion"] == 0.0


def test_profiles_leave_out_the_measures_without_value() -> None:
    frame = frame_of(two_groups())
    frame.loc[0, ["valor", "nivel"]] = [None, "sin dato"]
    frame.loc[len(frame)] = [1, len(frame), "Este", None, "sin dato"]
    table = profiles(frame)
    assert table.loc["Norte", "media"] == pytest.approx(11.0)
    # Una etiqueta sin ningún valor no tiene perfil: no puede estar en ningún grupo.
    assert "Este" not in table.index


# --- cluster ---


def test_cluster_finds_two_clear_groups() -> None:
    result = cluster(frame_of(two_groups()), 2)
    assert result.groups == {"Centro": 1, "Norte": 2, "Oeste": 2, "Sur": 1}
    assert result.separated


def test_cluster_numbers_the_groups_in_alphabetical_order() -> None:
    result = cluster(frame_of(two_groups()), 3)
    assert result.groups["Centro"] == 1
    assert sorted(set(result.groups.values())) == [1, 2, 3]


def test_cluster_scales_the_profiles() -> None:
    # Sin escalar, la desviación (de 0 a 30) decide sola; escalada, pesan igual que la
    # media y la mediana (de 10 a 12), que separan A y B de C y D.
    rows = spread({"A": (10.0, 0.0), "B": (10.0, 20.0), "C": (12.0, 10.0), "D": (12.0, 30.0)})
    assert cluster(frame_of(rows), 2).groups == {"A": 1, "B": 1, "C": 2, "D": 2}


def test_cluster_silhouette_is_measured_on_the_scaled_profiles() -> None:
    rows = spread({"A": (10.0, 0.0), "B": (10.0, 20.0), "C": (12.0, 10.0), "D": (12.0, 30.0)})
    scaled = StandardScaler().fit_transform(profiles(frame_of(rows)))
    expected = silhouette_score(scaled, [1, 1, 2, 2])
    assert cluster(frame_of(rows), 2).silhouette == pytest.approx(expected)


def test_cluster_silhouette_of_clear_groups_is_high() -> None:
    assert cluster(frame_of(two_groups()), 2).silhouette > 0.8


def test_cluster_silhouette_of_noise_is_low() -> None:
    result = cluster(noise(300), 2)
    assert result.silhouette < SEPARATED
    assert not result.separated


@pytest.mark.parametrize("k", [1, 4, 5])
def test_cluster_needs_between_two_and_one_less_than_the_labels(k: int) -> None:
    with pytest.raises(ValueError, match=r"^con 4 etiquetas, los grupos van de 2 a 3$"):
        cluster(frame_of(two_groups()), k)


def test_cluster_is_repeatable() -> None:
    # Doce etiquetas sin grupos claros: sin semilla, cada vez empezaría por otros centros.
    rows = [
        (f"zona {index:02}", float(value)) for index in range(12) for value in (index * 7 % 11, 5)
    ]
    frame = frame_of(rows)
    first = cluster(frame, 4)
    assert all(cluster(frame, 4) == first for _ in range(5))


@settings(max_examples=25, deadline=None)
@given(st.lists(st.floats(min_value=0, max_value=100), min_size=8, max_size=8), st.integers(2, 3))
def test_cluster_groups_go_from_one_to_k(values: list[float], k: int) -> None:
    labels = ["Centro", "Este", "Norte", "Sur"]
    rows = [(labels[index % 4], round(value, 1)) for index, value in enumerate(values)]
    frame = frame_of(rows)
    if profiles(frame).drop_duplicates().shape[0] < k:
        return
    result = cluster(frame, k)
    assert list(result.groups) == labels
    assert result.groups["Centro"] == 1
    assert sorted(set(result.groups.values())) == list(range(1, k + 1))
    assert -1.0 <= result.silhouette <= 1.0


# --- el comando agrupar ---


def test_agrupar_prints_the_data_the_table_and_the_verdict(tmp_path: Path) -> None:
    path = write(tmp_path, frame_of(two_groups()))
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    result = runner.invoke(cli.app, ["agrupar", str(path)])
    assert result.exit_code == 0, result.output
    assert f"instantanea.csv: 12 medidas · sha256: {digest}" in result.output
    assert "Grupos de etiquetas" in result.output
    silhouette = cluster(frame_of(two_groups()), 2).silhouette
    assert f"2 grupos · silueta {silhouette:.2f}: grupos separados" in result.output


def test_agrupar_one_row_per_label_with_its_group_and_profile(tmp_path: Path) -> None:
    result = runner.invoke(cli.app, ["agrupar", str(write(tmp_path, frame_of(two_groups())))])
    assert re.search(r"│ Centro +│ +1 │ +60\.0 │ +60\.0 │ +2\.0 │", result.output)
    assert re.search(r"│ Oeste +│ +2 │ +11\.0 │ +11\.0 │ +2\.0 │", result.output)


def test_agrupar_says_when_the_groups_overlap(tmp_path: Path) -> None:
    result = runner.invoke(cli.app, ["agrupar", str(write(tmp_path, noise(300))), "-g", "2"])
    silhouette = cluster(noise(300), 2).silhouette
    assert f"2 grupos · silueta {silhouette:.2f}: grupos que se solapan" in result.output


def test_agrupar_with_more_groups(tmp_path: Path) -> None:
    path = str(write(tmp_path, frame_of(two_groups())))
    result = runner.invoke(cli.app, ["agrupar", path, "--grupos", "3"])
    assert re.search(r"│ +3 │", result.output)
    assert "3 grupos · silueta" in result.output


def test_agrupar_with_too_many_groups(tmp_path: Path) -> None:
    path = str(write(tmp_path, frame_of(two_groups())))
    result = runner.invoke(cli.app, ["agrupar", path, "-g", "4"])
    assert result.exit_code == 1
    assert "con 4 etiquetas, los grupos van de 2 a 3" in result.output


def test_agrupar_rejects_less_than_two_groups(tmp_path: Path) -> None:
    path = str(write(tmp_path, frame_of(two_groups())))
    result = runner.invoke(cli.app, ["agrupar", path, "-g", "1"])
    assert result.exit_code == 2
    assert "not in the range x>=2" in result.output


def test_agrupar_checks_the_digest(tmp_path: Path) -> None:
    path = str(write(tmp_path, frame_of(two_groups())))
    result = runner.invoke(cli.app, ["agrupar", path, "--huella", "0000"])
    assert result.exit_code == 1
    assert "no 0000" in result.output


def test_agrupar_without_the_file(tmp_path: Path) -> None:
    result = runner.invoke(cli.app, ["agrupar", str(tmp_path / "no.csv")])
    assert result.exit_code == 2
    assert "no se puede leer" in result.output


def test_clustering_is_not_reexported_in_core() -> None:
    assert "clustering" not in observatorio.core.__all__
    assert not hasattr(observatorio.core, "cluster")
