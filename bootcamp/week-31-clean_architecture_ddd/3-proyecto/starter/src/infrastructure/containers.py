"""DI Container — configura e inyecta las dependencias."""
from __future__ import annotations

from dependency_injector import containers, providers
from pathlib import Path

from .json_repository import JsonJobRepository
from .memory_repository import InMemoryJobRepository
from .s3_adapter import S3AssetStore
from ..application.use_cases import ProcessAssetUseCase, GetJobStatusUseCase


class Container(containers.DeclarativeContainer):
    """
    TODO: Definir los providers:

    config = providers.Configuration()

    job_repository = providers.Singleton(
        JsonJobRepository,
        state_path=config.state_file,   # Path(.pipeline_state.json)
    )

    asset_store = providers.Singleton(
        S3AssetStore,
        bucket=config.s3_bucket,
        region=config.aws_region,
        dry_run=config.dry_run,
    )

    process_use_case = providers.Factory(
        ProcessAssetUseCase,
        job_repo=job_repository,
        asset_store=asset_store,
    )

    get_status_use_case = providers.Factory(
        GetJobStatusUseCase,
        job_repo=job_repository,
    )

    Referencia: ejercicio 04 — Container
    """
    pass
