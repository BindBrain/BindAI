from __future__ import annotations

from bindai_core import Message, MessageRole, ToolCall
from bindai_tool import ToolDefinition


class AnthropicMapper:
    """
    Converts BindAI models into Anthropic SDK-compatible structures.
    """

    @staticmethod
    def messages(
        messages: list[Message],
    ) -> tuple[str | None, list[dict]]:
        system: str | None = None
        result: list[dict] = []

        for message in messages:
            if message.role == MessageRole.SYSTEM:
                system = message.content
                continue

            if message.role == MessageRole.USER:
                result.append(
                    {
                        "role": "user",
                        "content": message.content,
                    }
                )
                continue

            if message.role == MessageRole.ASSISTANT:
                content: list[dict] = []

                if message.content:
                    content.append(
                        {
                            "type": "text",
                            "text": message.content,
                        }
                    )

                for tool in message.tool_calls:
                    content.append(
                        {
                            "type": "tool_use",
                            "id": tool.id,
                            "name": tool.name,
                            "input": tool.arguments,
                        }
                    )

                result.append(
                    {
                        "role": "assistant",
                        "content": content or message.content,
                    }
                )
                continue

            if message.role == MessageRole.TOOL:
                result.append(
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": message.tool_call_id,
                                "content": message.content,
                            }
                        ],
                    }
                )

        return system, result

    @staticmethod
    def tools(
        tools: list[ToolDefinition],
    ) -> list[dict]:
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
                    "name": tool.name,
                    "description": tool.description,
                    "input_schema": schema,
                }
            )

        return result

    @staticmethod
    def tool_calls(
        content: list,
    ) -> list[ToolCall]:
        result: list[ToolCall] = []

        for block in content:
            if getattr(block, "type", None) != "tool_use":
                continue

            result.append(
                ToolCall(
                    id=block.id,
                    name=block.name,
                    arguments=dict(block.input),
                )
            )

        return result
