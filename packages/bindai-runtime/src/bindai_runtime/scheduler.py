from __future__ import annotations

from collections import deque
from typing import Any


class Scheduler:
    def __init__(self):

        self._queue: deque[Any] = deque()

    def submit(
        self,
        executable,
    ):

        self._queue.append(
            executable,
        )

    def next(self):

        if self._queue:
            return self._queue.popleft()

        return None
