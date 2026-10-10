from __future__ import annotations

from .node import AgentNode
from .decorators import node_type


@node_type("debug")
class DebugNode(AgentNode):
    """
    Simple Studio test node.
    """

    def __init__(self):
        super().__init__(
            "debug",
            "Writes debug information",
        )


    def inputs(
        self,
    ):
        return [
            {
                "name": "message",
                "type": "string",
            }
        ]


    def outputs(
        self,
    ):
        return [
            {
                "name": "done",
                "type": "boolean",
            }
        ]


    def execute(
        self,
        agent,
        context,
    ):
        print(
            "DEBUG NODE RUNNING"
        )

        return None
