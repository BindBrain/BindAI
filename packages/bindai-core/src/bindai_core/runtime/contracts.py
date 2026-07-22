from __future__ import annotations

from typing import Protocol

from bindai_core.context import ExecutionContext
from bindai_core.executable import ExecutionResult


class RuntimeExecutable(
    Protocol,
):
    def execute(
        self,
        context: ExecutionContext,
    ) -> ExecutionResult: ...
