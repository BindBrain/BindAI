from __future__ import annotations

import uuid

from datetime import datetime

from ..node import WorkflowNode
from ..task import HumanTask


class HumanTaskNode(
    WorkflowNode,
):
    def __init__(
        self,
        node_id: str,
        assignee: str | None = None,
        form: str | None = None,
        name: str | None = None,
    ):

        super().__init__(
            node_id=node_id,
            name=name,
        )

        self.assignee = assignee

        self.form = form

    def execute(
        self,
        context,
    ):

        task = HumanTask(
            id=str(
                uuid.uuid4(),
            ),
            workflow_instance=context.instance.id,
            node_id=self.id,
            created_at=datetime.utcnow(),
        )

        context.task = task

        context.waiting = True

        return context

    def to_dict(
        self,
    ):

        data = super().to_dict()

        data.update(
            {
                "assignee": self.assignee,
                "form": self.form,
            }
        )

        return data

    def load_dict(
        self,
        data: dict,
    ):

        super().load_dict(
            data,
        )

        self.assignee = data.get(
            "assignee",
        )

        self.form = data.get(
            "form",
        )
