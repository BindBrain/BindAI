from bindai_agent import AssistantAgent
from bindai_core.middleware import Middleware
from bindai_core.model import (
    ModelResponse,
    TokenUsage,
)


class DummyProvider:
    def generate(
        self,
        request,
    ):

        return ModelResponse(
            content="Hello!",
            usage=TokenUsage(),
        )

    def stream(
        self,
        request,
    ):
        yield


class RecordingMiddleware(Middleware):
    def __init__(self):

        self.calls = []

    def before_execute(
        self,
        agent,
        context,
    ):

        self.calls.append("before")

    def after_execute(
        self,
        agent,
        context,
        result,
    ):

        self.calls.append("after")


def test_middleware_executes():

    middleware = RecordingMiddleware()

    agent = (
        AssistantAgent.builder()
        .instructions("You are helpful.")
        .provider(
            DummyProvider(),
        )
        .middleware(
            middleware,
        )
        .build()
    )

    agent.chat("Hello")

    assert middleware.calls == [
        "before",
        "after",
    ]
