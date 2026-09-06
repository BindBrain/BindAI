from bindai_agent.agent import Agent
from bindai_agent.executor import AgentExecutor
from bindai_core.model import MessageRole, ModelResponse
from bindai_core.provider import ModelProvider
from bindai_core.provider.configuration import ProviderConfiguration
from bindai_knowledge import (
    InMemoryKnowledgeProvider,
    Knowledge,
    KnowledgeDocument,
)


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


def test_agent_injects_knowledge_context():
    knowledge = Knowledge(
        InMemoryKnowledgeProvider(),
    )

    knowledge.add(
        KnowledgeDocument(
            id="doc-1",
            title="AI",
            content="BindAI supports retrieval augmented generation.",
        )
    )

    agent = Agent(
        name="Researcher",
        provider=create_provider(),
        instructions="Answer questions using the available knowledge.",
    )

    agent.use_knowledge(knowledge)
    agent.conversation.add_user(
        "What does BindAI support?"
    )

    executor = AgentExecutor()

    request = executor._build_request(
        agent,
        agent._create_context(
            "What does BindAI support?"
        ),
    )

    assert any(
        message.role == MessageRole.SYSTEM
        and "BindAI supports retrieval augmented generation."
        in message.content
        for message in request.messages
    )