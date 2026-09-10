from __future__ import annotations

import json

from bindai_core import (
    Message,
    MessageRole,
    ToolCall,
)
from bindai_tool import ToolDefinition
from groq.types.chat import ChatCompletionMessage


class GroqMapper:
    """
    Converts BindAI models into Groq SDK models.
    """

    @staticmethod
    def messages(
        messages: list[Message],
    ) -> list[dict]:
        """
        Convert BindAI messages into Groq messages.
        """

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
                            "arguments": json.dumps(
                                tool.arguments,
                            ),
                        },
                    }
                    for tool in message.tool_calls
                ]

            if message.role == MessageRole.TOOL and message.tool_call_id:
                item["tool_call_id"] = message.tool_call_id

            result.append(item)

        return result

    @staticmethod
    def tools(
        tools: list[ToolDefinition],
    ) -> list[dict]:
        """
        Convert BindAI tool definitions into
        Groq function-calling schema.
        """

        result: list[dict] = []

        for tool in tools:
            parameters = tool.parameters

            if (
                isinstance(parameters, dict)
                and parameters.get("type") == "object"
                and isinstance(parameters.get("properties"), dict)
            ):
                schema = parameters

            else:
                properties: dict[str, dict] = {}
                required: list[str] = []

                for key, value in parameters.items():
                    if not isinstance(value, dict):
                        continue

                    properties[key] = {
                        "type": value.get("type", "string"),
                    }

                    if value.get("required"):
                        required.append(key)

                schema = {
                    "type": "object",
                    "properties": properties,
                    "required": required,
                }

            result.append(
                {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": schema,
                    },
                }
            )

        return result

    @staticmethod
    def tool_calls(
        message: ChatCompletionMessage,
    ) -> list[ToolCall]:
        """
        Convert Groq tool calls into BindAI ToolCalls.
        """

        if not message.tool_calls:
            return []

        result: list[ToolCall] = []

        for call in message.tool_calls:
            if getattr(call, "type", None) != "function":
                continue

            function = getattr(call, "function", None)

            if function is None:
                continue

            result.append(
                ToolCall(
                    id=call.id,
                    name=function.name,
                    arguments=json.loads(
                        function.arguments or "{}",
                    ),
                )
            )

        return result
