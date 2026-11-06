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
