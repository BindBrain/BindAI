from __future__ import annotations

from .workflow import Workflow


class WorkflowRegistry:
    """
    Registry of workflow definitions.
    """

    def __init__(self) -> None:

        self._workflows: dict[str, Workflow] = {}

    def register(
        self,
        workflow: Workflow,
    ) -> None:

        if workflow.name in self._workflows:
            raise ValueError(f"Workflow '{workflow.name}' already registered.")

        self._workflows[workflow.name] = workflow

    def get(
        self,
        name: str,
    ) -> Workflow:

        if name not in self._workflows:
            raise KeyError(f"Workflow '{name}' is not registered.")

        return self._workflows[name]

    def contains(
        self,
        name: str,
    ) -> bool:

        return name in self._workflows

    def remove(
        self,
        name: str,
    ) -> None:

        self._workflows.pop(
            name,
            None,
        )

    def clear(
        self,
    ) -> None:

        self._workflows.clear()

    def names(
        self,
    ) -> list[str]:

        return sorted(self._workflows.keys())

    def all(
        self,
    ) -> list[Workflow]:

        return list(self._workflows.values())

    def __len__(
        self,
    ) -> int:

        return len(self._workflows)
