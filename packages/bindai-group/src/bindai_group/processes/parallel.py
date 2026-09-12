from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed

from bindai_core.context import ExecutionContext

from ..process import Process
from ..result import GroupResult
from ..state import GroupState


class ParallelProcess(Process):
    """
    Execute group tasks concurrently while respecting task dependencies.

    Tasks with no unresolved dependencies run concurrently. A task only
    becomes eligible after all tasks in its ``context`` have completed
    successfully.
    """

    def execute(self, group, context: ExecutionContext) -> GroupResult:
        group.state = GroupState.RUNNING

        completed: set[int] = set()
        outputs: dict[int, str] = {}

        while len(completed) < len(group.tasks):
            ready = self._ready_tasks(group, completed)

            if not ready:
                group.state = GroupState.FAILED

                return GroupResult(
                    success=False,
                    error="Unable to resolve task dependencies.",
                    tasks=group.tasks,
                )

            with ThreadPoolExecutor(max_workers=len(ready)) as executor:
                futures = {
                    executor.submit(
                        self._execute_task,
                        group.tasks[index],
                    ): index
                    for index in ready
                }

                for future in as_completed(futures):
                    index = futures[future]
                    task = group.tasks[index]

                    try:
                        result = future.result()
                    except Exception as ex:
                        group.state = GroupState.FAILED

                        return GroupResult(
                            success=False,
                            error=str(ex),
                            tasks=group.tasks,
                        )

                    task.result = result
                    completed.add(index)

                    if not result.success:
                        group.state = GroupState.FAILED

                        return GroupResult(
                            success=False,
                            error=result.error or "Task execution failed.",
                            tasks=group.tasks,
                        )

                    if result.output is not None:
                        outputs[index] = str(result.output)

        group.state = GroupState.COMPLETED

        output = "\n\n".join(
            outputs[index] for index in range(len(group.tasks)) if index in outputs
        )

        return GroupResult(
            success=True,
            output=output,
            tasks=group.tasks,
        )

    def _ready_tasks(
        self,
        group,
        completed: set[int],
    ) -> list[int]:
        ready = []

        for index, task in enumerate(group.tasks):
            if index in completed:
                continue

            if task.result is not None:
                completed.add(index)
                continue

            dependencies_ready = all(
                group.tasks.index(dependency) in completed for dependency in task.context
            )

            if dependencies_ready:
                ready.append(index)

        return ready

    def _execute_task(self, task):
        context = ExecutionContext()

        context.variables.set(
            "input",
            self._build_prompt(task),
        )

        return task.agent.execute(context)

    def _build_prompt(self, task) -> str:
        sections = [
            "Task",
            "----------------",
            task.description,
        ]

        if task.expected_output:
            sections.extend(
                [
                    "",
                    "Expected Output",
                    "----------------",
                    task.expected_output,
                ]
            )

        if task.context:
            sections.extend(
                [
                    "",
                    "Context",
                    "----------------",
                ]
            )

            for previous in task.context:
                if previous.result is None:
                    continue

                sections.extend(
                    [
                        "",
                        previous.agent.name,
                        "",
                        str(previous.result.output),
                    ]
                )

        return "\n".join(sections)
