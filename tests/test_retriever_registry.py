from bindai_retrieval import RetrievalRegistry
from bindai_retrieval.providers.memory import MemoryRetrieverProvider


def test_registry():

    provider = RetrievalRegistry.provider("memory")

    assert provider is MemoryRetrieverProvider
