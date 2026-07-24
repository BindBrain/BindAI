from .memory import Memory
from .provider import MemoryProvider
from .registry import MemoryRegistry

from .record import (
    MemoryRecord,
    MemoryType,
)

from .result import MemoryResult

from .providers import (
    InMemoryProvider,
    SQLiteMemoryProvider,
    VectorMemoryProvider,
)

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