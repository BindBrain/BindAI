from bindai_memory import Memory
from bindai_memory import MemoryRecord

from bindai_retrieval import Retriever
from bindai_retrieval.providers.memory import MemoryRetrieverProvider


def test_retrieve():

    memory = Memory("vector")

    memory.set(
        MemoryRecord(
            key="1",
            value="Paris is the capital of France.",
        )
    )

    retriever = Retriever(
        "memory",
        memory=memory,
    )

    docs = retriever.retrieve(
        "capital of France"
    )

    assert docs.success
    assert len(docs.documents) == 1
    assert "Paris" in docs.documents[0].value