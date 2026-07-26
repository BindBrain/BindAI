from bindai_knowledge import (
    Knowledge,
    KnowledgeDocument,
)
from bindai_knowledge.providers.in_memory import (
    InMemoryKnowledgeProvider,
)

print("=" * 60)
print("Knowledge")
print("=" * 60)

knowledge = Knowledge(
    InMemoryKnowledgeProvider(),
)

#
# Add Documents
#

knowledge.add(
    KnowledgeDocument(
        id="doc1",
        title="BindAI",
        content="BindAI is an AI agent framework written in Python.",
        metadata={
            "category": "framework",
        },
    )
)

knowledge.add(
    KnowledgeDocument(
        id="doc2",
        title="OpenAI",
        content="OpenAI develops advanced AI foundation models.",
        metadata={
            "category": "company",
        },
    )
)

knowledge.add(
    KnowledgeDocument(
        id="doc3",
        title="Python",
        content="Python is commonly used to build AI applications.",
        metadata={
            "category": "language",
        },
    )
)

print("\nDocuments Added")

#
# Get Document
#

result = knowledge.get("doc1")

print("\nRetrieved:")
print(result.success)
print(result.value)

#
# Search
#

print("\nSearch Results:")

result = knowledge.search(
    "agent framework",
)

for document in result.value:
    print(
        f"- {document.title}"
    )

#
# Search With Scores
#

print("\nSearch With Scores:")

result = knowledge.search_with_scores(
    "python",
)

for score, document in result.value:
    print(
        f"{score:>2} | {document.title}"
    )

#
# Retrieve Context
#

print("\nRetrieved Context:\n")

print(
    knowledge.retrieve(
        "python",
    )
)

#
# Retrieve With Sources
#

print("\nRetrieved Sources:")

for source in knowledge.retrieve_with_sources(
    "ai",
):
    print(
        source["title"],
        "-",
        source["metadata"],
    )

#
# Delete
#

knowledge.delete("doc2")

print("\nDeleted doc2")

#
# Clear
#

knowledge.clear()

print("Knowledge Cleared")