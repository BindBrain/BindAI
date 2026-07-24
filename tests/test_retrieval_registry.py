from bindai_retrieval import RetrievalRegistry


def test_memory_registered():

    provider = RetrievalRegistry.provider(
        "memory",
    )

    assert provider is not None


def test_vector_registered():

    provider = RetrievalRegistry.provider(
        "vector",
    )

    assert provider is not None


def test_bm25_registered():

    provider = RetrievalRegistry.provider(
        "bm25",
    )

    assert provider is not None


def test_hybrid_registered():

    provider = RetrievalRegistry.provider(
        "hybrid",
    )

    assert provider is not None