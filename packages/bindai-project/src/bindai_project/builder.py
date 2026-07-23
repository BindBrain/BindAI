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

    def application(
        self,
        application,
    ):

        self.project.add_application(
            application,
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
