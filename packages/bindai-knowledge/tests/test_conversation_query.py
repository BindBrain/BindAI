from bindai_core.conversation import Conversation
from bindai_knowledge.conversation_query import ConversationQuery


def test_conversation_query_uses_user_and_assistant_messages():
    conversation = Conversation()

    conversation.add_user("What is BindAI?")
    conversation.add_assistant("BindAI is an AI framework.")
    conversation.add_user("How does memory work?")

    query = ConversationQuery().build(conversation)

    assert query == (
        "user: What is BindAI?\nassistant: BindAI is an AI framework.\nuser: How does memory work?"
    )


def test_conversation_query_ignores_system_and_tool_messages():
    conversation = Conversation()

    conversation.add_system("You are a helpful assistant.")
    conversation.add_user("What is memory?")
    conversation.add_tool("Memory lookup result.")

    query = ConversationQuery().build(conversation)

    assert query == "user: What is memory?"


def test_conversation_query_limits_recent_messages():
    conversation = Conversation()

    conversation.add_user("Message one")
    conversation.add_assistant("Message two")
    conversation.add_user("Message three")
    conversation.add_assistant("Message four")

    query = ConversationQuery(max_messages=2).build(conversation)

    assert query == ("user: Message three\nassistant: Message four")


def test_conversation_query_returns_empty_for_empty_conversation():
    conversation = Conversation()

    query = ConversationQuery().build(conversation)

    assert query == ""


def test_conversation_query_ignores_empty_messages():
    conversation = Conversation()

    conversation.add_user("   ")
    conversation.add_user("Actual question")

    query = ConversationQuery().build(conversation)

    assert query == "user: Actual question"


def test_knowledge_search_conversation_uses_conversation_query():
    from bindai_knowledge import (
        InMemoryKnowledgeProvider,
        Knowledge,
        KnowledgeDocument,
    )

    knowledge = Knowledge(InMemoryKnowledgeProvider())

    knowledge.add(
        KnowledgeDocument(
            id="memory",
            title="Memory",
            content="BindAI stores conversation memory.",
        )
    )

    conversation = Conversation()
    conversation.add_user("How does BindAI store memory?")

    result = knowledge.search_conversation(
        conversation,
        limit=5,
    )

    assert result.success
    assert result.value
    assert result.value[0].id == "memory"
