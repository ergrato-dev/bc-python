# Proyecto hilo conductor: Observatorio de datos

Un sistema en Python que **recoge, guarda, analiza y predice** datos de tu dominio ([dominios.md](dominios.md)), y al final responde preguntas en lenguaje natural sobre ellos. Cada semana añade una capa al mismo repositorio: nada se descarta, todo se mejora.

| Fase | Semanas | Qué crece |
|---|---|---|
| 1 Fundamentos | 1-8 | Paquete `core`: modelo de registros del dominio, validación, lectura y escritura de CSV/JSON, resúmenes en consola. Se vuelve un proyecto `uv` con `pyproject.toml`, `uv.lock`, ruff y tests. |
| 2 Python idiomático | 9-15 | El modelo pasa a `dataclasses` y Pydantic con tipado estricto (mypy). Tests con fixtures, mocks y Hypothesis. Cierra con la CLI `observatorio` (Typer + Rich). |
| 3 Python profesional | 16-22 | Ingesta concurrente desde una API o un portal de datos abiertos, persistencia en PostgreSQL con migraciones (Alembic), una API mínima con FastAPI, CI en GitHub Actions e imagen Docker segura. |
| 4 Data science | 23-30 | Análisis con NumPy, pandas, Polars y DuckDB; gráficos; estadística; un notebook reproducible y un informe de hallazgos del dominio. |
| 5 IA y ML | 31-42 | Un modelo predictivo (scikit-learn, luego PyTorch), NLP sobre el texto libre, un asistente con RAG sobre pgvector, un agente con herramientas (MCP), el modelo servido y monitorizado (MLflow + FastAPI), revisión de seguridad y capstone. |

## Reglas

- Un repositorio por aprendiz: `bc-python-<tu-dominio>`.
- Una rama y un *pull request* por semana (`week-NN` → `main`).
- Nombres de código en inglés; datos y textos visibles en el idioma del dominio.
- Todo corre con `docker compose up` desde la fase 3; antes, con `uv run`.
- `pyproject.toml` y `uv.lock` siempre en el repositorio. Nunca `requirements.txt` hecho a mano.
- Secretos (claves de API, contraseñas de PostgreSQL) en `.env`, nunca en el repositorio. `.env.example` sí se sube.

---

## 🔗 Navegación

| Anterior | Actual | Siguiente |
| -------- | ------ | --------- |
| [Dominios](dominios.md) | **Proyecto hilo conductor** | [Versiones del stack](stack-versions.md) |

← [Volver al inicio del bootcamp](../README.md)
