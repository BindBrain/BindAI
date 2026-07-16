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
        return ModelResponse(
            content="Dummy response",
            usage=TokenUsage(),
        )


# Create the execution context
context = ExecutionContext()

# Create the agent
agent = AssistantAgent(
    name="assistant",
    instructions="You are helpful.",
    provider=DummyProvider(),
)

# First message
context.variables.set(
    "input",
    "Hello",
)

agent.execute(context)

# Second message
context.variables.set(
    "input",
    "How are you?",
)

agent.execute(context)

# Show memory
print(len(agent.conversation))

for message in agent.conversation.messages:
    print(message.role, message.content)