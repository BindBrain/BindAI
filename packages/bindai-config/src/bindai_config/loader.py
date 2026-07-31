from __future__ import annotations

from abc import ABC, abstractmethod

from bindai_group import Group


class ConfigLoader(ABC):
    @abstractmethod
    def load(
        self,
        path: str,
    ) -> Group:
        """
        Load a configuration file and return
        a ready-to-run Group.
        """
        ...
