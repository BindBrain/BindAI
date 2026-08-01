from bindai_memory import (
    Memory,
    MemoryRecord,
    MemoryType,
)

print("=" * 60)
print("Memory")
print("=" * 60)

memory = Memory()

#
# Store
#

record = MemoryRecord(
    key="favorite_language",
    value="Python",
    namespace="profile",
    type=MemoryType.LONG_TERM,
)

result = memory.set(record)

print("\nStored:")
print(result.success)
print(result.value)

#
# Retrieve
#

result = memory.get(
    "favorite_language",
    namespace="profile",
)

print("\nRetrieved:")
print(result.success)
print(result.value)

#
# Exists
#

print("\nExists:")
print(
    memory.exists(
        "favorite_language",
        namespace="profile",
    )
)

#
# Search
#

memory.set(
    MemoryRecord(
        key="framework",
        value="BindAI",
        namespace="profile",
    )
)

memory.set(
    MemoryRecord(
        key="database",
        value="PostgreSQL",
        namespace="profile",
    )
)

print("\nSearch Results:")

results = memory.search(
    "bind",
    namespace="profile",
)

for item in results:
    print(f"- {item.key}: {item.value}")

#
# Delete
#

memory.delete(
    "database",
    namespace="profile",
)

print("\nDatabase Exists:")
print(
    memory.exists(
        "database",
        namespace="profile",
    )
)

#
# Clear Namespace
#

memory.clear(
    namespace="profile",
)

print("\nNamespace Cleared")

print(
    memory.exists(
        "favorite_language",
        namespace="profile",
    )
)
