from .memory import Memory
from .provider import MemoryProvider
from .providers import (
    InMemoryProvider,
    SQLiteMemoryProvider,
    VectorMemoryProvider,
)
from .record import (
    MemoryRecord,
    MemoryType,
)
from .registry import MemoryRegistry
from .result import MemoryResult

#
# Register aliases
#

MemoryRegistry.register(
    "memory",
    InMemoryProvider,
)

MemoryRegistry.register(
    "in_memory",
    InMemoryProvider,
)

MemoryRegistry.register(
    "sqlite",
    SQLiteMemoryProvider,
)

#
# "vector" is already registered in registry.py
#

__all__ = [
    "Memory",
    "MemoryProvider",
    "MemoryRegistry",
    "MemoryRecord",
    "MemoryType",
    "MemoryResult",
    "InMemoryProvider",
    "SQLiteMemoryProvider",
    "VectorMemoryProvider",
]
