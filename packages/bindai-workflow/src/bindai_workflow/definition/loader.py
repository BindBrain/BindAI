from __future__ import annotations

from pathlib import Path

import yaml

from .models import WorkflowDefinition


class WorkflowDefinitionLoader:
    def load(
        self,
        path: str | Path,
        *,
        strict: bool = True,
    ) -> WorkflowDefinition:
        workflow_path = Path(path)

        data = yaml.safe_load(workflow_path.read_text(encoding="utf-8"))

        if not isinstance(data, dict):
            raise ValueError(f"Workflow definition must contain a mapping: {workflow_path}")

        return WorkflowDefinition.from_dict(
            data,
            strict=strict,
        )

    def loads(
        self,
        content: str,
        *,
        strict: bool = True,
    ) -> WorkflowDefinition:
        data = yaml.safe_load(content)

        if not isinstance(data, dict):
            raise ValueError("Workflow definition must contain a mapping.")

        return WorkflowDefinition.from_dict(
            data,
            strict=strict,
        )
