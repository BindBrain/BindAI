from .configuration import HostConfiguration
from .host import BindHost


class BindHostBuilder:

    def __init__(self):

        self.host = BindHost(
            HostConfiguration(),
        )

    def project(
        self,
        project,
    ):

        self.host.add_project(
            project,
        )

        return self

    def build(
        self,
    ):

        return self.host