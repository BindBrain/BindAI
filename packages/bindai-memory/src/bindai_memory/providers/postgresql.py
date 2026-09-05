from __future__ import annotations

import json
from datetime import UTC, datetime

import psycopg

from bindai_memory.provider import MemoryProvider
from bindai_memory.record import MemoryRecord
from bindai_memory.result import MemoryResult


class PostgreSQLMemoryProvider(MemoryProvider):
    """
    PostgreSQL-backed memory provider.
    """

    def __init__(
        self,
        database: str,
    ):
        self._connection = psycopg.connect(database)

        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS memory(
                namespace TEXT NOT NULL,
                key TEXT NOT NULL,
                value TEXT NOT NULL,
                type TEXT NOT NULL,
                metadata JSONB NOT NULL,
                importance DOUBLE PRECISION NOT NULL,
                access_count INTEGER NOT NULL,
                created_at TIMESTAMPTZ NOT NULL,
                updated_at TIMESTAMPTZ NOT NULL,
                last_accessed TIMESTAMPTZ,
                expires_at TIMESTAMPTZ,
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
            INSERT INTO memory (
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
            VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            ON CONFLICT (namespace, key)
            DO UPDATE SET
                value = EXCLUDED.value,
                type = EXCLUDED.type,
                metadata = EXCLUDED.metadata,
                importance = EXCLUDED.importance,
                access_count = EXCLUDED.access_count,
                updated_at = EXCLUDED.updated_at,
                last_accessed = EXCLUDED.last_accessed,
                expires_at = EXCLUDED.expires_at
            """,
            (
                record.namespace,
                record.key,
                str(record.value),
                record.type.value,
                json.dumps(record.metadata),
                record.importance,
                record.access_count,
                record.created_at,
                record.updated_at,
                record.last_accessed,
                record.expires_at,
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
            SELECT
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
            FROM memory
            WHERE namespace = %s
              AND key = %s
            """,
            (namespace, key),
        ).fetchone()

        if row is None:
            return MemoryResult(
                success=False,
                error="Memory record not found.",
            )

        (
            namespace,
            key,
            value,
            memory_type,
            metadata,
            importance,
            access_count,
            created_at,
            updated_at,
            last_accessed,
            expires_at,
        ) = row

        if expires_at is not None:
            if expires_at <= datetime.now(UTC):
                return MemoryResult(
                    success=False,
                    error="Memory record has expired.",
                )

        record = MemoryRecord(
            namespace=namespace,
            key=key,
            value=value,
            type=memory_type,
            metadata=metadata,
            importance=importance,
            access_count=access_count,
            created_at=created_at,
            updated_at=updated_at,
            last_accessed=last_accessed,
            expires_at=expires_at,
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

        rows = self._connection.execute(
            """
            SELECT
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
            FROM memory
            WHERE namespace = %s
            """,
            (namespace,),
        ).fetchall()

        query_lower = query.lower()
        results: list[MemoryRecord] = []

        for row in rows:
            (
                row_namespace,
                key,
                value,
                memory_type,
                row_metadata,
                importance,
                access_count,
                created_at,
                updated_at,
                last_accessed,
                expires_at,
            ) = row

            if expires_at is not None:
                if expires_at <= datetime.now(UTC):
                    continue

            if metadata:
                if any(
                    row_metadata.get(k) != v
                    for k, v in metadata.items()
                ):
                    continue

            if query_lower not in value.lower():
                continue

            results.append(
                MemoryRecord(
                    namespace=row_namespace,
                    key=key,
                    value=value,
                    type=memory_type,
                    metadata=row_metadata,
                    importance=importance,
                    access_count=access_count,
                    created_at=created_at,
                    updated_at=updated_at,
                    last_accessed=last_accessed,
                    expires_at=expires_at,
                )
            )

            if len(results) >= limit:
                break

        return results

    def delete(
        self,
        key: str,
        namespace: str = "default",
    ) -> MemoryResult:

        cursor = self._connection.execute(
            """
            DELETE FROM memory
            WHERE namespace = %s
              AND key = %s
            """,
            (namespace, key),
        )

        self._connection.commit()

        return MemoryResult(
            success=cursor.rowcount > 0,
        )

    def exists(
        self,
        key: str,
        namespace: str = "default",
    ) -> bool:

        row = self._connection.execute(
            """
            SELECT expires_at
            FROM memory
            WHERE namespace = %s
              AND key = %s
            """,
            (namespace, key),
        ).fetchone()

        if row is None:
            return False

        expires_at = row[0]

        if expires_at is not None:
            if expires_at <= datetime.now(UTC):
                return False

        return True

    def clear(
        self,
        namespace: str = "default",
    ) -> MemoryResult:

        self._connection.execute(
            """
            DELETE FROM memory
            WHERE namespace = %s
            """,
            (namespace,),
        )

        self._connection.commit()

        return MemoryResult(
            success=True,
        )

    def close(
        self,
    ) -> None:

        self._connection.close()