from dataclasses import dataclass


@dataclass(slots=True)
class ProviderCapabilities:

    chat: bool = True

    vision: bool = False

    tools: bool = False

    streaming: bool = False

    embeddings: bool = False