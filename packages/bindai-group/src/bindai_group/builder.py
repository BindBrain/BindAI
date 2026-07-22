from __future__ import annotations

from .group import Group
from .processes.sequential import SequentialProcess


class GroupBuilder:
    def __init__(self):

        self._name = "group"

        self._agents = []

        self._tasks = []

        self._process = SequentialProcess()

    #
    # Metadata
    #

    def name(
        self,
        value: str,
    ):

        self._name = value

        return self

    #
    # Agents
    #

    def agent(
        self,
        agent,
    ):

        self._agents.append(
            agent,
        )

        return self

    def add_agent(
        self,
        agent,
    ):

        return self.agent(
            agent,
        )

    #
    # Tasks
    #

    def task(
        self,
        task,
    ):

        self._tasks.append(
            task,
        )

        return self

    def add_task(
        self,
        task,
    ):

        return self.task(
            task,
        )

    #
    # Process
    #

    def process(
        self,
        process,
    ):

        self._process = process

        return self

    #
    # Build
    #

    def build(
        self,
    ):

        if not self._agents:
            raise ValueError("Group must contain at least one agent.")

        if not self._tasks:
            raise ValueError("Group must contain at least one task.")

        group = Group(
            name=self._name,
            process=self._process,
        )

        for agent in self._agents:
            group.agent(
                agent,
            )

        for task in self._tasks:
            if task.agent not in group.agents:
                raise ValueError(f'Task references unknown agent "{task.agent.name}".')

            group.task(
                task,
            )

        return group
