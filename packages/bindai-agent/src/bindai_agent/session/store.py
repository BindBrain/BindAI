from __future__ import annotations

from abc import ABC, abstractmethod


class SessionStore(ABC):
    @abstractmethod
    def save(self, session): ...

    @abstractmethod
    def load(self, session_id: str): ...

    @abstractmethod
    def delete(self, session_id: str): ...

    @abstractmethod
    def list(self): ...
