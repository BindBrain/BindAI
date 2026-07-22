from __future__ import annotations


class Worker:

    def execute(
        self,
        runtime,
        executable,
    ):

        return runtime.executor.execute(
            executable,
            runtime.context,
        )