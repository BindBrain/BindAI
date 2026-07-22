from __future__ import annotations

from uuid import uuid4

from .context import WorkflowContext


class WorkflowInstance:
    """
    Represents one execution of a workflow.

    A Workflow can have many WorkflowInstances.
    """

    def __init__(
        self,
        workflow,
    ) -> None:

        #
        # Identity
        #

        self.id = str(uuid4())

        #
        # Workflow definition
        #

        self.workflow = workflow

        self.workflow_id = workflow.id

        self.workflow_version = workflow.version

        #
        # Runtime
        #

        self.context = WorkflowContext()

        self.context.instance = self

        self.completed = False

        self.success = False

    @property
    def current_node(self):
        return self.context.current_node

    @property
    def variables(self):
        return self.context.variables
