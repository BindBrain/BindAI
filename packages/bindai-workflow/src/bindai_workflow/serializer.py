from __future__ import annotations

import json

from pathlib import Path

from .workflow import Workflow


class WorkflowSerializer:
    """
    Serializes workflow definitions into dictionaries
    and JSON files.

    Runtime state is intentionally excluded.
    """

    def to_dict(
        self,
        workflow: Workflow,
    ) -> dict:

        return {
            "id": workflow.id,
            "name": workflow.name,
            "version": workflow.version,
            "start_node": workflow.start_node,
            "nodes": [node.to_dict() for node in workflow.nodes.values()],
        }

    def to_json(
        self,
        workflow: Workflow,
    ) -> str:

        return json.dumps(
            self.to_dict(
                workflow,
            ),
            indent=4,
        )

    def save(
        self,
        workflow: Workflow,
        path: str | Path,
    ):

        Path(path).write_text(
            self.to_json(
                workflow,
            ),
            encoding="utf8",
        )
