from __future__ import annotations

import copy
import uuid

from bindai_core.context import ExecutionContext
from bindai_core.executable import Executable

from .executor import WorkflowExecutor
from .instance import WorkflowInstance
from .node import WorkflowNode
from .result import WorkflowResult
from .memory_store import MemoryWorkflowStore


class Workflow(Executable):
    """
    Represents an executable workflow.
    """

    def __init__(
        self,
        name: str | None = None,
    ):

        self.id = str(uuid.uuid4())

        self.version = 1

        self.name = name or self.id

        self.nodes: dict[str, WorkflowNode] = {}

        self.start_node: str | None = None

        self.agents: dict[str, object] = {}

        self.executor = WorkflowExecutor(
            MemoryWorkflowStore(),
        )

    def add_node(
        self,
        node: WorkflowNode,
    ) -> None:

        self.nodes[node.id] = node

        if self.start_node is None:
            self.start_node = node.id

    def get(
        self,
        node_id: str,
    ) -> WorkflowNode:

        return self.nodes[node_id]

    def create_instance(
        self,
    ) -> WorkflowInstance:

        return WorkflowInstance(
            self,
        )

    def execute(
        self,
        context: ExecutionContext,
    ) -> WorkflowResult:

        instance = self.create_instance()

        #
        # propagate variables
        #

        if hasattr(context, "variables"):
            instance.context.variables.update(
                context.variables,
            )

        return self.executor.execute(
            instance,
        )

    def clone(
        self,
    ) -> Workflow:

        workflow = copy.deepcopy(
            self,
        )

        workflow.version += 1

        return workflow

    def run(
        self,
        context: ExecutionContext | None = None,
    ) -> WorkflowResult:
        
        if context is None:
            context = ExecutionContext()

        return self.execute(
            context,
        )