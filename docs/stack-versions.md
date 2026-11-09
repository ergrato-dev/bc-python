# Versiones del stack

Última revisión: 2026-11-05. Regla: versión completa pinada, nunca `latest`. Antes de fijar una versión: el tag existe, sin CVEs sin parchear (OSV), compatibilidad entre piezas.

| Pieza | Versión pinada | Verificación |
|---|---|---|
| Python | 3.14.10 (`python:3.14.10-slim-trixie`) | endoflife.date (2026-11-05): 3.14.10 publicada el 2026-10-25. 3.15.2 existe; se adopta cuando lo soporten las bibliotecas de data/IA (NumPy, PyTorch, scikit-learn). Los proyectos fijan `requires-python = ">=3.14,<3.15"`. |
| uv | 0.13.7 (`ghcr.io/astral-sh/uv:0.13.7`) | PyPI, publicada el 2026-11-03. Sin avisos en OSV. Equipo del autor con 0.12.2: actualizar con `uv self update`. |
| uv_build | 0.13.7 | PyPI (`uv-build`), la misma versión que uv. Sin avisos en OSV. Backend de build de los proyectos (`[build-system]`), fijado con `==` (semana 01). |
| pytest (transitivas) | iniconfig 2.3.1, packaging 26.3, pluggy 1.7.0, pygments 2.21.0 | Resueltas por uv 0.13.7 en los starters de la semana 01 (2026-11-05). Sin avisos en OSV. |
| ruff | 0.17.3 | PyPI, 2026-10-27. Sin avisos en OSV. Revisada en la semana 8 (2026-11-05): 0.17.4 salió ese mismo día y se espera a que madure. Desde la semana 8 va en el grupo `dev` de los proyectos, con mypy. |
| pytest | 9.2.0 | PyPI, 2026-10-27. Sin avisos en OSV. |
| mypy | 2.4.1 | PyPI, 2026-10-28. Sin avisos en OSV. |
| mypy (transitivas) | ast-serialize 0.13.1, librt 0.16.0, mypy-extensions 1.2.0, pathspec 1.1.1, typing-extensions 4.16.0 | Resueltas por uv 0.13.7 al añadir mypy al grupo `dev` del proyecto (semana 8, 2026-11-05). Sin avisos en OSV. |
| colorama | 0.4.6 | Transitiva de pytest, solo en Windows: está en `uv.lock` (que es universal) pero no se instala en Linux ni macOS. Sin avisos en OSV (2026-11-05). |
| pydantic | 2.14.2 | PyPI, 2026-10-29. Sin avisos en OSV (2026-11-06). 2.14.3 salió el 2026-11-05 y se espera a que madure. Primera dependencia del programa (no de `dev`): entra en la semana 13 con `uv add`. El plugin `pydantic.mypy` va en `[tool.mypy] plugins`. |
| pydantic (transitivas) | pydantic-core 2.50.2, annotated-types 0.8.0, typing-inspection 0.4.5, typing-extensions 4.16.0 | Resueltas por uv 0.13.7 al añadir pydantic (semana 13, 2026-11-06). Sin avisos en OSV. |
| hypothesis | 6.170.8 | PyPI, 2026-10-22. Sin avisos en OSV (2026-11-06). Hypothesis publica casi a diario: se fija la última con dos semanas (6.170.15 es del 2026-11-06). Entra en el grupo `dev` en la semana 14. |
| hypothesis (transitivas) | sortedcontainers 2.4.0 | Resuelta por uv 0.13.7 al añadir hypothesis (semana 14, 2026-11-06). Sin avisos en OSV. |
| coverage | 7.17.0 | PyPI, 2026-10-22. Sin avisos en OSV (2026-11-06). 7.17.2 salió el 2026-11-04 y se espera a que madure. Grupo `dev`, semana 14; sin dependencias. Se usa sin `pytest-cov`: `coverage run -m pytest`. |
| typer | 0.27.3 | PyPI, 2026-10-06. Sin avisos en OSV (2026-11-06). 0.28.0 salió el 2026-11-06 y se espera a que madure. Dependencia del programa desde la semana 15. Lleva Click dentro (`typer._click`): no aparece `click` en `uv.lock`. |
| rich | 15.0.0 | PyPI, 2026-04-12. Sin avisos en OSV (2026-11-06). Typer ya la trae, pero se fija aparte porque `cli.py` la importa directamente (semana 15). |
| typer y rich (transitivas) | shellingham 1.5.4, annotated-doc 0.0.5, markdown-it-py 4.2.0, mdurl 0.1.2 | Resueltas por uv 0.13.7 al añadir typer y rich (semana 15, 2026-11-06). Sin avisos en OSV. pygments 2.21.0 y colorama 0.4.6 ya estaban por pytest. |
| httpx | 0.28.1 | PyPI, 2024-12-06. Sin avisos en OSV (2026-11-06). Es la última estable: la serie 1.0 sigue en versiones `dev` (1.0.dev6, 2026-08-31) y no se usa. Dependencia del programa desde la semana 18 (`core/remote.py`). |
| pydantic-settings | 2.16.1 | PyPI, 2026-10-20. Sin avisos en OSV (2026-11-06). 2.16.2 salió el 2026-10-28 y se espera a que madure. Dependencia del programa desde la semana 18 (`settings.py`). |
| httpx y pydantic-settings (transitivas) | anyio 4.16.0, httpcore 1.0.9, h11 0.16.0, certifi 2026.10.23, idna 3.20, python-dotenv 1.2.4 | Resueltas por uv 0.13.7 al añadir httpx y pydantic-settings (semana 18, 2026-11-06). Sin avisos en OSV. anyio 4.16.0 es del 2026-11-01: uv elige la última, y se acepta por no tener avisos. certifi trae los certificados raíz con los que httpx comprueba HTTPS. |
| psycopg[binary] | 3.3.6 | PyPI, 2026-09-18. Sin avisos en OSV (2026-11-07). 3.3.7 y 3.3.8 tienen menos de dos semanas y se espera. El extra `binary` trae `psycopg-binary` 3.3.6, con `libpq` dentro. Dependencia del programa desde la semana 19 (*driver* de PostgreSQL). |
| sqlalchemy | 2.1.6 | PyPI, 2026-10-21. Sin avisos en OSV (2026-11-07). 2.1.7 y 2.1.8 tienen menos de dos semanas y se espera. En la serie 2.1, `postgresql://` usa psycopg 3 por defecto y `greenlet` ya no se instala. Dependencia del programa desde la semana 19 (`core/database.py`). |
| alembic | 1.20.1 | PyPI, 2026-10-22. Sin avisos en OSV (2026-11-07). Dependencia del programa desde la semana 19 (`migrations/`). |
| psycopg, sqlalchemy y alembic (transitivas) | psycopg-binary 3.3.6, mako 1.4.3, markupsafe 3.0.4, typing-extensions 4.16.0 | Resueltas por uv 0.13.7 al añadirlas (semana 19, 2026-11-07). Sin avisos en OSV. mako y markupsafe son las plantillas con las que Alembic escribe las migraciones. |
| fastapi | 0.162.0 | PyPI, 2026-10-23. Sin avisos en OSV (2026-11-08). 0.162.1 y 0.162.2 son del 2026-11-07 y se espera. Dependencia del programa desde la semana 20 (`api.py`). |
| uvicorn | 0.54.0 | PyPI, 2026-09-25. Sin avisos en OSV (2026-11-08). Servidor ASGI de `observatorio servir`, desde la semana 20. Sin el extra `[standard]`: no hacen falta `uvloop` ni `watchfiles`. |
| httpx2 | 2.16.0 | PyPI, 2026-10-21. Sin avisos en OSV (2026-11-08). Sucesor de httpx (pydantic/httpx2); Starlette 1.10 lo pide para `TestClient` y avisa si solo encuentra httpx. Grupo `dev` desde la semana 20: el programa sigue con httpx 0.28.1. |
| fastapi, uvicorn y httpx2 (transitivas) | starlette 1.10.0, opentelemetry-api 1.45.2, click 8.5.1, httpcore2 2.16.0, truststore 0.10.5 | Resueltas por uv 0.13.7 al añadirlas (semana 20, 2026-11-08). Sin avisos en OSV. starlette 1.10.0 es del 2026-10-24 y la fija fastapi. annotated-doc, anyio y h11 ya estaban. |
| pre-commit | 4.7.0 | PyPI, 2026-10-12. Sin avisos en OSV (2026-11-08). Grupo `dev` desde la semana 21. Desde 4.4, `language: unsupported` es el nombre nuevo de `system`. |
| pyyaml | 6.0.3 | PyPI, 2025-09-25. Sin avisos en OSV (2026-11-08). Ya venía con pre-commit; se declara en `dev` porque `test_delivery.py` lo importa (semana 21). |
| types-pyyaml | 6.0.12.20260906 | PyPI, 2026-09-06. Anotaciones de PyYAML para `mypy --strict` (semana 21). 6.0.12.20261030 y 20261103 son recientes y se espera. |
| pre-commit (transitivas) | cfgv 3.5.0, distlib 0.4.4, filelock 4.2.9, identify 2.6.20, nodeenv 1.12.0, platformdirs 4.14.5, virtualenv 21.15.6 | Resueltas por uv 0.13.7 al añadir pre-commit (semana 21, 2026-11-08). Sin avisos en OSV. |
| pre-commit-hooks | v6.0.0 (`3e8a8703264a2f4a69428a0aa4dcb512790b2c8c`) | GitHub pre-commit/pre-commit-hooks. Fijado por SHA con `autoupdate --freeze` (semana 21, 2026-11-08). |
| actions/checkout | v7.0.1 (`3d3c42e5aac5ba805825da76410c181273ba90b1`) | GitHub, SHA de la etiqueta comprobado con `gh api` (2026-11-08). Siempre con `persist-credentials: false`. |
| astral-sh/setup-uv | v10.3.2 (`07a047e608db84b3d8c06cd9a7c7dcc9c355c18e`) | GitHub (2026-11-08). v10.3.3 tenía 11 días y se espera; Dependabot la propondrá. Instala uv 0.13.7 (`version:` fijada). |
| `python:3.14.10-slim-trixie` | `sha256:9aaa474097d094040649f2162a627c0049b408f52138d980916788d80f04802f` | Docker Hub, digest del índice con `docker buildx imagetools inspect` (2026-11-08). Base de `builder` y `runtime` desde la semana 21. |
| `ghcr.io/astral-sh/uv:0.13.7` | `sha256:96f40d3904aad8d0bd010539001d36c8e2188b981e1334471a90c4a1d93bb490` | GHCR (2026-11-08). Etapa `uv` del `Dockerfile`. |
| `postgres:18.6-alpine` (digest) | `sha256:123b17998ccaf47e53b502e8c6a1e79afd8f579c6f3eec83c563da026f957395` | Docker Hub (2026-11-08). En `compose.yaml` y en el servicio de la CI desde la semana 21. |
| Trivy | `aquasec/trivy:0.76.1@sha256:790fd66d1697395d8693d1acaa1ea702406a20f109b6fc7bac8db623eca6c06c` | Docker Hub (2026-11-08). 0.76.2 tenía 3 días y se espera. Se usa la imagen por digest y no `aquasecurity/trivy-action`, cuyas etiquetas se movieron en marzo de 2026 (CVE-2026-33634). |
| actionlint | `rhysd/actionlint:1.7.12@sha256:b1934ee5f1c509618f2508e6eb47ee0d3520686341fec936f3b79331f9315667` | Docker Hub (2026-11-08). Revisión de workflows, semana 21. |
| Ejercicio 03, semana 21 (versiones viejas a propósito) | jinja2 3.1.4, requests 2.32.3, urllib3 2.2.3 y luego jinja2 3.1.6, requests 2.34.2, urllib3 2.8.0 | Las primeras tienen avisos conocidos para que `uv audit` los encuentre; las segundas, sin avisos en OSV (2026-11-08). Solo en el ejercicio. |
| py-spy | 0.4.2 | PyPI, 2026-04-24, sin avisos en OSV. Perfilador por muestreo, dependencia de desarrollo del proyecto y del ejercicio 03 (semana 22). Es la primera versión compatible con Python 3.14; 0.4.3 (2026-11-02) es reciente y se espera. En WSL2 escribe a veces `Error: No child process (os error 10)` al terminar en modo normal, sin afectar al gráfico (comprobado el 2026-11-08). |
| numpy | 2.5.4 | PyPI, 2026-10-10, sin avisos en OSV, ruedas `cp314` para Linux, macOS y Windows. Revisado el 2026-11-08: sigue siendo la última y sin avisos. Ejercicio 04 de la semana 22; dependencia del proyecto desde la semana 23 (comando `estadisticas`, +94 MB en la imagen `runtime`). |
| pandas | 3.1.0 | PyPI, 2026-10-22, sin avisos en OSV (consultado el 2026-11-08). 3.1.1 tenía 4 días y se espera. Ruedas `cp314` para Linux, macOS y Windows. Dependencia del proyecto desde la semana 24 (comando `filtrar`, importado solo dentro del comando: unos 0,29 s, NumPy incluido) y de los cuatro ejercicios de esa semana. La imagen `runtime` pasa de 395 MB a 508 MB. |
| pandas-stubs | 3.1.0.261029 | PyPI, 2026-10-29, sin avisos en OSV. Los tipos de pandas para mypy (pandas no trae `py.typed`); la versión es la de pandas más la fecha de los tipos. Dependencia de desarrollo del proyecto desde la semana 24. |
| python-dateutil y tzdata (transitivas de pandas) | 4.0.0 y 2026.6 | PyPI, sin avisos en OSV (2026-11-08). python-dateutil 4.0.0 (2026-11-01) es la que resuelve uv y ya depende de tzdata; ya no trae `six`. |
| Python free-threaded | 3.14.10t (`cpython-3.14.10+freethreaded`, gestionado por uv) | El mismo 3.14.10 compilado sin GIL (PEP 779: compatible oficialmente en 3.14). uv 0.13.7 lo descarga con `--python 3.14.10t` (comprobado el 2026-11-06). Solo para el ejercicio 03 y el paso 12 del proyecto de la semana 16, en un entorno aparte (`.venv-ft`); pydantic-core 2.50.2 tiene ruedas `cp314t` y la suite pasa con el GIL apagado. Las imágenes Docker siguen con el Python con GIL. |
| PostgreSQL | `postgres:18.6-alpine` | Docker Hub (2026-11-05). El volumen va en `/var/lib/postgresql` (cambio de la imagen 18). |
| Docker Engine | 29 o superior | Probado con 29.9.3 en el equipo del autor (2026-11-05). |
| Docker Compose | plugin `docker compose` v5 | Probado con v5.7.0. Nunca `docker-compose` (v1, EOL desde 2023). |

Las dependencias de cada semana se añaden a esta tabla cuando entran, con versión, fecha y resultado de OSV.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Proyecto hilo conductor](proyecto-hilo-conductor.md) | **Versiones del stack** | [Decisión de ritmo](decision-semanas.md) |

← [Volver al inicio del bootcamp](../README.md)
