from __future__ import annotations

import logging
import time
from typing import Any

from src.ulid import prefixed_ulid
from src.events import get_bus, ArtifactCreated, Event
from src.orchestrator.db import insert, fetch_one, fetch_all

logger = logging.getLogger("provenance")

RELATIONSHIP_GENERATED_FROM = "generated_from"
RELATIONSHIP_DERIVED_FROM = "derived_from"
RELATIONSHIP_CONSUMED_BY = "consumed_by"


async def record_artifact(
    workflow_id: str,
    producer_task_id: str,
    artifact_type: str,
    location: str | None = None,
    content_hash: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    artifact_id = prefixed_ulid("art")
    now = time.time()
    await insert("artifacts", {
        "id": artifact_id,
        "workflow_id": workflow_id,
        "producer_task_id": producer_task_id,
        "artifact_type": artifact_type,
        "location": location or "",
        "hash": content_hash or "",
        "created_at": now,
        "metadata_json": (metadata or {}),
    })
    bus = get_bus()
    await bus.publish(ArtifactCreated(artifact_id, workflow_id, producer_task_id, artifact_type))
    logger.info("Artifact %s (%s) created by task %s", artifact_id, artifact_type, producer_task_id)
    return {"artifact_id": artifact_id, "type": artifact_type}


async def record_edge(
    source_artifact_id: str,
    target_artifact_id: str,
    relationship: str,
    workflow_id: str,
) -> dict[str, Any]:
    edge_id = prefixed_ulid("prov")
    await insert("provenance_edges", {
        "id": edge_id,
        "source_artifact_id": source_artifact_id,
        "target_artifact_id": target_artifact_id,
        "relationship": relationship,
        "workflow_id": workflow_id,
    })
    return {"edge_id": edge_id, "relationship": relationship}


async def get_artifact_lineage(artifact_id: str) -> dict[str, Any]:
    artifact = await fetch_one("SELECT * FROM artifacts WHERE id = ?", [artifact_id])
    if not artifact:
        return {"error": "Artifact not found"}

    ancestors = await fetch_all(
        """SELECT a.*, pe.relationship FROM provenance_edges pe
           JOIN artifacts a ON a.id = pe.source_artifact_id
           WHERE pe.target_artifact_id = ?
        """, [artifact_id])

    descendants = await fetch_all(
        """SELECT a.*, pe.relationship FROM provenance_edges pe
           JOIN artifacts a ON a.id = pe.target_artifact_id
           WHERE pe.source_artifact_id = ?
        """, [artifact_id])

    return {
        "artifact": dict(artifact),
        "ancestors": [dict(a) for a in ancestors],
        "descendants": [dict(a) for a in descendants],
    }


async def get_workflow_provenance(workflow_id: str) -> list[dict[str, Any]]:
    artifacts = await fetch_all("SELECT * FROM artifacts WHERE workflow_id = ?", [workflow_id])
    edges = await fetch_all("SELECT * FROM provenance_edges WHERE workflow_id = ?", [workflow_id])
    return {"artifacts": [dict(a) for a in artifacts], "edges": [dict(e) for e in edges]}


async def get_tool_provenance(tool_id: str) -> list[dict[str, Any]]:
    return await fetch_all(
        """SELECT a.*, t.tool_namespace, t.status as task_status
           FROM artifacts a
           JOIN tasks t ON t.id = a.producer_task_id
           WHERE t.tool_id = ?
           ORDER BY a.created_at DESC
        """, [tool_id]
    )
