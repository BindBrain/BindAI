from __future__ import annotations

from .node import WorkflowNode


class WorkflowNodeFactory:
    """
    Creates workflow nodes from
    serialized definitions.
    """

    def __init__(self):

        self._types: dict[
            str,
            type[WorkflowNode],
        ] = {}

    def register(
        self,
        node_type: type[WorkflowNode],
    ):

        self._types[
            node_type.__name__
        ] = node_type

    def create(
        self,
        data: dict,
    ):

        node_class = self._types[
            data["type"]
        ]

        node = node_class(

            node_id=data["id"],

            name=data.get(
                "name",
            ),

        )

        node.load_dict(
            data,
        )

        return node