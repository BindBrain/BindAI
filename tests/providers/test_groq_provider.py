import os

import pytest
from dotenv import load_dotenv

load_dotenv()

if "GROQ_API_KEY" not in os.environ:
    pytest.skip(
        "GROQ_API_KEY not configured",
        allow_module_level=True,
    )

from bindai_core import (
    Message,
    MessageRole,
    ModelRequest,
    ProviderConfiguration,
)
from bindai_provider_groq import GroqProvider
from bindai_tool.definition import ToolDefinition


def test_chat_completion():

    provider = GroqProvider(
        ProviderConfiguration(
            api_key=os.environ["GROQ_API_KEY"],
            model="openai/gpt-oss-120b",
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

    provider = GroqProvider(
        ProviderConfiguration(
            api_key=os.environ["GROQ_API_KEY"],
            model="openai/gpt-oss-120b",
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

    provider = GroqProvider(
        ProviderConfiguration(
            api_key=os.environ["GROQ_API_KEY"],
            model="openai/gpt-oss-120b",
        )
    )

    tool = ToolDefinition(
        name="add",
        description="Add two integers.",
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

    request = ModelRequest(
        messages=[
            Message(
                role=MessageRole.USER,
                content="What is 5 + 7? Use the add tool.",
            )
        ],
        tools=[
            tool,
        ],
    )

    response = provider.generate(request)

    assert isinstance(
        response.tool_calls,
        list,
    )