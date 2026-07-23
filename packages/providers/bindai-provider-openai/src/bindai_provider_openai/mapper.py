from __future__ import annotations

import json

from openai.types.chat import ChatCompletionMessage

from bindai_core import (
    Message,
    MessageRole,
    ToolCall,
    ToolDefinition,
)


class OpenAIMapper:
    """
    Converts BindAI models into OpenAI SDK models.
    """

    @staticmethod
    def messages(
        messages: list[Message],
    ) -> list[dict]:

        result = []

        for message in messages:
            item: dict[str, object] = {
                "role": message.role.value,
                "content": message.content,
            }

            #
            # Assistant tool calls
            #

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

            #
            # Tool response
            #

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
        OpenAI function-calling schema.
        """

        return [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": {
                        "type": "object",
                        "properties": {
                            key: {
                                "type": value["type"],
                            }
                            for key, value in tool.parameters.items()
                        },
                        "required": [
                            key
                            for key, value in tool.parameters.items()
                            if value.get("required")
                        ],
                    },
                },
            }
            for tool in tools
        ]

    @staticmethod
    def tool_calls(
        message: ChatCompletionMessage,
    ) -> list[ToolCall]:
        """
        Convert OpenAI tool calls into BindAI ToolCalls.
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
                    arguments=json.loads(function.arguments or "{}"),
                )
            )

        return result
