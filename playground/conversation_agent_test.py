from bindai_core import (
    AssistantAgent,
    ExecutionContext,
    ModelProvider,
    ModelResponse,
    TokenUsage,
)


class DummyProvider(ModelProvider):

    @property
    def name(self):
        return "dummy"

    def generate(self, request):

        print("Conversation:")

        for message in request.messages:
            print(
                message.role,
                message.content,
            )

        return ModelResponse(
            content="OK",
            usage=TokenUsage(),
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

agent.execute(context)

context.variables.set(
    "input",
    "How are you?",
)

agent.execute(context)