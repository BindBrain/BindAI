"""
14. RAG Chatbot

Demonstrates Retrieval-Augmented Generation.

Flow:

Documents
    ↓
Knowledge Provider
    ↓
Retriever
    ↓
Agent
    ↓
Answer
"""

from bindai import AgentBuilder
from bindai_knowledge import (
    InMemoryKnowledgeProvider,
    Knowledge,
    KnowledgeDocument,
)

# ---------------------------------------------------------
# Knowledge Documents
# ---------------------------------------------------------


documents = [
    KnowledgeDocument(
        id="bindai-overview",
        title="BindAI Overview",
        content="""
        BindAI is a Python framework for building AI applications.

        It provides:

        - agents
        - workflows
        - tools
        - memory
        - knowledge
        - retrieval
        - provider integrations
        """,
    ),
    KnowledgeDocument(
        id="agents",
        title="BindAI Agents",
        content="""
        Agents in BindAI can execute tasks using tools
        and external providers.

        Agents maintain context and produce structured
        responses.
        """,
    ),
    KnowledgeDocument(
        id="workflows",
        title="BindAI Workflows",
        content="""
        Workflows in BindAI allow developers to build
        multi-step AI pipelines.

        They support:

        - nodes
        - conditions
        - retries
        - scheduling
        """,
    ),
]


# ---------------------------------------------------------
# Knowledge Store
# ---------------------------------------------------------


provider = InMemoryKnowledgeProvider()


knowledge = Knowledge(provider)


knowledge.add_many(documents)


# ---------------------------------------------------------
# Retriever
# ---------------------------------------------------------


retriever = knowledge.retrieve


# ---------------------------------------------------------
# Agent
# ---------------------------------------------------------


agent = (
    AgentBuilder()
    .openai("gpt-4.1-mini")
    .instructions(
        """
        You answer questions using the provided
        BindAI knowledge base.

        If the answer is not available,
        say you don't know.
        """
    )
    .knowledge(knowledge)
    .build()
)


# ---------------------------------------------------------
# Query
# ---------------------------------------------------------


response = agent.chat("What features does BindAI provide?")


print("=" * 60)

print("RAG Response")

print("=" * 60)


print(response.output)
