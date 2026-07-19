from bindai_memory import (
    InMemoryProvider,
    Memory,
    MemoryRecord,
)

memory = Memory(
    InMemoryProvider(),
)

memory.set(
    MemoryRecord(
        key="employee",
        value="John",
        namespace="acme",
    )
)

result = memory.get(
    "employee",
    namespace="acme",
)

print(result.value.value)