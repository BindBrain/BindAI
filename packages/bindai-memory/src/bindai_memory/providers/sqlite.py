from __future__ import annotations

import json
import sqlite3
from datetime import UTC, datetime

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

                metadata TEXT NOT NULL,

                importance REAL NOT NULL,

                access_count INTEGER NOT NULL,

                created_at TEXT,
                updated_at TEXT,
                last_accessed TEXT,
                expires_at TEXT,

                PRIMARY KEY(namespace,key)
            )
            """
        )

        self._connection.commit()

        connection = self._ensure_connection()

        columns = {row[1] for row in connection.execute("PRAGMA table_info(memory)")}

        required = {
            "metadata": "TEXT NOT NULL DEFAULT '{}'",
            "importance": "REAL NOT NULL DEFAULT 1.0",
            "access_count": "INTEGER NOT NULL DEFAULT 0",
            "created_at": "TEXT",
            "updated_at": "TEXT",
            "last_accessed": "TEXT",
            "expires_at": "TEXT",
        }

        for column, definition in required.items():
            if column not in columns:
                connection.execute(
                    f"""
                    ALTER TABLE memory
                    ADD COLUMN {column}
                    {definition}
                    """
                )

        connection.commit()

    def _ensure_connection(self) -> sqlite3.Connection:
        """
        Return active SQLite connection.
        """

        if self._connection is None:
            raise RuntimeError("SQLiteMemoryProvider is closed")

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

        now = datetime.now(
            UTC,
        )

        if record.created_at is None:
            record.created_at = now

        record.updated_at = now

        connection.execute(
            """
            INSERT INTO memory
            (
                namespace,
                key,
                value,
                type,
                metadata,
                importance,
                access_count,
                created_at,
                updated_at,
                last_accessed,
                expires_at
            )
            VALUES
            (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )

            ON CONFLICT(namespace,key)
            DO UPDATE SET

                value=excluded.value,
                type=excluded.type,
                metadata=excluded.metadata,
                importance=excluded.importance,
                access_count=excluded.access_count,
                updated_at=excluded.updated_at,
                last_accessed=excluded.last_accessed,
                expires_at=excluded.expires_at
            """,
            (
                record.namespace,
                record.key,
                str(record.value),
                record.type.value,
                json.dumps(
                    record.metadata,
                ),
                record.importance,
                record.access_count,
                record.created_at.isoformat() if record.created_at else None,
                record.updated_at.isoformat() if record.updated_at else None,
                record.last_accessed.isoformat() if record.last_accessed else None,
                record.expires_at.isoformat() if record.expires_at else None,
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
            SELECT
                key,
                value,
                type,
                metadata,
                importance,
                access_count,
                created_at,
                updated_at,
                last_accessed,
                expires_at
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

        record = MemoryRecord(
            key=row[0],
            value=row[1],
            namespace=namespace,
            metadata=json.loads(
                row[3],
            ),
            importance=row[4],
            access_count=row[5],
            created_at=(datetime.fromisoformat(row[6]) if row[6] else datetime.now(UTC)),
            updated_at=(datetime.fromisoformat(row[7]) if row[7] else datetime.now(UTC)),
            last_accessed=(datetime.fromisoformat(row[8]) if row[8] else None),
            expires_at=(datetime.fromisoformat(row[9]) if row[9] else None),
        )

        if record.expires_at is not None and datetime.now(UTC) >= record.expires_at:
            return MemoryResult(
                success=False,
            )

        return MemoryResult(
            success=True,
            value=record,
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
            SELECT
                key,
                value,
                type,
                metadata,
                importance,
                access_count,
                created_at,
                updated_at,
                last_accessed,
                expires_at
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

        results: list[MemoryRecord] = []

        for row in rows:
            record = MemoryRecord(
                key=row[0],
                value=row[1],
                namespace=namespace,
                metadata=json.loads(
                    row[3],
                ),
                importance=row[4],
                access_count=row[5],
                created_at=(datetime.fromisoformat(row[6]) if row[6] else datetime.now(UTC)),
                updated_at=(datetime.fromisoformat(row[7]) if row[7] else datetime.now(UTC)),
                last_accessed=(datetime.fromisoformat(row[8]) if row[8] else None),
                expires_at=(datetime.fromisoformat(row[9]) if row[9] else None),
            )

            if record.expires_at is not None and datetime.now(UTC) >= record.expires_at:
                continue

            if metadata:
                matches = all(record.metadata.get(key) == value for key, value in metadata.items())

                if not matches:
                    continue

            results.append(
                record,
            )

        return results

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
            SELECT expires_at
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
            return False

        expires_at = row[0]

        if expires_at is None:
            return True

        return datetime.now(UTC) < datetime.fromisoformat(expires_at)

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
