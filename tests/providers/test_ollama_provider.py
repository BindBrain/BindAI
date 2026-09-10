from unittest.mock import Mock

from bindai_core import (
    Message,
    MessageRole,
    ModelRequest,
    ProviderConfiguration,
)
from bindai_core.schema import ResponseSchema
from bindai_provider_ollama.provider import OllamaProvider
from pydantic import create_model


def create_provider() -> OllamaProvider:
    configuration = ProviderConfiguration(
        api_key="",
        model="llama3.2",
        endpoint="http://localhost:11434",
    )
    return OllamaProvider(configuration)


def test_ollama_structured_output():
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
    response.message.content = '{"city": "Lisbon", "temperature": 24}'
    response.message.tool_calls = []
    response.prompt_eval_count = 10
    response.eval_count = 5
    response.done_reason = "stop"
    response.model = "llama3.2"

    provider._client.client.chat = Mock(return_value=response)

    request = ModelRequest(
        messages=[
            Message(
                role=MessageRole.USER,
                content="Give weather",
            )
        ],
        response_schema=schema,
    )

    result = provider.generate(request)

    assert result.content == '{"city": "Lisbon", "temperature": 24}'
    assert result.structured_output.city == "Lisbon"
    assert result.structured_output.temperature == 24
    assert result.usage.prompt_tokens == 10
    assert result.usage.completion_tokens == 5
    assert result.usage.total_tokens == 15


def test_ollama_chat():
    provider = create_provider()

    response = Mock()
    response.message.content = "Hello from Ollama"
    response.message.tool_calls = []
    response.prompt_eval_count = 12
    response.eval_count = 8
    response.done_reason = "stop"
    response.model = "llama3.2"

    provider._client.client.chat = Mock(return_value=response)

    request = ModelRequest(
        messages=[
            Message(
                role=MessageRole.USER,
                content="Say hello",
            )
        ],
    )

    result = provider.generate(request)

    assert result.content == "Hello from Ollama"
    assert result.tool_calls == []
    assert result.usage.prompt_tokens == 12
    assert result.usage.completion_tokens == 8
    assert result.usage.total_tokens == 20
    assert result.finish_reason == "stop"
    assert result.model == "llama3.2"


def test_ollama_streaming():
    provider = create_provider()

    chunk_1 = Mock()
    chunk_1.message.content = "Hello "

    chunk_2 = Mock()
    chunk_2.message.content = "from Ollama"

    provider._client.client.chat = Mock(return_value=iter([chunk_1, chunk_2]))

    request = ModelRequest(
        messages=[
            Message(
                role=MessageRole.USER,
                content="Say hello",
            )
        ],
        stream=True,
    )

    chunks = list(provider.stream(request))

    assert chunks[0].delta == "Hello "
    assert chunks[1].delta == "from Ollama"
    assert chunks[2].delta == ""
    assert chunks[2].finished is True


def test_ollama_tool_call():
    provider = create_provider()

    tool_call = Mock()
    tool_call.function.name = "get_weather"
    tool_call.function.arguments = {"city": "Lisbon"}

    response = Mock()
    response.message.content = ""
    response.message.tool_calls = [tool_call]
    response.prompt_eval_count = 15
    response.eval_count = 10
    response.done_reason = "stop"
    response.model = "llama3.2"

    provider._client.client.chat = Mock(return_value=response)

    request = ModelRequest(
        messages=[
            Message(
                role=MessageRole.USER,
                content="What is the weather?",
            )
        ],
    )

    result = provider.generate(request)

    assert len(result.tool_calls) == 1
    assert result.tool_calls[0].name == "get_weather"
    assert result.tool_calls[0].arguments == {"city": "Lisbon"}
