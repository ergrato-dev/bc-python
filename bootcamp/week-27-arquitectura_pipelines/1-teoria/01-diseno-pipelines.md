# Diseño de Pipelines

## 1. ¿Qué es un Pipeline?

Un **pipeline** es una cadena de etapas donde la salida de cada etapa es la entrada de la siguiente. Cada etapa tiene una única responsabilidad; el pipeline coordina el flujo.

```
Input → [Ingest] → [Validate] → [Process] → [Export] → Output
```

Ventajas de este modelo:
- Cada etapa es testeable de forma aislada
- Las etapas son intercambiables si respetan el mismo contrato
- Se puede insertar logging, retry o branching entre etapas sin modificarlas

---

## 2. Contrato de Etapa con `Protocol`

En lugar de herencia, usamos `Protocol` para definir el contrato. Cualquier clase con el método correcto cumple el protocolo sin heritar nada.

```python
from __future__ import annotations
from typing import Protocol
from dataclasses import dataclass
from pathlib import Path


@dataclass
class StageResult:
    success: bool
    data: dict[str, object]
    error: str | None = None


class Stage(Protocol):
    name: str

    def process(self, data: dict[str, object]) -> StageResult:
        ...
```

Una etapa concreta:

```python
class IngestStage:
    name = "ingest"

    def process(self, data: dict[str, object]) -> StageResult:
        path = Path(str(data.get("path", "")))
        if not path.exists():
            return StageResult(success=False, data=data, error=f"No existe: {path}")
        size = path.stat().st_size
        return StageResult(
            success=True,
            data={**data, "size_bytes": size, "stem": path.stem},
        )
```

`IngestStage` no hereda de `Stage` — pero como implementa `process`, mypy lo acepta donde se espera un `Stage`.

---

## 3. Pipeline Lineal

```python
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)


class Pipeline:
    def __init__(self, stages: list[Stage]) -> None:
        self._stages = stages

    def run(self, initial_data: dict[str, object]) -> StageResult:
        data = initial_data
        for stage in self._stages:
            logger.info("Etapa [%s] — inicio", stage.name)
            result = stage.process(data)
            if not result.success:
                logger.error("Etapa [%s] — FALLO: %s", stage.name, result.error)
                return result
            logger.info("Etapa [%s] — OK", stage.name)
            data = result.data

        return StageResult(success=True, data=data)
```

### Uso

```python
pipeline = Pipeline([
    IngestStage(),
    ValidateStage(),
    TranscodeStage(),
    ExportStage(),
])

result = pipeline.run({"path": "footage/entrevista.mp4", "project": "canal9/spot"})
if result.success:
    print("Pipeline completado:", result.data)
else:
    print("Pipeline fallido:", result.error)
```

---

## 4. Pipeline Ramificado

A veces la siguiente etapa depende del resultado de la anterior. Usamos un `dict` de rutas:

```python
from __future__ import annotations
from typing import Callable

StageRoute = Callable[[StageResult], str]  # devuelve nombre de siguiente etapa


class BranchingPipeline:
    def __init__(self) -> None:
        self._stages: dict[str, Stage] = {}
        self._routes: dict[str, StageRoute] = {}
        self._entry: str = ""

    def add_stage(self, stage: Stage, route: StageRoute | None = None) -> "BranchingPipeline":
        self._stages[stage.name] = stage
        if route:
            self._routes[stage.name] = route
        if not self._entry:
            self._entry = stage.name
        return self

    def run(self, data: dict[str, object]) -> StageResult:
        current = self._entry
        while current:
            stage = self._stages[current]
            result = stage.process(data)
            if not result.success:
                return result
            data = result.data
            route = self._routes.get(current)
            current = route(result) if route else ""
        return StageResult(success=True, data=data)
```

---

## 5. Composición: Stage que envuelve otro

```python
class LoggingStage:
    """Decorador de etapa que agrega logging sin modificar la etapa original."""

    def __init__(self, inner: Stage) -> None:
        self.name = f"logged:{inner.name}"
        self._inner = inner

    def process(self, data: dict[str, object]) -> StageResult:
        print(f"→ [{self._inner.name}] datos de entrada: {list(data.keys())}")
        result = self._inner.process(data)
        print(f"← [{self._inner.name}] éxito={result.success}")
        return result
```

---

## Resumen

| Concepto | Descripción |
|----------|-------------|
| `Stage` Protocol | Contrato sin herencia: cualquier clase con `process()` lo cumple |
| `StageResult` | Objeto inmutable con `success`, `data` y `error` opcional |
| Pipeline lineal | Lista de etapas; detiene ante primer fallo |
| Pipeline ramificado | El resultado decide la siguiente etapa |
| Stage decorator | Envuelve una etapa para agregar cross-cutting concerns |
