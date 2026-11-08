# 03 · Integración continua con GitHub Actions

⏱️ 55 min

## 🎯 Objetivos

- Leer un workflow de GitHub Actions: eventos, jobs, *runners* y *steps*.
- Elegir los eventos que disparan la CI y evitar el que expone tus secretos.
- Ejecutar jobs en paralelo, con una matriz y con un PostgreSQL como servicio.
- Explicar por qué una acción se fija a su SHA, con un caso real.
- Dar al token del workflow solo el permiso que necesita.
- Leer el resultado desde la terminal y revisar un workflow antes de subirlo.

---

## 1. La integración continua

**Integración continua** (*continuous integration*, CI): cada cambio que se sube se comprueba **solo**, en una máquina limpia, y el resultado se ve junto al cambio. En GitHub, eso lo hace **GitHub Actions**: lee los archivos YAML de `.github/workflows/` de tu repositorio y los ejecuta cuando pasa algo (un *push*, un *pull request*...).

"Máquina limpia" importa: no tiene tu `.venv`, ni tu `.env`, ni el paquete que instalaste a mano hace tres semanas. Si la CI pasa, el proyecto funciona con lo que hay en Git, y nada más.

---

## 2. Anatomía de un workflow

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:

permissions:
  contents: read

jobs:
  tests:
    runs-on: ubuntu-24.04
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
        with:
          persist-credentials: false
      - uses: astral-sh/setup-uv@07a047e608db84b3d8c06cd9a7c7dcc9c355c18e # v10.3.2
        with:
          version: "0.13.7"
      - run: uv sync
      - run: uv run coverage run -m pytest
```

| Pieza | Qué es |
|---|---|
| **workflow** | El archivo entero. Un repositorio puede tener varios |
| `on` | Los **eventos** que lo disparan (sección 3) |
| **job** | Un trabajo, en una máquina **nueva**. Los jobs corren a la vez, salvo que uno diga `needs: otro` |
| `runs-on` | El **runner**: la máquina. `ubuntu-24.04` es una máquina virtual de GitHub |
| **step** | Un paso del job, en orden. Si uno falla, los siguientes no se ejecutan |
| `run` | Un paso que es una orden de bash |
| `uses` | Un paso que es una **acción**: un programa publicado en otro repositorio |
| `with` | Los parámetros de una acción |

Sin `actions/checkout`, la máquina no tiene tu código: es lo primero de cada job. `setup-uv` instala uv; uv descarga el Python de `.python-version` y lo demás sale de `uv.lock`.

Por qué `ubuntu-24.04` y no `ubuntu-latest`: `latest` cambia cuando GitHub quiere. En noviembre de 2026, cada ejecución con `ubuntu-latest` mostraba este aviso:

```
The ubuntu-latest label will migrate to Ubuntu 26 beginning October 19, 2026.
```

Con la versión escrita, el cambio de sistema lo decides tú, en un *pull request*.

---

## 3. Los eventos

| Evento | Cuándo | Con tus secretos |
|---|---|---|
| `push` | Al subir commits. `branches: [main]` lo limita a `main` | Sí |
| `pull_request` | Al abrir un *pull request* o subirle commits | No, si viene de un *fork* |
| `pull_request_target` | Igual, pero con el workflow y los permisos de **tu** rama | **Sí** |
| `schedule` | Con un horario `cron`, por ejemplo una auditoría semanal | Sí |
| `workflow_dispatch` | A mano, con un botón o `gh workflow run` | Sí |

El Observatorio usa `push` a `main` y `pull_request`: cada cambio se prueba en su *pull request*, y `main` se vuelve a probar al fusionar.

**`pull_request_target` es peligroso**: está pensado para etiquetar o comentar *pull requests*, y se ejecuta con los secretos y permisos de tu repositorio. Si además hace *checkout* del código del *pull request*, cualquiera puede abrir uno con código que lea tus secretos. Tu proyecto no lo usa, y un test lo comprueba.

---

## 4. Varios jobs, una matriz y un servicio

Los tres jobs del Observatorio (`quality`, `tests`, `image`) no dependen unos de otros: corren **a la vez**, y el tiempo total es el del más lento, no la suma.

Una **matriz** crea un job por cada combinación:

```yaml
    strategy:
      matrix:
        python: ["3.13", "3.14"]
    env:
      UV_PYTHON: ${{ matrix.python }}
```

`${{ ... }}` es una **expresión**: GitHub la sustituye antes de ejecutar. Dos detalles:

- las versiones **entre comillas**: en YAML, `3.10` es el número 3.1;
- **`fail-fast`**, activado por defecto: si una combinación falla, GitHub **cancela** las demás para no gastar minutos. Verás `The strategy configuration was canceled because "tests._3_13" failed`.

Tu proyecto fija Python 3.14, así que no usa matriz. Sí usa un **servicio**: un contenedor que GitHub arranca junto al job, como un `compose.yaml` pequeño.

```yaml
    services:
      db:
        image: postgres:18.6-alpine@sha256:123b...
        env:
          POSTGRES_USER: observatorio
          POSTGRES_PASSWORD: observatorio
          POSTGRES_DB: observatorio
        ports:
          - 5432:5432
        options: >-
          --health-cmd "pg_isready -U observatorio -d observatorio"
          --health-interval 2s --health-timeout 5s --health-retries 15
```

`ports` publica el 5432 del contenedor en el 5432 del runner: los tests usan `127.0.0.1:5432`, la misma URL que en tu máquina. `options` son opciones de `docker run`; con `--health-cmd`, GitHub espera a que PostgreSQL acepte conexiones antes de empezar los *steps*, como `condition: service_healthy` en compose. Esa contraseña no es un secreto: es la de una base que nace y muere con el job.

---

## 5. Variables y `--locked`

`env` define variables para el workflow entero, un job o un paso. El Observatorio pone una arriba:

```yaml
env:
  UV_LOCKED: "1"
```

Con `UV_LOCKED=1`, cada `uv sync` y `uv run` falla si `uv.lock` no corresponde a `pyproject.toml`, igual que `--locked`. Sin ella, uv actualizaría `uv.lock` en la máquina de la CI, probaría otra cosa y nadie lo vería.

Y en el job de tests, la del caso de la teoría 01:

```yaml
    env:
      OBSERVATORIO_DATABASE_URL: postgresql+psycopg://observatorio:observatorio@127.0.0.1:5432/observatorio
      TERM: dumb
```

---

## 6. Acciones de terceros: etiqueta o SHA

`uses: actions/checkout@v7.0.1` ejecuta, **con tus permisos y tus secretos**, el código que haya en la etiqueta `v7.0.1` del repositorio `actions/checkout` **en el momento de ejecutar**. Y una etiqueta se puede mover.

![Una etiqueta movida a un commit malicioso: el workflow que usa la etiqueta ejecuta el código nuevo, el que usa el SHA sigue con el revisado; y cómo fija tu proyecto paquetes, acciones e imágenes](../0-assets/02-etiqueta-sha-y-digest.svg)

No es teoría. El 19 de marzo de 2026, alguien con credenciales robadas movió más de 70 etiquetas de `aquasecurity/trivy-action`, la acción del escáner que usarás en la teoría 05, a un commit con un programa que robaba los secretos del runner. Durante unas 12 horas, cada workflow que usaba `trivy-action@v0.x` ejecutó ese código (CVE-2026-33634). Los que la usaban por SHA no se enteraron.

Por eso, cada acción va fijada al **SHA completo de su commit**, con la versión en un comentario para las personas:

```yaml
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
```

El SHA de una etiqueta lo da GitHub:

```bash
gh api repos/actions/checkout/commits/v7.0.1 --jq .sha
```

```
3d3c42e5aac5ba805825da76410c181273ba90b1
```

¿Y para actualizar? Dependabot (teoría 04) lee el comentario y propone el cambio de SHA y de comentario a la vez, en un *pull request*:

```diff
-      - uses: astral-sh/setup-uv@07a047e608db84b3d8c06cd9a7c7dcc9c355c18e # v10.3.2
+      - uses: astral-sh/setup-uv@68559e99cc807c1eb7e9238fd43a15bba460eec2 # v10.3.3
```

Usa pocas acciones. Tu CI usa dos (`checkout` y `setup-uv`); lo demás son órdenes `run` que ves enteras. Trivy, por ejemplo, va con `docker run` de su imagen fijada por digest, no con su acción.

---

## 7. El token, y lo que no debe salir

Cada job recibe un token, `GITHUB_TOKEN`, para hablar con la API de GitHub. Lo que puede hacer depende de `permissions`:

```yaml
permissions:
  contents: read
```

Solo **leer** el repositorio: tu CI no publica nada, no comenta ni etiqueta. Si un paso se ve comprometido (una acción con la etiqueta movida...), con ese token no puede escribir en tu código.

`actions/checkout` guarda por defecto ese token en `.git/config` del runner, para que los pasos siguientes puedan hacer `git push`. En el registro del ejercicio 02 lo ves: `persist-credentials: true`. Tu CI no hace *push*, así que:

```yaml
        with:
          persist-credentials: false
```

Los **secretos** de verdad (una clave de API, un token para publicar) se guardan en *Settings → Secrets and variables → Actions* y se usan como `${{ secrets.NOMBRE }}`. GitHub los tapa con `***` en los registros, pero solo si aparecen tal cual: nunca los imprimas ni los transformes. Tu CI no necesita ninguno.

---

## 8. Que no se acumule ni se cuelgue

```yaml
concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true
```

Si subes tres commits seguidos a una rama, solo interesa el último. `concurrency` agrupa las ejecuciones por rama (`github.ref`) y cancela la anterior al empezar una nueva.

```yaml
    timeout-minutes: 15
```

Por defecto, un job puede durar **6 horas**. Un test colgado esperando a una red que no existe gasta 6 horas de minutos. Pon un límite un poco por encima de lo normal: los jobs del Observatorio tardan menos de un minuto.

En repositorios públicos, los minutos de los runners de GitHub son gratis; en uno privado de una cuenta gratuita, hay 2000 minutos al mes.

---

## 9. Leer el resultado

En la pestaña **Actions** de tu repositorio, y en cada *pull request*, abajo. Desde la terminal, con `gh`:

| Orden | Qué hace |
|---|---|
| `gh run list` | Las últimas ejecuciones, con su estado |
| `gh run watch` | Sigue una ejecución en curso hasta el final |
| `gh run view ID` | Jobs y pasos de una ejecución, con ✓ y X |
| `gh run view ID --log-failed` | Solo el registro de los pasos que fallaron |
| `gh pr checks --watch` | Las comprobaciones del *pull request* de tu rama |

Cuando algo falla solo en la CI, el método de la teoría 01: leer, reproducir en local con lo que cambia, arreglar.

Y antes de subir un workflow, revísalo con **actionlint**: entiende la sintaxis de GitHub Actions, las expresiones `${{ }}` y las etiquetas de los runners:

```bash
docker run --rm -v "$PWD":/repo -w /repo rhysd/actionlint:1.7.12@sha256:b1934ee5f1c509618f2508e6eb47ee0d3520686341fec936f3b79331f9315667
```

```
.github/workflows/ci.yml:52:22: property "pyhton" is not defined in object type {python: number} [expression]
```

GitHub habría aceptado ese *push* y fallado al ejecutar.

---

## ⚠️ Errores comunes

| Error | Por qué está mal | Qué hacer |
|---|---|---|
| `uses: alguien/accion@v1` | La etiqueta se puede mover a otro código, que corre con tus permisos | SHA completo y la versión en un comentario |
| Sin `permissions` | El token puede tener permisos de escritura, según la configuración del repositorio | `permissions: contents: read` arriba |
| `pull_request_target` para ejecutar tests | Código ajeno con tus secretos | `pull_request` |
| `runs-on: ubuntu-latest` | El sistema cambia sin que lo decidas | `ubuntu-24.04` |
| Sin `timeout-minutes` | Un job colgado gasta hasta 6 horas | Un límite por job |
| `uv sync` sin `--locked` ni `UV_LOCKED` | La CI puede probar otras versiones que las de `uv.lock` | `UV_LOCKED: "1"` |
| Imprimir un secreto "para depurar" | Si lo transformas, GitHub no lo tapa | Nunca: comprueba que existe, no su valor |

---

## ✅ Qué debes saber al terminar

- [ ] Workflow, job, runner, step, `run`, `uses` y `with`.
- [ ] Qué eventos usa el Observatorio, y por qué no `pull_request_target`.
- [ ] Qué hace una matriz, qué es `fail-fast` y cómo funciona un servicio con su *healthcheck*.
- [ ] Por qué cada acción va por SHA, y qué pasó con `trivy-action` en marzo de 2026.
- [ ] `permissions: contents: read`, `persist-credentials: false`, `concurrency` y `timeout-minutes`.
- [ ] Cómo leer un fallo con `gh run view --log-failed` y revisar un workflow con actionlint.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [02 · Ganchos de Git con pre-commit](02-ganchos-de-git-con-pre-commit.md) | **03 · Integración continua con GitHub Actions** | [04 · La cadena de suministro: auditar y actualizar dependencias](04-cadena-de-suministro-auditar-y-actualizar-dependencias.md) |
