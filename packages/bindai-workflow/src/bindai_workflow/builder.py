from __future__ import annotations

from .workflow import Workflow


class WorkflowBuilder:
    def __init__(self):

        self._workflow = Workflow()

    def build(
        self,
    ) -> Workflow:

        validator = WorkflowValidator()

    errors = validator.validate(
        self._workflow,
    )

    if errors:
        raise ValueError("\n".join(errors))

    return self._workflow
