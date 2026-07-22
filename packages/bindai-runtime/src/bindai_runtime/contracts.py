from __future__ import annotations

from typing import Any
from typing import Protocol

from bindai_core import ExecutionContext


class Executable(Protocol):

    def execute(
        self,
        context: ExecutionContext,
    ) -> Any:
        ...