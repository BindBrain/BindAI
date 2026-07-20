from __future__ import annotations

import yaml

from bindai import (
    AgentBuilder,
    GroupBuilder,
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
            "r",
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

        builder = (
            GroupBuilder()
            .name(
                config.name,
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

            agent = (
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
                .max_tokens(
                    item.max_tokens,
                )
                .build()
            )

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

                raise ValueError(
                    f'Unknown agent "{item.agent}".'
                )

            task = Task(

                description=item.description,

                expected_output=item.expected_output,

                agent=agents[
                    item.agent
                ],
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

            task = tasks[
                item.id
            ]

            for dependency in item.context:

                if dependency not in tasks:

                    raise ValueError(
                        f'Unknown task "{dependency}".'
                    )

                task.context_from(
                    tasks[
                        dependency
                    ]
                )

            builder.task(
                task,
            )