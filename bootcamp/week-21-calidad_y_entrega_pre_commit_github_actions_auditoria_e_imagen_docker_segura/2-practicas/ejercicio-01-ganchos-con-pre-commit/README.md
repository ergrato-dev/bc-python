# Ejercicio 01 — Ganchos de Git con pre-commit

⏱️ 1 h 30 min · Teoría previa: [01](../../1-teoria/01-de-tu-maquina-a-main-calidad-automatica.md) y [02](../../1-teoria/02-ganchos-de-git-con-pre-commit.md)

## Objetivo

Hacer que Git compruebe tu código **antes** de cada commit, sin que tengas que acordarte:

- escribir un **gancho de Git a mano** y ver cómo para un commit;
- instalar **pre-commit** y sus ganchos genéricos, que **arreglan** archivos solos;
- añadir **ganchos locales** con ruff y mypy, con las versiones de tu `uv.lock`;
- ver cómo un gancho detecta un `uv.lock` desfasado;
- saltarte un gancho cuando toca (`SKIP`, `--no-verify`) y fijar los ganchos a un **SHA** con `autoupdate --freeze`.

Ejercicio **guiado**: descomentas cada paso de `.pre-commit-config.yaml` y de `main.py`, haces commit y comparas. No se entrega.

## Antes de empezar

pre-commit trabaja sobre un repositorio de Git propio. Copia el `starter/` **fuera** del repositorio del bootcamp (si no, quedaría un repositorio dentro de otro):

```bash
mkdir -p ~/practicas/semana-21
cp -r bootcamp/week-21-calidad_y_entrega_pre_commit_github_actions_auditoria_e_imagen_docker_segura/2-practicas/ejercicio-01-ganchos-con-pre-commit/starter ~/practicas/semana-21/ej01
cd ~/practicas/semana-21/ej01
git init -b main
uv run python main.py
```

```
Initialized empty Git repository in /home/<tú>/practicas/semana-21/ej01/.git/
...
Ejercicio 01 · Ganchos de Git con pre-commit
media: 16.666666666666668
```

`uv` instala `pre-commit`, `ruff` y `mypy`, con las versiones de `uv.lock`. Mira también `notas.txt`: tiene espacios al final de la primera línea y le falta el salto de línea final. Lo notarás en el paso 2.

## Pasos

### 1. Un gancho a mano

Un gancho es un programa en `.git/hooks/` con un nombre que Git conoce. Si `pre-commit` termina con un código distinto de 0, Git no hace el commit. Escribe uno que siempre falla:

```bash
cat > .git/hooks/pre-commit <<'EOF'
#!/bin/sh
echo "gancho: vas a guardar $(git diff --cached --name-only | wc -l) archivos"
exit 1
EOF
chmod +x .git/hooks/pre-commit
git add .
git commit -m "chore: first commit"
echo $?
```

```
gancho: vas a guardar 7 archivos
1
```

Git ejecutó el gancho, el gancho dijo que no (`exit 1`) y no hay commit: `git log` dice `does not have any commits yet`. Ahora sáltatelo:

```bash
git commit --no-verify -m "chore: first commit"
git log --oneline
rm .git/hooks/pre-commit
```

`--no-verify` no ejecuta el gancho. Por eso un gancho es una **ayuda** para ti, no una garantía para el equipo: la garantía es la CI (ejercicio 02). Y `.git/hooks/` no viaja con `git push`: cada persona tendría que copiarse el script. pre-commit resuelve las dos cosas que sí se pueden resolver: la configuración vive en el repositorio y cada uno la instala con un comando.

### 2. pre-commit y sus ganchos genéricos

Descomenta el **PASO 2** de `.pre-commit-config.yaml` e instala el gancho:

```bash
uv run pre-commit install
uv run pre-commit run --all-files
echo $?
```

```
pre-commit installed at .git/hooks/pre-commit
[INFO] Initializing environment for https://github.com/pre-commit/pre-commit-hooks.
[INFO] Installing environment for https://github.com/pre-commit/pre-commit-hooks.
[INFO] Once installed this environment will be reused.
[INFO] This may take a few minutes...
trim trailing whitespace.................................................Failed
- hook id: trailing-whitespace
- exit code: 1
- files were modified by this hook

Fixing notas.txt

fix end of files.........................................................Failed
- hook id: end-of-file-fixer
- exit code: 1
- files were modified by this hook

Fixing notas.txt

check yaml...............................................................Passed
check toml...............................................................Passed
check for added large files..............................................Passed
1
```

`install` escribe su propio `.git/hooks/pre-commit`, que lee la configuración. La primera vez, pre-commit **clona** `pre-commit-hooks` en la etiqueta `v6.0.0` y le prepara un entorno de Python (en `~/.cache/pre-commit`); las siguientes lo reutiliza.

Dos ganchos dicen `Failed` pero **ya arreglaron** `notas.txt`: son *fixers*. Fallan para que mires el cambio antes de guardarlo. Míralo y repite:

```bash
git diff notas.txt
uv run pre-commit run --all-files
git add .
git commit -m "chore: add pre-commit"
```

Ahora todo dice `Passed`, y en el commit `check toml` dice `(no files to check)Skipped`: `git commit` solo pasa a los ganchos los archivos del commit, y en este no hay ningún `.toml`. `--all-files` los pasa todos: es lo que usarás en la CI.

### 3. ruff, con la versión de `uv.lock`

Descomenta el **PASO 3** de `.pre-commit-config.yaml` y el **PASO 3** de `main.py`, y ejecuta:

```bash
uv run python main.py
git add .
git commit -m "feat: add double"
```

```
...
doble: 42.0
...
ruff check...............................................................Failed
- hook id: ruff-check
- files were modified by this hook

Found 1 error (1 fixed, 0 remaining).

ruff format..............................................................Failed
- hook id: ruff-format
- files were modified by this hook

1 file reformatted
```

El programa funciona, pero el commit no se hace. `ruff check --fix` quitó `import math`, que nadie usa, y `ruff format` reescribió `def  double( value:float )->float :`. Míralo:

```bash
git status --short
git diff main.py
```

```
M  .pre-commit-config.yaml
MM main.py
```

`MM`: hay una versión de `main.py` en el *stage* (la tuya, la del `git add`) y otra en tu carpeta (la arreglada). Añade la arreglada y repite el commit: ahora pasa.

Estos ganchos son **locales** (`repo: local`): `entry` es una orden de tu proyecto, `uv run --locked ruff`, con la versión de `uv.lock`. Es la misma ruff que usas en la terminal y la que usará la CI. `language: unsupported` le dice a pre-commit que no prepare ningún entorno: la orden ya funciona tal cual (antes se llamaba `system`).

### 4. Un error que solo ve mypy

Descomenta el **PASO 4** de los dos archivos y ejecuta:

```bash
uv run python main.py
git add .
git commit -m "feat: add label"
```

```
...
etiqueta: 12.5
...
ruff format..............................................................Failed
- hook id: ruff-format
- files were modified by this hook

1 file reformatted

mypy.....................................................................Failed
- hook id: mypy
- exit code: 1

main.py:38: error: Incompatible return value type (got "float", expected "str")  [return-value]
Found 1 error in 1 file (checked 1 source file)
```

El programa escribe `etiqueta: 12.5` y parece que funciona, pero `label` promete un `str` y devuelve un `float`. ruff format no puede arreglar eso; mypy lo encuentra. Arréglalo tú: `return f"{value:.1f}"`. Después, `git add .` y otro commit: todo `Passed`.

`pass_filenames: false`: mypy no recibe los archivos del commit, sino que revisa lo que dice `[tool.mypy] files`. Un cambio en un archivo puede romper los tipos de otro que no tocaste.

### 5. `uv.lock` al día

Descomenta el **PASO 5** de `.pre-commit-config.yaml` y guárdalo con un commit. Después, añade una dependencia **a mano**, sin `uv add`: en `pyproject.toml`, cambia `dependencies = []` por `dependencies = ["rich==15.0.0"]`, y:

```bash
git add pyproject.toml
git commit -m "build: add rich"
```

```
...
uv.lock al día...........................................................Failed
- hook id: uv-lock
- exit code: 1

Resolved 23 packages in 279ms
error: The lockfile at `uv.lock` needs to be updated, but `--check` was provided.

hint: To update the lockfile, run `uv lock`.
```

`pyproject.toml` pide `rich`, pero `uv.lock` no lo tiene: quien clonara el repositorio con este commit tendría un `uv sync --locked` que falla. El gancho solo corre cuando cambia uno de los dos archivos (`files`). Arréglalo:

```bash
uv lock
git add pyproject.toml uv.lock
git commit -m "build: add rich"
```

```
Added pygments v2.21.0
Added rich v15.0.0
...
uv.lock al día...........................................................Passed
```

### 6. Saltarse un gancho, y fijarlos a un SHA

A veces quieres guardar un trabajo a medias. Salta solo un gancho, por su `id`:

```bash
SKIP=mypy uv run pre-commit run --all-files
```

```
...
mypy....................................................................Skipped
uv.lock al día...........................................................Passed
```

`SKIP=mypy git commit ...` hace lo mismo en un commit. Es mejor que `--no-verify`: los demás ganchos siguen corriendo.

Por último, `rev: v6.0.0` es una **etiqueta**, y quien controla un repositorio puede mover una etiqueta a otro commit (teoría 03, sección 6). Fíjala a su SHA:

```bash
uv run pre-commit autoupdate --freeze
git diff .pre-commit-config.yaml
```

```
[https://github.com/pre-commit/pre-commit-hooks] updating v6.0.0 -> v6.0.0 (frozen)
...
-    rev: v6.0.0
+    rev: 3e8a8703264a2f4a69428a0aa4dcb512790b2c8c  # frozen: v6.0.0
```

`autoupdate` sube cada repositorio a su última etiqueta (aquí ya lo estaba) y `--freeze` escribe el SHA de su commit, con la versión en un comentario para las personas. Ejecuta `uv run pre-commit run --all-files` y guárdalo con un commit: esta es la forma de tu proyecto.

## 🧯 Si algo sale mal

| Síntoma | Qué hacer |
|---|---|
| `InvalidConfigError` ... `At key: repos` ... `Expected array but got 'NoneType'` | Ningún paso está descomentado: descomenta el PASO 2 |
| `InvalidConfigError` con otra clave, o `is not valid YAML` | La sangría no coincide: compara con el comentario, espacio a espacio |
| `FatalError: git failed. Is it installed, and are you in a Git repository directory?` | Te falta `git init -b main` en la carpeta del ejercicio |
| `Running in migration mode with existing hooks at .git/hooks/pre-commit.legacy` | No borraste el gancho del paso 1, que sigue corriendo y siempre falla: `rm .git/hooks/pre-commit.legacy` |
| El paso 2 tarda o falla en `Initializing environment` | Necesita Internet para clonar `pre-commit-hooks` (solo la primera vez) |
| `Executable \`uv\` not found` | El gancho busca `uv` en tu `PATH`: comprueba `uv --version` en la misma terminal |
| Un gancho dice `Failed` sin error y `files were modified by this hook` | Es un *fixer*: ya lo arregló. `git diff`, `git add .` y repite el commit |

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Teoría 05 · Una imagen Docker segura](../../1-teoria/05-una-imagen-docker-segura.md) | **Ejercicio 01 · Ganchos de Git con pre-commit** | [Ejercicio 02 · Integración continua con GitHub Actions](../ejercicio-02-integracion-continua-con-github-actions/README.md) |
