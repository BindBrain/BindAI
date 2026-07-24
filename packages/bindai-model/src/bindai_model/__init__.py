from .model import Model
from .provider import ModelProvider
from .providers import OpenAIProvider
from .registry import ModelRegistry
from .result import ModelResult

ModelRegistry.register(
    "openai",
    OpenAIProvider,
)

__all__ = [
    "Model",
    "ModelProvider",
    "ModelRegistry",
    "ModelResult",
    "OpenAIProvider",
]