# Proyecto — studio-bc-manager

## Descripción

CLI de gestión de producción para Studio BC que integra las seis tecnologías de la Fase 2:
Typer + Rich, SQLModel, httpx async, Polars, asyncio, y type hints estrictos.

## Instalación

```bash
cd starter
pip install -e ".[dev]"
python main.py --help
```

## Comandos disponibles

```
manager clients list
manager clients create --name "Canal 9" --email prod@canal9.com
manager clients delete --id 1

manager projects list
manager projects list --client-id 1
manager projects create --name "Spot" --client-id 1 --budget 5000
manager projects update --id 1 --budget 7500
manager projects deactivate --id 1

manager assets list --project-id 1
manager assets add --project-id 1 --name intro.mp4 --type video --size-mb 450
manager assets tag --id 1 --tags hd,4k

manager report generate
manager report generate --export report.csv
manager report generate --export report.parquet
manager report kpis
manager report exchange --base USD
```

## Arquitectura

```
src/
├── commands/           # Typer — solo I/O de terminal
├── services/           # Lógica de negocio
├── repositories/       # Acceso a SQLModel
├── api_clients/        # httpx async
├── models.py           # SQLModel table=True
├── database.py         # engine, get_session_ctx
├── config.py           # pydantic-settings
└── exceptions.py       # errores de dominio
```

## Variables de entorno (.env)

```env
DATABASE_URL=sqlite:///studio.db
EXCHANGE_API_URL=https://open.er-api.com/v6/latest
EXCHANGE_API_KEY=
LOG_LEVEL=WARNING
```
