from __future__ import annotations

import uuid

from .context import WorkflowContext
from .workflow import Workflow

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bindai_project import Project

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

        self.completed = False

        self.workflow_id = workflow.id

        self.workflow_version = workflow.version

        self.retry_policy = None

        self.project: Project | None = None
