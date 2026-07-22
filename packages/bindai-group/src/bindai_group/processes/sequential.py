from __future__ import annotations

from ..process import Process
from ..result import GroupResult
from ..state import GroupState


class SequentialProcess(Process):
    """
    Executes tasks one-by-one.
    """

    def execute(
        self,
        group,
    ):

        group.state = GroupState.RUNNING

        outputs = []

        for task in group.tasks:
            result = self._execute_task(
                task,
            )

            task.result = result

            if not result.success:
                group.state = GroupState.FAILED

                return GroupResult(
                    success=False,
                    error=result.error,
                    tasks=group.tasks,
                )

            if result.output:
                outputs.append(
                    str(
                        result.output,
                    )
                )

        group.state = GroupState.COMPLETED

        return GroupResult(
            success=True,
            output="\n\n".join(outputs),
            tasks=group.tasks,
        )

    #
    # Helpers
    #

    def _execute_task(
        self,
        task,
    ):

        prompt = self._build_prompt(
            task,
        )

        return task.agent.chat(
            prompt,
        )

    def _build_prompt(
        self,
        task,
    ) -> str:

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
                        str(
                            previous.result.output,
                        ),
                    ]
                )

        return "\n".join(
            sections,
        )
