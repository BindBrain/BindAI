from abc import ABC, abstractmethod


class BaseProvider(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def capabilities(self): ...

    @abstractmethod
    async def generate(self, request): ...

    @abstractmethod
    async def stream(self, request): ...
