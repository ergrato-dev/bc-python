from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass
class StageResult:
    success: bool
    data: dict[str, object]
    error: str | None = None


class Stage(Protocol):
    name: str

    def process(self, data: dict[str, object]) -> StageResult:
        ...
