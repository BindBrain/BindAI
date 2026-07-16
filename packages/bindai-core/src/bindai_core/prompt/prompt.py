from dataclasses import dataclass


@dataclass(slots=True)
class Prompt:
    """
    Final prompt passed to a model provider.
    """

    system: str = ""

    user: str = ""