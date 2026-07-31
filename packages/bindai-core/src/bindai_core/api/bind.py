from bindai_host import BindHostBuilder


class Bind:
    @staticmethod
    def create(name: str):
        # name is currently ignored by the new host implementation
        return BindHostBuilder().build()
