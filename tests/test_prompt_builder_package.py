from bindai_prompt_builder import PromptBuilder
from bindai_agent.execution.state import ExecutionState
from bindai_core.context import ExecutionContext


class DummyConversation:

    def to_request(self):

        from bindai_core.model import ModelRequest

        return ModelRequest()


class DummyTools:

    def definitions(self):
        return []


class DummyAgent:

    def __init__(self):

        self.conversation = DummyConversation()
        self.tools = DummyTools()


def test_prompt_builder():

    context = ExecutionContext()
    context.data = ExecutionState()

    builder = PromptBuilder()

    request = builder.build(
        DummyAgent(),
        context,
    )

    assert request is not None