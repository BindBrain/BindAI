from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import Any

import chromadb

from bindai_memory.provider import MemoryProvider
from bindai_memory.record import MemoryRecord, MemoryType
from bindai_memory.result import MemoryResult


class ChromaMemoryProvider(MemoryProvider):
    """
    Chroma-backed memory provider.
    """

    def __init__(
        self,
        path: str = "bindai_chroma",
        collection_name: str = "bindai_memory",
    ) -> None:
        self.path = path
        self.collection_name = collection_name

        self._client = chromadb.PersistentClient(
            path=path,
        )

        self._collection = self._client.get_or_create_collection(
            name=collection_name,
            metadata={
                "description": "BindAI memory collection",
            },
        )

    def _storage_key(
        self,
        key: str,
        namespace: str,
    ) -> str:
        return f"{namespace}:{key}"

    def set(
        self,
        record: MemoryRecord,
    ) -> MemoryResult:
        now = datetime.now(UTC)

        if record.created_at is None:
            record.created_at = now

        record.updated_at = now

        metadata = self._record_metadata(record)

        storage_key = self._storage_key(
            record.key,
            record.namespace,
        )

        if record.embedding is not None:
            self._collection.upsert(
                ids=[storage_key],
                embeddings=[record.embedding],
                documents=[str(record.value)],
                metadatas=[metadata],
            )
        else:
            self._collection.upsert(
                ids=[storage_key],
                documents=[str(record.value)],
                metadatas=[metadata],
            )

        return MemoryResult(
            success=True,
            value=record,
        )

    def get(
        self,
        key: str,
        namespace: str = "default",
    ) -> MemoryResult:
        storage_key = self._storage_key(
            key,
            namespace,
        )

        response = self._collection.get(
            ids=[storage_key],
            include=[
                "documents",
                "metadatas",
            ],
        )

        ids = response.get("ids", [])

        if not ids:
            return MemoryResult(
                success=False,
            )

        metadata_list = response.get("metadatas") or [{}]
        metadata = metadata_list[0] or {}

        record = self._record_from_metadata(
            key,
            metadata,
            namespace,
        )

        if self._expired(record):
            return MemoryResult(
                success=False,
            )

        record.last_accessed = datetime.now(UTC)
        record.access_count += 1

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
        namespace_condition = {
            "namespace": namespace,
        }

        where: dict[str, Any]

        if metadata:
            conditions = [
                {
                    f"meta__{key}": value,
                }
                for key, value in metadata.items()
            ]

            where = {
                "$and": [
                    namespace_condition,
                    *conditions,
                ],
            }
        else:
            where = namespace_condition

        response = self._collection.query(
            query_texts=[query],
            n_results=limit,
            where=where,
            include=[
                "documents",
                "metadatas",
                "distances",
            ],
        )

        ids = response.get("ids") or [[]]
        metadata_groups = response.get("metadatas") or [[]]
        distances = response.get("distances") or [[]]

        result_ids = ids[0] if ids else []
        result_metadata = (
            metadata_groups[0]
            if metadata_groups
            else []
        )
        result_distances = (
            distances[0]
            if distances
            else []
        )

        results: list[MemoryRecord] = []

        for index, storage_key in enumerate(result_ids):
            record_metadata = (
                result_metadata[index]
                if index < len(result_metadata)
                else {}
            )

            original_key = record_metadata.get(
                "key",
                storage_key,
            )

            record = self._record_from_metadata(
                original_key,
                record_metadata or {},
                namespace,
            )

            if self._expired(record):
                continue

            if index < len(result_distances):
                distance = result_distances[index]

                if distance is not None:
                    record.score = 1.0 / (
                        1.0 + float(distance)
                    )

            record.last_accessed = datetime.now(UTC)
            record.access_count += 1

            results.append(record)

        return results

    def delete(
        self,
        key: str,
        namespace: str = "default",
    ) -> MemoryResult:
        storage_key = self._storage_key(
            key,
            namespace,
        )

        self._collection.delete(
            ids=[storage_key],
        )

        return MemoryResult(
            success=True,
        )

    def exists(
        self,
        key: str,
        namespace: str = "default",
    ) -> bool:
        storage_key = self._storage_key(
            key,
            namespace,
        )

        response = self._collection.get(
            ids=[storage_key],
            include=[
                "metadatas",
            ],
        )

        ids = response.get("ids", [])

        if not ids:
            return False

        metadata_list = response.get("metadatas") or [{}]
        metadata = metadata_list[0] or {}

        record = self._record_from_metadata(
            key,
            metadata,
            namespace,
        )

        return not self._expired(record)

    def clear(
        self,
        namespace: str = "default",
    ) -> MemoryResult:
        response = self._collection.get(
            where={
                "namespace": namespace,
            },
            include=[],
        )

        ids = response.get("ids", [])

        if ids:
            self._collection.delete(
                ids=ids,
            )

        return MemoryResult(
            success=True,
        )

    def _record_metadata(
        self,
        record: MemoryRecord,
    ) -> dict[str, Any]:
        metadata: dict[str, Any] = {
            "namespace": record.namespace,
            "key": record.key,
            "value": json.dumps(
                record.value,
                default=str,
            ),
            "type": record.type.value,
            "metadata": json.dumps(
                record.metadata,
                default=str,
            ),
            "importance": record.importance,
            "access_count": record.access_count,
        }

        if record.created_at is not None:
            metadata["created_at"] = (
                record.created_at.isoformat()
            )

        if record.updated_at is not None:
            metadata["updated_at"] = (
                record.updated_at.isoformat()
            )

        if record.last_accessed is not None:
            metadata["last_accessed"] = (
                record.last_accessed.isoformat()
            )

        if record.expires_at is not None:
            metadata["expires_at"] = (
                record.expires_at.isoformat()
            )

        for key, value in record.metadata.items():
            if isinstance(
                value,
                (str, int, float, bool),
            ):
                metadata[f"meta__{key}"] = value

            elif isinstance(value, list) and all(
                isinstance(item, str)
                for item in value
            ):
                metadata[f"meta__{key}"] = json.dumps(
                    value,
                )

        return metadata

    def _record_from_metadata(
        self,
        key: str,
        metadata: dict[str, Any],
        namespace: str,
    ) -> MemoryRecord:
        value = metadata.get(
            "value",
            "",
        )

        try:
            value = json.loads(value)
        except (
            TypeError,
            json.JSONDecodeError,
        ):
            pass

        record_metadata = metadata.get(
            "metadata",
            "{}",
        )

        try:
            record_metadata = json.loads(
                record_metadata,
            )
        except (
            TypeError,
            json.JSONDecodeError,
        ):
            record_metadata = {}

        return MemoryRecord(
            key=key,
            value=value,
            namespace=namespace,
            type=MemoryType(
                metadata.get(
                    "type",
                    MemoryType.LONG_TERM.value,
                ),
            ),
            metadata=record_metadata,
            importance=float(
                metadata.get(
                    "importance",
                    0.5,
                ),
            ),
            access_count=int(
                metadata.get(
                    "access_count",
                    0,
                ),
            ),
            created_at=self._datetime(
                metadata.get("created_at"),
            ),
            updated_at=self._datetime(
                metadata.get("updated_at"),
            ),
            last_accessed=self._datetime(
                metadata.get("last_accessed"),
            ),
            expires_at=self._datetime(
                metadata.get("expires_at"),
            ),
        )

    def _datetime(
        self,
        value: Any,
    ) -> datetime | None:
        if value is None:
            return None

        return datetime.fromisoformat(value)

    def _expired(
        self,
        record: MemoryRecord,
    ) -> bool:
        if record.expires_at is None:
            return False

        return datetime.now(UTC) >= record.expires_at

    def close(self) -> None:
        """
        Chroma PersistentClient does not require an explicit close.
        """
        return None
