from __future__ import annotations

from pathlib import Path


class WorkflowValidator:
    @staticmethod
    def validate(
        path: Path,
    ) -> list[str]:

        errors: list[str] = []

        if not path.exists():
            errors.append("Workflow file does not exist.")

            return errors

        if path.suffix != ".py":
            errors.append("Workflow must be a Python file.")

        source = path.read_text(
            encoding="utf-8",
        )

        if "WorkflowBuilder" not in source:
            errors.append("WorkflowBuilder not found.")

        if ".build(" not in source:
            errors.append("Workflow is never built.")

        return errors
