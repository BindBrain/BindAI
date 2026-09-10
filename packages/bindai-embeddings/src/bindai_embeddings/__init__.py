from .openai_provider import OpenAIEmbeddingProvider
from .provider import EmbeddingProvider
from .random_provider import RandomEmbeddingProvider
from .registry import EmbeddingRegistry

EmbeddingRegistry.register(
    "random",
    RandomEmbeddingProvider,
)

EmbeddingRegistry.register(
    "openai",
    OpenAIEmbeddingProvider,
)

__all__ = [
    "EmbeddingProvider",
    "EmbeddingRegistry",
    "OpenAIEmbeddingProvider",
    "RandomEmbeddingProvider",
]
