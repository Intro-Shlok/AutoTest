from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass, field
from typing import Any

from src.storage.blob_store import BlobStore
from src.orchestrator.db import fetch_all, fetch_one, insert
from src.provenance.lineage import record_artifact, record_edge
from src.ulid import prefixed_ulid

logger = logging.getLogger("cache")

TRUST_RANK = {"ai-generated": 0, "experimental": 1, "community": 2, "verified": 3}


@dataclass
class CacheHit:
    artifact_id: str
    artifact_type: str
    content_hash: str
    location: str
    producer_tool_id: str
    created_at: float
    trust_level: str
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def age_seconds(self) -> float:
        return time.time() - self.created_at


class ArtifactCache:
    def __init__(self, blob_store: BlobStore) -> None:
        self.blob_store = blob_store

    async def record_artifact(
        self,
        workflow_id: str,
        task_id: str,
        tool_id: str,
        artifact_type: str,
        content: bytes,
        metadata: dict[str, Any] | None = None,
        trust_level: str = "community",
    ) -> dict[str, Any] | None:
        if not content:
            return None
        content_hash = self.blob_store.store(content)
        location = f"blob:{content_hash}"
        meta = {"tool_id": tool_id, "trust_level": trust_level, **(metadata or {})}

        art = await record_artifact(
            workflow_id=workflow_id,
            producer_task_id=task_id,
            artifact_type=artifact_type,
            location=location,
            content_hash=content_hash,
            metadata=meta,
        )
        if art and art.get("artifact_id"):
            logger.info(
                "Cached artifact %s type=%s hash=%s",
                art["artifact_id"], artifact_type, content_hash[:12],
            )
        return art

    async def find_cached(
        self,
        artifact_type: str,
        max_age_seconds: float = 3600,
        min_trust: str = "community",
    ) -> CacheHit | None:
        min_rank = TRUST_RANK.get(min_trust, 2)
        rows = await fetch_all(
            "SELECT * FROM artifacts WHERE artifact_type = ? ORDER BY created_at DESC LIMIT 20",
            [artifact_type],
        )
        for row in rows:
            meta = json.loads(row.get("metadata_json", "{}") or "{}")
            artifact_trust = meta.get("trust_level", "community")
            if TRUST_RANK.get(artifact_trust, 0) < min_rank:
                continue
            if max_age_seconds > 0:
                age = time.time() - row["created_at"]
                if age > max_age_seconds:
                    continue
            if row.get("hash") and not self.blob_store.exists(row["hash"]):
                continue
            return CacheHit(
                artifact_id=row["id"],
                artifact_type=row["artifact_type"],
                content_hash=row.get("hash", ""),
                location=row.get("location", ""),
                producer_tool_id=meta.get("tool_id", ""),
                created_at=row["created_at"],
                trust_level=artifact_trust,
                metadata=meta,
            )
        return None

    async def get_artifact_content(self, artifact_id: str) -> bytes | None:
        row = await fetch_one("SELECT * FROM artifacts WHERE id = ?", [artifact_id])
        if not row:
            return None
        content_hash = row.get("hash", "")
        if not content_hash:
            return None
        return self.blob_store.retrieve(content_hash)

    async def get_cached_types(self, max_age_seconds: float = 0) -> dict[str, list[dict[str, Any]]]:
        query = "SELECT * FROM artifacts ORDER BY created_at DESC"
        rows = await fetch_all(query)
        grouped: dict[str, list[dict[str, Any]]] = {}
        now = time.time()
        for row in rows:
            if max_age_seconds > 0 and now - row["created_at"] > max_age_seconds:
                continue
            atype = row["artifact_type"]
            if atype not in grouped:
                grouped[atype] = []
            meta = json.loads(row.get("metadata_json", "{}") or "{}")
            grouped[atype].append({
                "artifact_id": row["id"],
                "content_hash": row.get("hash", "")[:12] if row.get("hash") else "",
                "created_at": row["created_at"],
                "age_seconds": round(now - row["created_at"], 1),
                "trust_level": meta.get("trust_level", "community"),
                "producer_tool_id": meta.get("tool_id", ""),
            })
        return grouped

    async def evict_artifact(self, artifact_id: str) -> bool:
        row = await fetch_one("SELECT * FROM artifacts WHERE id = ?", [artifact_id])
        if not row:
            return False
        content_hash = row.get("hash", "")
        if content_hash:
            self.blob_store.delete(content_hash)
        from src.orchestrator.db import update
        await update("artifacts", {"hash": "", "location": ""}, "id = ?", [artifact_id])
        logger.info("Evicted artifact %s (type=%s)", artifact_id, row["artifact_type"])
        return True

    async def get_stats(self) -> dict[str, Any]:
        rows = await fetch_all("SELECT artifact_type, COUNT(*) as count FROM artifacts GROUP BY artifact_type ORDER BY count DESC")
        total = sum(r["count"] for r in rows)
        return {
            "total_artifacts": total,
            "blob_count": self.blob_store.count(),
            "blob_size_bytes": self.blob_store.total_size_bytes(),
            "by_type": {r["artifact_type"]: r["count"] for r in rows},
        }
