# Proyecto — Observatorio, capa 29: el informe de tu dominio

> Cierre de la fase 4. Tus datos ya recorren el Observatorio de la fuente a una instantánea con huella, y los has explorado en un notebook. Esta semana **confirmas**: haces una pregunta antes de mirar la respuesta, comparas cada par de etiquetas corrigiendo por comparaciones múltiples, y publicas un informe que sale de un comando y que la CI vigila.

## Qué construyes

```
$ uv run observatorio hallazgos notebooks/instantanea.csv informe
instantanea.csv: 2000 medidas · sha256: 3193779438eecdede9910a3cbc922f05a883e69a8a92fd4ef9a33e482d636c65
Difieren 0 de 10 pares de etiquetas (BH, α = 0.05)
informe: informe/hallazgos.md · figura: informe/diferencias.svg
```

| Pieza | Qué hace |
|---|---|
| `core/findings.py` | `read_snapshot` lee la instantánea y comprueba su huella; `compare_all` compara cada par de etiquetas y corrige con Benjamini-Hochberg; `differences_figure` dibuja las diferencias con su intervalo; `render` escribe el informe en Markdown |
| `hallazgos INSTANTANEA CARPETA` | Escribe `hallazgos.md` y `diferencias.svg`, con `--huella`, `--confianza` y `--alfa` |
| `informe/README.md` | Tu informe: pregunta, datos, hallazgos, limitaciones y siguientes pasos, escrito por ti |

Ninguna dependencia nueva: `findings.py` usa pandas, SciPy y matplotlib, que ya tienes.

```
src/observatorio/
├── cli.py                  # modificado: hallazgos
└── core/
    └── findings.py         # nuevo: sin reexportar en core/__init__.py
informe/
├── README.md               # nuevo: tu informe
├── hallazgos.md            # nuevo: lo escribe `hallazgos`
└── diferencias.svg         # nuevo: lo escribe `hallazgos`
tests/
├── test_findings.py        # nuevo: los tests del bootcamp
├── test_informe.py         # nuevo: tu informe, al día
├── test_my_findings.py     # nuevo: los tuyos
├── test_delivery.py        # modificado: las imágenes week-30
├── test_notebook.py        # modificado: la imagen week-30-notebook
└── test_package.py         # modificado: findings en core y la versión 0.30.0
compose.yaml                # modificado: las imágenes week-30
```

## Dónde trabajas

En **tu repositorio** `python-<nombre>-<apellido>`, en una rama nueva `week-30`. El `starter/` trae la capa 28 resuelta: `core/etl.py`, el comando `extraer`, JupyterLab en Docker y un notebook de ejemplo con su instantánea. **Tú** escribes `findings.py`, `hallazgos` y tu informe.

## Pasos

### 1. Rama de la semana

Comprueba que el *pull request* `week-29` está fusionado en `main` y su CI en verde. Después:

```bash
cd ~/proyectos/python-<nombre>-<apellido>
git switch main
git pull
git switch -c week-30
```

### 2. Copia los archivos nuevos

```bash
STARTER=<ruta-al-bootcamp>/bootcamp/week-30-proyecto_de_fase_analisis_de_tu_dominio/3-proyecto/starter
cp $STARTER/tests/test_findings.py $STARTER/tests/test_informe.py $STARTER/tests/test_my_findings.py tests/
cp $STARTER/tests/test_delivery.py $STARTER/tests/test_notebook.py $STARTER/tests/test_package.py tests/
git status --short
```

- **Nuevos:** `test_findings.py`, con 45 tests (uno con Hypothesis); `test_informe.py`, con 6; y `test_my_findings.py`, con un ejemplo.
- **Modificados:** `test_delivery.py` y `test_notebook.py`, las imágenes `week-30`; `test_package.py`, `findings` es un módulo de `core` y la versión es `0.30.0`.

### 3. Tests en rojo

```bash
docker compose up -d --wait db
uv run pytest -q
```

```
E   ModuleNotFoundError: No module named 'observatorio.core.findings'
...
!!!!!!!!!!!!!!!!!!! Interrupted: 3 errors during collection !!!!!!!!!!!!!!!!!!!!
```

Antes de seguir, lee `tests/test_findings.py` y `tests/test_informe.py` enteros. Fíjate en:

- `ROWS`, la tabla de prueba: tres etiquetas comparables, una con un solo valor y otra sin ninguno;
- `test_compare_all_correction_by_hand`, que calcula BH sin SciPy (teoría 03, sección 3);
- `finding()`, que construye un hallazgo con números fijos para probar la figura y el informe sin depender de SciPy;
- `test_render_escapes_a_bar_in_a_label`: los datos son una frontera de confianza;
- `test_report_is_up_to_date`, que genera el informe de nuevo y lo compara con el tuyo (teoría 04, sección 6);
- `test_readme_cites_the_digest_of_the_notebook`: tu informe y tu notebook hablan de los mismos datos.

### 4. La pregunta, antes que la respuesta

Antes de escribir código, decide qué vas a preguntar (teoría 01). Mira tu `notebooks/eda.ipynb` de la semana 29: ¿qué etiquetas te parecieron distintas? ¿Cuál es la unidad de tus datos? ¿Hay algo, como la hora o el sensor, que podría confundir la comparación?

Crea `informe/README.md` solo con el título y la pregunta, con sus cuatro piezas:

```markdown
# Informe: ¿difieren las zonas?

## Pregunta

En la carga 1 (2000 medidas de marzo), ¿difiere la media del valor entre zonas? Cada medida es un caso; se comparan todos los pares de zonas, con un intervalo del 95 % y los p-valores corregidos por Benjamini-Hochberg (α = 0,05).
```

Con las etiquetas, la unidad y la carga de **tu dominio**. Y haz commit **ya**:

```bash
git add informe/README.md
git commit -m "docs: state the question of the report"
```

La hora de este commit demuestra que la pregunta estaba antes que la respuesta.

### 5. El módulo `findings.py`

Crea `src/observatorio/core/findings.py`:

```python
"""Los hallazgos de una instantánea: qué etiquetas difieren de verdad, con su informe.

Qué: read_snapshot lee la instantánea de `extraer` y comprueba su huella, compare_all
compara cada par de etiquetas con inference.difference y corrige los p-valores por
comparaciones múltiples, differences_figure dibuja cada diferencia con su intervalo, y
render escribe el informe en Markdown.
Para qué: con cinco etiquetas hay diez pares; si los compruebas uno a uno con α = 0,05, lo
normal es que alguno salga "significativo" por azar. La corrección de Benjamini-Hochberg
controla cuántos de los hallazgos que publicas son falsos, y el informe, generado desde el
código, dice exactamente con qué datos y con qué método se obtuvo cada número.
Impacto: importa pandas, scipy y matplotlib: core/__init__.py no lo reexporta, y la CLI lo
importa solo en `hallazgos`.
"""

import hashlib
import io
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
from matplotlib.figure import Figure
from scipy import stats

from observatorio.core.inference import Comparison, difference

# Los nombres de los dos archivos que escribe `hallazgos`; el informe enlaza la figura.
REPORT = "hallazgos.md"
FIGURE = "diferencias.svg"
COLUMNS = {"etiqueta", "valor"}


@dataclass(frozen=True)
class Finding:
    """Un par de etiquetas comparado; p_adjusted es el p de Welch ya corregido."""

    first: str
    second: str
    comparison: Comparison
    p_adjusted: float


def read_snapshot(path: Path, expected: str | None = None) -> tuple[pd.DataFrame, str]:
    """La instantánea y su huella SHA-256. Lanza ValueError si la huella no es expected o
    si le faltan las columnas `etiqueta` y `valor`."""
    # Una sola lectura: la huella es la de los mismos bytes que se analizan.
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if expected is not None and digest != expected:
        raise ValueError(f"la huella de {path.name} es {digest}, no {expected}")
    # Como el notebook: "NA" es una etiqueta, solo una celda vacía de `valor` falta.
    frame = pd.read_csv(
        io.BytesIO(data),
        keep_default_na=False,
        na_values={"valor": [""]},
        dtype={"etiqueta": "str", "valor": "float64"},
    )
    missing = COLUMNS - set(frame.columns)
    if missing:
        raise ValueError(f"a {path.name} le faltan las columnas {', '.join(sorted(missing))}")
    return frame, digest


def comparable(frame: pd.DataFrame) -> list[str]:
    """Las etiquetas con al menos dos valores distintos, en orden alfabético: las que
    inference.difference puede comparar."""
    distinct = frame.groupby("etiqueta")["valor"].nunique()
    return [str(label) for label in distinct.index[distinct >= 2]]


def compare_all(frame: pd.DataFrame, confidence: float = 0.95) -> list[Finding]:
    """Cada par de etiquetas comparables, en orden alfabético, con su p corregido.

    Lanza ValueError si hay menos de dos etiquetas comparables.
    """
    labels = comparable(frame)
    if len(labels) < 2:
        raise ValueError(f"hacen falta dos etiquetas con valores que varíen (hay {len(labels)})")
    samples = {
        label: frame.loc[frame["etiqueta"] == label, "valor"].dropna().to_numpy(np.float64)
        for label in labels
    }
    pairs = list(combinations(labels, 2))
    comparisons = [difference(samples[a], samples[b], confidence) for a, b in pairs]
    # Benjamini-Hochberg: el p de cada par, corregido por todos los que se comparan a la vez.
    adjusted = stats.false_discovery_control([c.p_welch for c in comparisons], method="bh")
    return [
        Finding(a, b, comparison, float(p))
        for (a, b), comparison, p in zip(pairs, comparisons, adjusted, strict=True)
    ]


def headline(findings: list[Finding], alpha: float) -> str:
    """La conclusión en una frase: el título de la figura y el resumen del informe."""
    real = sum(finding.p_adjusted < alpha for finding in findings)
    return f"Difieren {real} de {len(findings)} pares de etiquetas (BH, α = {alpha:g})"


def differences_figure(findings: list[Finding], unit: str, alpha: float) -> Figure:
    """Un punto por par con su intervalo, y una línea en el cero: un intervalo que la cruza
    es una diferencia que puede no existir."""
    figure = Figure(figsize=(8, 1.5 + 0.4 * len(findings)), layout="constrained")
    axes = figure.add_subplot()
    rows = range(len(findings))
    centers = [finding.comparison.difference for finding in findings]
    below = [finding.comparison.difference - finding.comparison.low for finding in findings]
    above = [finding.comparison.high - finding.comparison.difference for finding in findings]
    axes.errorbar(centers, rows, xerr=[below, above], fmt="o", capsize=4)
    axes.axvline(0, color="grey", linestyle="--")
    axes.set_yticks(rows, [f"{finding.first} - {finding.second}" for finding in findings])
    # El primer par arriba, como en la tabla del informe.
    axes.invert_yaxis()
    axes.set(title=headline(findings, alpha), xlabel=f"diferencia de medias ({unit})")
    return figure


def cell(label: str) -> str:
    """Una etiqueta dentro de una tabla de Markdown: una barra la partiría en dos columnas."""
    return label.replace("|", "\\|")


def render(
    frame: pd.DataFrame,
    findings: list[Finding],
    *,
    name: str,
    digest: str,
    confidence: float = 0.95,
    alpha: float = 0.05,
) -> str:
    """El informe en Markdown. Sin fecha ni rutas: los mismos datos dan los mismos bytes."""
    level = f"{confidence * 100:g} %"
    compared = {label for finding in findings for label in (finding.first, finding.second)}
    left_out = sorted(set(frame["etiqueta"]) - compared)
    lines = [
        "# Hallazgos: diferencias entre etiquetas",
        "",
        (
            f"**Datos**: `{name}`, sha256 `{digest}`: {len(frame)} medidas,"
            f" {int(frame['valor'].notna().sum())} con valor."
        ),
        "",
        (
            f"**Método**: para cada par de etiquetas ({len(findings)} pares), la diferencia de"
            f" medias con su intervalo del {level} (Welch) y el tamaño del efecto (d de Cohen)."
            " Los p-valores de Welch se corrigen con Benjamini-Hochberg; un par difiere si su p"
            f" corregido es menor que {alpha:g}. Mann-Whitney, que no supone una campana, sirve de"
            " contraste."
        ),
        "",
        "## Resumen",
        "",
        f"{headline(findings, alpha)}.",
        "",
        f"![Diferencia de medias de cada par, con su intervalo del {level}]({FIGURE})",
        "",
        "## Pares",
        "",
        (
            f"| Par | Medidas | Diferencia | IC {level} | d | p Welch | p corregido"
            " | p Mann-Whitney | ¿Difiere? |"
        ),
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for finding in findings:
        result = finding.comparison
        lines.append(
            f"| {cell(finding.first)} - {cell(finding.second)}"
            f" | {result.sizes[0]} / {result.sizes[1]} | {result.difference:.2f}"
            f" | [{result.low:.2f}, {result.high:.2f}] | {result.effect:.2f}"
            f" | {result.p_welch:.3g} | {finding.p_adjusted:.3g} | {result.p_ranks:.3g}"
            f" | {'sí' if finding.p_adjusted < alpha else 'no'} |"
        )
    if left_out:
        lines += [
            "",
            (
                "Sin comparar, por tener menos de dos valores distintos:"
                f" {', '.join(cell(label) for label in left_out)}."
            ),
        ]
    return "\n".join(lines) + "\n"
```

Por partes:

- **`read_snapshot`** lee los bytes **una vez**: la huella es la de lo que se analiza (como `write_snapshot` de la semana 29). Lee igual que tu notebook (`keep_default_na=False`) y fija los tipos: una etiqueta `01` sigue siendo `01`, y un valor `doce` es un error, no un texto. Sin las columnas `etiqueta` y `valor`, `ValueError`.
- **`comparable`** cuenta los valores **distintos** de cada etiqueta: `inference.difference` necesita al menos dos, y que varíen. Las que no llegan se quedan fuera, y el informe lo dice.
- **`compare_all`** reutiliza `difference` de la semana 28 para cada par, en orden alfabético, y corrige los p de Welch **todos juntos** con `false_discovery_control`, que los devuelve en el mismo orden (teoría 03, sección 3).
- **`headline`** se usa en el título de la figura, en el resumen del informe y en la salida del comando: escrita una vez, no pueden contradecirse.
- **`differences_figure`** es el *forest plot* de la teoría 04, sección 3, con `Figure` y sin `pyplot`, como `charts.py`.
- **`render`** construye el Markdown con una lista de líneas, sin fecha ni rutas: los mismos datos dan los mismos bytes.

```bash
uv run pytest -q
```

```
19 failed, 1089 passed
```

Fallan los del comando, los de la versión y las imágenes, y los de tu informe.

### 6. El comando `hallazgos`

En `src/observatorio/cli.py`, después de `extraer`:

```python
@app.command()
def hallazgos(
    instantanea: Annotated[
        Path, typer.Argument(metavar="INSTANTANEA", help="El CSV que escribió `extraer`.")
    ],
    carpeta: Annotated[
        Path, typer.Argument(metavar="CARPETA", help="Donde escribe el informe y la figura.")
    ],
    huella: Annotated[
        str | None, typer.Option(help="La huella SHA-256 que debe tener la instantánea.")
    ] = None,
    confianza: Annotated[
        float, typer.Option(min=0.5, max=0.999, help="Nivel de los intervalos: 0.9, 0.95...")
    ] = 0.95,
    alfa: Annotated[
        float,
        typer.Option(min=0.001, max=0.5, help="Umbral del p corregido para decir que difieren."),
    ] = 0.05,
) -> None:
    """Compara cada par de etiquetas de una instantánea y escribe el informe de hallazgos."""
    # Importar aquí, como en `comparar`: pandas, scipy y matplotlib tardan en cargarse.
    from observatorio.core import charts, findings

    try:
        frame, digest = findings.read_snapshot(instantanea, huella)
        found = findings.compare_all(frame, confianza)
    except OSError as problem:
        raise fail(f"no se puede leer {instantanea}: {problem}", 2) from problem
    except ValueError as problem:
        raise fail(str(problem), 1) from problem
    report = findings.render(
        frame, found, name=instantanea.name, digest=digest, confidence=confianza, alpha=alfa
    )
    try:
        carpeta.mkdir(parents=True, exist_ok=True)
        charts.save(findings.differences_figure(found, UNIT, alfa), carpeta / findings.FIGURE)
        (carpeta / findings.REPORT).write_text(report, encoding="utf-8")
    except OSError as problem:
        raise fail(f"no se puede escribir en {carpeta}: {problem}", 2) from problem
    out.print(f"{instantanea.name}: {len(frame)} medidas · sha256: {digest}")
    out.print(findings.headline(found, alfa))
    out.print(f"informe: {carpeta / findings.REPORT} · figura: {carpeta / findings.FIGURE}")
```

- Los dos `try` separan **leer** (código 2 si el archivo no se puede leer; 1 si la huella no coincide o no hay dos etiquetas comparables) de **escribir** (código 2 si la carpeta no se puede crear o escribir). Un error al leer no deja una carpeta a medias.
- `--huella` es opcional: con ella, `hallazgos` se niega a analizar otra instantánea que la que dices.
- `charts.save` (semana 27) guarda el SVG sin fecha, con sal fija y con el texto como texto.
- Importa `findings` y `charts` dentro: la CLI sigue arrancando sin pandas, SciPy ni matplotlib.

Actualiza el docstring del módulo: "veinte comandos", con `hallazgos` entre `extraer` y `borrar`.

```bash
uv run pytest -q
uv run observatorio hallazgos notebooks/instantanea.csv /tmp/informe
uv run observatorio hallazgos notebooks/instantanea.csv /tmp/informe --huella 0000; echo $?
```

```
10 failed, 1098 passed
...
error: la huella de instantanea.csv es 3193779438eecdede9910a3cbc922f05a883e69a8a92fd4ef9a33e482d636c65, no 0000
1
```

### 7. Versión e imágenes

En `pyproject.toml`, `version = "0.30.0"`. En `compose.yaml`, las imágenes `local/observatorio:week-30-test`, `local/observatorio:week-30` y `local/observatorio:week-30-notebook`.

```bash
uv run pytest -q
```

```
6 failed, 1102 passed
```

Quedan los seis de `test_informe.py`: tu informe.

### 8. Tu informe

Genera los números con tu instantánea, **con las opciones por defecto** (las que usa `test_report_is_up_to_date`):

```bash
uv run observatorio hallazgos notebooks/instantanea.csv informe
```

Abre `informe/hallazgos.md` en la vista previa de VS Code y `informe/diferencias.svg` en el navegador. Lee la tabla con la teoría 02: primero el intervalo y la d, después el p corregido, y compara Welch con Mann-Whitney.

Después completa `informe/README.md`, debajo de tu pregunta, con esta plantilla. Cambia cada `<...>` por lo tuyo: `test_readme_has_no_placeholders` comprueba que no queda ninguno.

```markdown
[Hallazgos con todos los números](hallazgos.md) · [Notebook del análisis exploratorio](../notebooks/eda.ipynb)

## Datos

`notebooks/instantanea.csv`: <cuántas medidas, de qué carga y de qué fechas>, extraídas de PostgreSQL con `observatorio extraer`, huella `<la de EXPECTED en tu notebook>`. <Qué falta y dónde>. <De dónde salen: sensor, API, portal de datos abiertos; si son sintéticos o anonimizados>.

## Hallazgos

![<La conclusión, en una frase>](diferencias.svg)

1. **<Conclusión en negrita.>** <El número que la sostiene: diferencia, intervalo y d.>
2. **<...>** <...>

## Limitaciones

- <Lo que estos datos no permiten decir: ¿una sola carga? ¿qué variable de confusión no puedes descartar?>

## Siguientes pasos

- <Qué harías después, y qué hipótesis quedan abiertas para la fase 5.>
```

Dos o tres hallazgos bastan. Si no difiere ningún par, ese es tu primer hallazgo (teoría 01, sección 5): di qué diferencias podrías haber visto con tus datos, mirando la anchura de los intervalos.

Como referencia, el informe de ejemplo del bootcamp, con los datos sintéticos del starter:

```markdown
## Hallazgos

![Diferencia de medias de cada par de zonas, con su intervalo del 95 %](diferencias.svg)

1. **Ninguna zona difiere de otra.** Los diez intervalos del 95 % cruzan el cero, y ningún p corregido baja de 0,83.
2. **Las diferencias son pequeñas aunque fueran reales.** La mayor, Centro - Sur, es de -2,45 unidades en una escala de 0 a 80; su d de Cohen, -0,11, queda por debajo de lo que se considera un efecto pequeño (0,2).
3. **Welch y Mann-Whitney coinciden** en cada par: la conclusión no depende de suponer una campana.

## Limitaciones

- Una sola carga: no dice si las zonas difieren en otros días.
- Los valores que faltan se dejan fuera. Si faltaran más en una zona y por un motivo (por ejemplo, un sensor que falla con valores altos), las medias estarían sesgadas; aquí faltan por igual.
- Con unas 380 medidas por zona, una diferencia de menos de 3 unidades no se distingue del azar.
```

```bash
uv run pytest -q
```

```
1108 passed
```

Comprueba que el informe es reproducible: ejecuta `hallazgos` otra vez y mira `git status --short informe/`. No cambia nada: los mismos datos dieron los mismos bytes.

### 9. Una prueba de mutación, y tus tests

Haz cada cambio, **uno cada vez**, ejecuta `uv run pytest -x -q tests/test_findings.py tests/test_my_findings.py` y deshazlo con `git checkout <archivo>`:

| Archivo | Mutante | ¿Lo detectan? |
|---|---|---|
| `findings.py` | `digest != expected` por `digest == expected` | |
| `findings.py` | `keep_default_na=False` por `keep_default_na=True` | |
| `findings.py` | `dtype={"etiqueta": "str", "valor": "float64"}` por `dtype={"valor": "float64"}` | |
| `findings.py` | `distinct >= 2` por `distinct >= 1` | |
| `findings.py` | `method="bh"` por `method="by"` | |
| `findings.py` | quita `.dropna()` de `samples` | |
| `findings.py` | `finding.p_adjusted < alpha` por `<=` en `headline` | |
| `findings.py` | `xerr=[below, above]` por `xerr=[above, below]` | |
| `findings.py` | en `cell`, quita el `.replace(...)`: `return label` | |
| `findings.py` | `if left_out:` por `if False:` | |
| `cli.py` | en `hallazgos`, `read_snapshot(instantanea, huella)` por `read_snapshot(instantanea)` | |
| `cli.py` | en `hallazgos`, quita `alpha=alfa` de `render` | |

Los doce mueren. Mira **qué** test mata cada uno. Dos preguntas para el *pull request*:

- Con el de `xerr`, ¿qué test falla? En `finding()`, el intervalo de prueba **no** está centrado en la diferencia (−5,00 y −0,25 alrededor de −2,50). ¿Por qué con un intervalo de Welch de verdad este mutante no cambiaría el dibujo, y por qué aun así merece un test?
- Con el de `distinct >= 1`, ¿qué test falla? ¿Qué le pasaría a `hallazgos` con tu instantánea si una etiqueta de tu dominio tuviera una sola medida?

Después, en `tests/test_my_findings.py`, sustituye el ejemplo por **al menos 6 tests** tuyos, con las etiquetas y los valores de tu dominio y las funciones de `test_findings.py` (`frame_of`, `write`, `finding`). Ideas:

- dos etiquetas de tu dominio muy distintas, que difieren, y dos casi iguales, que no;
- una etiqueta de tu dominio con un solo valor, que queda fuera y aparece en "Sin comparar";
- la figura con tu unidad en el eje;
- una etiqueta de tu dominio con un carácter raro (`|`, comillas, tildes) en la tabla;
- `hallazgos --huella` con la huella de tu instantánea, y con otra;
- que con tu instantánea, `compare_all` dé tantos pares como k·(k−1)/2 con tus k etiquetas comparables.

Haz que cada uno falle una vez, con un mutante, antes de darlo por bueno. Al final, al menos 1260 tests en verde.

### 10. README y pull request

En el `README.md` de tu repositorio, añade una sección "Informe": cómo regenerarlo, el enlace a `informe/README.md`, y tu hallazgo principal en una frase.

Commits sugeridos, en este orden (el primero ya lo hiciste en el paso 4):

1. `docs: state the question of the report`
2. `test: add findings and report tests`
3. `feat: add findings module`
4. `feat: add hallazgos command`
5. `chore: bump version to 0.30.0`
6. `docs: add findings report`
7. `test: add my findings tests`

```bash
git push -u origin week-30
gh pr create --fill
gh pr checks --watch
```

En GitHub, el *pull request* `week-30` → `main` con:

1. La salida de `uv run pre-commit run --all-files`, `uv run coverage report` y `uv run alembic check`, y la CI en verde.
2. La salida de `hallazgos` y el enlace a `informe/README.md` en tu rama: GitHub lo muestra con la figura.
3. El enlace al commit de tu pregunta: su hora, anterior a la de `docs: add findings report`.
4. La tabla de mutantes del paso 9 y las respuestas a sus dos preguntas.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ModuleNotFoundError: No module named 'observatorio.core.findings'` | Falta el paso 5, o el archivo no está en `src/observatorio/core/` |
| `AttributeError: module 'scipy.stats' has no attribute 'false_discovery_control'` | Tu SciPy es anterior a 1.11: `uv sync` con el `uv.lock` del proyecto |
| `test_compare_all_corrects_with_benjamini_hochberg` falla | Corriges cada p por separado, o con `method="by"`: pasa la lista entera con `method="bh"` |
| `test_importing_the_cli_does_not_load_pandas` falla | Importaste `findings` arriba de `cli.py`: va dentro de `hallazgos` |
| `test_report_is_up_to_date` falla | Cambiaste la instantánea o `findings.py` sin regenerar, o lo generaste con `--confianza` o `--alfa`: ejecuta `hallazgos` sin opciones y mira `git diff informe/` |
| `test_readme_cites_the_digest_of_the_notebook` falla | La huella del README no es la de `EXPECTED` en tu notebook: cópiala de ahí |
| `test_readme_has_no_placeholders` falla | Queda un `<...>` de la plantilla, o un `TODO` |
| `test_readme_has_the_sections_of_a_report_in_order` falla | Una sección falta, cambia de nombre o va en otro orden: `## Pregunta`, `## Datos`, `## Hallazgos`, `## Limitaciones`, `## Siguientes pasos` |
| `hallazgos` sale con `hacen falta dos etiquetas con valores que varíen` | Tu instantánea tiene una sola etiqueta con valores distintos: extrae una carga con varias |
| La figura no se ve en GitHub | El enlace es relativo a `informe/` y distingue mayúsculas: `diferencias.svg`, sin carpeta delante |

## Entrega

1. Rama `week-30` con `core/findings.py`, el comando `hallazgos`, la carpeta `informe/` de tu dominio, las imágenes `week-30`, la versión `0.30.0` y al menos 6 tests tuyos en `test_my_findings.py`.
2. Todo en verde en tu máquina (`pre-commit run --all-files`, `pytest`, `coverage report`, `alembic check`), en Docker (`docker compose run --rm app`) y en GitHub Actions.
3. `README.md` con la sección "Informe".
4. *Pull request* `week-30` → `main` con lo que pide el paso 10.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 04 · Un informe desde el código](../2-practicas/ejercicio-04-un-informe-desde-el-codigo/README.md) | **Proyecto · El informe de tu dominio** | [Webgrafía](../4-recursos/webgrafia/README.md) |
