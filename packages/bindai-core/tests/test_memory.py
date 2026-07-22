from bindai_core.memory import ChatMemory
from bindai_core.model import Message, MessageRole


def test_add_message():

    memory = ChatMemory()

    memory.add(
        Message(
            role=MessageRole.USER,
            content="Hello",
        )
    )

    assert len(memory.messages()) == 1


def test_clear():

    memory = ChatMemory()

    memory.add(
        Message(
            role=MessageRole.USER,
            content="Hi",
        )
    )

    memory.clear()

    assert memory.messages() == []


def test_messages_returns_copy():

    memory = ChatMemory()

    memory.add(
        Message(
            role=MessageRole.USER,
            content="Hello",
        )
    )

    messages = memory.messages()

    messages.clear()

    assert len(memory.messages()) == 1
