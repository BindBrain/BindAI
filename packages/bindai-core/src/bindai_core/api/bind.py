from bindai_core.host import BindHostBuilder


class Bind:

    @staticmethod
    def create(name: str):

        return BindHostBuilder(name).build()