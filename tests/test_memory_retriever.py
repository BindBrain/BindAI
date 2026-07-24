from bindai_memory import Memory
from bindai_memory import MemoryRecord

from bindai_retrieval.providers.memory import (
    MemoryRetrieverProvider,
)
from bindai_retrieval import RetrievalQuery

def test_memory_provider():

    memory = Memory("vector")

    memory.set(
        MemoryRecord(
            key="1",
            value="Paris is the capital of France.",
        )
    )

    provider = MemoryRetrieverProvider(
        memory,
    )

    docs = provider.retrieve(
        RetrievalQuery(
            text="capital",
        )
    )

    assert docs.success
    assert len(docs.documents) == 1
    assert "Paris" in docs.documents[0].value