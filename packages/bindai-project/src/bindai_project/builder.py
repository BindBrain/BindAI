from .configuration import ProjectConfiguration
from .project import Project


class ProjectBuilder:

    def __init__(
        self,
        name: str,
    ):

        self.project = Project(
            ProjectConfiguration(
                name=name,
            )
        )

    def agent(
        self,
        agent,
    ):

        self.project.add_agent(
            agent,
        )

        return self

    def tool(
        self,
        tool,
    ):

        self.project.add_tool(
            tool,
        )

        return self

    def build(
        self,
    ):

        return self.project