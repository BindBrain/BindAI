from bindai_agent import AssistantAgent
from bindai_knowledge import (
    Knowledge,
    KnowledgeDocument,
    InMemoryKnowledgeProvider,
)

from bindai_core.model import (
    ModelResponse,
    TokenUsage,
)


class CaptureProvider:
    def __init__(self):

        self.last_request = None

    def generate(
        self,
        request,
    ):

        self.last_request = request

        return ModelResponse(
            content="BindAI is an AI framework.",
            usage=TokenUsage(),
        )


def test_knowledge_is_injected():

    knowledge = Knowledge(
        InMemoryKnowledgeProvider(),
    )

    knowledge.add(
        KnowledgeDocument(
            id="1",
            title="BindAI",
            content="BindAI is an AI framework.",
        )
    )

    provider = CaptureProvider()

    agent = (
        AssistantAgent.builder()
        .instructions("You are helpful.")
        .knowledge(
            knowledge,
        )
        .provider(
            provider,
        )
        .build()
    )

    agent.chat("What is BindAI?")

    conversation = "\n".join(
        message.content for message in provider.last_request.messages
    )

    assert "Relevant knowledge:" in conversation

    assert "BindAI is an AI framework." in conversation
