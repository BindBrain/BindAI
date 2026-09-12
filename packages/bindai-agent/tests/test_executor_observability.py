from __future__ import annotations

from bindai_agent.agent import Agent
from bindai_agent.executor import AgentExecutor
from bindai_core.context import ExecutionContext
from bindai_core.events import EventTypes
from bindai_core.model import ModelResponse
from bindai_core.provider import ModelProvider
from bindai_core.provider.configuration import ProviderConfiguration


class FakeProvider(ModelProvider):
    @property
    def name(self) -> str:
        return "fake"

    def generate(self, request):
        return ModelResponse(
            content="response",
        )

    def stream(self, request):
        return iter([])

    @property
    def capabilities(self):
        return {}


def create_provider():
    return FakeProvider(
        ProviderConfiguration(),
    )


def test_agent_execution_publishes_observability_events():
    agent = Agent(
        name="TestAgent",
        provider=create_provider(),
    )
    context = ExecutionContext()

    events = []
    context.events.subscribe("*", events.append)

    result = AgentExecutor().execute(
        agent,
        context,
    )

    assert result.success is True

    event_names = [event.name for event in events]

    assert event_names == [
        EventTypes.AGENT_STARTED,
        EventTypes.MODEL_REQUESTED,
        EventTypes.MODEL_RESPONDED,
        EventTypes.AGENT_FINISHED,
    ]

    for event in events:
        assert event.payload["execution_id"] == context.execution_id
