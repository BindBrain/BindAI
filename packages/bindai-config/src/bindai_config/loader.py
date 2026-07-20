from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class ConfigLoader(ABC):

    @abstractmethod
    def load(
        self,
        path: str,
    ):
        """
        Load a configuration file and return
        a ready-to-run runtime object.
        """
        ...