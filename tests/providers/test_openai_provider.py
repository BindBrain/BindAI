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

from bindai_core.tool import (
    Tool,
    ToolResult,
)

from bindai_provider_openai import OpenAIProvider


class AddTool(Tool):
    @property
    def name(self):
        return "add"

    @property
    def description(self):
        return "Add two integers."

    def execute(
        self,
        a: int,
        b: int,
    ):
        return ToolResult(
            output=a + b,
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

    chunks = list(
        provider.stream(request)
    )

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
            tool.definition(),
        ],
    )

    response = provider.generate(request)

    assert isinstance(
        response.tool_calls,
        list,
    )