from bindai_memory import Memory, MemoryRecord
from bindai_retrieval import RetrievalQuery
from bindai_retrieval.providers.vector import VectorRetrieverProvider


def test_vector_provider():

    memory = Memory("vector")

    memory.set(
        MemoryRecord(
            key="1",
            value="BindAI agent framework",
        )
    )

    memory.set(
        MemoryRecord(
            key="2",
            value="Weather forecast",
        )
    )

    provider = VectorRetrieverProvider(
        memory,
    )

    result = provider.retrieve(
        RetrievalQuery(
            text="agent",
        )
    )

    assert result.success
    assert len(result.documents) == 2
    assert result.documents[0].score >= result.documents[1].score
