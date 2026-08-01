from __future__ import annotations

import sqlite3

from bindai_memory.provider import MemoryProvider
from bindai_memory.record import MemoryRecord
from bindai_memory.result import MemoryResult


class SQLiteMemoryProvider(MemoryProvider):
    """
    SQLite-backed memory provider.
    """

    def __init__(
        self,
        database: str = "bindai.db",
    ):
        self._connection: sqlite3.Connection | None = sqlite3.connect(
            database,
            check_same_thread=False,
        )

        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS memory(
                namespace TEXT NOT NULL,
                key TEXT NOT NULL,
                value TEXT NOT NULL,
                type TEXT NOT NULL,
                PRIMARY KEY(namespace, key)
            )
            """
        )

        self._connection.commit()

    def _ensure_connection(self) -> sqlite3.Connection:
        """
        Return active SQLite connection.
        """

        if self._connection is None:
            raise RuntimeError(
                "SQLiteMemoryProvider is closed"
            )

        return self._connection

    def close(self) -> None:
        """
        Close SQLite database connection.
        """

        if self._connection is not None:
            self._connection.close()
            self._connection = None

    def set(
        self,
        record: MemoryRecord,
    ) -> MemoryResult:

        connection = self._ensure_connection()

        connection.execute(
            """
            INSERT INTO memory
            (
                namespace,
                key,
                value,
                type
            )
            VALUES (?, ?, ?, ?)

            ON CONFLICT(namespace,key)
            DO UPDATE SET
                value=excluded.value,
                type=excluded.type
            """,
            (
                record.namespace,
                record.key,
                str(record.value),
                record.type.value,
            ),
        )

        connection.commit()

        return MemoryResult(
            success=True,
            value=record,
        )

    def get(
        self,
        key: str,
        namespace: str = "default",
    ) -> MemoryResult:

        connection = self._ensure_connection()

        row = connection.execute(
            """
            SELECT key, value, type
            FROM memory
            WHERE namespace=? 
            AND key=?
            """,
            (
                namespace,
                key,
            ),
        ).fetchone()

        if row is None:
            return MemoryResult(
                success=False,
            )

        return MemoryResult(
            success=True,
            value=MemoryRecord(
                key=row[0],
                value=row[1],
                namespace=namespace,
            ),
        )

    def search(
        self,
        query: str,
        namespace: str = "default",
        limit: int = 10,
        metadata: dict | None = None,
    ) -> list[MemoryRecord]:

        connection = self._ensure_connection()

        rows = connection.execute(
            """
            SELECT key, value, type
            FROM memory
            WHERE namespace=?
            AND value LIKE ?
            LIMIT ?
            """,
            (
                namespace,
                f"%{query}%",
                limit,
            ),
        ).fetchall()

        return [
            MemoryRecord(
                key=row[0],
                value=row[1],
                namespace=namespace,
            )
            for row in rows
        ]

    def delete(
        self,
        key: str,
        namespace: str = "default",
    ) -> MemoryResult:

        connection = self._ensure_connection()

        connection.execute(
            """
            DELETE FROM memory
            WHERE namespace=?
            AND key=?
            """,
            (
                namespace,
                key,
            ),
        )

        connection.commit()

        return MemoryResult(
            success=True,
        )

    def exists(
        self,
        key: str,
        namespace: str = "default",
    ) -> bool:

        connection = self._ensure_connection()

        row = connection.execute(
            """
            SELECT 1
            FROM memory
            WHERE namespace=?
            AND key=?
            """,
            (
                namespace,
                key,
            ),
        ).fetchone()

        return row is not None

    def clear(
        self,
        namespace: str = "default",
    ) -> MemoryResult:

        connection = self._ensure_connection()

        connection.execute(
            """
            DELETE FROM memory
            WHERE namespace=?
            """,
            (namespace,),
        )

        connection.commit()

        return MemoryResult(
            success=True,
        )