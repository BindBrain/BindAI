from bindai_core.context import ExecutionContext
from bindai_tool import FunctionTool, ToolRegistry


def test_tool_registry_does_not_execute_real_tool_during_simulation():
    calls = []

    def send_email(recipient: str):
        calls.append(recipient)
        return "email sent"

    registry = ToolRegistry()

    registry.register(
        FunctionTool(
            function=send_email,
            name="send_email",
        )
    )

    context = ExecutionContext()

    context.metadata["bindai_simulation"] = True

    result = registry.execute(
        "send_email",
        context=context,
        recipient="customer@example.com",
    )

    assert result.success is True

    assert result.value == {
        "simulated": True,
        "tool": "send_email",
        "arguments": {
            "recipient": "customer@example.com",
        },
    }

    assert calls == []
