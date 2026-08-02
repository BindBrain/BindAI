"""
26 Vector Database Integration

Demonstrates integrating BindAI with
a vector database.

Concepts:
- Vector storage
- Similarity search
- Document indexing
- Retrieval pipelines

This example uses a simple in-memory
vector database for demonstration.

Production systems can use:

- Chroma
- Qdrant
- Pinecone
- Weaviate
- Milvus
- PostgreSQL pgvector
"""


class SimpleVectorDatabase:
    """
    Minimal vector database implementation.

    Stores documents and embeddings.
    """

    def __init__(self):
        self.documents: list[dict] = []

    def add(
        self,
        text: str,
        vector: list[float],
    ):
        self.documents.append(
            {
                "text": text,
                "vector": vector,
            }
        )

    def search(
        self,
        query_vector: list[float],
        limit: int = 3,
    ):

        results = []

        for item in self.documents:
            score = sum(
                a * b
                for a, b in zip(
                    query_vector,
                    item["vector"],
                )
            )

            results.append(
                {
                    "text": item["text"],
                    "score": score,
                }
            )

        return sorted(
            results,
            key=lambda x: x["score"],
            reverse=True,
        )[:limit]


class SimpleEmbedding:
    def embed(
        self,
        text: str,
    ) -> list[float]:

        return [
            float(len(text)),
            float(sum(ord(c) for c in text)),
        ]


def main():

    embedding = SimpleEmbedding()

    database = SimpleVectorDatabase()

    documents = [
        "BindAI builds autonomous agents",
        "Workflows automate complex tasks",
        "Memory stores conversations",
        "Knowledge enables RAG systems",
    ]

    print("Indexing documents...\n")

    for document in documents:
        vector = embedding.embed(document)

        database.add(
            document,
            vector,
        )

    query = "AI agents and workflows"

    query_vector = embedding.embed(query)

    print("Search results:\n")

    results = database.search(query_vector)

    for result in results:
        print(f"{result['text']} ({result['score']:.2f})")


if __name__ == "__main__":
    main()
