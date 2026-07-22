from abc import ABC
from abc import abstractmethod


class Middleware(ABC):
    @abstractmethod
    def before_execute(
        self,
        agent,
        context,
    ): ...

    @abstractmethod
    def after_execute(
        self,
        agent,
        context,
        result,
    ): ...
