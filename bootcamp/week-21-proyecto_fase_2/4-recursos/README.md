# Recursos — Semana 21: Proyecto Integrador Fase 2

## Documentación oficial

- [Typer — Building CLIs](https://typer.tiangolo.com/) — referencia completa del framework CLI
- [Rich — Console markup](https://rich.readthedocs.io/en/latest/markup.html) — tablas, paneles, estilos
- [SQLModel — Tutorial](https://sqlmodel.tiangolo.com/tutorial/) — CRUD, relaciones, sesiones
- [Alembic — Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html) — migraciones autogeneradas
- [httpx — Async Client](https://www.python-httpx.org/async/) — cliente HTTP asíncrono
- [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) — configuración desde `.env`
- [Polars — User Guide](https://docs.pola.rs/user-guide/) — transformaciones de DataFrames
- [pytest — Fixtures](https://docs.pytest.org/en/latest/reference/fixtures.html) — fixture scope, conftest.py

## Artículos y guías

- [The Clean Architecture (Robert C. Martin)](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) — principio de dependencia
- [Repository Pattern in Python](https://www.cosmicpython.com/book/chapter_02_repository.html) — Cosmic Python, Harry Percival
- [Dependency Injection without frameworks](https://testdriven.io/blog/python-dependency-injection/) — inyección manual de dependencias
- [Integration Testing with pytest and SQLite `:memory:`](https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#connect-strings) — motores en memoria
- [asyncio.run() in sync code](https://docs.python.org/3/library/asyncio-runner.html) — puente sync/async

## Videos

- [Arch Patterns with Python — PyCon 2020](https://www.youtube.com/watch?v=RS0yOFkWtK0) — Repository y Service Layer
- [SQLModel Full Tutorial (Sebastián Ramírez)](https://www.youtube.com/watch?v=9UaZtOsnHBg) — SQLModel completo
- [Testing FastAPI / Typer apps](https://www.youtube.com/watch?v=7DqHlh0aFp8) — CliRunner y fixtures
- [Polars vs Pandas (performance)](https://www.youtube.com/watch?v=GTNfAzrqBTE) — cuándo elegir Polars

## Herramientas del proyecto

| Herramienta | Versión | Propósito |
|-------------|---------|-----------|
| `typer` | ≥0.12 | CLI con subcomandos |
| `rich` | ≥13 | Renderizado de tablas y errores |
| `sqlmodel` | ≥0.0.19 | ORM + modelos Pydantic |
| `alembic` | ≥1.13 | Migraciones de esquema |
| `httpx` | ≥0.27 | Cliente HTTP async |
| `tenacity` | ≥8.3 | Reintentos con backoff |
| `pydantic-settings` | ≥2.3 | Configuración con `.env` |
| `polars` | ≥0.20 | Reportes y transformaciones |
| `pytest` | ≥8 | Suite de tests |
| `pytest-asyncio` | ≥0.23 | Tests async |

## Complementario

- [Twelve-Factor App — Config](https://12factor.net/config) — variables de entorno como configuración
- [Cosmic Python — Service Layer](https://www.cosmicpython.com/book/chapter_04_service_layer.html) — separación CLI/lógica
- [tenacity docs](https://tenacity.readthedocs.io/) — estrategias de retry avanzadas
- [ExchangeRate API — open.er-api.com](https://www.exchangerate-api.com/docs/free) — API de tipos de cambio usada en el proyecto
