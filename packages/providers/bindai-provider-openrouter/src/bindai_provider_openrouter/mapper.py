from __future__ import annotations

import json

from bindai_core import Message, MessageRole, ToolCall
from bindai_tool import ToolDefinition


class OpenRouterMapper:
    @staticmethod
    def messages(messages: list[Message]) -> list[dict]:
        result: list[dict] = []

        for message in messages:
            item: dict[str, object] = {
                "role": message.role.value,
                "content": message.content,
            }

            if message.role == MessageRole.ASSISTANT and message.tool_calls:
                item["tool_calls"] = [
                    {
                        "id": tool.id,
                        "type": "function",
                        "function": {
                            "name": tool.name,
                            "arguments": tool.arguments,
                        },
                    }
                    for tool in message.tool_calls
                ]

            if message.role == MessageRole.TOOL:
                if message.tool_call_id:
                    item["tool_call_id"] = message.tool_call_id

            result.append(item)

        return result

    @staticmethod
    def tools(tools: list[ToolDefinition]) -> list[dict]:
        result: list[dict] = []

        for tool in tools:
            result.append(
                {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.parameters,
                    },
                }
            )

        return result

    @staticmethod
    def tool_calls(message) -> list[ToolCall]:
        if not message.tool_calls:
            return []

        result: list[ToolCall] = []

        for call in message.tool_calls:
            function = call.function

            result.append(
                ToolCall(
                    id=call.id,
                    name=function.name,
                    arguments=(
                        json.loads(function.arguments)
                        if isinstance(function.arguments, str)
                        else dict(function.arguments)
                    ),
                )
            )

        return result
