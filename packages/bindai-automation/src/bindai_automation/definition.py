from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from bindai_core.executable import Executable


@dataclass(slots=True)
class AutomationDefinition:
    """
    Describes an automation and the executable it invokes.

    Triggers are managed separately by the automation trigger layer.
    The definition describes the automation identity and its execution target.
    """

    name: str
    target: Executable
    id: str = field(default_factory=lambda: str(uuid4()))
    version: int = 1
    metadata: dict[str, Any] = field(default_factory=dict)

    def run(self, context=None):
        """
        Execute the automation target.
        """
        if context is None:
            from bindai_core.context import ExecutionContext

            context = ExecutionContext()

        return self.target.execute(context)

    def clone(self) -> AutomationDefinition:
        """
        Create a new version of this automation definition.
        """
        from copy import deepcopy

        definition = deepcopy(self)
        definition.version += 1
        return definition
