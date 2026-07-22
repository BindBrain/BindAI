from __future__ import annotations

from .knowledge import Knowledge


class KnowledgeRegistry:
    """
    Registry of knowledge bases.
    """

    def __init__(self):

        self._knowledge: dict[
            str,
            Knowledge,
        ] = {}

    def register(
        self,
        name: str,
        knowledge: Knowledge,
    ):

        self._knowledge[name] = knowledge

    def get(
        self,
        name: str,
    ) -> Knowledge:

        return self._knowledge[name]

    def remove(
        self,
        name: str,
    ):

        del self._knowledge[name]

    def names(
        self,
    ) -> list[str]:

        return list(self._knowledge.keys())
