from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from typing import Any

from pinecone import Pinecone

from bindai_memory.provider import MemoryProvider
from bindai_memory.record import MemoryRecord, MemoryType
from bindai_memory.result import MemoryResult


class PineconeMemoryProvider(MemoryProvider):
    """
    Pinecone-backed memory provider.
    """

    def __init__(
        self,
        index_name: str = "crewai-ba-bindbrain-knowledge",
        api_key: str | None = None,
        embedding: str = "openai",
    ) -> None:

        if api_key is None:
            api_key = os.getenv("PINECONE_API_KEY")

        if not api_key:
            raise ValueError("PINECONE_API_KEY is required for PineconeMemoryProvider.")

        from bindai_embeddings import EmbeddingRegistry

        self.embedding = EmbeddingRegistry.provider(
            embedding,
        )()

        self._pinecone = Pinecone(
            api_key=api_key,
        )

        self._index = self._pinecone.Index(
            index_name,
        )

    def set(
        self,
        record: MemoryRecord,
    ) -> MemoryResult:

        now = datetime.now(
            UTC,
        )

        if record.created_at is None:
            record.created_at = now

        record.updated_at = now

        record.embedding = self.embedding.embed(
            str(record.value),
        )

        metadata = self._record_metadata(
            record,
        )

        self._index.upsert(
            vectors=[
                {
                    "id": record.key,
                    "values": record.embedding,
                    "metadata": metadata,
                }
            ],
            namespace=record.namespace,
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

        response = self._index.fetch(
            ids=[key],
            namespace=namespace,
        )

        vectors = getattr(
            response,
            "vectors",
            {},
        )

        vector = vectors.get(
            key,
        )

        if vector is None:
            return MemoryResult(
                success=False,
            )

        record = self._record_from_metadata(
            key,
            vector.metadata or {},
            namespace,
        )

        if self._expired(record):
            return MemoryResult(
                success=False,
            )

        record.last_accessed = datetime.now(
            UTC,
        )

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

        query_embedding = self.embedding.embed(
            query,
        )

        response = self._index.query(
            vector=query_embedding,
            top_k=limit,
            namespace=namespace,
            filter=metadata,
            include_metadata=True,
        )

        results: list[MemoryRecord] = []

        for match in response.matches:
            record = self._record_from_metadata(
                match.id,
                match.metadata or {},
                namespace,
            )

            if self._expired(record):
                continue

            record.score = match.score

            record.last_accessed = datetime.now(
                UTC,
            )

            record.access_count += 1

            results.append(
                record,
            )

        return results

    def delete(
        self,
        key: str,
        namespace: str = "default",
    ) -> MemoryResult:

        self._index.delete(
            ids=[key],
            namespace=namespace,
        )

        return MemoryResult(
            success=True,
        )

    def exists(
        self,
        key: str,
        namespace: str = "default",
    ) -> bool:

        response = self._index.fetch(
            ids=[key],
            namespace=namespace,
        )

        vectors = getattr(
            response,
            "vectors",
            {},
        )

        vector = vectors.get(
            key,
        )

        if vector is None:
            return False

        record = self._record_from_metadata(
            key,
            vector.metadata or {},
            namespace,
        )

        return not self._expired(record)

    def clear(
        self,
        namespace: str = "default",
    ) -> MemoryResult:

        self._index.delete(
            delete_all=True,
            namespace=namespace,
        )

        return MemoryResult(
            success=True,
        )

    def _record_metadata(
        self,
        record: MemoryRecord,
    ) -> dict[str, Any]:

        metadata: dict[str, Any] = {
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
            metadata["created_at"] = record.created_at.isoformat()

        if record.updated_at is not None:
            metadata["updated_at"] = record.updated_at.isoformat()

        if record.last_accessed is not None:
            metadata["last_accessed"] = record.last_accessed.isoformat()

        if record.expires_at is not None:
            metadata["expires_at"] = record.expires_at.isoformat()

        for key, value in record.metadata.items():
            if isinstance(value, (str, int, float, bool)):
                metadata[f"meta__{key}"] = value
            elif isinstance(value, list) and all(isinstance(item, str) for item in value):
                metadata[f"meta__{key}"] = value

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
            value = json.loads(
                value,
            )
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
                metadata.get(
                    "created_at",
                ),
            ),
            updated_at=self._datetime(
                metadata.get(
                    "updated_at",
                ),
            ),
            last_accessed=self._datetime(
                metadata.get(
                    "last_accessed",
                ),
            ),
            expires_at=self._datetime(
                metadata.get(
                    "expires_at",
                ),
            ),
        )

    def _datetime(
        self,
        value: Any,
    ) -> datetime | None:

        if value is None:
            return None

        return datetime.fromisoformat(
            value,
        )

    def _expired(
        self,
        record: MemoryRecord,
    ) -> bool:

        if record.expires_at is None:
            return False

        return datetime.now(UTC) >= record.expires_at

    def close(
        self,
    ) -> None:
        """
        Pinecone client does not require an explicit close.
        """
        return None
