from bindai_core.application import BindApplication

from .host import BindHost


class BindHostBuilder:

    def __init__(self, name: str):

        self._application = BindApplication(name=name)

    def build(self) -> BindHost:

        return BindHost(self._application)