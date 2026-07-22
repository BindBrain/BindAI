from bindai import (
    AssistantMessage,
    Role,
    SystemMessage,
    ToolMessage,
    UserMessage,
)


def test_system():

    msg = SystemMessage("Rules")

    assert msg.role == Role.SYSTEM

    assert msg.content == "Rules"


def test_user():

    msg = UserMessage("Hello")

    assert msg.role == Role.USER


def test_assistant():

    msg = AssistantMessage("Hi")

    assert msg.role == Role.ASSISTANT


def test_tool():

    msg = ToolMessage("Calculator")

    assert msg.role == Role.TOOL
