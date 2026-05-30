# Sitios Web — Semana 30: Proyecto Fase 3

Esta semana no introduce tecnología nueva — integra todo lo visto en semanas 22–29.
Los recursos de cada semana anterior siguen siendo válidos. Aquí se listan los más útiles para la integración.

## Integración y arquitectura

| Recurso | Descripción |
|---------|-------------|
| [Python typing.Protocol](https://docs.python.org/3/library/typing.html#typing.Protocol) | Contratos sin herencia — base del Stage Protocol |
| [Python dataclasses](https://docs.python.org/3/library/dataclasses.html) | StageResult, JobRecord — modelos de datos inmutables |
| [Python pathlib](https://docs.python.org/3/library/pathlib.html) | Manipulación de rutas — esencial para paths de media |
| [Python queue](https://docs.python.org/3/library/queue.html) | Queue thread-safe para el watcher daemon |

## Por etapa del pipeline

| Etapa | Recurso clave |
|-------|---------------|
| Watcher | [watchdog Docs](https://python-watchdog.readthedocs.io/) |
| Transcode | [ffmpeg-python GitHub](https://github.com/kkroening/ffmpeg-python) |
| Cloud | [boto3 S3 Reference](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html) |
| Distribute | [Slack Incoming Webhooks](https://api.slack.com/messaging/webhooks) |
| Monitor | [Rich Live](https://rich.readthedocs.io/en/stable/live.html) |

## Testing con mocks

| Recurso | Descripción |
|---------|-------------|
| [pytest docs](https://docs.pytest.org/) | Fixtures, parametrize, capsys |
| [unittest.mock](https://docs.python.org/3/library/unittest.mock.html) | `patch`, `MagicMock`, `assert_called_once` |
| [pytest-cov](https://pytest-cov.readthedocs.io/) | Cobertura de código: `pytest --cov=src --cov-report=term-missing` |

## Configuración y herramientas

| Recurso | Descripción |
|---------|-------------|
| [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) | Variables de entorno tipadas desde `.env` |
| [mypy strict mode](https://mypy.readthedocs.io/en/stable/command_line.html#cmdoption-mypy-strict) | `mypy --strict src/` — cero errores de tipo |
| [LocalStack](https://docs.localstack.cloud/) | Emulación local de S3 para tests sin costo |
