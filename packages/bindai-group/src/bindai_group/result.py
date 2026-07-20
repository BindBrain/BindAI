from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .task import Task


@dataclass(slots=True)
class GroupResult:

    success: bool

    output: str | None = None

    error: str | None = None

    tasks: list["Task"] = field(
        default_factory=list,
    )