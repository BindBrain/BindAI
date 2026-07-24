from bindai_memory import Memory
from bindai_memory import MemoryRecord

from bindai_agent.rag.context_builder import ContextBuilder
from bindai_agent.rag.pipeline import RAGPipeline

from bindai_retrieval import (
    Retriever,
    MemoryRetrieverProvider,
)


def test_rag():

    memory = Memory("vector")

    memory.set(
        MemoryRecord(
            key="1",
            value="Paris is the capital of France.",
        )
    )

    pipeline = RAGPipeline(
        Retriever(
            MemoryRetrieverProvider(
                memory,
            )
        ),
        ContextBuilder(),
    )

    prompt = pipeline.build_prompt(
        "What is the capital of France?"
    )

    assert "Paris" in prompt