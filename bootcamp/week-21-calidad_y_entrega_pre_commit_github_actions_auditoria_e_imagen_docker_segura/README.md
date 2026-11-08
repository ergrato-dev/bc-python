# Semana 21 — Calidad y entrega: pre-commit, GitHub Actions, auditoría e imagen Docker segura

> Tu Observatorio tiene más de 700 tests, mypy estricto y una API en Docker. Pero todo eso depende de que te acuerdes de ejecutarlo, tus versiones fijadas envejecen sin que nadie mire, y la imagen que sirve la API lleva uv, pip, pytest y el código fuente. Esta semana automatizas la **entrega**: **ganchos de Git** con pre-commit que revisan cada commit en segundos, una **CI en GitHub Actions** que lo comprueba todo en una máquina limpia, una **auditoría de dependencias** con `uv audit` y Dependabot, y una **imagen Docker segura**: pequeña, fijada por digest, sin root y en solo lectura. Y como la configuración también es código, la pruebas con tests.

---

## 🎯 Objetivos de la Semana

Al finalizar esta semana serás capaz de:

- **Decidir** qué comprobación va en tu terminal, cuál en un gancho de Git y cuál en la CI, con las mismas versiones en los tres sitios
- **Configurar** pre-commit con ganchos remotos fijados a un SHA y ganchos locales con `uv run --locked`
- **Escribir** un workflow de GitHub Actions con un servicio de PostgreSQL, permisos mínimos y acciones fijadas por SHA, y **reproducir** en local un fallo que solo pasa en la CI
- **Auditar** dependencias con `uv audit`, **leer** un aviso y **actualizar** dependencias directas y transitivas
- **Construir** una imagen *multi-stage* sin herramientas de desarrollo, fijada por digest, sin root y en solo lectura, y **escanearla** con Trivy
- **Probar** la configuración de la entrega con tests y mutantes

---

## 📋 Prerrequisitos

- [Semana 20](../week-20-fastapi_lo_justo_para_servir_tu_proyecto/README.md): FastAPI, lo justo para servir tu proyecto.
- El *pull request* `week-20` de tu proyecto fusionado en `main`.
- Docker funcionando y unos 3 GB libres (ejercicio 04).
- Una cuenta de GitHub y `gh` con tu sesión iniciada: `gh auth status`.

---

## 🗂️ Estructura de la Semana

```
week-21-calidad_y_entrega_pre_commit_github_actions_auditoria_e_imagen_docker_segura/
├── README.md                    # este archivo
├── rubrica-evaluacion.md        # cómo se evalúa la semana
├── 0-assets/                    # 3 diagramas SVG
├── 1-teoria/                    # 5 archivos, un concepto cada uno
├── 2-practicas/                 # 4 ejercicios guiados (descomentar y ejecutar)
├── 3-proyecto/                  # la capa 20 de tu Observatorio: el entregable
├── 4-recursos/                  # webgrafía, ebooks, vídeos
└── 5-glosario/                  # los términos de la semana, A-Z
```

---

## 📝 Contenidos

### Teoría

| Archivo | Tema | Duración |
| ------- | ---- | -------- |
| [01 · De tu máquina a main: calidad automática](1-teoria/01-de-tu-maquina-a-main-calidad-automatica.md) | Las diez comprobaciones, el problema de acordarse, tres redes, rápido delante y completo detrás, una sola fuente de versiones, "funciona en mi máquina" y tests sobre la configuración | 45 min |
| [02 · Ganchos de Git con pre-commit](1-teoria/02-ganchos-de-git-con-pre-commit.md) | Ganchos de Git, pre-commit, anatomía del archivo, cómo corre un commit, ganchos que arreglan y que comprueban, remotos y locales, fijar a un SHA y `SKIP` | 50 min |
| [03 · Integración continua con GitHub Actions](1-teoria/03-integracion-continua-con-github-actions.md) | Workflow, job, runner y step, eventos, matriz y servicios, `UV_LOCKED`, acciones por SHA y el caso de `trivy-action`, el token, `concurrency` y `timeout-minutes`, `gh` y actionlint | 55 min |
| [04 · La cadena de suministro: auditar y actualizar dependencias](1-teoria/04-cadena-de-suministro-auditar-y-actualizar-dependencias.md) | Dependencias transitivas, el precio de fijar, CVE, GHSA y OSV, `uv audit`, actualizar una cosa cada vez, ignorar con motivo y Dependabot | 45 min |
| [05 · Una imagen Docker segura](1-teoria/05-una-imagen-docker-segura.md) | Superficie de ataque, cuatro etapas, base pequeña y fijada por digest, fuera pip, sin root, solo lectura y sin capacidades, secretos fuera y Trivy | 45 min |

### Prácticas

Guiadas y sin entrega: el código y la configuración vienen comentados por pasos, los descomentas, ejecutas y comparas con la salida esperada. Preparan el proyecto. El 01 y el 02 trabajan en una copia del `starter/` con su propio repositorio de Git; el 02 sube el suyo a un repositorio privado de práctica en GitHub.

| Ejercicio | Qué haces | Duración |
| --------- | --------- | -------- |
| [01 · Ganchos de Git con pre-commit](2-practicas/ejercicio-01-ganchos-con-pre-commit/README.md) | Un gancho a mano, los ganchos genéricos que arreglan, ruff y mypy locales, `uv.lock` desfasado, `SKIP` y `autoupdate --freeze` | 1 h 30 min |
| [02 · Integración continua con GitHub Actions](2-practicas/ejercicio-02-integracion-continua-con-github-actions/README.md) | Un workflow, los tests con uv, una matriz de Python, un *pull request* en rojo y en verde, permisos, SHA y actionlint | 1 h 30 min |
| [03 · Auditar dependencias](2-practicas/ejercicio-03-auditar-dependencias/README.md) | Quién pide qué, `uv audit` con 13 avisos, actualizar directas y una transitiva sujeta, e ignorar con `--ignore-until-fixed` | 1 h 30 min |
| [04 · Una imagen Docker segura](2-practicas/ejercicio-04-una-imagen-docker-segura/README.md) | Una sonda en cuatro imágenes, de 1,69 GB y root a 198 MB sin pip ni root, solo lectura y sin capacidades, y Trivy | 1 h 30 min |

### Proyecto

Añades a tu Observatorio la configuración de la entrega:

- `.pre-commit-config.yaml`, con seis ganchos genéricos fijados por SHA y ruff, mypy y `uv.lock` como ganchos locales;
- `.github/workflows/ci.yml`, con tres jobs: `quality`, `tests` con PostgreSQL e `image` con Trivy;
- `.github/dependabot.yml`, para paquetes, acciones e imágenes;
- un `Dockerfile` en cuatro etapas, con `runtime` pequeña, sin uv, sin pip y sin root;
- `compose.yaml` con un *target* por servicio y `api` en solo lectura y sin capacidades.

`src/` no cambia: 48 tests nuevos comprueban la configuración. Después mides la imagen y la CI, y haces una prueba de mutación sobre la configuración. La versión sube a `0.21.0`. **Es el único entregable de la semana.**
→ [3-proyecto/README.md](3-proyecto/README.md)

---

## ⏱️ Distribución del Tiempo (18 horas)

| Actividad | Tiempo |
| --------- | ------ |
| Teoría (5 archivos) | 4 h |
| Ejercicio 01 | 1 h 30 min |
| Ejercicio 02 | 1 h 30 min |
| Ejercicio 03 | 1 h 30 min |
| Ejercicio 04 | 1 h 30 min |
| Proyecto | 6 h 30 min |
| Recursos y glosario | 30 min |
| Autoevaluación (cuestionario de la rúbrica) | 1 h |
| **Total** | **18 h** |

---

## 🎩 Trucos y atajos

| Truco | Cómo |
|---|---|
| Todos los ganchos, sobre todo | `uv run pre-commit run --all-files` |
| Solo un gancho | `uv run pre-commit run mypy --all-files` |
| Un commit sin un gancho | `SKIP=mypy git commit -m "..."` |
| El SHA de una etiqueta | `gh api repos/actions/checkout/commits/v7.0.1 --jq .sha` |
| El digest de una imagen | `docker buildx imagetools inspect python:3.14.10-slim-trixie \| grep Digest` |
| Qué falló en la CI | `gh run view --log-failed` |
| Las comprobaciones de tu *pull request* | `gh pr checks --watch` |
| Reproducir la CI en local | `GITHUB_ACTIONS=true uv run pytest` |
| Quién trae un paquete | `uv tree --invert --package urllib3` |
| Qué hay más nuevo | `uv tree --outdated` |

---

## 📌 Entregable

El único entregable es el **proyecto**, en tu dominio asignado:

1. ✅ Rama `week-21` de `python-<nombre>-<apellido>` con:
   - `.pre-commit-config.yaml`, `.github/workflows/ci.yml` y `.github/dependabot.yml`;
   - el `Dockerfile` en cuatro etapas y `compose.yaml` con `app` en `test` y `api` en `runtime`;
   - las dependencias `pre-commit==4.7.0`, `pyyaml==6.0.3` y `types-pyyaml==6.0.12.20260906` en `dev`, la versión `0.21.0` y al menos 6 tests propios en `tests/test_my_delivery.py`.

   Todo en verde en tu máquina, en Docker y en GitHub Actions.
2. ✅ `README.md` del repositorio con la insignia de la CI y la sección "Calidad y entrega"
3. ✅ Pull request `week-21` → `main` con:
   - las salidas de los ganchos, la cobertura, `alembic check` y el enlace a la CI en verde;
   - la tabla de medidas del paso 12;
   - la tabla de mutantes y el test que mata al superviviente;
   - por qué ruff y mypy son ganchos locales, y por qué cada acción va fijada a un SHA.

El cuestionario de la [rúbrica](rubrica-evaluacion.md) es tu autoevaluación: respóndelo antes de mirar las respuestas.

---

## ✅ Verificación

En tu proyecto:

```bash
docker compose up -d --wait db
uv run pre-commit run --all-files
uv run pytest
uv run coverage run -m pytest -q && uv run coverage report
uv run alembic upgrade head && uv run alembic check
uv audit --preview-features audit-command
uv run observatorio --version
docker compose build app api && docker compose run --rm app
docker compose up -d --wait api && curl -s http://127.0.0.1:8000/health
gh pr checks
```

Lo que debes ver:

- todos los ganchos en `Passed` (o `Skipped`);
- los tests terminan en `passed` sin `failed`, al menos 815;
- `coverage report` termina sin `Coverage failure`;
- `alembic check` dice `No new upgrade operations detected.`;
- `uv audit` dice `Found no known vulnerabilities`;
- `--version` escribe `observatorio 0.21.0`;
- `curl` escribe `{"status":"ok","version":"0.21.0"}`;
- `gh pr checks` con `quality`, `tests` e `image` en `pass`.

En los ejercicios, cada paso descomentado da la salida que muestra su README, con los tiempos y los números de avisos de tu máquina y tu fecha.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Semana 20](../week-20-fastapi_lo_justo_para_servir_tu_proyecto/README.md) | **Semana 21** | [Semana 22](../week-22-rendimiento_profiling_cprofile_py_spy_y_vectorizacion/README.md) |
