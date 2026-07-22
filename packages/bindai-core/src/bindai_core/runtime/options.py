from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class RuntimeOptions:
    """
    Runtime configuration options.
    """

    debug: bool = False

    capture_exceptions: bool = True

    publish_events: bool = True

    use_pipeline: bool = True
