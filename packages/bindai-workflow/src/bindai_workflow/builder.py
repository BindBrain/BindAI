from __future__ import annotations

from .workflow import Workflow
from .node import WorkflowNode
from .validation import WorkflowValidator


class WorkflowBuilder:

    def __init__(
        self,
        name: str | None = None,
    ):

        self._workflow = Workflow(name)

        self._last: WorkflowNode | None = None

    def start(
        self,
        node: WorkflowNode,
    ):

        self._workflow.add_node(node)

        self._workflow.start_node = node.id

        self._last = node

        return self

    def then(
        self,
        node: WorkflowNode,
    ):

        if self._last is None:
            raise RuntimeError(
                "Workflow has no start node.",
            )

        self._workflow.add_node(node)

        self._last.next_nodes.append(
            node.id,
        )

        self._last = node

        return self

    def add(
        self,
        node: WorkflowNode,
    ):

        self._workflow.add_node(node)

        return self

    def build(
        self,
    ) -> Workflow:

        validator = WorkflowValidator()

        errors = validator.validate(
            self._workflow,
        )

        if errors:
            raise ValueError(
                "\n".join(errors),
            )

        return self._workflow