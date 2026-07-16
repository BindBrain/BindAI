from bindai_core import (
    AssistantAgent,
    ExecutionContext,
    ExecutionPipeline,
    Middleware,
    ModelProvider,
    ModelResponse,
    TokenUsage,
)


class DummyProvider(ModelProvider):

    @property
    def name(self):
        return "dummy"

    def generate(self, request):
        return ModelResponse(
            content="Hello",
            usage=TokenUsage(),
        )


class LoggingMiddleware(Middleware):

    def before_execute(
        self,
        agent,
        context,
    ):
        print("Before")

    def after_execute(
        self,
        agent,
        context,
        result,
    ):
        print("After")


pipeline = ExecutionPipeline()

pipeline.use(
    LoggingMiddleware(),
)

agent = AssistantAgent(
    name="assistant",
    instructions="You are helpful.",
    provider=DummyProvider(),
)

context = ExecutionContext()

context.variables.set(
    "input",
    "Hello",
)

pipeline.execute(
    agent,
    context,
)