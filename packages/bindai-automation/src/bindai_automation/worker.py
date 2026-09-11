from __future__ import annotations

from concurrent.futures import Future, ThreadPoolExecutor
from typing import Any

from .definition import AutomationDefinition
from .history import AutomationRunHistory
from .memory_history import MemoryAutomationRunHistory
from .memory_store import MemoryAutomationStateStore
from .run import AutomationRun
from .state_store import AutomationStateStore


class AutomationWorker:
    """
    Executes automation definitions in background threads.

    The worker manages the lifecycle of each AutomationRun, persists the
    current execution state, and records the completed or failed run in
    automation history.
    """

    def __init__(
        self,
        *,
        state_store: AutomationStateStore | None = None,
        history: AutomationRunHistory | None = None,
        max_workers: int = 4,
    ) -> None:
        if max_workers < 1:
            raise ValueError("max_workers must be at least 1.")

        self.state_store = (
            state_store
            if state_store is not None
            else MemoryAutomationStateStore()
        )
        self.history = (
            history
            if history is not None
            else MemoryAutomationRunHistory()
        )
        self._executor = ThreadPoolExecutor(max_workers=max_workers)

    def submit(
        self,
        definition: AutomationDefinition,
        *,
        input: Any = None,
    ) -> Future[AutomationRun]:
        """
        Submit an automation for background execution.

        Returns a Future that resolves to the completed AutomationRun.
        """

        run = AutomationRun(
            definition_id=definition.id,
            definition_version=definition.version,
            input=input,
        )

        self.state_store.save(run)

        return self._executor.submit(
            self._execute,
            definition,
            run,
        )

    def run(
        self,
        definition: AutomationDefinition,
        *,
        input: Any = None,
    ) -> AutomationRun:
        """
        Execute an automation immediately in the current thread.
        """

        run = AutomationRun(
            definition_id=definition.id,
            definition_version=definition.version,
            input=input,
        )

        return self._execute(definition, run)

    def _execute(
        self,
        definition: AutomationDefinition,
        run: AutomationRun,
    ) -> AutomationRun:
        run.start()
        self.state_store.save(run)

        try:
            result = definition.run()

            if getattr(result, "success", False):
                run.complete(result.output)
            else:
                run.fail(
                    getattr(result, "error", None)
                    or "Automation execution failed."
                )
        except Exception as exc:
            run.fail(str(exc))

        self.state_store.save(run)
        self.history.record(run)

        return run

    def shutdown(
        self,
        *,
        wait: bool = True,
        cancel_futures: bool = False,
    ) -> None:
        """
        Shut down the background worker.
        """

        self._executor.shutdown(
            wait=wait,
            cancel_futures=cancel_futures,
        )

    def __enter__(self) -> AutomationWorker:
        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ) -> None:
        self.shutdown()

