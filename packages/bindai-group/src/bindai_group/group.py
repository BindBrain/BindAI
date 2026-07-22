from __future__ import annotations

from typing import TYPE_CHECKING

from .executor import GroupExecutor
from .processes.sequential import SequentialProcess
from .state import GroupState

if TYPE_CHECKING:
    from bindai_agent import Agent
    from .task import Task


class Group:
    """
    Coordinates a collection of agents executing tasks.
    """

    def __init__(
        self,
        *,
        name: str = "group",
        process=None,
    ):

        self.name = name

        self.agents: list[Agent] = []

        self.tasks: list[Task] = []

        self.process = process if process is not None else SequentialProcess()

        self.executor = GroupExecutor()

        self.state = GroupState.CREATED

    #
    # Agents
    #

    def agent(
        self,
        agent: Agent,
    ) -> "Group":

        self.agents.append(
            agent,
        )

        return self

    def add_agent(
        self,
        agent: Agent,
    ) -> "Group":

        return self.agent(
            agent,
        )

    #
    # Tasks
    #

    def task(
        self,
        task: Task,
    ) -> "Group":

        self.tasks.append(
            task,
        )

        return self

    def add_task(
        self,
        task: Task,
    ) -> "Group":

        return self.task(
            task,
        )

    #
    # Process
    #

    def use_process(
        self,
        process,
    ) -> "Group":

        self.process = process

        return self

    #
    # Execution
    #

    def run(
        self,
    ):

        return self.executor.execute(
            self,
        )

    #
    # Utilities
    #

    def clear(
        self,
    ):

        self.agents.clear()

        self.tasks.clear()

        self.state = GroupState.CREATED

        return self
