from .provider import EmbeddingProvider
from .random_provider import RandomEmbeddingProvider
from .registry import EmbeddingRegistry

EmbeddingRegistry.register(
    "random",
    RandomEmbeddingProvider,
)

__all__ = [
    "EmbeddingProvider",
    "EmbeddingRegistry",
    "RandomEmbeddingProvider",
]