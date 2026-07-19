from __future__ import annotations

from .workflow import Workflow
from .node_factory import WorkflowNodeFactory


class WorkflowFactory:
    """
    Rebuilds Workflow objects
    from serialized data.
    """

    def __init__(
        self,
        node_factory: WorkflowNodeFactory,
    ):

        self.node_factory = node_factory

    def create(
        self,
        data: dict,
    ) -> Workflow:

        workflow = Workflow(

            name=data["name"],

        )

        workflow.id = data["id"]

        workflow.version = data["version"]

        workflow.start_node = data["start_node"]

        for node_data in data["nodes"]:

            node = self.node_factory.create(
                node_data,
            )

            workflow.nodes[
                node.id
            ] = node

        return workflow