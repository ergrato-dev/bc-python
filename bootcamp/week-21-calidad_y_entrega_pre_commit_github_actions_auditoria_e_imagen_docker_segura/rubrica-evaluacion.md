# Rúbrica de Evaluación — Semana 21: Calidad y entrega

## 📊 Distribución de Evidencias

| Tipo | Peso | Instrumento |
| ---- | ---- | ----------- |
| Conocimiento 🧠 | 30% | Cuestionario de autoevaluación (10 preguntas) |
| Desempeño 💪 | 40% | Proceso en el proyecto: historial de Git, ejecución y sustentación ante el instructor |
| Producto 📦 | 30% | Proyecto semanal: Observatorio, capa 20 |

**Nota mínima para aprobar**: 70% en cada tipo de evidencia. Los ejercicios guiados no se entregan ni se evalúan.

---

## 🧠 Conocimiento (30%)

Responde por escrito **antes** de abrir las respuestas.

| # | Pregunta | Puntaje |
| - | -------- | ------- |
| 1 | Si ya tienes un gancho de pre-commit que ejecuta ruff y mypy, ¿para qué la CI? Y al revés: si tienes la CI, ¿para qué el gancho? | 10 |
| 2 | ¿Por qué `pytest` no está en el gancho del Observatorio y sí en la CI? ¿Qué pasaría con un gancho de un minuto? | 10 |
| 3 | Un compañero cambia el gancho local de ruff por el remoto de `astral-sh/ruff-pre-commit` "porque es lo estándar". ¿Qué puede dejar de coincidir, y por qué mypy no puede ser remoto en tu proyecto? | 10 |
| 4 | Haces `git commit` y `ruff format` dice `Failed` con `files were modified by this hook`. ¿Se hizo el commit? ¿Qué hay ahora en el *stage* y qué en tu carpeta? ¿Qué haces? | 10 |
| 5 | Tus tests pasan en tu máquina y cinco fallan en GitHub Actions con `\x1b[1m` en el mensaje. ¿Qué es eso, por qué solo en la CI, y cómo lo reproduces sin hacer otro *push*? | 10 |
| 6 | ¿Qué pasó con `trivy-action` en marzo de 2026, y qué línea de tu workflow te protege de algo así? ¿Qué hace Dependabot con esa línea? | 10 |
| 7 | ¿Para qué sirven `permissions: contents: read` y `persist-credentials: false`, si tu CI no tiene secretos? | 10 |
| 8 | `uv audit` dio 0 avisos el lunes y 2 el viernes, sin que cambiaras nada. ¿Cómo es posible? ¿Cómo actualizas una dependencia que no está en tu `pyproject.toml`, y por qué `uv lock` a secas no lo hace? | 10 |
| 9 | ¿Por qué `runtime` copia solo `/opt/venv` y no todo `builder`? ¿Por qué va la última? ¿Qué hace `--no-editable` y qué pasaría sin él? | 10 |
| 10 | El usuario de `runtime` ya no tiene capacidades. ¿Para qué entonces `cap_drop: [ALL]` en `compose.yaml`? ¿Y por qué `apt-get upgrade` si la base está fijada por digest? | 10 |

**Total**: 100 puntos → 30% de la nota final.

<details>
<summary>Respuestas</summary>

1. El gancho es **rápido y temprano**: te avisa en segundos, antes de que el error salga de tu máquina, y arregla solo el formato. Pero es una **ayuda**: no se versiona su instalación (cada uno hace `pre-commit install`), se salta con `--no-verify` y solo mira los archivos del commit. La CI es la **garantía**: corre en una máquina limpia, sobre todos los archivos, con los servicios que hagan falta, y su resultado sale en el *pull request*, donde nadie puede ocultarlo. Sin gancho, los errores llegan a la CI y cada uno cuesta un *push* y minutos de espera.
2. `pytest` tarda unos 20 segundos y necesita PostgreSQL arrancado. En el gancho, cada commit tardaría eso, y fallaría si no tienes `db` arriba. Un gancho lento se acaba saltando con `--no-verify`, y entonces no protege nada, ni siquiera lo rápido. Lo rápido va en el gancho; lo lento y lo que necesita servicios, en la CI.
3. Las **versiones**: el remoto fija ruff en su `rev`, y tu proyecto en `uv.lock`. Tarde o temprano se separan, y el gancho, tu terminal y la CI dicen cosas distintas. Con `uv run --locked ruff` solo hay una fuente. mypy no puede ser remoto porque necesita **tu proyecto**: tus dependencias (FastAPI, SQLAlchemy, Pydantic) y el plugin de Pydantic para revisar `from observatorio.core import ...`; el entorno aislado de un gancho remoto no las tiene.
4. **No** se hizo el commit: un gancho falló. `ruff format` es un gancho que **arregla**: cambió el archivo en tu carpeta, y en el *stage* sigue tu versión sin formatear (`git status --short` dice `MM`). Miras el cambio con `git diff`, lo añades con `git add` y repites el commit.
5. `\x1b[1m` es un código **ANSI**: negrita para una terminal. En GitHub Actions existe `GITHUB_ACTIONS=true`, y Typer, al verla, le dice a Rich que hay terminal y que use colores: la ayuda sale troceada en códigos y `'--verbose' in result.stdout` falla. En tu máquina no hay esa variable. Se reproduce con `GITHUB_ACTIONS=true uv run pytest`, y se arregla con `TERM: dumb` en el `env` del job.
6. Alguien con credenciales robadas movió más de 70 etiquetas de `trivy-action` a un commit que robaba los secretos del runner; durante unas 12 horas, todo workflow que la usaba por etiqueta ejecutó ese código (CVE-2026-33634). Te protege `uses: owner/accion@<SHA de 40 caracteres> # vX.Y.Z`: un SHA no se puede mover. Dependabot lee el comentario y propone el SHA y el comentario nuevos en un *pull request*.
7. Son defensa por si algo sale mal. Con `contents: read`, el token del job no puede escribir en tu repositorio aunque un paso esté comprometido (una acción con la etiqueta movida, una dependencia maliciosa en los tests). Con `persist-credentials: false`, ese token no se queda guardado en `.git/config`, donde cualquier paso posterior podría leerlo. Tu CI no necesita más, así que no tiene más.
8. La base de datos de avisos **crece**: el jueves se publicó un aviso para una versión que tienes fijada. Tu código no cambió; lo que se sabe de él, sí. Por eso la auditoría va en la CI. Una transitiva se actualiza con `uv lock --upgrade-package <paquete>`, que cambia solo `uv.lock`. `uv lock` a secas no actualiza lo que ya está en `uv.lock` si sigue siendo válido, para que añadir una dependencia no cambie las demás por sorpresa.
9. En `builder` están uv, la caché, `pyproject.toml`, `src/`: lo necesario para **instalar**, no para ejecutar. Copiando solo `/opt/venv`, nada de eso llega a producción. `runtime` va la última porque `docker build .` sin `--target` construye la última etapa, y lo que se construye sin pensar debe ser lo seguro. `--no-editable` copia tu paquete dentro de `/opt/venv`; sin él, el entorno apuntaría a `/app/src`, que en `runtime` no existe, y `observatorio` fallaría al importar.
10. Es **defensa en profundidad**: si alguien cambia la configuración y ejecuta como root (`--user 0`), con `cap_drop` sigue sin capacidades; cada capa protege aunque falle otra. El digest **congela** la base con sus fallos del día en que la fijaste; `apt-get upgrade` aplica los parches de Debian publicados después (por ejemplo, el de `zlib1g` que encontró Trivy). A cambio, dos construcciones en días distintos pueden diferir en algún paquete de Debian.

</details>

---

## 💪 Desempeño (40%)

Se evalúa **cómo** construiste el proyecto, con evidencia del repositorio y una sustentación corta (10 min) con el instructor.

| Criterio | Evidencia | Puntaje |
| -------- | --------- | ------- |
| Pasos pequeños | El historial de `week-21` muestra un commit por paso (tests, dependencias, ganchos, el arreglo de la primera pasada aparte, `Dockerfile`, `compose.yaml`, CI, Dependabot, versión, tests propios), sin cambiar los tests del bootcamp, y cada commit pasó por los ganchos | 8 |
| Configuración con cuidado | Acciones por SHA con su versión en un comentario; imágenes por digest; `permissions: contents: read`; ninguna contraseña real ni `.env` en Git; `runtime` sin uv, sin pip y sin root | 8 |
| Ejecución en vivo | Ante el instructor: `pre-commit run --all-files`, un commit bloqueado por un gancho, `uv audit`, `docker compose build app api`, `docker run ... id` en `runtime`, Trivy sobre `runtime`, y la ejecución de la CI en verde en GitHub con `gh pr checks` | 8 |
| Rompe y explica | Cambia `contents: read` por `write` y explica qué test falla; quita `USER` de `runtime` y enseña la sonda o `id`; reproduce en local el fallo de los colores con `GITHUB_ACTIONS=true` | 8 |
| Explica sus medidas | Explica su tabla del paso 12 (de dónde salen los MB y las vulnerabilidades que ya no están), qué mutante sobrevivió y cómo lo mata su test, y qué propuso Dependabot | 8 |
| **Total** | | **40** |

**Total Desempeño**: 40 puntos → 40% de la nota final.

---

## 📦 Producto (30%)

### Proyecto Semanal — Observatorio, capa 20

| Criterio | Descripción | Puntaje |
| -------- | ----------- | ------- |
| Ganchos | `.pre-commit-config.yaml` con los seis ganchos genéricos fijados por SHA y `# frozen:`, y los cuatro locales con `uv run --locked` (o `uv lock --check`), `language: unsupported`, mypy con `pass_filenames: false`; instalados en el repositorio | 15 |
| CI | `ci.yml` con `push` a `main` y `pull_request`, `permissions: contents: read`, `concurrency`, `UV_LOCKED`, los jobs `quality`, `tests` (PostgreSQL de compose, `TERM: dumb`, cobertura, `alembic check`) e `image` (build, arranque y Trivy); acciones por SHA, `persist-credentials: false`, `timeout-minutes` y `ubuntu-24.04`; en verde en GitHub | 20 |
| Imagen | `Dockerfile` con `uv`, `builder` (`--no-dev --no-editable`, `.pyc`), `test` y `runtime` la última (solo `/opt/venv`, `apt-get upgrade`, sin pip, `USER 10001:10001`, sirve por defecto); bases por digest | 15 |
| Compose y dependencias | `app` con `test`, `api` con `runtime`, `read_only`, `tmpfs`, `cap_drop`, `no-new-privileges` y puertos en `127.0.0.1`; `dependabot.yml` con los tres ecosistemas, `cooldown` y el `ignore` de Python; `uv audit` limpio | 10 |
| Tests propios | Al menos 6 tests en `tests/test_my_delivery.py`, cada uno visto fallar con un mutante; al menos uno mata el mutante que sobrevive a los tests del bootcamp | 15 |
| Calidad | `pre-commit run --all-files`, `coverage report` y `alembic check` sin avisos; `docker compose run --rm app` en verde y `api` sano; dependencias fijadas; versión `0.21.0` | 10 |
| Git y README | Rama `week-21` en `python-<nombre>-<apellido>`; README con la insignia de la CI y la sección "Calidad y entrega" | 5 |
| Pull request | Salidas y enlace a la CI en verde, las tablas de medidas y de mutantes, y las dos preguntas del paso 16 | 10 |
| **Total** | | **100** |

**Total Producto**: 100 puntos → 30% de la nota final.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Glosario](5-glosario/README.md) | **Rúbrica de evaluación** | Semana 22 (próximamente) |
