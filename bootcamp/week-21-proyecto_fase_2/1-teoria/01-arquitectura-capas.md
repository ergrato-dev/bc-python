# Arquitectura en Capas

## Objetivos

- Entender por qué una aplicación real necesita capas separadas
- Mapear cada tecnología de la Fase 2 a su capa correcta
- Reconocer violaciones de capa y cómo corregirlas

---

## 1. El problema sin capas

Una CLI pequeña puede crecer hasta volverse imposible de mantener si mezcla responsabilidades:

```python
# ANTI-PATRÓN — todo mezclado en el comando
@app.command()
def create_project(name: str, client_id: int, budget: float) -> None:
    # SQL directo en el comando
    with Session(engine) as session:
        client = session.get(Client, client_id)
        if not client:
            typer.echo("Cliente no encontrado"); raise typer.Exit(1)
        project = Project(name=name, client_id=client_id, budget=budget)
        session.add(project); session.commit(); session.refresh(project)

    # HTTP directo en el comando
    import httpx
    r = httpx.get(f"https://api.exchange.bc/usd", timeout=5)
    usd_rate = r.json()["rate"]

    # Polars inline en el comando
    import polars as pl
    df = pl.DataFrame({"name": [name], "budget_usd": [budget / usd_rate]})
    typer.echo(df)
```

Problemas:
- Imposible testear sin CLI, sin DB real, sin red
- Cambiar la API externa requiere tocar el comando
- Cambiar la DB requiere tocar el comando
- Un cambio rompe todo simultáneamente

---

## 2. La arquitectura en 4 capas

```
┌─────────────────────────────────────────────────┐
│  CLI (Typer + Rich)                             │  ← Capa 1: Presentación
│  commands/clients.py, projects.py, report.py   │
└────────────────────┬────────────────────────────┘
                     │ llama a
┌────────────────────▼────────────────────────────┐
│  Services                                       │  ← Capa 2: Lógica de negocio
│  services/project_service.py                   │
│  services/report_service.py                    │
│  services/exchange_service.py                  │
└──────────┬──────────────────────┬───────────────┘
           │ usa                  │ usa
┌──────────▼──────────┐  ┌───────▼───────────────┐
│  Repositories       │  │  External APIs        │  ← Capa 3: Acceso a datos
│  repos/project.py   │  │  clients/exchange.py  │
│  repos/asset.py     │  │  (httpx async)        │
└──────────┬──────────┘  └───────────────────────┘
           │ usa
┌──────────▼──────────┐
│  Database / Models  │  ← Capa 4: Infraestructura
│  SQLModel + SQLite  │
│  Polars DataFrames  │
└─────────────────────┘
```

---

## 3. Responsabilidad de cada capa

### Capa 1 — CLI (Typer + Rich)

**Solo hace:**
- Parsear argumentos y opciones del usuario
- Llamar al servicio correspondiente
- Renderizar el resultado con Rich (tabla, panel, error)
- Manejar `typer.Exit` con códigos de error

**No hace:** queries SQL, llamadas HTTP, transformaciones de datos

```python
# commands/projects.py
@projects_app.command("list")
def projects_list(
    client_id: int | None = typer.Option(None, help="Filtrar por cliente"),
) -> None:
    with get_session_ctx() as session:
        projects = project_service.list_active(session, client_id=client_id)
    _render_projects_table(projects)   # Rich
```

### Capa 2 — Servicios

**Solo hace:**
- Orquestar repositorios y clientes HTTP
- Aplicar reglas de negocio (validaciones, cálculos)
- Coordinar transacciones que involucran varios repositorios

**No hace:** Rich, Typer, SQL directo, parseo de respuestas HTTP

```python
# services/project_service.py
class ProjectService:
    def create(
        self,
        session: Session,
        name: str,
        client_id: int,
        budget: float,
    ) -> Project:
        client = client_repo.get(session, client_id)
        if client is None:
            raise ValueError(f"Cliente {client_id} no existe")
        return project_repo.create(session, Project(
            name=name, client_id=client_id, budget=budget
        ))
```

### Capa 3 — Repositorios y clientes HTTP

Los repositorios solo ejecutan queries. Los clientes HTTP solo hacen llamadas y validan con Pydantic. Sin lógica de negocio.

### Capa 4 — Infraestructura

Modelos SQLModel, engine, configuración. No se importa desde la capa CLI directamente.

---

## 4. La regla de la dependencia

Las capas solo dependen **hacia adentro** (hacia la infraestructura), nunca hacia afuera:

```
CLI → Services → Repositories → Database
         ↓
    API Clients → External APIs
```

Si un repositorio importa algo de `commands/`, hay una violación de capa.

---

## 5. Estructura de directorios

```
studio-bc-manager/
├── src/
│   ├── commands/           # Capa 1 — Typer
│   │   ├── clients.py
│   │   ├── projects.py
│   │   ├── assets.py
│   │   └── report.py
│   ├── services/           # Capa 2 — Lógica
│   │   ├── project_service.py
│   │   ├── report_service.py
│   │   └── exchange_service.py
│   ├── repositories/       # Capa 3a — DB
│   │   ├── base.py
│   │   ├── client.py
│   │   └── project.py
│   ├── api_clients/        # Capa 3b — HTTP
│   │   └── exchange.py
│   ├── models.py           # Capa 4 — SQLModel
│   ├── database.py         # engine, get_session
│   └── config.py           # Settings desde env
├── tests/
├── main.py
└── pyproject.toml
```

---

## ✅ Resumen

| Capa | Tecnología | Regla |
|------|-----------|-------|
| CLI | Typer + Rich | Solo I/O de terminal |
| Services | Python puro | Orquesta, no implementa |
| Repositories | SQLModel `Session` | Solo SQL |
| API Clients | httpx async | Solo HTTP |
| Models | SQLModel `table=True` | Solo estructura |
| Config | pydantic-settings | Solo configuración |
