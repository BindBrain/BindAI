from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from .context import WorkflowContext

if TYPE_CHECKING:
    from bindai_project import Project

    from .workflow import Workflow


class WorkflowInstance:
    """
    Represents one running execution
    of a workflow.
    """

    def __init__(
        self,
        workflow: Workflow,
    ):

        self.id = str(uuid.uuid4())

        self.workflow = workflow

        self.context = WorkflowContext()

        self.context.instance = self

        self.completed: bool = False

        self.workflow_id = workflow.id

        self.workflow_version = workflow.version

        self.retry_policy: object | None = None

        self.project: Project | None = None
