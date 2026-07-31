from __future__ import annotations

from typing import Any, Protocol

from bindai_core import ExecutionContext


class Executor(Protocol):
    def __init__(
        self,
        executable: Any,
    ) -> None: ...

    def execute(
        self,
        context: ExecutionContext,
    ) -> Any: ...
