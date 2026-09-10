from bindai_core.context import ExecutionContext
from bindai_core.model import ModelResponse, ToolCall
from bindai_agent.execution.state import ExecutionState
from bindai_agent.execution.tool_execution_step import ToolExecutionStep
from bindai_tool.result import ToolResult


class FakeConversation:
    def __init__(self):
        self.tool_messages = []

    def add_assistant_tool_call(self, tool_calls):
        pass

    def add_tool(self, *, tool_call_id, content):
        self.tool_messages.append(
            {
                "tool_call_id": tool_call_id,
                "content": content,
            }
        )

    def to_request(self):
        return None


class FakeAgent:
    def __init__(self, result):
        self.conversation = FakeConversation()
        self.result = result

    def execute_tool(self, name, **kwargs):
        return self.result


def test_failed_tool_result_preserves_error_in_conversation():
    agent = FakeAgent(
        ToolResult.failed("boom"),
    )

    context = ExecutionContext()
    context.data = ExecutionState(
        response=ModelResponse(
            tool_calls=[
                ToolCall(
                    id="call-1",
                    name="fail",
                )
            ]
        )
    )

    ToolExecutionStep().execute(agent, context)

    assert agent.conversation.tool_messages == [
        {
            "tool_call_id": "call-1",
            "content": "Tool execution failed: boom",
        }
    ]