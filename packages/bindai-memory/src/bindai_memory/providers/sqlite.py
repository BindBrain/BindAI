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

        self._connection = sqlite3.connect(
            database,
        )

        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS memory(
                namespace TEXT,
                key TEXT,
                value TEXT,
                type TEXT,
                PRIMARY KEY(namespace, key)
            )
            """
        )

        self._connection.commit()

    def set(
        self,
        record: MemoryRecord,
    ) -> MemoryResult:

        self._connection.execute(

            """
            INSERT OR REPLACE INTO memory
            (namespace,key,value,type)
            VALUES (?,?,?,?)
            """,

            (
                record.namespace,
                record.key,
                str(record.value),
                record.type.value,
            ),
        )

        self._connection.commit()

        return MemoryResult(
            success=True,
            value=record,
        )

    def get(
        self,
        key: str,
        namespace: str = "default",
    ) -> MemoryResult:

        row = self._connection.execute(

            """
            SELECT key,value,type
            FROM memory
            WHERE namespace=? AND key=?
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

    def delete(
        self,
        key: str,
        namespace: str = "default",
    ) -> MemoryResult:

        self._connection.execute(

            """
            DELETE FROM memory
            WHERE namespace=? AND key=?
            """,

            (
                namespace,
                key,
            ),
        )

        self._connection.commit()

        return MemoryResult(
            success=True,
        )

    def exists(
        self,
        key: str,
        namespace: str = "default",
    ) -> bool:

        row = self._connection.execute(

            """
            SELECT 1
            FROM memory
            WHERE namespace=? AND key=?
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

        self._connection.execute(

            """
            DELETE FROM memory
            WHERE namespace=?
            """,

            (
                namespace,
            ),
        )

        self._connection.commit()

        return MemoryResult(
            success=True,
        )