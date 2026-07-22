from bindai_core.agent import Agent
from bindai_core.agent import AgentResult
from bindai_core.context import ExecutionContext
from bindai_core.model import (
    ModelProvider,
    ProviderCapabilities,
    ModelResponse,
)


class DemoProvider(ModelProvider):
    @property
    def name(self):
        return "demo"

    @property
    def capabilities(self):
        return ProviderCapabilities()

    def generate(self, request):
        return ModelResponse(
            content="Hello",
            model="demo",
        )


class HelloAgent(Agent):
    def execute(self, context):

        print(f"Running {self.name}")

        return AgentResult(
            success=True,
            output="Finished",
        )


provider = DemoProvider()

agent = HelloAgent(
    name="Support Agent",
    provider=provider,
)

result = agent.execute(
    ExecutionContext(),
)

print(result.output)
