from dataclasses import dataclass


@dataclass(slots=True)
class ModelCapabilities:
    supports_tools: bool = False
    supports_streaming: bool = True
    supports_structured_output: bool = False
    supports_vision: bool = False
    supports_embeddings: bool = False
