from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class WorkflowResult:

    success: bool

    output: Any = None

    error: str | None = None