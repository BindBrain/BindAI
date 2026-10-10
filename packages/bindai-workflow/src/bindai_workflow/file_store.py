from __future__ import annotations

import json
from datetime import datetime

from bindai_core.executable.result import ExecutionResult
from pathlib import Path
from typing import Callable

from .instance import WorkflowInstance
from .store import WorkflowStore
from .task import HumanTask


class FileWorkflowStore(WorkflowStore):
    """
    File-backed workflow instance store.

    Workflow definitions are not persisted here. They are resolved by
    workflow_resolver when an instance is loaded.
    """

    SCHEMA_VERSION = 1

    def __init__(
        self,
        root: str | Path,
        workflow_resolver: Callable[[str, int], object | None],
    ) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.workflow_resolver = workflow_resolver

    def _path(self, instance_id: str) -> Path:
        return self.root / f"{instance_id}.json"

    def save(self, instance: WorkflowInstance) -> None:
        data = self._serialize(instance)
        path = self._path(instance.id)
        temporary = path.with_suffix(".tmp")

        temporary.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        temporary.replace(path)

    def load(self, instance_id: str) -> WorkflowInstance | None:
        path = self._path(instance_id)

        if not path.exists():
            return None

        data = json.loads(path.read_text(encoding="utf-8"))

        if data.get("schema_version") != self.SCHEMA_VERSION:
            raise ValueError(
                f"Unsupported workflow run schema version: "
                f"{data.get('schema_version')!r}"
            )

        workflow_id = data["workflow_id"]
        workflow_version = int(data["workflow_version"])

        workflow = self.workflow_resolver(
            workflow_id,
            workflow_version,
        )

        if workflow is None:
            raise ValueError(
                f"Workflow '{workflow_id}' version "
                f"{workflow_version} could not be resolved."
            )

        instance = workflow.create_instance()
        instance.id = data["instance_id"]
        instance.workflow_id = workflow_id
        instance.workflow_version = workflow_version
        instance.completed = bool(data["completed"])

        context = instance.context
        context.instance = instance

        context.variables.update(
            data["context"]["variables"],
        )
        context.metadata.update(
            data["context"]["metadata"],
        )
        context.execution_queue = list(
            data["context"]["execution_queue"],
        )
        context.current_node = data["context"]["current_node"]
        context.waiting = bool(data["context"]["waiting"])
        context.subworkflow = data["context"]["subworkflow"]
        context.join_state = dict(
            data["context"]["join_state"],
        )

        context.started_at = datetime.fromisoformat(
            data["context"]["started_at"],
        )

        finished_at = data["context"]["finished_at"]
        context.finished_at = (
            datetime.fromisoformat(finished_at)
            if finished_at is not None
            else None
        )

        context.user = data["context"]["user"]
        context.tenant = data["context"]["tenant"]
        context.application = data["context"]["application"]
        context.errors = list(data["context"]["errors"])
        context.retry_attempt = int(
            data["context"]["retry_attempt"],
        )

        task = data["context"]["task"]
        context.task = (
            self._deserialize_task(task)
            if task is not None
            else None
        )

        return instance

    def delete(self, instance_id: str) -> None:
        self._path(instance_id).unlink(missing_ok=True)

    def _serialize(self, instance: WorkflowInstance) -> dict:
        context = instance.context

        return {
            "schema_version": self.SCHEMA_VERSION,
            "instance_id": instance.id,
            "workflow_id": instance.workflow_id,
            "workflow_version": instance.workflow_version,
            "completed": instance.completed,
            "context": {
                "variables": self._serialize_value(context.variables.as_dict()),
                "metadata": context.metadata,
                "execution_queue": list(context.execution_queue),
                "current_node": context.current_node,
                "waiting": context.waiting,
                "subworkflow": context.subworkflow,
                "join_state": dict(context.join_state),
                "started_at": context.started_at.isoformat(),
                "finished_at": (
                    context.finished_at.isoformat()
                    if context.finished_at is not None
                    else None
                ),
                "user": context.user,
                "tenant": context.tenant,
                "application": context.application,
                "errors": list(context.errors),
                "retry_attempt": context.retry_attempt,
                "task": self._serialize_task(context.task),
            },
        }

    @classmethod
    def _serialize_value(cls, value: object) -> object:
        if isinstance(value, ExecutionResult):
            return {
                "__bindai_type__": "execution_result",
                "class": value.__class__.__name__,
                "success": bool(value.success),
                "output": cls._serialize_value(value.output),
                "value": cls._serialize_value(
                    getattr(value, "value", None),
                ),
                "error": value.error,
            }

        if isinstance(value, dict):
            return {
                str(key): cls._serialize_value(item)
                for key, item in value.items()
            }

        if isinstance(value, (list, tuple)):
            return [
                cls._serialize_value(item)
                for item in value
            ]

        if isinstance(value, set):
            return [
                cls._serialize_value(item)
                for item in value
            ]

        return value

    @staticmethod
    def _deserialize_value(value: object) -> object:
        if isinstance(value, dict):
            if value.get("__bindai_type__") == "execution_result":
                from bindai_tool import ToolResult

                return ToolResult(
                    success=bool(value["success"]),
                    output=FileWorkflowStore._deserialize_value(
                        value.get("output"),
                    ),
                    value=FileWorkflowStore._deserialize_value(
                        value.get("value"),
                    ),
                    error=value.get("error"),
                )

            return {
                key: FileWorkflowStore._deserialize_value(item)
                for key, item in value.items()
            }

        if isinstance(value, list):
            return [
                FileWorkflowStore._deserialize_value(item)
                for item in value
            ]

        return value

    @staticmethod
    def _serialize_task(task: object | None) -> dict | None:
        if task is None:
            return None

        if not isinstance(task, HumanTask):
            raise TypeError(
                "Only HumanTask instances can currently be persisted."
            )

        return {
            "id": task.id,
            "workflow_instance": task.workflow_instance,
            "node_id": task.node_id,
            "assignee": task.assignee,
            "role": task.role,
            "created_at": task.created_at.isoformat(),
            "completed": task.completed,
            "result": task.result,
        }

    @staticmethod
    def _deserialize_task(data: dict) -> HumanTask:
        return HumanTask(
            id=data["id"],
            workflow_instance=data["workflow_instance"],
            node_id=data["node_id"],
            assignee=data.get("assignee"),
            role=data.get("role"),
            created_at=datetime.fromisoformat(data["created_at"]),
            completed=bool(data["completed"]),
            result=data.get("result"),
        )
