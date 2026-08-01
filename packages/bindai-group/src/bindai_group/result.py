from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from bindai_core.executable.result import ExecutionResult

if TYPE_CHECKING:
    from .task import Task


@dataclass(slots=True)
class GroupResult(ExecutionResult):
    output: str | None = None

    tasks: list[Task] = field(default_factory=list)
