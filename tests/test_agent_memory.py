from bindai_agent import AssistantAgent

from bindai_memory import (
    Memory,
    MemoryRecord,
    InMemoryProvider,
)

from bindai_core.model import (
    ModelResponse,
)


class DummyProvider:
    """
    Simple fake provider used for testing.
    """

    def __init__(
        self,
        response: str,
    ):
        self.response = response

    def generate(
        self,
        request,
    ):

        return ModelResponse(
            content=self.response,
            tool_calls=[],
        )

    def stream(
        self,
        request,
    ):
        yield from ()


def test_agent_memory():

    memory = Memory(
        InMemoryProvider(),
    )

    memory.set(
        MemoryRecord(
            key="__context__",
            value="User name is John.",
        )
    )

    agent = AssistantAgent(
        name="assistant",
        provider=None,
    )

    agent.use_memory(
        memory,
    )

    result = agent.memory.get(
        "__context__",
    )

    assert result.success

    assert result.value.value == "User name is John."


def test_memory_is_saved():

    memory = Memory(
        InMemoryProvider(),
    )

    agent = (
        AssistantAgent.builder()
        .instructions("You are helpful.")
        .memory(
            memory,
        )
        .provider(DummyProvider("Hello!"))
        .build()
    )

    agent.chat("Hi")

    result = memory.get(
        "__context__",
    )

    assert result.success
    assert result.value is not None
    assert "Hi" in result.value.value
    assert "Hello!" in result.value.value
