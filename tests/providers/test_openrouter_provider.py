from unittest.mock import Mock

from bindai_core import (
    Message,
    MessageRole,
    ModelRequest,
    ProviderConfiguration,
)
from bindai_core.schema import ResponseSchema
from bindai_provider_openrouter.provider import OpenRouterProvider
from pydantic import create_model


def create_provider() -> OpenRouterProvider:
    configuration = ProviderConfiguration(
        api_key="test",
        model="google/gemini-3.8-flash",
        endpoint="https://openrouter.ai/api/v1",
    )
    return OpenRouterProvider(configuration)


def test_openrouter_chat():
    provider = create_provider()

    response = Mock()
    response.choices = [Mock()]
    response.choices[0].message.content = "Hello from OpenRouter"
    response.choices[0].message.tool_calls = []
    response.choices[0].finish_reason = "stop"
    response.usage.prompt_tokens = 12
    response.usage.completion_tokens = 8
    response.model = "google/gemini-3.8-flash"

    provider._client.client.chat.completions.create = Mock(return_value=response)

    request = ModelRequest(
        messages=[
            Message(
                role=MessageRole.USER,
                content="Say hello",
            )
        ],
        max_tokens=500,
    )

    result = provider.generate(request)

    assert result.content == "Hello from OpenRouter"
    assert result.tool_calls == []
    assert result.usage.prompt_tokens == 12
    assert result.usage.completion_tokens == 8
    assert result.usage.total_tokens == 20
    assert result.finish_reason == "stop"
    assert result.model == "google/gemini-3.8-flash"


def test_openrouter_streaming():
    provider = create_provider()

    chunk_1 = Mock()
    chunk_1.choices = [Mock()]
    chunk_1.choices[0].delta.content = "Hello "

    chunk_2 = Mock()
    chunk_2.choices = [Mock()]
    chunk_2.choices[0].delta.content = "from OpenRouter"

    provider._client.client.chat.completions.create = Mock(return_value=iter([chunk_1, chunk_2]))

    request = ModelRequest(
        messages=[
            Message(
                role=MessageRole.USER,
                content="Say hello",
            )
        ],
        max_tokens=500,
        stream=True,
    )

    chunks = list(provider.stream(request))

    assert chunks[0].delta == "Hello "
    assert chunks[1].delta == "from OpenRouter"
    assert chunks[2].delta == ""
    assert chunks[2].finished is True


def test_openrouter_tool_call():
    provider = create_provider()

    tool_call = Mock()
    tool_call.id = "call_123"
    tool_call.function.name = "get_weather"
    tool_call.function.arguments = '{"city":"Lisbon"}'

    response = Mock()
    response.choices = [Mock()]
    response.choices[0].message.content = ""
    response.choices[0].message.tool_calls = [tool_call]
    response.choices[0].finish_reason = "tool_calls"
    response.usage.prompt_tokens = 15
    response.usage.completion_tokens = 10
    response.model = "google/gemini-3.8-flash"

    provider._client.client.chat.completions.create = Mock(return_value=response)

    request = ModelRequest(
        messages=[
            Message(
                role=MessageRole.USER,
                content="What is the weather?",
            )
        ],
        max_tokens=500,
    )

    result = provider.generate(request)

    assert len(result.tool_calls) == 1
    assert result.tool_calls[0].id == "call_123"
    assert result.tool_calls[0].name == "get_weather"
    assert result.tool_calls[0].arguments == {"city": "Lisbon"}


def test_openrouter_structured_output():
    Weather = create_model(
        "Weather",
        city=(str, ...),
        temperature=(int, ...),
    )

    schema = ResponseSchema(
        model=Weather,
        json_schema=Weather.model_json_schema(),
    )

    provider = create_provider()

    response = Mock()
    response.choices = [Mock()]
    response.choices[0].message.content = '{"city":"Lisbon","temperature":24}'
    response.choices[0].message.tool_calls = []
    response.choices[0].finish_reason = "stop"
    response.usage.prompt_tokens = 10
    response.usage.completion_tokens = 5
    response.model = "google/gemini-3.8-flash"

    provider._client.client.chat.completions.create = Mock(return_value=response)

    request = ModelRequest(
        messages=[
            Message(
                role=MessageRole.USER,
                content="Give weather",
            )
        ],
        max_tokens=500,
        response_schema=schema,
    )

    result = provider.generate(request)

    assert result.structured_output.city == "Lisbon"
    assert result.structured_output.temperature == 24
