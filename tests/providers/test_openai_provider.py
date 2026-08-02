import os

import pytest

if "OPENAI_API_KEY" not in os.environ:
    pytest.skip(
        "OPENAI_API_KEY not configured",
        allow_module_level=True,
    )

from bindai_core import (
    Message,
    MessageRole,
    ModelRequest,
    ProviderConfiguration,
)
from bindai_core.context import ExecutionContext
from bindai_core.tool import (
    Tool,
    ToolResult,
)
from bindai_provider_openai import OpenAIProvider
from bindai_tool.definition import ToolDefinition


class AddTool(Tool):
    @property
    def name(self) -> str:
        return "add"

    @property
    def description(self) -> str:
        return "Add two integers."

    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name=self.name,
            description=self.description,
            parameters={
                "type": "object",
                "properties": {
                    "a": {
                        "type": "integer",
                    },
                    "b": {
                        "type": "integer",
                    },
                },
                "required": [
                    "a",
                    "b",
                ],
            },
        )

    def execute(
        self,
        context: ExecutionContext,
    ) -> ToolResult:

        data = context.data

        if not isinstance(data, dict):
            return ToolResult(
                success=False,
                error="Missing tool arguments",
            )

        a = data["a"]
        b = data["b"]

        return ToolResult(
            success=True,
            value=a + b,
        )


def test_chat_completion():

    provider = OpenAIProvider(
        ProviderConfiguration(
            api_key=os.environ["OPENAI_API_KEY"],
            model="gpt-4.1-mini",
        )
    )

    request = ModelRequest(
        messages=[
            Message(
                role=MessageRole.USER,
                content="Say hello.",
            )
        ]
    )

    response = provider.generate(request)

    assert response.content != ""


def test_streaming():

    provider = OpenAIProvider(
        ProviderConfiguration(
            api_key=os.environ["OPENAI_API_KEY"],
            model="gpt-4.1-mini",
        )
    )

    request = ModelRequest(
        messages=[
            Message(
                role=MessageRole.USER,
                content="Count to three.",
            )
        ]
    )

    chunks = list(provider.stream(request))

    assert len(chunks) > 0
    assert chunks[-1].finished


def test_tool_call():

    provider = OpenAIProvider(
        ProviderConfiguration(
            api_key=os.environ["OPENAI_API_KEY"],
            model="gpt-4.1-mini",
        )
    )

    tool = AddTool()

    request = ModelRequest(
        messages=[
            Message(
                role=MessageRole.USER,
                content="What is 5 + 7?",
            )
        ],
        tools=[
            tool.definition,
        ],
    )

    response = provider.generate(request)

    assert isinstance(
        response.tool_calls,
        list,
    )
