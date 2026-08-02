"""
25 Custom Embedding Provider

Demonstrates creating a custom embedding provider.

Concepts:
- Embedding interfaces
- Custom vector generation
- Provider abstraction
- Using embeddings for similarity search
"""

from math import sqrt


class CustomEmbeddingProvider:
    """
    Example custom embedding provider.

    A production implementation could wrap:

    - OpenAI embeddings
    - HuggingFace models
    - Sentence Transformers
    - Local embedding models
    """

    def __init__(self, dimensions: int = 5):
        self.dimensions = dimensions

    def embed(
        self,
        text: str,
    ) -> list[float]:
        """
        Convert text into a vector.

        This is a simple demo implementation.
        Real providers use ML models.
        """

        values = [float(ord(char)) for char in text[: self.dimensions]]

        while len(values) < self.dimensions:
            values.append(0.0)

        magnitude = sqrt(sum(value * value for value in values))

        if magnitude == 0:
            return values

        return [value / magnitude for value in values]


def cosine_similarity(
    a: list[float],
    b: list[float],
) -> float:

    return sum(x * y for x, y in zip(a, b))


def main():

    provider = CustomEmbeddingProvider()

    documents = [
        "BindAI creates AI agents",
        "Python framework for workflows",
        "Cooking recipes and ingredients",
    ]

    query = "AI agent framework"

    query_vector = provider.embed(query)

    print("Query vector:")
    print(query_vector)

    print("\nSimilarity results:")

    for document in documents:
        vector = provider.embed(document)

        score = cosine_similarity(
            query_vector,
            vector,
        )

        print(f"{document}: {score:.4f}")


if __name__ == "__main__":
    main()
