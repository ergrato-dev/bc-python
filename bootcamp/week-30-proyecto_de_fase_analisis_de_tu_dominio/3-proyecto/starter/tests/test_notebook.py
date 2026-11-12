"""Tests de la semana 29: tu notebook de análisis es reproducible, y JupyterLab corre en Docker.

Qué: leen notebooks/eda.ipynb como lo que es, un JSON, y comprueban que llega a Git sin
salidas, que en Colab instala las versiones de tu pyproject.toml, que comprueba la huella
de su instantánea y que se ejecuta de arriba abajo en un proceso limpio. Después, las
piezas que lo sirven: el grupo `notebook`, la etapa del Dockerfile, el servicio de
compose.yaml y el gancho de pre-commit.
Para qué: un notebook que solo funciona en el orden en que lo ejecutaste tú, con lo que
tenías en memoria, no se puede repetir. Aquí se ejecuta cada celda en orden, sin Jupyter,
y sin nada de lo que dejó la sesión anterior.
Impacto: no necesitan JupyterLab ni PostgreSQL: se ejecutan con el resto, en tu máquina,
en Docker y en la CI.
"""

import json
import re
import tomllib
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import pytest
from test_delivery import compose, hooks_of, stage, unprivileged

ROOT = Path(__file__).parent.parent
FOLDER = ROOT / "notebooks"
NOTEBOOK = FOLDER / "eda.ipynb"
SNAPSHOT = FOLDER / "instantanea.csv"
PIN = re.compile(r'"([A-Za-z0-9_.\[\]-]+)==([^"]+)"')


def notebook() -> dict[str, Any]:
    data = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def cells(kind: str) -> list[dict[str, Any]]:
    return [cell for cell in notebook()["cells"] if cell["cell_type"] == kind]


def source(cell: dict[str, Any]) -> str:
    # En el JSON, el código de una celda es una lista de líneas (o, a veces, un texto).
    text = cell["source"]
    return text if isinstance(text, str) else "".join(text)


def pyproject() -> dict[str, Any]:
    with (ROOT / "pyproject.toml").open("rb") as file:
        return tomllib.load(file)


# --- el notebook ----------------------------------------------------------------------


def test_notebook_is_nbformat_4() -> None:
    assert notebook()["nbformat"] == 4


def test_notebook_has_no_outputs() -> None:
    # Las salidas (tablas, imágenes en base64) inflan el archivo y ensucian cada diff.
    dirty = [index for index, cell in enumerate(cells("code")) if cell["outputs"]]
    assert dirty == [], "ejecuta `uv run pre-commit run notebook-outputs --all-files`"


def test_notebook_has_no_execution_counts() -> None:
    counts = [cell["execution_count"] for cell in cells("code")]
    assert counts == [None] * len(counts)


def test_notebook_has_no_execution_times() -> None:
    # Jupyter guarda en cada celda la hora a la que se ejecutó: un cambio en cada diff.
    timed = [index for index, cell in enumerate(notebook()["cells"]) if cell["metadata"]]
    assert timed == [], "ejecuta `uv run pre-commit run notebook-outputs --all-files`"


def test_notebook_keeps_its_kernel() -> None:
    assert notebook()["metadata"]["kernelspec"]["name"] == "python3"


def test_notebook_starts_with_a_colab_button() -> None:
    first = notebook()["cells"][0]
    assert first["cell_type"] == "markdown"
    assert "colab.research.google.com/assets/colab-badge.svg" in source(first)
    assert re.search(
        r"colab\.research\.google\.com/github/[^)\s]+/notebooks/eda\.ipynb", source(first)
    )


def test_colab_cell_installs_the_pinned_versions() -> None:
    first = source(cells("code")[0])
    assert 'if "google.colab" in sys.modules:' in first
    pins = PIN.findall(first)
    assert pins, "la primera celda de código no instala ninguna versión fijada"
    dependencies = set(pyproject()["project"]["dependencies"])
    assert {f"{name}=={version}" for name, version in pins} <= dependencies


def test_notebook_is_plain_python() -> None:
    # Ni `%magia` ni `!orden` de IPython, ni display(): así se ejecuta también sin Jupyter.
    for cell in cells("code"):
        for line in source(cell).splitlines():
            assert not line.lstrip().startswith(("%", "!")), line
        assert "display(" not in source(cell)


def test_notebook_checks_the_digest_of_its_snapshot() -> None:
    code = "\n".join(source(cell) for cell in cells("code"))
    assert "instantanea.csv" in code
    assert "hashlib.sha256" in code
    assert re.search(r'^EXPECTED = "[0-9a-f]{64}"$', code, re.MULTILINE)
    assert "assert hashlib.sha256" in code


def test_notebook_writes_its_conclusions() -> None:
    assert any("## Conclusiones" in source(cell) for cell in cells("markdown"))


def test_snapshot_is_small_enough_for_git() -> None:
    # check-added-large-files para el commit por encima de 500 KB.
    assert SNAPSHOT.stat().st_size < 500 * 1024


def test_notebook_runs_top_to_bottom(monkeypatch: pytest.MonkeyPatch) -> None:
    # Como "Restart Kernel and Run All Cells": un espacio de nombres vacío, cada celda de
    # código en orden, en la carpeta del notebook. Si una celda usa algo de una celda
    # borrada o posterior, falla aquí.
    monkeypatch.chdir(FOLDER)
    namespace: dict[str, Any] = {"__name__": "__main__"}
    try:
        for index, cell in enumerate(cells("code")):
            # exec, solo sobre tu propio notebook: es exactamente lo que hace Jupyter.
            exec(compile(source(cell), f"celda {index}", "exec"), namespace)  # noqa: S102
    finally:
        plt.close("all")


# --- JupyterLab -----------------------------------------------------------------------


def test_jupyterlab_is_its_own_pinned_group() -> None:
    assert pyproject()["dependency-groups"]["notebook"] == ["jupyterlab==4.6.4"]


def test_jupyterlab_is_not_installed_by_default() -> None:
    # Sin default-groups, uv sync instala solo `dev`: ni la CI de tests ni la imagen cargan
    # JupyterLab y sus decenas de paquetes.
    assert "default-groups" not in pyproject().get("tool", {}).get("uv", {})


def test_notebook_stage_adds_the_notebook_group() -> None:
    assert stage("notebook").base == "builder"
    assert (
        stage("notebook").lines("RUN")[0]
        == "uv sync --locked --no-dev --no-editable --group notebook"
    )


def test_notebook_stage_runs_as_an_unprivileged_user() -> None:
    assert [unprivileged(user) for user in stage("notebook").lines("USER")] == [True]


def test_notebook_stage_serves_jupyterlab() -> None:
    (command,) = stage("notebook").lines("CMD")
    assert json.loads(command) == [
        "jupyter",
        "lab",
        "--ip",
        "0.0.0.0",
        "--port",
        "8888",
        "--no-browser",
    ]
    assert stage("notebook").lines("EXPOSE") == ["8888"]


def test_notebook_stage_keeps_the_random_token() -> None:
    # Sin token, cualquiera que llegue al puerto ejecuta código en tu máquina.
    assert "token" not in " ".join(stage("notebook").instructions).lower()


def test_runtime_has_no_jupyter() -> None:
    assert "jupyter" not in " ".join(stage("runtime").instructions)


def test_notebook_service() -> None:
    service = compose()["services"]["notebook"]
    assert service["build"] == {"context": ".", "target": "notebook"}
    assert service["image"] == "local/observatorio:week-30-notebook"
    assert service["profiles"] == ["notebook"]
    assert service["volumes"] == ["./notebooks:/app/notebooks"]
    assert service["ports"] == ["127.0.0.1:8888:8888"]


def test_hook_clears_outputs_and_cell_metadata() -> None:
    hook = hooks_of("local")["notebook-outputs"]
    assert hook["entry"].split() == [
        *[
            "uv",
            "run",
            "--locked",
            "--group",
            "notebook",
            "jupyter",
            "nbconvert",
            "--clear-output",
            "--inplace",
        ],
        "--ClearMetadataPreprocessor.enabled=True",
        "--ClearMetadataPreprocessor.preserve_nb_metadata_mask=kernelspec",
    ]
    assert hook["files"] == r"\.ipynb$"
    assert "pass_filenames" not in hook
