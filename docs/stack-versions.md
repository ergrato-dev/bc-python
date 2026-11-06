# Versiones del stack

Última revisión: 2026-11-05. Regla: versión completa pinada, nunca `latest`. Antes de fijar una versión: el tag existe, sin CVEs sin parchear (OSV), compatibilidad entre piezas.

| Pieza | Versión pinada | Verificación |
|---|---|---|
| Python | 3.14.10 (`python:3.14.10-slim-trixie`) | endoflife.date (2026-11-05): 3.14.10 publicada el 2026-10-25. 3.15.2 existe; se adopta cuando lo soporten las bibliotecas de data/IA (NumPy, PyTorch, scikit-learn). Los proyectos fijan `requires-python = ">=3.14,<3.15"`. |
| uv | 0.13.7 (`ghcr.io/astral-sh/uv:0.13.7`) | PyPI, publicada el 2026-11-03. Sin avisos en OSV. Equipo del autor con 0.12.2: actualizar con `uv self update`. |
| ruff | 0.17.3 | PyPI. Sin avisos en OSV. Hay 0.17.4 (2026-11-05), se revisa en la semana 8. |
| pytest | 9.2.0 | PyPI, 2026-10-27. Sin avisos en OSV. |
| mypy | 2.4.1 | PyPI, 2026-10-28. Sin avisos en OSV. |
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
