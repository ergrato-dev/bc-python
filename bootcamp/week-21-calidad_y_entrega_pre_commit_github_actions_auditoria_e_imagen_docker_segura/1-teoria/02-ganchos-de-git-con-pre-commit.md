# 02 · Ganchos de Git con pre-commit

⏱️ 50 min

## 🎯 Objetivos

- Explicar qué es un gancho de Git, cuándo se ejecuta y por qué no basta para un equipo.
- Leer y escribir un `.pre-commit-config.yaml`: repositorios, `rev`, ganchos y sus opciones.
- Saber qué archivos ve cada gancho en un commit, y qué pasa con los cambios sin añadir.
- Distinguir un gancho que **arregla** de uno que **comprueba**.
- Elegir entre ganchos remotos y locales, y fijar los remotos a un SHA.
- Saltarte un gancho cuando toca, sin saltarte los demás.

---

## 1. Ganchos de Git

Git ejecuta programas en momentos concretos si existen en `.git/hooks/` con un nombre que conoce: `pre-commit` (antes de crear un commit), `commit-msg` (con el mensaje ya escrito), `pre-push` (antes de enviar)... Si `pre-commit` termina con un código distinto de 0, **no hay commit**.

```bash
cat .git/hooks/pre-commit
```

```sh
#!/bin/sh
echo "gancho: vas a guardar $(git diff --cached --name-only | wc -l) archivos"
exit 1
```

Útil, pero con dos problemas:

- `.git/hooks/` **no se versiona**: no viaja con `git push` ni con `git clone`. Cada persona tendría que copiarse el script, y nadie sabría si lo tiene;
- `git commit --no-verify` se lo salta. Un gancho es una **ayuda** para quien lo usa, nunca una garantía: la garantía es la CI (teoría 03).

---

## 2. pre-commit, el programa

**pre-commit** resuelve el primer problema. La configuración vive en el repositorio, en `.pre-commit-config.yaml`, y cada persona la activa con una orden:

```bash
uv add --dev pre-commit==4.7.0
uv run pre-commit install
```

```
pre-commit installed at .git/hooks/pre-commit
```

`install` escribe en `.git/hooks/pre-commit` un script pequeño que llama a pre-commit, y pre-commit lee la configuración en cada commit. Si cambias la configuración, no hace falta reinstalar.

Va en el grupo `dev` de tu proyecto, con su versión fijada, como ruff o mypy: así la tiene cualquiera que haga `uv sync`, y la CI usa la misma.

---

## 3. Anatomía de `.pre-commit-config.yaml`

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: 3e8a8703264a2f4a69428a0aa4dcb512790b2c8c  # frozen: v6.0.0
    hooks:
      - id: trailing-whitespace
      - id: check-added-large-files

  - repo: local
    hooks:
      - id: mypy
        name: mypy
        entry: uv run --locked mypy
        language: unsupported
        types: [python]
        pass_filenames: false
```

- **`repos`**: una lista de repositorios de ganchos;
- **`repo`**: de dónde salen. Una URL de Git, o `local` para ganchos que defines tú;
- **`rev`**: qué versión del repositorio (sección 7);
- **`hooks`**: cuáles usas, por su `id`.

Las opciones de cada gancho:

| Opción | Qué hace | Ejemplo |
|---|---|---|
| `entry` | La orden que ejecuta (en los locales) | `uv run --locked mypy` |
| `language` | Cómo prepara pre-commit el entorno del gancho | `python`, `unsupported` |
| `types` | Solo archivos de ese tipo, según su extensión y contenido | `[python]`, `[yaml]` |
| `files` | Solo archivos cuya ruta casa con la expresión regular | `^(pyproject\.toml\|uv\.lock)$` |
| `exclude` | Ninguno cuya ruta case con la expresión | `^migrations/versions/` |
| `pass_filenames` | Si recibe los nombres de los archivos (por defecto, sí) | `false` |
| `args` | Argumentos extra | `[--maxkb=200]` |

---

## 4. Cómo corre un commit

Cuando haces `git commit`:

1. pre-commit mira los archivos **del commit** (los del *stage*, los que añadiste con `git add`);
2. si tienes cambios **sin añadir** en esos archivos, los aparta (`Stashing unstaged files`): los ganchos ven exactamente lo que vas a guardar, no lo que tienes en la carpeta;
3. ejecuta cada gancho, en orden, con los archivos que le tocan según `types`, `files` y `exclude`. Si no le toca ninguno: `(no files to check)Skipped`;
4. devuelve tus cambios apartados a su sitio;
5. si algún gancho falló, **no hay commit**.

Hay dos clases de ganchos, y fallan distinto:

- los que **comprueban** (`mypy`, `check-yaml`) dicen qué está mal y no tocan nada. Lo arreglas tú;
- los que **arreglan** (`trailing-whitespace`, `ruff format`) cambian el archivo y fallan igualmente, con `files were modified by this hook`. Fallan para que **veas** el cambio antes de guardarlo: `git diff`, `git add` y otra vez `git commit`.

```
ruff format..............................................................Failed
- hook id: ruff-format
- files were modified by this hook

1 file reformatted
```

Después del fallo, `git status --short` dice `MM main.py`: una versión en el *stage* (la tuya) y otra en la carpeta (la arreglada).

---

## 5. Ganchos remotos y ganchos locales

Un gancho **remoto** vive en otro repositorio de Git. La primera vez, pre-commit lo **clona** en la versión de `rev` y le prepara su propio entorno (con `language: python`, un *virtualenv*), en `~/.cache/pre-commit`. Las siguientes, lo reutiliza:

```
[INFO] Initializing environment for https://github.com/pre-commit/pre-commit-hooks.
[INFO] Installing environment for https://github.com/pre-commit/pre-commit-hooks.
[INFO] Once installed this environment will be reused.
```

Un gancho **local** (`repo: local`) ejecuta una orden de tu proyecto. Con `language: unsupported`, pre-commit no prepara nada: la orden ya funciona tal cual. (Antes se llamaba `system`. Desde pre-commit 4.4, `unsupported` es su nombre nuevo; `system` sigue funcionando, pero acabará marcado como obsoleto. El nombre nuevo dice lo que es: pre-commit no se ocupa de instalarlo.)

Para ruff y mypy, tu proyecto usa ganchos **locales** con `uv run --locked`:

- **la misma versión**: la de `uv.lock`, la de tu terminal y la de la CI. Con el gancho remoto de ruff, la versión vive en `rev` y en `uv.lock`, y tarde o temprano se separan;
- **mypy necesita tu proyecto**: para revisar `from observatorio.core import ...` tiene que ver tus dependencias y el plugin de Pydantic. En el entorno aislado de un gancho remoto, no están.

Para los ganchos genéricos (espacios, YAML, claves privadas), el remoto es perfecto: no dependen de tu proyecto.

`pass_filenames: false` en mypy: no recibe los archivos del commit, sino que revisa lo que dice `[tool.mypy] files`. Si cambias una función en `model.py`, el error puede estar en `cli.py`, que no tocaste.

---

## 6. Los ganchos genéricos del Observatorio

De [pre-commit-hooks](https://github.com/pre-commit/pre-commit-hooks):

| Gancho | Qué hace |
|---|---|
| `trailing-whitespace` | Quita los espacios al final de las líneas (arregla) |
| `end-of-file-fixer` | Deja un solo salto de línea al final de cada archivo (arregla) |
| `check-yaml` | Que cada `.yaml` se puede leer |
| `check-toml` | Que cada `.toml` se puede leer |
| `check-added-large-files` | Que no añades un archivo de más de 500 KB (un CSV enorme, un modelo) |
| `detect-private-key` | Que no se cuela una clave privada (`-----BEGIN ... PRIVATE KEY-----`) |

La primera vez que los pases por todo el Observatorio, `end-of-file-fixer` arreglará un archivo que no escribiste tú:

```
fix end of files.........................................................Failed
- hook id: end-of-file-fixer
- exit code: 1
- files were modified by this hook

Fixing migrations/README
```

`alembic init` lo generó sin salto de línea final (semana 19). Es normal que la primera pasada arregle cosas viejas: guárdalas en un commit aparte (`style: fix end of files`), para que no se mezclen con tu cambio.

---

## 7. Fijar un gancho remoto

`rev: v6.0.0` es una **etiqueta** de Git, y una etiqueta es un nombre que apunta a un commit: quien controla el repositorio puede moverla a otro commit (teoría 03, sección 6). Un **SHA** es el commit mismo: no se puede mover. pre-commit lo escribe por ti:

```bash
uv run pre-commit autoupdate --freeze
```

```
[https://github.com/pre-commit/pre-commit-hooks] updating v6.0.0 -> v6.0.0 (frozen)
```

```yaml
    rev: 3e8a8703264a2f4a69428a0aa4dcb512790b2c8c  # frozen: v6.0.0
```

`autoupdate` sube cada repositorio a su **última** etiqueta; `--freeze` escribe el SHA de su commit y deja la versión en un comentario, para las personas. Haz `autoupdate` cuando quieras actualizar, no por costumbre: revisa qué cambió, como con cualquier dependencia.

---

## 8. Saltarse un gancho, y ejecutarlos a mano

| Orden | Qué hace |
|---|---|
| `uv run pre-commit run` | Los ganchos, sobre los archivos del *stage*, sin hacer commit |
| `uv run pre-commit run --all-files` | Sobre **todos** los archivos del repositorio. Es lo que hace la CI |
| `uv run pre-commit run mypy --all-files` | Solo un gancho, por su `id` |
| `SKIP=mypy git commit -m "..."` | El commit, sin ese gancho; los demás sí corren |
| `git commit --no-verify -m "..."` | Sin ningún gancho |

`SKIP` es mejor que `--no-verify`: si guardas un trabajo a medias con un error de tipos, sigues sin colar espacios ni una clave privada. Y lo que te saltes, la CI lo verá.

En la CI añades `--show-diff-on-failure`: si un gancho que arregla cambia algo, el registro enseña el *diff*, porque allí nadie puede mirar la carpeta.

---

## ⚠️ Errores comunes

| Error | Por qué está mal | Qué hacer |
|---|---|---|
| Hacer `git add .` después de un fallo sin mirar | Guardas lo que el gancho cambió sin saber qué es | `git diff` antes de `git add` |
| `git commit --no-verify` por costumbre | El gancho deja de proteger, y el error llega a la CI | `SKIP=<id>` solo para el gancho que toca |
| ruff remoto con otra versión que la de `uv.lock` | La CI y tu terminal dicen cosas distintas | Gancho local con `uv run --locked` |
| mypy con `pass_filenames` por defecto | Solo mira los archivos del commit y no ve los errores que causas en otros | `pass_filenames: false` |
| `rev: v6.0.0` | Una etiqueta se puede mover | `autoupdate --freeze`: SHA y comentario |
| Mezclar la primera pasada con tu cambio | El *diff* de tu *pull request* se llena de espacios | Un commit aparte para lo que arregla la primera pasada |

---

## ✅ Qué debes saber al terminar

- [ ] Qué es un gancho de Git, por qué no se versiona y por qué `--no-verify` lo anula.
- [ ] Las partes de `.pre-commit-config.yaml` y las opciones `types`, `files`, `pass_filenames`.
- [ ] Qué archivos ve un gancho en un commit, y qué hace pre-commit con los cambios sin añadir.
- [ ] La diferencia entre un gancho que arregla y uno que comprueba, y qué hacer cuando falla cada uno.
- [ ] Cuándo un gancho remoto y cuándo uno local con `uv run --locked`.
- [ ] Cómo fijar un gancho remoto a su SHA, y cómo saltar solo uno.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [01 · De tu máquina a main: calidad automática](01-de-tu-maquina-a-main-calidad-automatica.md) | **02 · Ganchos de Git con pre-commit** | [03 · Integración continua con GitHub Actions](03-integracion-continua-con-github-actions.md) |
