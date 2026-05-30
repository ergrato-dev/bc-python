# Clean Architecture

## 1. El Problema que Resuelve

Cuando el código de negocio (lógica de qué hace el sistema) mezcla código de infraestructura (cómo guarda datos, cómo llama a APIs), ocurre:

- Para testear la lógica de negocio hay que tener una BD real
- Cambiar de SQLite a Postgres requiere tocar código de negocio
- Añadir una nueva interfaz (CLI → API REST) requiere duplicar lógica

Clean Architecture separa explícitamente estas preocupaciones en capas.

---

## 2. Las Capas

```
┌──────────────────────────────────────┐
│         Presentation (CLI, API)      │  ← Frameworks, drivers
├──────────────────────────────────────┤
│      Infrastructure (S3, Slack, DB)  │  ← Adapters
├──────────────────────────────────────┤
│          Application (Use Cases)     │  ← Business logic orchestration
├──────────────────────────────────────┤
│           Domain (Entities, VOs)     │  ← Core business rules
└──────────────────────────────────────┘
```

| Capa | Responsabilidad | Puede importar |
|------|-----------------|----------------|
| `domain` | Entidades, Value Objects, interfaces | Solo stdlib Python |
| `application` | Use Cases, Services | Solo `domain` |
| `infrastructure` | S3, Slack, SQLite, JSON | `domain` + `application` |
| `presentation` | CLI, API, UI | `application` + `infrastructure` (vía DI) |

---

## 3. La Regla de Dependencias

**Las dependencias solo apuntan hacia adentro.**

```
presentation → application → domain
infrastructure → domain (implements interfaces)
```

`domain` no importa nada de infraestructura. `application` tampoco.

```python
# CORRECTO — application usa la INTERFAZ del dominio
from studio.domain.repositories import IJobRepository

class ProcessAssetUseCase:
    def __init__(self, job_repo: IJobRepository) -> None:
        self._repo = job_repo

# INCORRECTO — application importa infraestructura directamente
from boto3 import client  # ← esto no debería estar en application
```

---

## 4. Ports & Adapters (Hexagonal Architecture)

Clean Architecture y Hexagonal Architecture comparten el mismo principio:

- **Port**: Interface (abstracta) definida en el dominio/aplicación
- **Adapter**: Implementación concreta en infraestructura

```python
# Port — en domain/
from typing import Protocol

class IJobRepository(Protocol):
    def save(self, job: "Job") -> None: ...
    def find_by_id(self, job_id: str) -> "Job | None": ...

# Adapter — en infrastructure/
class JsonJobRepository:
    def save(self, job: "Job") -> None:
        # escribe en .pipeline_state.json
        ...

    def find_by_id(self, job_id: str) -> "Job | None":
        # lee de .pipeline_state.json
        ...
```

El use case recibe `IJobRepository`. En producción recibe `JsonJobRepository`. En tests recibe `InMemoryJobRepository`.

---

## 5. Ejemplo Completo de Estructura

```
studio_refactored/
├── domain/
│   ├── entities.py        # Asset, Job
│   ├── value_objects.py   # ProjectSlug, MediaType, S3Key
│   ├── repositories.py    # IJobRepository, IAssetRepository (Protocols)
│   └── events.py          # JobCreated, JobCompleted, JobFailed
├── application/
│   ├── use_cases.py       # ProcessAssetUseCase, GetJobStatusUseCase
│   └── services.py        # PipelineService (orquesta use cases)
├── infrastructure/
│   ├── json_repository.py # JsonJobRepository — implements IJobRepository
│   ├── s3_adapter.py      # S3AssetStore — implements IAssetStore
│   └── slack_adapter.py   # SlackNotifier — implements INotifier
└── presentation/
    └── cli.py             # Typer CLI — usa DI container
```

---

## 6. ¿Cuándo Aplicar Clean Architecture?

| Contexto | Recomendación |
|----------|---------------|
| Script de 50 líneas | No aplica — over-engineering |
| Servicio con múltiples adapters (S3, Drive, local) | Aplica Repository Pattern |
| Sistema con tests unitarios de la lógica de negocio | Aplica separación domain/application |
| Sistema que cambia de BD o plataforma | Aplica Ports & Adapters |

---

## Resumen

| Concepto | Clave |
|----------|-------|
| Capa Domain | Solo lógica de negocio pura — sin imports externos |
| Capa Application | Orquesta el dominio — sin imports de infraestructura |
| Capa Infrastructure | Implementa ports del dominio con tecnología concreta |
| Regla de dependencias | Siempre hacia adentro: infra → app → domain |
| Port | Interface definida en domain/application |
| Adapter | Implementación en infrastructure que cumple el Port |
