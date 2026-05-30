# DDD Básico — Entities, Value Objects, Aggregates y Domain Events

## 1. Entity — Identidad que persiste en el tiempo

Una **Entity** tiene identidad única. Dos objetos con los mismos datos pero distinto ID son entidades distintas.

```python
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
import uuid


class JobStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    DONE = "done"
    FAILED = "failed"


@dataclass
class Job:
    job_id: str
    asset_path: str
    project: str
    status: JobStatus = JobStatus.PENDING
    error: str | None = None
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Job):
            return NotImplemented
        return self.job_id == other.job_id  # identidad, no valores

    def __hash__(self) -> int:
        return hash(self.job_id)

    @classmethod
    def create(cls, asset_path: str, project: str) -> "Job":
        return cls(job_id=str(uuid.uuid4())[:8], asset_path=asset_path, project=project)

    # Comportamiento de dominio:
    def start(self) -> None:
        if self.status != JobStatus.PENDING:
            raise ValueError(f"No se puede iniciar un job en estado {self.status}")
        self.status = JobStatus.RUNNING

    def complete(self) -> None:
        self.status = JobStatus.DONE

    def fail(self, error: str) -> None:
        self.status = JobStatus.FAILED
        self.error = error
```

El método `start()` encapsula la regla de negocio: solo se puede iniciar desde PENDING. Esta lógica vive en el dominio, no en el service.

---

## 2. Value Object — Igualdad por valor, sin identidad

Un **Value Object** no tiene ID. Dos objetos con los mismos valores son el mismo concepto.

```python
from __future__ import annotations
from dataclasses import dataclass
import re


@dataclass(frozen=True)  # frozen=True → inmutable + __hash__ automático
class ProjectSlug:
    """'canal9/spot-verano-2024' — formato cliente/proyecto."""
    value: str

    def __post_init__(self) -> None:
        if not re.match(r"^[a-z0-9_-]+/[a-z0-9_-]+$", self.value):
            raise ValueError(
                f"ProjectSlug inválido: '{self.value}'. "
                "Formato esperado: 'cliente/proyecto' (solo minúsculas, guiones y números)"
            )

    @property
    def client(self) -> str:
        return self.value.split("/")[0]

    @property
    def project(self) -> str:
        return self.value.split("/")[1]

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class MediaType:
    value: str

    _VALID = {"video", "audio", "image", "document", "other"}

    def __post_init__(self) -> None:
        if self.value not in self._VALID:
            raise ValueError(f"MediaType inválido: '{self.value}'")

    @classmethod
    def from_extension(cls, ext: str) -> "MediaType":
        mapping = {
            ".mp4": "video", ".mov": "video", ".mxf": "video",
            ".mp3": "audio", ".wav": "audio", ".flac": "audio",
            ".jpg": "image", ".png": "image", ".tif": "image",
            ".pdf": "document", ".docx": "document",
        }
        return cls(mapping.get(ext.lower(), "other"))
```

```python
# Value Objects son iguales por valor
slug1 = ProjectSlug("canal9/spot")
slug2 = ProjectSlug("canal9/spot")
assert slug1 == slug2  # True — mismo valor

# Son inmutables
# slug1.value = "otro"  # TypeError: cannot assign to field

# Encapsulan validación
# ProjectSlug("INVALIDO")  # ValueError
```

---

## 3. Aggregate — Consistencia transaccional

Un **Aggregate** es un grupo de entidades y value objects que se tratan como una unidad para cambios de estado. El **Aggregate Root** es la única entrada al aggregate.

```python
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Asset:
    """Aggregate Root — encapsula el archivo y sus outputs."""
    asset_id: str
    original_path: str
    project: ProjectSlug
    media_type: MediaType
    proxy_path: str | None = None
    web_path: str | None = None
    thumb_path: str | None = None
    s3_url: str | None = None

    @classmethod
    def from_path(cls, path: Path, project: ProjectSlug) -> "Asset":
        ext = path.suffix.lower()
        return cls(
            asset_id=str(uuid.uuid4())[:8],
            original_path=str(path),
            project=project,
            media_type=MediaType.from_extension(ext),
        )

    def set_transcoded(self, proxy: str, web: str, thumb: str) -> None:
        """Regla de dominio: solo se puede establecer si media_type es video."""
        if self.media_type.value != "video":
            raise ValueError("Solo los videos tienen proxy/web/thumb")
        self.proxy_path = proxy
        self.web_path = web
        self.thumb_path = thumb

    def set_uploaded(self, s3_url: str) -> None:
        self.s3_url = s3_url

    @property
    def stem(self) -> str:
        return Path(self.original_path).stem
```

---

## 4. Domain Events

Los eventos de dominio representan hechos que han ocurrido. Se usan para comunicación entre aggregates o para notificar efectos secundarios.

```python
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass(frozen=True)
class DomainEvent:
    occurred_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


@dataclass(frozen=True)
class JobCreated(DomainEvent):
    job_id: str = ""
    asset_path: str = ""
    project: str = ""


@dataclass(frozen=True)
class JobCompleted(DomainEvent):
    job_id: str = ""
    s3_url: str = ""


@dataclass(frozen=True)
class JobFailed(DomainEvent):
    job_id: str = ""
    error: str = ""
    stage: str = ""
```

Los eventos son inmutables (frozen=True) porque representan algo que ya ocurrió — no se puede cambiar el pasado.

---

## 5. Cuándo usar Entity vs Value Object

| Pregunta | Entity | Value Object |
|----------|--------|-------------|
| ¿Tiene identidad única? | Sí | No |
| ¿Cambia con el tiempo? | Sí | No (inmutable) |
| ¿Dos objetos iguales son intercambiables? | No | Sí |
| Ejemplo Studio BC | `Job`, `Asset` | `ProjectSlug`, `MediaType`, `S3Key` |

---

## Resumen

| Concepto | Característica |
|----------|----------------|
| Entity | Tiene `id` único, mutable, `__eq__` por id |
| Value Object | Sin id, `frozen=True`, `__eq__` por valor |
| Aggregate | Grupo de entidades con un Root — entrada única |
| Domain Event | Hecho inmutable que describe algo que ocurrió |
| Regla de dominio | Lógica de negocio que vive en la entity, no en el service |
