from __future__ import annotations

from typing import Any, Callable

from bindai_core.context import ExecutionContext
from bindai_tool import Tool, ToolDefinition, ToolResult


class WebhookConnectionTool(Tool):
    """Expose one configured BindAI Webhook connection as a Tool."""

    def __init__(
        self,
        connection_name: str,
        send: Callable[[str, object], object],
    ) -> None:
        self.connection_name = connection_name
        self._send = send

    @property
    def name(self) -> str:
        return f"webhook_{self.connection_name}"

    @property
    def description(self) -> str:
        return (
            f"Send a JSON payload through the configured "
            f"Webhook connection '{self.connection_name}'."
        )

    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name=self.name,
            description=self.description,
            parameters={
                "type": "object",
                "properties": {
                    "payload": {
                        "type": "object",
                        "description": "JSON payload to send.",
                    },
                },
                "required": ["payload"],
            },
        )

    def execute(
        self,
        context: ExecutionContext,
    ) -> ToolResult:
        payload = context.variables.get("payload")

        if payload is None:
            return ToolResult.failed(
                "Webhook tool requires a 'payload' variable."
            )

        try:
            result = self._send(
                self.connection_name,
                payload,
            )

            return ToolResult(
                success=True,
                output=result,
                value=result,
            )
        except Exception as exc:
            return ToolResult(
                success=False,
                output=None,
                value=None,
                error=str(exc),
            )
