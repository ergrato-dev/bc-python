# Ejercicio 02 — Integración continua con GitHub Actions

⏱️ 1 h 30 min · Teoría previa: [01](../../1-teoria/01-de-tu-maquina-a-main-calidad-automatica.md) y [03](../../1-teoria/03-integracion-continua-con-github-actions.md)

## Objetivo

Que una máquina de GitHub, limpia, compruebe tu código en cada *push* y en cada *pull request*:

- escribir un **workflow** con un *job* y sus *steps*, y leer su registro;
- ejecutar los tests con **uv**, exactamente con las versiones de `uv.lock`;
- probar en **dos versiones de Python** con una matriz;
- ver un **pull request en rojo**, encontrar el fallo en el registro y ponerlo en verde;
- dejar el token en **solo lectura**, fijar las acciones a su **SHA** y revisar el workflow con **actionlint** antes de subirlo.

Ejercicio **guiado**: descomentas cada paso de `.github/workflows/ci.yml`, haces *push* y comparas lo que ves en GitHub. No se entrega.

## Antes de empezar

Necesitas una cuenta de GitHub y `gh` con tu sesión iniciada: `gh auth status` debe decir `Logged in to github.com`. Si no, `gh auth login`. Copia el `starter/` fuera del repositorio del bootcamp y pruébalo:

```bash
cp -r bootcamp/week-21-calidad_y_entrega_pre_commit_github_actions_auditoria_e_imagen_docker_segura/2-practicas/ejercicio-02-integracion-continua-con-github-actions/starter ~/practicas/semana-21/ej02
cd ~/practicas/semana-21/ej02
git init -b main
uv run python main.py
uv run pytest -q
```

```
Ejercicio 02 · Integración continua con GitHub Actions
Python 3.14.10
12.5 -> bajo
30.0 -> medio
55.1 -> alto
..                                                                       [100%]
2 passed in 0.01s
```

## Pasos

### 1. Un workflow, un job, cuatro pasos

Descomenta el **PASO 1** de `.github/workflows/ci.yml`. Crea un repositorio **privado** de práctica y súbelo:

```bash
git add .
git commit -m "ci: add hello workflow"
gh repo create practica-actions-semana-21 --private --source . --push
gh run watch
```

`gh run watch` te pregunta qué ejecución en curso seguir (solo hay una) y la sigue hasta el final:

```
✓ main CI · 42454241549
Triggered via push less than a minute ago

JOBS
✓ hello in 6s (ID 128649754455)
```

Mira el registro de cada paso, en la terminal (`gh run view --log`) o en la pestaña **Actions** de tu repositorio:

```
hola desde Linux, en la rama main
Python 3.12.3
...
.
..
.git
.github
.gitignore
.python-version
main.py
pyproject.toml
tests
uv.lock
```

Un **workflow** se dispara con un evento (`on: push`). Tiene **jobs**, y cada job corre en una máquina nueva (`runs-on: ubuntu-24.04`, el **runner**) y ejecuta sus **steps** en orden: `run` es una orden de bash; `uses` es una **acción**, un programa de otro repositorio. Sin `actions/checkout`, la máquina no tendría tu código. El Python del sistema es 3.12.3, no el tuyo: por eso el paso 2 usa uv.

### 2. Los tests, con uv

Descomenta el **PASO 2**, y:

```bash
git commit -am "ci: run the tests with uv"
git push
gh run watch
```

```
✓ hello in 4s (ID 128649853435)
✓ tests in 10s (ID 128649853630)
```

En el registro de `tests`:

```
Downloading cpython-3.14.10-linux-x86_64-gnu (download) (35.1MiB)
Using CPython 3.14.10
Creating virtual environment at: .venv
Resolved 8 packages in 0.79ms
...
 + pytest==9.2.0
 + ruff==0.17.3
...
All checks passed!
...
tests/test_main.py::test_low PASSED                                      [ 50%]
tests/test_main.py::test_medium PASSED                                   [100%]
```

`setup-uv` instala uv 0.13.7, y uv descarga el Python de `.python-version`. `--locked` hace que `uv sync` falle si `uv.lock` no corresponde a `pyproject.toml`: la CI prueba lo que fijaste, no lo último que haya salido. Los dos jobs corren **a la vez**, cada uno en su máquina.

### 3. Una matriz de versiones de Python

Descomenta el **PASO 3**: `strategy` y `env` son claves del job `tests`, como `steps`. Sube el cambio:

```bash
git commit -am "ci: test on python 3.13 and 3.14"
git push
gh run watch
```

```
✓ hello in 5s (ID 128649954213)
✓ tests (3.14) in 10s (ID 128649954466)
✓ tests (3.13) in 11s (ID 128649954507)
```

```
tests (3.14)   Using CPython 3.14.10
tests (3.13)   Using CPython 3.13.18
```

La **matriz** crea un job por valor: `${{ matrix.python }}` vale `"3.13"` en uno y `"3.14"` en el otro. `UV_PYTHON` le dice a uv qué Python usar, por encima de `.python-version`. Las versiones van **entre comillas**: en YAML, `3.10` sin comillas es el número 3.1.

### 4. Un pull request en rojo

Primero, que la CI corra también en los *pull requests*. En `on:`, cambia `push:` por:

```yaml
on:
  push:
    branches: [main]
  pull_request:
```

Con `branches: [main]`, un *push* a otra rama no dispara nada: para eso está su *pull request*. Guárdalo en `main` y abre una rama con un test nuevo, el **PASO 4** de `tests/test_main.py`:

```bash
git commit -am "ci: run on pull requests"
git push
git switch -c limite-alto
# descomenta el PASO 4 de tests/test_main.py
git commit -am "test: high starts at the limit"
git push -u origin limite-alto
gh pr create --fill
gh pr checks --watch
```

```
tests (3.13)	fail	8s	https://github.com/<tú>/practica-actions-semana-21/actions/runs/...
hello	pass	4s	...
tests (3.14)	fail	10s	...
```

En la página del *pull request*, abajo, verás las comprobaciones en rojo. ¿Qué falló? Sin abrir el navegador:

```bash
gh run view --log-failed
```

```
tests/test_main.py::test_high_starts_at_the_limit FAILED                 [100%]
    def test_high_starts_at_the_limit() -> None:
>       assert level(50.0) == "alto"
E       AssertionError: assert 'medio' == 'alto'
...
========================= 1 failed, 2 passed in 0.07s ==========================
```

Fíjate en `gh run view`: falló `tests (3.13)` y GitHub **canceló** `tests (3.14)` (`The strategy configuration was canceled because "tests._3_13" failed`). Es `fail-fast`, activado por defecto en una matriz: si una combinación falla, no gasta minutos en las demás.

El *docstring* de `level` dice "alto desde HIGH", y el código usa `>`. Arregla `main.py` (`if value >= HIGH:`) y sube el arreglo a la misma rama:

```bash
git commit -am "fix: high starts at HIGH"
git push
gh pr checks --watch
```

```
hello	pass	7s	...
tests (3.13)	pass	10s	...
tests (3.14)	pass	13s	...
```

Fusiona el *pull request* (`gh pr merge --squash --delete-branch`) y vuelve a `main`: `git switch main && git pull`.

### 5. Solo leer, una ejecución cada vez y acciones fijadas

Descomenta el **PASO 5**: `permissions` y `concurrency` van al final, sin sangría, porque son del workflow, no de un job. Después, a mano:

- cambia cada `uses: actions/checkout@v7.0.1` por `uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1`, y añade debajo `with:` y `persist-credentials: false` (tres líneas, con la sangría de `uses`);
- cambia `uses: astral-sh/setup-uv@v10.3.2` por `uses: astral-sh/setup-uv@07a047e608db84b3d8c06cd9a7c7dcc9c355c18e # v10.3.2`.

Antes de subirlo, revísalo con **actionlint**, sin instalar nada:

```bash
docker run --rm -v "$PWD":/repo -w /repo rhysd/actionlint:1.7.12@sha256:b1934ee5f1c509618f2508e6eb47ee0d3520686341fec936f3b79331f9315667
echo $?
```

```
0
```

Sin salida y con código 0: no encuentra nada. Ahora estropéalo a propósito: cambia `matrix.python` por `matrix.pyhton` y `ubuntu-24.04` por `ubuntu-24.4` en el job `tests`, y repite:

```
.github/workflows/ci.yml:31:14: label "ubuntu-24.4" is unknown. available labels are "windows-latest", ... [runner-label]
   |
31 |     runs-on: ubuntu-24.4
   |              ^~~~~~~~~~~
.github/workflows/ci.yml:52:22: property "pyhton" is not defined in object type {python: number} [expression]
   |
52 |       UV_PYTHON: ${{ matrix.pyhton }}
   |                      ^~~~~~~~~~~~~
```

GitHub habría aceptado el *push* y fallado después. Deshaz los dos errores, vuelve a pasar actionlint y sube:

```bash
git commit -am "ci: read-only token, pinned actions, one run at a time"
git push
gh run watch
```

Todo en verde, como antes, pero ahora (teoría 03):

- el token del workflow **solo puede leer** el repositorio;
- `actions/checkout` no deja ese token guardado en `.git/config` (en el registro del paso 1 viste `persist-credentials: true`, el valor por defecto);
- cada acción es **exactamente** el commit que revisaste: aunque alguien mueva la etiqueta `v7.0.1`, tu workflow no cambia;
- un *push* nuevo a la misma rama **cancela** la ejecución anterior.

Cuando termines, puedes borrar el repositorio de práctica: `gh repo delete practica-actions-semana-21`. gh te pide confirmación: borrar no se puede deshacer.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `gh: command not found` o `You are not logged into any GitHub hosts` | Instala `gh` y ejecuta `gh auth login`; o crea el repositorio en github.com y súbelo con `git remote add origin ...` y `git push -u origin main` |
| `push declined due to email privacy restrictions` | Tu `user.email` es el privado: usa el `...@users.noreply.github.com` de github.com/settings/emails (`git config user.email ...` y `git commit --amend --reset-author --no-edit`) |
| `found no in progress runs to watch` | GitHub tarda unos segundos en crear la ejecución: repite. Si ya terminó, `gh run list` y `gh run view`. Si no aparece ninguna, el archivo no está en `.github/workflows/` o el paso sigue comentado |
| `Invalid workflow file` en la pestaña Actions | YAML mal sangrado: pasa actionlint y compara la sangría con el comentario |
| ``error: The lockfile at `uv.lock` needs to be updated, but `--locked` was provided.`` | Cambiaste `pyproject.toml` sin `uv lock`: ejecútalo, haz commit de `uv.lock` y sube |
| El *pull request* no muestra comprobaciones | Te falta `pull_request:` en `on:`, o lo añadiste en la rama y no en `main` |
| actionlint dice `no project was found in any parent directories` | Ejecútalo en la carpeta del ejercicio, que tiene `.git` |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Ejercicio 01 · Ganchos de Git con pre-commit](../ejercicio-01-ganchos-con-pre-commit/README.md) | **Ejercicio 02 · Integración continua con GitHub Actions** | [Ejercicio 03 · Auditar dependencias](../ejercicio-03-auditar-dependencias/README.md) |
