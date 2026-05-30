# Dependency Injection

## 1. El Problema sin DI

```python
# Sin DI — dependencias hardcodeadas
class ProcessAssetUseCase:
    def __init__(self) -> None:
        self._repo = JsonJobRepository()        # ← hardcodeado
        self._store = S3AssetStore("mi-bucket") # ← hardcodeado
```

Para cambiar de S3 a Drive, o para testear con mocks, hay que modificar el use case.

---

## 2. DI Manual — Constructor Injection

La forma más simple: pasar las dependencias por el constructor.

```python
# Con DI manual — dependencias inyectadas
class ProcessAssetUseCase:
    def __init__(
        self,
        job_repo: IJobRepository,
        asset_store: IAssetStore,
    ) -> None:
        self._repo = job_repo
        self._store = asset_store


# En producción:
repo = JsonJobRepository(Path(".pipeline_state.json"))
store = S3AssetStore(bucket="studio-bc-prod", region="us-east-1")
use_case = ProcessAssetUseCase(repo, store)

# En tests:
repo = InMemoryJobRepository()
store = FakeAssetStore()
use_case = ProcessAssetUseCase(repo, store)
```

DI manual es suficiente para la mayoría de los casos. Para sistemas grandes, un container ayuda.

---

## 3. `dependency-injector` — Container Declarativo

```bash
pip install dependency-injector
```

```python
# infrastructure/containers.py
from __future__ import annotations

from dependency_injector import containers, providers
from pathlib import Path
import os

from ..infrastructure.json_repository import JsonJobRepository
from ..infrastructure.s3_adapter import S3AssetStore
from ..application.use_cases import ProcessAssetUseCase


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    job_repository = providers.Singleton(
        JsonJobRepository,
        state_path=config.state_file,
    )

    asset_store = providers.Singleton(
        S3AssetStore,
        bucket=config.s3_bucket,
        region=config.aws_region,
        dry_run=config.dry_run,
    )

    process_asset_use_case = providers.Factory(
        ProcessAssetUseCase,
        job_repo=job_repository,
        asset_store=asset_store,
    )
```

```python
# presentation/cli.py
from dependency_injector.wiring import Provide, inject
from ..infrastructure.containers import Container

import typer
app = typer.Typer()


@app.command()
@inject
def run(
    path: str = typer.Argument(...),
    use_case: ProcessAssetUseCase = Provide[Container.process_asset_use_case],
) -> None:
    job = use_case.execute(path, "canal9/spot")
    typer.echo(f"Job {job.job_id}: {job.status}")


if __name__ == "__main__":
    container = Container()
    container.config.from_dict({
        "state_file": ".pipeline_state.json",
        "s3_bucket": "studio-bc-prod",
        "aws_region": "us-east-1",
        "dry_run": True,
    })
    container.wire(modules=["presentation.cli"])
    app()
```

---

## 4. Tipos de Providers en `dependency-injector`

| Provider | Comportamiento | Cuándo usar |
|----------|----------------|-------------|
| `Singleton` | Una sola instancia por container | Repos, connections |
| `Factory` | Nueva instancia en cada llamada | Use cases, requests |
| `Configuration` | Parámetros desde dict/env/yaml | Config, settings |
| `Resource` | Con lifecycle (init/teardown) | DB connections, pools |

---

## 5. Alternativa: `dishka`

`dishka` es una librería más moderna y Pythónica para DI:

```bash
pip install dishka
```

```python
from dishka import Provider, Scope, provide, make_container
from ..domain.repositories import IJobRepository
from ..infrastructure.json_repository import JsonJobRepository


class AppProvider(Provider):
    scope = Scope.APP

    @provide
    def job_repository(self) -> IJobRepository:
        return JsonJobRepository()

    @provide
    def process_use_case(self, repo: IJobRepository) -> ProcessAssetUseCase:
        return ProcessAssetUseCase(repo, S3AssetStore(...))


container = make_container(AppProvider())

with container() as c:
    use_case = c.get(ProcessAssetUseCase)
    job = use_case.execute("clip.mp4", "canal9/spot")
```

---

## 6. DI para Tests — Override del Container

```python
# tests/test_use_case.py
from dependency_injector import providers
from ..infrastructure.containers import Container
from ..infrastructure.memory_repository import InMemoryJobRepository


def test_process_asset_with_di() -> None:
    container = Container()
    container.config.from_dict({
        "state_file": ":memory:",
        "s3_bucket": "test",
        "aws_region": "us-east-1",
        "dry_run": True,
    })

    # Override: reemplazar el repositorio real con uno en memoria
    container.job_repository.override(
        providers.Singleton(InMemoryJobRepository)
    )

    use_case = container.process_asset_use_case()
    job = use_case.execute("clip.mp4", "test/proj")
    assert job.status == "done"
```

---

## Resumen

| Técnica | Cuándo |
|---------|--------|
| DI manual (constructor) | Proyectos pequeños/medianos — claro y sin magia |
| `dependency-injector` Singleton | Servicios que se crean una vez (repos, stores) |
| `dependency-injector` Factory | Objetos que se crean por request (use cases) |
| Container override en tests | Reemplazar infra real por mocks sin modificar código |
| `dishka` | Alternativa más moderna, ideal con async |
