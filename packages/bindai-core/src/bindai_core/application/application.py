from __future__ import annotations

from dataclasses import dataclass

from bindai_core.resource import Resource
from bindai_core.version import __version__


@dataclass(slots=True)
class BindApplication(Resource):
    """
    Root BindAI application.
    """

    @property
    def version(self) -> str:
        return __version__