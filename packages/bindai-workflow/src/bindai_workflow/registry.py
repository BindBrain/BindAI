from __future__ import annotations

from .workflow import Workflow


class WorkflowRegistry:
    """
    Global registry of workflows.
    """

    _workflows: dict[str, Workflow] = {}

    @classmethod
    def register(
        cls,
        workflow: Workflow,
    ) -> None:

        cls._workflows[
            workflow.id
        ] = workflow

    @classmethod
    def get(
        cls,
        workflow_id: str,
    ) -> Workflow:

        return cls._workflows[
            workflow_id
        ]

    @classmethod
    def remove(
        cls,
        workflow_id: str,
    ) -> None:

        cls._workflows.pop(
            workflow_id,
            None,
        )

    @classmethod
    def contains(
        cls,
        workflow_id: str,
    ) -> bool:

        return workflow_id in cls._workflows

    @classmethod
    def all(
        cls,
    ) -> list[Workflow]:

        return list(
            cls._workflows.values()
        )

    @classmethod
    def clear(
        cls,
    ) -> None:

        cls._workflows.clear()

    @classmethod
    def size(
        cls,
    ) -> int:

        return len(
            cls._workflows
        )