from bindai_memory import Memory, MemoryRecord
from bindai_retrieval import Retriever


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

    docs = retriever.retrieve("capital of France")

    assert docs.success
    assert len(docs.documents) == 1
    assert "Paris" in docs.documents[0].value
