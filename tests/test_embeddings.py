from bindai_knowledge import (
    DummyEmbeddingProvider,
    Embedding,
)


def test_dummy_embedding():

    embedding = Embedding(
        DummyEmbeddingProvider(),
    )

    vector = embedding.embed(
        "BindAI",
    )

    assert isinstance(
        vector,
        list,
    )

    assert vector[0] == 6.0
