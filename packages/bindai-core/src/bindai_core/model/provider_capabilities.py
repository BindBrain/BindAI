from dataclasses import dataclass


@dataclass(slots=True)
class ProviderCapabilities:
    """
    Describes what a model provider supports.
    """

    chat: bool = True
    streaming: bool = False
    vision: bool = False
    embeddings: bool = False
    tool_calling: bool = False
    structured_output: bool = False
    reasoning: bool = False