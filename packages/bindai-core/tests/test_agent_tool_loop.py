from bindai_agent import Agent
from bindai_core.model import (
    ModelProvider,
    ModelResponse,
    ToolCall,
)
from bindai_core.model.provider_capabilities import ProviderCapabilities
from bindai_core.provider.configuration import ProviderConfiguration
from bindai_core.tool import tool


@tool()
def calculator() -> str:
    return "42"


class FakeProvider(ModelProvider):

    def __init__(self):

        super().__init__(
            ProviderConfiguration(),
        )

        self.calls = 0

    @property
    def name(self):
        return "fake"

    @property
    def capabilities(self):

        return ProviderCapabilities(
            tool_calling=True,
        )

    def generate(
        self,
        request,
    ):

        self.calls += 1

        if self.calls == 1:
            return ModelResponse(
                tool_calls=[
                    ToolCall(
                        id="tool-1",
                        name="calculator",
                        arguments={},
                    )
                ],
            )

        return ModelResponse(
            content="The answer is 42.",
        )

    def stream(
        self,
        request,
    ):
        raise NotImplementedError()


def test_recursive_tool_loop():

    provider = FakeProvider()

    agent = Agent(
        name="assistant",
        instructions="You are helpful.",
        provider=provider,
    )

    agent.add_tool(
        calculator,
    )

    result = agent.chat(
        "What is 6 * 7?",
    )

    assert result.success

    assert result.output == "The answer is 42."

    assert provider.calls == 2