from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4

from bindai_core.context import ExecutionContext


@dataclass(slots=True)
class AgentSession:

    agent: object

    id: str = field(
        default_factory=lambda: str(uuid4())
    )

    context: ExecutionContext = field(
        default_factory=ExecutionContext
    )