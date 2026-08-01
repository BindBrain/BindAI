from __future__ import annotations

from datetime import UTC, datetime, timedelta

from bindai_memory.record import (
    MemoryRecord,
    MemoryType,
)


class MemoryManager:
    """
    Memory maintenance utilities.
    """

    def should_promote(
        self,
        record: MemoryRecord,
    ) -> bool:

        return record.importance >= 2.0 or record.access_count >= 5

    def promote(
        self,
        record: MemoryRecord,
    ) -> bool:
        """
        Promote a memory to semantic memory.
        """

        if (
            self.should_promote(
                record,
            )
            and record.type != MemoryType.SEMANTIC
        ):
            record.type = MemoryType.SEMANTIC
            record.touch()
            return True

        return False

    def should_forget(
        self,
        record: MemoryRecord,
    ) -> bool:

        if record.expires_at is None:
            return False

        return (
            datetime.now(
                UTC,
            )
            >= record.expires_at
        )

    #
    # Legacy compatibility
    #

    def forget(
        self,
        record: MemoryRecord,
    ) -> bool:

        return self.should_forget(
            record,
        )

    def touch(
        self,
        record: MemoryRecord,
    ) -> None:

        record.access_count += 1

        record.last_accessed = datetime.now(
            UTC,
        )

        record.touch()

    def reinforce(
        self,
        record: MemoryRecord,
        amount: float = 0.25,
    ) -> None:

        record.importance += amount

        record.touch()

    #
    # Importance decay
    #

    def decay(
        self,
        record: MemoryRecord,
        amount: float = 0.05,
    ) -> None:
        """
        Gradually reduce memory importance.

        Importance never becomes negative.
        """

        record.importance = max(
            0.0,
            record.importance - amount,
        )

        record.touch()

    #
    # Alias for newer API
    #

    def weaken(
        self,
        record: MemoryRecord,
        amount: float = 0.1,
    ) -> None:

        self.decay(
            record,
            amount,
        )

    #
    # Expiration helpers
    #

    def set_expiration(
        self,
        record: MemoryRecord,
        *,
        days: int,
    ) -> None:

        record.expires_at = datetime.now(
            UTC,
        ) + timedelta(
            days=days,
        )

        record.touch()

    def clear_expiration(
        self,
        record: MemoryRecord,
    ) -> None:

        record.expires_at = None

        record.touch()
