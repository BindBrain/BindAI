from __future__ import annotations

import yaml
from bindai_agent import AgentBuilder
from bindai_group import (
    GroupBuilder,
    ParallelProcess,
    SequentialProcess,
    Task,
)

from .loader import ConfigLoader
from .models import (
    AgentConfig,
    GroupConfig,
    TaskConfig,
)


class YamlLoader(ConfigLoader):
    def load(
        self,
        path: str,
    ):

        with open(
            path,
            encoding="utf-8",
        ) as file:
            data = yaml.safe_load(
                file,
            )

        config = self._parse_group(
            data,
        )

        return self._build_group(
            config,
        )

    #
    # Parsing
    #

    def _parse_group(
        self,
        data,
    ) -> GroupConfig:

        group_data = data["group"]

        config = GroupConfig(
            name=group_data.get(
                "name",
                "group",
            ),
            description=group_data.get(
                "description",
                "",
            ),
            process=group_data.get(
                "process",
                "sequential",
            ),
        )

        #
        # Agents
        #

        for item in group_data.get(
            "agents",
            [],
        ):
            config.agents.append(
                AgentConfig(
                    id=item["id"],
                    name=item["name"],
                    instructions=item["instructions"],
                    provider=item.get(
                        "provider",
                        "openai",
                    ),
                    model=item.get(
                        "model",
                        "gpt-4.1",
                    ),
                    temperature=item.get(
                        "temperature",
                        0.7,
                    ),
                    max_tokens=item.get(
                        "max_tokens",
                    ),
                )
            )

        #
        # Tasks
        #

        for item in group_data.get(
            "tasks",
            [],
        ):
            config.tasks.append(
                TaskConfig(
                    id=item["id"],
                    description=item["description"],
                    expected_output=item.get(
                        "expected_output",
                    ),
                    agent=item["agent"],
                    context=item.get(
                        "context",
                        [],
                    ),
                )
            )

        return config

    #
    # Runtime objects
    #

    def _build_group(
        self,
        config: GroupConfig,
    ):

        process_name = config.process.lower()

        if process_name == "sequential":
            process = SequentialProcess()

        elif process_name == "parallel":
            process = ParallelProcess()

        else:
            raise ValueError(
                f'Unknown group process "{config.process}". '
                'Expected "sequential" or "parallel".'
            )

        builder = (
            GroupBuilder()
            .name(
                config.name,
            )
            .process(
                process,
            )
        )

        agents = self._build_agents(
            config,
            builder,
        )

        tasks = self._build_tasks(
            config,
            agents,
        )

        self._wire_dependencies(
            builder,
            config,
            tasks,
        )

        return builder.build()

    def _build_agents(
        self,
        config: GroupConfig,
        builder: GroupBuilder,
    ):

        agents = {}

        for item in config.agents:
            agent_builder = (
                AgentBuilder()
                .name(
                    item.name,
                )
                .instructions(
                    item.instructions,
                )
                .openai(
                    model=item.model,
                )
                .temperature(
                    item.temperature,
                )
            )

            if item.max_tokens is not None:
                agent_builder.max_tokens(
                    item.max_tokens,
                )

            agent = agent_builder.build()

            agents[item.id] = agent

            builder.agent(
                agent,
            )

        return agents

    def _build_tasks(
        self,
        config: GroupConfig,
        agents: dict,
    ):

        tasks = {}

        for item in config.tasks:
            if item.agent not in agents:
                raise ValueError(f'Unknown agent "{item.agent}".')

            task = Task(
                description=item.description,
                expected_output=item.expected_output,
                agent=agents[item.agent],
            )

            tasks[item.id] = task

        return tasks

    def _wire_dependencies(
        self,
        builder: GroupBuilder,
        config: GroupConfig,
        tasks: dict,
    ):

        for item in config.tasks:
            task = tasks[item.id]

            for dependency in item.context:
                if dependency not in tasks:
                    raise ValueError(f'Unknown task "{dependency}".')

                task.context_from(tasks[dependency])

            builder.task(
                task,
            )
