from __future__ import annotations


class ExecutorRegistry:
    """
    Registry mapping executable
    types to executors.
    """

    def __init__(self):

        self._executors: dict[
            type,
            object,
        ] = {}

    def register(
        self,
        executable_type: type,
        executor,
    ) -> None:

        self._executors[executable_type] = executor

    def resolve(
        self,
        executable,
    ):

        for executable_type, executor in self._executors.items():
            if isinstance(
                executable,
                executable_type,
            ):
                return executor

        raise RuntimeError(f"No executor registered for {type(executable).__name__}.")
