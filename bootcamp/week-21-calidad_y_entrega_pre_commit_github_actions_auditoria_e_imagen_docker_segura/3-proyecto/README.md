# Proyecto — Observatorio, capa 20: calidad y entrega

⏱️ 6 h 30 min · Capa 20 del [proyecto hilo conductor](../../../docs/proyecto-hilo-conductor.md). **Único entregable de la semana.**

## Qué construyes

Tu Observatorio funciona, tiene más de 700 tests y sirve una API. Pero sus comprobaciones dependen de que te acuerdes de ejecutarlas, sus versiones fijadas envejecen sin que nadie mire, y su imagen de Docker lleva de todo: uv, pip, pytest, el código fuente, y se ejecuta con permisos de escribir en sí misma. Esta semana preparas la **entrega**: lo que pasa entre tu commit y lo que se despliega.

```
$ git commit -m "feat: add label"
ruff check...............................................................Passed
ruff format..............................................................Passed
mypy.....................................................................Failed
- hook id: mypy
- exit code: 1

src/observatorio/cli.py:500: error: Incompatible return value type (got "float", expected "str")  [return-value]
```

```
$ gh pr checks
image	pass	46s	https://github.com/<tú>/python-<nombre>-<apellido>/actions/runs/...
quality	pass	19s	...
tests	pass	47s	...
```

| Pieza | Qué hace |
|---|---|
| `.pre-commit-config.yaml` | Antes de cada commit: espacios, YAML, TOML, archivos grandes, claves privadas, ruff, mypy y `uv.lock` al día |
| `.github/workflows/ci.yml` | En cada *push* a `main` y en cada *pull request*, tres jobs: `quality`, `tests` (con PostgreSQL) e `image` (con Trivy) |
| `.github/dependabot.yml` | Un *pull request* por cada versión nueva de tus paquetes, acciones e imágenes, tras 7 días |
| `Dockerfile` | Cuatro etapas: `uv`, `builder`, `test` y `runtime`, la imagen pequeña y sin root que se despliega |
| `compose.yaml` | `app` con la etapa `test`; `api` con `runtime`, en solo lectura, sin capacidades |

```
.github/
├── dependabot.yml          # nuevo
└── workflows/
    └── ci.yml              # nuevo
.pre-commit-config.yaml     # nuevo
Dockerfile                  # reescrito: cuatro etapas
compose.yaml                # modificado: un target por servicio, api endurecido
tests/
├── test_delivery.py        # nuevo: los tests del bootcamp, sobre la configuración
├── test_my_delivery.py     # nuevo: los tuyos
└── test_package.py         # modificado: las dependencias nuevas y 0.21.0
```

`src/` **no cambia**, salvo la versión. Esta semana el código es la configuración, y la configuración también tiene tests.

## Dónde trabajas

En **tu repositorio** `python-<nombre>-<apellido>`, en una rama nueva `week-21`. El `starter/` trae la capa 19 resuelta. **Tú** escribes la configuración de la entrega.

Necesitas `gh` con tu sesión iniciada (`gh auth status`), como en el ejercicio 02.

## Pasos

### 1. Rama de la semana

Comprueba que el *pull request* `week-20` está fusionado en `main`. Después:

```bash
cd ~/proyectos/python-<nombre>-<apellido>
git switch main
git pull
git switch -c week-21
```

### 2. Copia los archivos nuevos

```bash
STARTER=<ruta-al-bootcamp>/bootcamp/week-21-calidad_y_entrega_pre_commit_github_actions_auditoria_e_imagen_docker_segura/3-proyecto/starter
cp $STARTER/tests/test_delivery.py $STARTER/tests/test_my_delivery.py $STARTER/tests/test_package.py tests/
git status --short
```

- **Nuevos:**
  - `tests/test_delivery.py`, con 48 tests sobre la configuración de la entrega;
  - `tests/test_my_delivery.py`, con un ejemplo.
- **Modificado:** `test_package.py`, que espera las dependencias de desarrollo nuevas y la versión `0.21.0`.

### 3. Dependencias y tests en rojo

```bash
docker compose up -d --wait db
uv run pytest
```

```
E   ModuleNotFoundError: No module named 'yaml'
...
!!!!!!!!!!!!!!!!!!! Interrupted: 2 errors during collection !!!!!!!!!!!!!!!!!!!!
```

Los tests leen YAML con PyYAML. Añade las tres dependencias de desarrollo, con la versión fijada (`docs/stack-versions.md`):

```bash
uv add --dev pre-commit==4.7.0 pyyaml==6.0.3 types-pyyaml==6.0.12.20260906
uv run pytest
```

```
47 failed, 661 passed
```

- `pre-commit` trae `cfgv`, `identify`, `nodeenv` y `virtualenv` (con `distlib`, `filelock` y `platformdirs`);
- `pyyaml` ya venía con pre-commit, pero tus tests lo importan: se declara lo que se importa;
- `types-pyyaml` son las anotaciones de tipos de PyYAML, que no trae las suyas: sin ellas, `mypy --strict` dice `Library stubs not installed for "yaml"`.

Lee `tests/test_delivery.py` antes de escribir nada (teoría 01, sección 7). Fíjate en:

- `read_yaml`, que comprueba que el archivo es un diccionario;
- `triggers()`, que busca `on` **y** `True` (la trampa de YAML 1.1);
- `stages()`, que parte el `Dockerfile` en etapas y une las líneas que acaban en `\`;
- `SHA` y `DIGEST`, las dos expresiones regulares de lo que es "fijado".

De los 47 en rojo, 46 son de `test_delivery.py` (todo lo que aún no existe) y uno es la versión.

### 4. Los ganchos

Crea `.pre-commit-config.yaml` en la raíz:

```yaml
# Qué: las comprobaciones que corren solas antes de cada `git commit`.
# Para qué: que un error de formato, de tipos o un uv.lock desfasado no llegue al commit.
# Impacto: si una falla, el commit no se hace; arreglas, vuelves a añadir y repites.
repos:
  # Ganchos genéricos. `rev` es el SHA del commit de la etiqueta, no la etiqueta: una
  # etiqueta se puede mover, un SHA no. El comentario dice a qué versión corresponde.
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: 3e8a8703264a2f4a69428a0aa4dcb512790b2c8c  # frozen: v6.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-toml
      - id: check-added-large-files
      - id: detect-private-key

  # Ganchos locales: usan las herramientas de tu proyecto, con las versiones de uv.lock.
  # Así ruff y mypy son los mismos en el gancho, en tu terminal y en la CI.
  - repo: local
    hooks:
      - id: ruff-check
        name: ruff check
        entry: uv run --locked ruff check --fix
        language: unsupported
        types: [python]
      - id: ruff-format
        name: ruff format
        entry: uv run --locked ruff format
        language: unsupported
        types: [python]
      # mypy revisa el proyecto entero ([tool.mypy] files), no solo los archivos del
      # commit: un cambio en un archivo puede romper los tipos de otro.
      - id: mypy
        name: mypy
        entry: uv run --locked mypy
        language: unsupported
        types: [python]
        pass_filenames: false
      - id: uv-lock
        name: uv.lock al día
        entry: uv lock --check
        language: unsupported
        files: ^(pyproject\.toml|uv\.lock)$
        pass_filenames: false
```

Instálalo y pásalo por **todos** los archivos (teoría 02):

```bash
uv run pre-commit install
uv run pre-commit run --all-files
```

```
pre-commit installed at .git/hooks/pre-commit
[INFO] Initializing environment for https://github.com/pre-commit/pre-commit-hooks.
[INFO] Installing environment for https://github.com/pre-commit/pre-commit-hooks.
[INFO] Once installed this environment will be reused.
[INFO] This may take a few minutes...
trim trailing whitespace.................................................Passed
fix end of files.........................................................Failed
- hook id: end-of-file-fixer
- exit code: 1
- files were modified by this hook

Fixing migrations/README

check yaml...............................................................Passed
check toml...............................................................Passed
check for added large files..............................................Passed
detect private key.......................................................Passed
ruff check...............................................................Passed
ruff format..............................................................Passed
mypy.....................................................................Passed
uv.lock al día...........................................................Passed
```

`alembic init` dejó `migrations/README` sin salto de línea final (semana 19). Guarda ese arreglo en su propio commit, para que no se mezcle con lo demás. Si tus archivos tienen más espacios o finales de línea, `pre-commit` los arreglará también: revísalos con `git diff` y van en el mismo commit.

```bash
uv run pre-commit run --all-files
uv run pytest
```

```
37 failed, 671 passed
```

### 5. El gancho, en acción

Rompe algo a propósito, para verlo funcionar en tu proyecto: en `src/observatorio/cli.py`, añade al final una función que mienta sobre su tipo:

```python
def broken() -> str:
    return 1.5
```

```bash
git add src/observatorio/cli.py
git commit -m "test: try the hooks"
```

```
...
mypy.....................................................................Failed
- hook id: mypy
- exit code: 1

src/observatorio/cli.py:500: error: Incompatible return value type (got "float", expected "str")  [return-value]
Found 1 error in 1 file (checked 65 source files)
```

No hay commit. Deshazlo: `git restore --staged src/observatorio/cli.py && git restore src/observatorio/cli.py`.

### 6. El `Dockerfile`, en cuatro etapas

Sustituye tu `Dockerfile` por este (teoría 05). Lee cada comentario:

```dockerfile
# Cuatro etapas: `uv` y `builder` preparan, `test` ejecuta los tests y `runtime` es la
# imagen que se despliega. Cada imagen base, fijada por su digest (sha256): la etiqueta
# dice qué versión es, el digest garantiza que es exactamente esa imagen.

# Etapa 1: de esta imagen solo se toma el binario de uv.
FROM ghcr.io/astral-sh/uv:0.13.7@sha256:96f40d3904aad8d0bd010539001d36c8e2188b981e1334471a90c4a1d93bb490 AS uv

# Etapa 2: instala tu programa y sus dependencias, sin las de desarrollo, en /opt/venv.
FROM python:3.14.10-slim-trixie@sha256:9aaa474097d094040649f2162a627c0049b408f52138d980916788d80f04802f AS builder

COPY --from=uv /uv /bin/

# UV_PYTHON_DOWNLOADS=never: usar el Python de la imagen, nunca descargar otro.
# UV_PROJECT_ENVIRONMENT: el entorno vive en /opt/venv, que es lo que copia `runtime`.
# UV_COMPILE_BYTECODE=1: compila a .pyc al instalar; en `runtime` nadie podrá escribirlos.
# UV_LINK_MODE=copy: archivos copiados, no enlaces a la caché de uv, que no se copia.
ENV UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

# Primero solo las dependencias: esta capa se reutiliza mientras no cambie uv.lock.
COPY pyproject.toml uv.lock .python-version README.md ./
RUN uv sync --locked --no-dev --no-install-project

# Después tu paquete. --no-editable lo copia dentro de /opt/venv: el entorno ya no
# necesita la carpeta src.
COPY src ./src
RUN uv sync --locked --no-dev --no-editable

# Etapa 3: los tests, con las dependencias de desarrollo. `docker compose run app`.
FROM builder AS test

# PATH: python, pytest y observatorio se usan sin `uv run`.
# PYTEST_ADDOPTS y HYPOTHESIS_STORAGE_DIRECTORY: nada se escribe en /app.
ENV PATH="/opt/venv/bin:$PATH" \
    PYTEST_ADDOPTS="-p no:cacheprovider" \
    HYPOTHESIS_STORAGE_DIRECTORY=/tmp/hypothesis

COPY . .
RUN uv sync --locked

RUN useradd --create-home --uid 10001 app
USER 10001:10001

CMD ["pytest"]

# Etapa 4, la última: lo que se ejecuta en producción, y lo que construye
# `docker build .` sin --target. Solo Python y /opt/venv: ni uv, ni las herramientas de
# desarrollo, ni los tests, ni el código fuente.
FROM python:3.14.10-slim-trixie@sha256:9aaa474097d094040649f2162a627c0049b408f52138d980916788d80f04802f AS runtime

COPY --from=builder /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

# Tres arreglos en una capa:
# - apt-get upgrade: los parches de seguridad de Debian publicados después de la imagen
#   base (el digest la congela, también con sus fallos);
# - fuera pip: en producción nadie instala nada, y pip trae sus propias dependencias
#   dentro (urllib3, msgpack...), cada una con sus avisos;
# - un usuario sin privilegios, por número: si alguien explota tu programa, no es root,
#   y quien ejecute la imagen puede comprobarlo sin buscar el nombre.
RUN apt-get update \
    && apt-get upgrade --yes \
    && rm -rf /var/lib/apt/lists/* \
        /usr/local/bin/pip* \
        /usr/local/lib/python3.14/site-packages/pip \
        /usr/local/lib/python3.14/site-packages/pip-*.dist-info \
    && useradd --no-create-home --shell /usr/sbin/nologin --uid 10001 app
USER 10001:10001

EXPOSE 8000

CMD ["observatorio", "servir", "--host", "0.0.0.0"]
```

Los digests son los de `docs/stack-versions.md`. Para comprobar uno:

```bash
docker buildx imagetools inspect python:3.14.10-slim-trixie | grep Digest
```

```
Digest:    sha256:9aaa474097d094040649f2162a627c0049b408f52138d980916788d80f04802f
```

```bash
uv run pytest
```

```
26 failed, 682 passed
```

### 7. `compose.yaml`: un *target* por servicio

En `compose.yaml`, añade el digest a la imagen de `db` (`postgres:18.6-alpine@sha256:123b17998ccaf47e53b502e8c6a1e79afd8f579c6f3eec83c563da026f957395`) y cambia `app` y `api` hasta que queden así (de `api`, lo de debajo de `security_opt` no cambia):

```yaml
  app:
    # La etapa `test` del Dockerfile: con las dependencias de desarrollo y los tests.
    build:
      context: .
      target: test
    image: local/observatorio:week-21-test
    environment:
      # Dentro de la red de compose, PostgreSQL se llama `db`, no 127.0.0.1.
      OBSERVATORIO_DATABASE_URL: postgresql+psycopg://observatorio:observatorio@db:5432/observatorio
      OBSERVATORIO_TEST_DATABASE_URL: postgresql+psycopg://observatorio:observatorio@db:5432/observatorio_test
    depends_on:
      db:
        condition: service_healthy

  api:
    # La etapa `runtime`: la imagen pequeña, sin uv ni herramientas de desarrollo, cuya
    # orden ya es servir en 0.0.0.0.
    build:
      context: .
      target: runtime
    image: local/observatorio:week-21
    # Nada en la imagen se puede modificar mientras corre, salvo /tmp, que vive en
    # memoria y se pierde al parar.
    read_only: true
    tmpfs:
      - /tmp
    # Sin capacidades especiales de Linux (cambiar de usuario, abrir puertos bajos...)
    # y sin poder ganar privilegios nuevos, aunque haya un programa setuid en la imagen.
    cap_drop:
      - ALL
    security_opt:
      - no-new-privileges:true
    ...
```

`api` ya no necesita `command`: `runtime` sirve por defecto. Cambia también el comentario de arriba del archivo, que hablaba de una sola imagen.

```bash
uv run pytest
```

```
21 failed, 687 passed
```

### 8. La CI: `.github/workflows/ci.yml`

```yaml
# Qué: la integración continua del Observatorio. GitHub la ejecuta en cada push a main y
# en cada pull request.
# Para qué: que las mismas comprobaciones que haces en tu máquina las haga una máquina
# limpia, sin nada instalado a mano, y que el resultado se vea en el pull request.
name: CI

on:
  push:
    branches: [main]
  pull_request:

# El token de GitHub de cada job solo puede leer el repositorio. Nadie lo necesita para
# más, y si un paso se ve comprometido, no puede escribir en él.
permissions:
  contents: read

# Un push nuevo a la misma rama cancela la ejecución anterior, que ya no interesa.
concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true

# Todos los `uv sync` y `uv run` fallan si uv.lock no corresponde a pyproject.toml,
# como `--locked`: la CI prueba exactamente lo que fijaste.
env:
  UV_LOCKED: "1"

jobs:
  quality:
    runs-on: ubuntu-24.04
    timeout-minutes: 10
    steps:
      # Cada acción, fijada al SHA de su commit; el comentario dice la versión.
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
        with:
          persist-credentials: false
      - uses: astral-sh/setup-uv@07a047e608db84b3d8c06cd9a7c7dcc9c355c18e # v10.3.2
        with:
          version: "0.13.7"
      - run: uv sync
      - run: uv run pre-commit run --all-files --show-diff-on-failure
      - run: uv audit --preview-features audit-command

  tests:
    runs-on: ubuntu-24.04
    timeout-minutes: 15
    # Un PostgreSQL de verdad, como el de compose.yaml, en 127.0.0.1:5432 del runner.
    services:
      db:
        image: postgres:18.6-alpine@sha256:123b17998ccaf47e53b502e8c6a1e79afd8f579c6f3eec83c563da026f957395
        env:
          POSTGRES_USER: observatorio
          POSTGRES_PASSWORD: observatorio
          POSTGRES_DB: observatorio
        ports:
          - 5432:5432
        options: >-
          --health-cmd "pg_isready -U observatorio -d observatorio"
          --health-interval 2s --health-timeout 5s --health-retries 15
    env:
      OBSERVATORIO_DATABASE_URL: postgresql+psycopg://observatorio:observatorio@127.0.0.1:5432/observatorio
      # En GitHub Actions (GITHUB_ACTIONS=true), Typer fuerza los colores de Rich y la
      # ayuda sale llena de códigos ANSI que rompen los tests de la CLI. TERM=dumb los
      # quita. Lo reproduces en tu máquina con `GITHUB_ACTIONS=true uv run pytest`.
      TERM: dumb
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
        with:
          persist-credentials: false
      - uses: astral-sh/setup-uv@07a047e608db84b3d8c06cd9a7c7dcc9c355c18e # v10.3.2
        with:
          version: "0.13.7"
      - run: uv sync
      - run: uv run coverage run -m pytest
      - run: uv run coverage report
      - run: uv run alembic upgrade head
      - run: uv run alembic check

  image:
    runs-on: ubuntu-24.04
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
        with:
          persist-credentials: false
      - run: docker build --target runtime --tag observatorio:ci .
      - run: docker run --rm observatorio:ci observatorio --version
      # Trivy busca vulnerabilidades conocidas en los paquetes del sistema y de Python de
      # la imagen. Falla (exit 1) si hay alguna HIGH o CRITICAL con arreglo publicado.
      - run: >-
          docker run --rm -v /var/run/docker.sock:/var/run/docker.sock
          aquasec/trivy:0.76.1@sha256:790fd66d1697395d8693d1acaa1ea702406a20f109b6fc7bac8db623eca6c06c
          image --exit-code 1 --severity HIGH,CRITICAL --ignore-unfixed observatorio:ci
```

Fíjate (teoría 03):

- `quality` ejecuta **los mismos ganchos** que tu commit, sobre todos los archivos, y audita las dependencias;
- `tests` arranca el **mismo PostgreSQL** que `compose.yaml` (un test lo comprueba) en `127.0.0.1:5432`, la URL por defecto de `db_fixtures.py`;
- `image` construye `runtime`, comprueba que arranca y la escanea;
- `TERM: dumb`: sin él, cinco tests de la CLI fallan **solo** en GitHub (teoría 01, sección 6). Reprodúcelo antes de creerlo:

  ```bash
  GITHUB_ACTIONS=true uv run pytest -q tests/test_cli.py tests/test_batch.py tests/test_api.py
  GITHUB_ACTIONS=true TERM=dumb uv run pytest -q tests/test_cli.py tests/test_batch.py tests/test_api.py
  ```

Revísalo con actionlint, como en el ejercicio 02:

```bash
docker run --rm -v "$PWD":/repo -w /repo rhysd/actionlint:1.7.12@sha256:b1934ee5f1c509618f2508e6eb47ee0d3520686341fec936f3b79331f9315667
uv run pytest
```

```
4 failed, 704 passed
```

### 9. Dependabot: `.github/dependabot.yml`

```yaml
# Qué: Dependabot abre un pull request cuando sale una versión nueva de lo que fijaste.
# Para qué: tus versiones están fijadas, así que nadie las actualiza si no lo pide alguien.
# Impacto: cada pull request pasa por la CI antes de que lo fusiones; `cooldown` espera
# 7 días desde la publicación, como haces tú al fijar versiones (docs/stack-versions.md).
version: 2
updates:
  - package-ecosystem: uv
    directory: /
    schedule:
      interval: weekly
    cooldown:
      default-days: 7
  - package-ecosystem: github-actions
    directory: /
    schedule:
      interval: weekly
    cooldown:
      default-days: 7
  - package-ecosystem: docker
    directory: /
    schedule:
      interval: weekly
    cooldown:
      default-days: 7
    # Dependabot no lee requires-python: propondría python:3.15 aunque tu proyecto pide
    # <3.15. Solo parches (3.14.x); el salto de versión lo decides tú.
    ignore:
      - dependency-name: python
        update-types:
          - version-update:semver-major
          - version-update:semver-minor
```

```bash
uv run pytest
```

```
1 failed, 707 passed
```

Queda la versión.

### 10. La auditoría, en tu máquina

```bash
uv audit --preview-features audit-command
uv audit --preview-features audit-command --no-dev
```

```
Found no known vulnerabilities and no adverse project statuses in 61 packages
Found no known vulnerabilities and no adverse project statuses in 33 packages
```

Si te sale algún aviso, es que alguno es posterior a este README: léelo (teoría 04, sección 3) y actualiza el paquete en un commit aparte, `fix(deps): ...`. `--no-dev` audita solo lo que va a `runtime`: 33 de los 61 paquetes.

### 11. La versión

```bash
uv version --bump minor
uv run observatorio --version
uv run pytest
```

```
observatorio 0.21.0
...
708 passed
```

### 12. Construir de verdad, y medir

```bash
docker compose build app api
docker images local/observatorio
docker run --rm local/observatorio:week-21 id
docker run --rm local/observatorio:week-21 sh -c 'which uv pip pytest; ls /app'
```

```
uid=10001(app) gid=10001(app) groups=10001(app)
ls: cannot access '/app': No such file or directory
```

`which` no encuentra ninguna de las tres, y no hay `/app`: en `runtime` solo está Python y `/opt/venv`. Ahora, los tests en `app` y la API en `api`:

```bash
docker compose run --rm app
docker compose run --rm app alembic upgrade head
docker compose up -d --wait api
curl -s http://127.0.0.1:8000/health
docker compose exec api sh -c 'touch /opt/venv/x; grep -E "CapEff|NoNewPrivs" /proc/1/status'
docker compose stop api
```

```
{"status":"ok","version":"0.21.0"}
touch: cannot touch '/opt/venv/x': Read-only file system
CapEff:	0000000000000000
NoNewPrivs:	1
```

Escanea la imagen de la semana 20 y la nueva (teoría 05, sección 8):

```bash
TRIVY=aquasec/trivy:0.76.1@sha256:790fd66d1697395d8693d1acaa1ea702406a20f109b6fc7bac8db623eca6c06c
for image in local/observatorio:week-20 local/observatorio:week-21; do
  docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v trivycache:/root/.cache $TRIVY \
    image -q --severity HIGH,CRITICAL --ignore-unfixed $image | grep -E "Total|^│ [a-z]"
done
```

Y el gancho: cuánto tarda la primera vez (con la instalación de `pre-commit-hooks`) y las siguientes:

```bash
uv run pre-commit clean
time uv run pre-commit run --all-files
time uv run pre-commit run --all-files
```

Rellena la tabla para tu *pull request*. En la máquina del bootcamp:

| Medida | Semana 20 | Semana 21 |
|---|---|---|
| Imagen para servir | 718 MB | 301 MB (`runtime`) |
| Imagen para probar | 718 MB | 768 MB (`test`) |
| HIGH o CRITICAL con arreglo (Trivy) | 7 | 0 |
| Vulnerabilidades en total (Trivy, sin filtros) | 197 | 186 |
| Usuario en la imagen que sirve | uid 10001 | uid 10001, sin capacidades, solo lectura |
| `pre-commit run --all-files`, primera vez | — | 21 s |
| `pre-commit run --all-files`, siguientes | — | 6 s |
| CI en GitHub (`quality` · `tests` · `image`) | — | 19 s · 47 s · 46 s |

Las 186 que quedan son de Debian y no tienen arreglo publicado. Las de la semana 20 que sí lo tenían: `zlib1g` (Debian) y `msgpack`, `setuptools` y `urllib3`, los que pip lleva dentro.

### 13. Calidad y cobertura

```bash
uv run pre-commit run --all-files
uv run coverage run -m pytest -q && uv run coverage report
uv run alembic check
```

`pre-commit run --all-files` sustituye a `ruff check`, `ruff format --check` y `mypy`: los ejecuta todos. La cobertura no cambia, porque `src/` no cambia: `test_delivery.py` no ejecuta código de `observatorio`, lo lee.

### 14. Una prueba de mutación

Haz cada cambio, **uno cada vez**, ejecuta `uv run pytest tests/test_delivery.py tests/test_package.py -x -q` y deshazlo con `git checkout <archivo>`:

| Archivo | Mutante | ¿Lo detectan? |
|---|---|---|
| `.pre-commit-config.yaml` | `rev: <sha>  # frozen: v6.0.0` por `rev: v6.0.0` | |
| `.pre-commit-config.yaml` | quita `pass_filenames: false` de `mypy` | |
| `ci.yml` | `contents: read` por `contents: write` | |
| `ci.yml` | `pull_request:` por `pull_request_target:` | |
| `ci.yml` | `actions/checkout@<sha>` por `actions/checkout@v7.0.1` (solo el primero) | |
| `ci.yml` | `--exit-code 1` por `--exit-code 0` en Trivy | |
| `Dockerfile` | quita `--no-dev` del último `uv sync` de `builder` | |
| `Dockerfile` | quita `USER 10001:10001` de `runtime` | |
| `Dockerfile` | quita la línea `UV_COMPILE_BYTECODE=1 \` de `builder` | |
| `compose.yaml` | quita `read_only: true` de `api` | |

Nueve mueren. Uno **sobrevive**: ¿cuál, y por qué ningún test del bootcamp lo ve? Pista: la imagen funciona igual sin esa línea, pero ¿qué tiene que hacer Python al arrancar, si no encuentra los `.pyc` y no puede escribirlos? Constrúyela sin la línea y mide:

```bash
docker build --target runtime -t local/observatorio:sin-pyc .
for image in local/observatorio:week-21 local/observatorio:sin-pyc; do
  docker run --rm --read-only $image python -c "
import subprocess, time
start = time.perf_counter()
subprocess.run(['observatorio', '--version'], capture_output=True)
print(round(time.perf_counter() - start, 2))"
done
```

En la máquina del bootcamp, 1,33 s con los `.pyc` y 2,37 s sin ellos, **en cada arranque**: sin poder escribirlos, Python compila en memoria todo lo que importa, cada vez. Lo vas a matar en el paso siguiente.

### 15. Tus tests

En `tests/test_my_delivery.py`, sustituye el ejemplo por **al menos 6 tests** tuyos, con las funciones de `test_delivery.py` (`compose`, `stage`, `jobs`, `runs_of`, `read_yaml`...). Ideas:

- el mutante que sobrevivió en el paso 14: `UV_COMPILE_BYTECODE=1` en el `ENV` de `builder` (con `stage("builder").lines("ENV")`);
- que Trivy no falle por lo que no tiene arreglo: `--ignore-unfixed`;
- que `api` espera a que `db` esté sana y tiene su *healthcheck*;
- que `.dockerignore` deja fuera `.venv/` y las cachés;
- que en `ci.yml` no hay ningún `secrets.`;
- que `tests` e `image` no tardan más de 15 minutos.

Haz que cada uno falle una vez, con un mutante, antes de darlo por bueno. Al final, al menos 815 tests en verde.

### 16. GitHub, README y pull request

Sube la rama y abre el *pull request*:

```bash
git push -u origin week-21
gh pr create --fill
gh pr checks --watch
```

```
image	pass	46s	...
quality	pass	19s	...
tests	pass	47s	...
```

Si algo sale en rojo, `gh run view --log-failed`, y el método de la teoría 01: leer, reproducir en local, arreglar.

Al fusionar, `dependabot.yml` llega a `main` y Dependabot empieza a trabajar: en unos minutos verás sus primeros *pull requests* (`gh pr list`). Revísalos uno a uno: la CI en verde, qué cambia, y fusiona o cierra. Si tu repositorio es público, añade en *Settings → Rules → Rulesets* una regla para `main` que exija *pull request* y los tres jobs en verde (teoría 01, sección 8).

En el `README.md` de tu repositorio, añade arriba la insignia de la CI:

```markdown
![CI](https://github.com/<usuario>/python-<nombre>-<apellido>/actions/workflows/ci.yml/badge.svg)
```

y una sección "Calidad y entrega": cómo instalar los ganchos (`uv run pre-commit install`), qué comprueba la CI y cómo construir cada imagen (`docker compose build app api`).

Commits sugeridos, en este orden:

1. `test: add delivery tests`
2. `build: add pre-commit and pyyaml`
3. `chore: add pre-commit hooks`
4. `style: fix end of files`
5. `build: split the image into builder, test and runtime stages`
6. `build: harden the api service`
7. `ci: add github actions workflow`
8. `ci: add dependabot`
9. `chore: bump version to 0.21.0`
10. `test: add my delivery tests`

Con los ganchos instalados, cada commit pasa por ellos. En GitHub, el *pull request* `week-21` → `main` con:

1. La salida de `uv run pre-commit run --all-files`, `uv run coverage report` y `uv run alembic check`, y el enlace a la ejecución de la CI en verde.
2. La tabla de medidas del paso 12.
3. La tabla de mutantes del paso 14, y el test con el que mataste al superviviente.
4. Por qué ruff y mypy son ganchos **locales**, y por qué cada acción va fijada a un SHA.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `ModuleNotFoundError: No module named 'yaml'` | Te falta el paso 3: `uv add --dev pre-commit==4.7.0 pyyaml==6.0.3 types-pyyaml==6.0.12.20260906` |
| `Library stubs not installed for "yaml"` en mypy | Falta `types-pyyaml` en `dev` |
| `test_each_pinned_rev_says_its_version` falla | Falta el comentario `# frozen: v6.0.0` detrás del SHA: `uv run pre-commit autoupdate --freeze` lo escribe |
| Un gancho falla con `files were modified by this hook` | Ya lo arregló: `git diff`, `git add` y otro commit |
| `Executable \`uv\` not found` en un gancho | El gancho busca `uv` en tu `PATH`: abre la terminal donde `uv --version` funciona |
| `failed to solve: target stage "runtime" could not be found` | El `Dockerfile` no tiene una etapa con `AS runtime`, o no es la tuya |
| `docker compose run --rm app` dice `Couldn't use data file '/app/.coverage'` | En el contenedor, `/app` no es escribible: `coverage` va en tu máquina, o con `-e COVERAGE_FILE=/tmp/.coverage` |
| `api` no arranca: `Read-only file system` | Algo intenta escribir fuera de `/tmp`: mira `docker compose logs api` |
| En GitHub, 5 tests de la CLI fallan con `\x1b[1m` | Falta `TERM: dumb` en el `env` del job `tests` |
| En GitHub, Trivy falla con HIGH `fixed` en paquetes de Debian | Debian publicó un parche después de tu digest: vuelve a construir (el `apt-get upgrade` lo aplica) o actualiza el digest |
| `gh pr create` dice `must first push the current branch` | `git push -u origin week-21` primero |

## Entrega

1. Rama `week-21` con los cinco archivos de configuración, `test_delivery.py`, `test_my_delivery.py` (al menos 6 tests tuyos), `test_package.py` y la versión `0.21.0`.
2. Todo en verde en tu máquina (`pre-commit run --all-files`, `pytest`, `coverage report`, `alembic check`), en Docker (`docker compose run --rm app`) y **en GitHub Actions**.
3. `README.md` con la insignia de la CI y la sección "Calidad y entrega".
4. *Pull request* `week-21` → `main` con lo que pide el paso 16.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 04 · Una imagen Docker segura](../2-practicas/ejercicio-04-una-imagen-docker-segura/README.md) | **Proyecto · Calidad y entrega del Observatorio** | [Rúbrica de la semana 21](../rubrica-evaluacion.md) |
