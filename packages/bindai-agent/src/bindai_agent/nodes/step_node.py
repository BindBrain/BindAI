from __future__ import annotations

from ..execution.step import ExecutionStep
from .node import AgentNode


class NodeExecutionStep(
    ExecutionStep,
):

    def __init__(
        self,
        node: AgentNode,
    ):
        self.node = node


    def execute(
        self,
        agent,
        context,
    ):

        return self.node.execute(
            agent,
            context,
        )
