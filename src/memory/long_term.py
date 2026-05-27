from __future__ import annotations

import json
import logging
import time
from typing import Any

from src.events import get_bus, Event, MemoryUpdated
from src.orchestrator.db import fetch_one, fetch_all, insert, update
from src.ulid import prefixed_ulid

logger = logging.getLogger("memory")

MEMORY_TABLES = {
    "factorial": "factual_memories",
    "statistical": "statistical_memories",
    "preference": "preference_memories",
    "episodic": "episodic_memories",
    "semantic": "semantic_memories",
}


async def store_factual(key: str, value: Any, ttl: float | None = None, environment: str | None = None) -> dict[str, Any]:
    existing = await fetch_one("SELECT * FROM factual_memories WHERE key = ? AND (environment = ? OR (environment IS NULL AND ? IS NULL))", [key, environment or "", environment])
    now = time.time()
    value_json = json.dumps(value)
    if existing:
        await update("factual_memories", {"value_json": value_json, "ttl": ttl, "created_at": now}, "id = ?", [existing["id"]])
    else:
        await insert("factual_memories", {"id": prefixed_ulid("mem"), "key": key, "value_json": value_json, "environment": environment, "created_at": now, "ttl": ttl})
    get_bus().publish(MemoryUpdated("factorial", key, value))
    return {"memory_type": "factorial", "key": key}


async def store_statistical(key: str, value: Any, sample_count: int = 1, environment: str | None = None) -> dict[str, Any]:
    existing = await fetch_one("SELECT * FROM statistical_memories WHERE key = ?", [key])
    now = time.time()
    value_json = json.dumps(value)
    if existing:
        merged = {**json.loads(existing["value_json"]), **value}
        new_count = existing["sample_count"] + sample_count
        await update("statistical_memories", {"value_json": json.dumps(merged), "sample_count": new_count, "updated_at": now}, "id = ?", [existing["id"]])
    else:
        await insert("statistical_memories", {"id": prefixed_ulid("mem"), "key": key, "value_json": value_json, "sample_count": sample_count, "environment": environment, "created_at": now, "updated_at": now})
    get_bus().publish(MemoryUpdated("statistical", key, value))
    return {"memory_type": "statistical", "key": key}


async def store_preference(key: str, value: Any, priority: int = 0, environment: str | None = None) -> dict[str, Any]:
    existing = await fetch_one("SELECT * FROM preference_memories WHERE key = ?", [key])
    now = time.time()
    value_json = json.dumps(value)
    if existing:
        await update("preference_memories", {"value_json": value_json, "priority": priority}, "id = ?", [existing["id"]])
    else:
        await insert("preference_memories", {"id": prefixed_ulid("mem"), "key": key, "value_json": value_json, "priority": priority, "environment": environment, "created_at": now})
    get_bus().publish(MemoryUpdated("preference", key, value))
    return {"memory_type": "preference", "key": key}


async def store_episodic(episode_type: str, summary: str, outcome: str | None = None, details: dict[str, Any] | None = None, workflow_id: str | None = None, environment: str | None = None) -> dict[str, Any]:
    await insert("episodic_memories", {
        "id": prefixed_ulid("mem"),
        "workflow_id": workflow_id,
        "episode_type": episode_type,
        "summary": summary,
        "outcome": outcome,
        "details_json": json.dumps(details or {}),
        "environment": environment,
        "created_at": time.time(),
    })
    return {"memory_type": "episodic", "episode_type": episode_type}


async def store_semantic(key: str, value: Any, confidence: float = 1.0, environment: str | None = None) -> dict[str, Any]:
    existing = await fetch_one("SELECT * FROM semantic_memories WHERE key = ?", [key])
    now = time.time()
    value_json = json.dumps(value)
    if existing:
        merged = {**json.loads(existing["value_json"]), **value}
        avg_conf = (existing["confidence"] + confidence) / 2
        await update("semantic_memories", {"value_json": json.dumps(merged), "confidence": avg_conf}, "id = ?", [existing["id"]])
    else:
        await insert("semantic_memories", {"id": prefixed_ulid("mem"), "key": key, "value_json": value_json, "confidence": confidence, "environment": environment, "created_at": time.time()})
    get_bus().publish(MemoryUpdated("semantic", key, value))
    return {"memory_type": "semantic", "key": key}


async def get_memory(memory_type: str, key: str) -> Any | None:
    table = MEMORY_TABLES.get(memory_type)
    if not table:
        return None
    row = await fetch_one(f"SELECT * FROM {table} WHERE key = ?", [key])
    if not row:
        return None
    return json.loads(row["value_json"])


async def get_all_memories(memory_type: str | None = None) -> list[dict[str, Any]]:
    if memory_type:
        table = MEMORY_TABLES.get(memory_type)
        if not table:
            return []
        rows = await fetch_all(f"SELECT * FROM {table} ORDER BY created_at DESC")
        return [{k: v for k, v in dict(r).items() if k != "value_json"} | {"value": json.loads(r["value_json"])} for r in rows]
    result = []
    for mtype, table in MEMORY_TABLES.items():
        rows = await fetch_all(f"SELECT * FROM {table} ORDER BY created_at DESC LIMIT 20")
        for r in rows:
            d = {k: v for k, v in dict(r).items() if k != "value_json"}
            d["memory_type"] = mtype
            d["value"] = json.loads(r["value_json"])
            result.append(d)
    return result


async def record_execution_result(tool_id: str, success: bool, runtime_ms: float, environment: str | None = None) -> None:
    key = f"reliability:{tool_id}"
    existing = await fetch_one("SELECT * FROM statistical_memories WHERE key = ?", [key])
    if existing:
        data = json.loads(existing["value_json"])
        data["executions"] = data.get("executions", 0) + 1
        if success:
            data["successes"] = data.get("successes", 0) + 1
        data["total_runtime_ms"] = data.get("total_runtime_ms", 0) + runtime_ms
        data["avg_runtime_ms"] = round(data["total_runtime_ms"] / data["executions"], 1)
        data["success_rate"] = round(data["successes"] / data["executions"], 3)
        await store_statistical(key, data, environment=environment)
    else:
        data = {"executions": 1, "successes": 1 if success else 0, "total_runtime_ms": runtime_ms, "avg_runtime_ms": round(runtime_ms, 1), "success_rate": 1.0 if success else 0.0}
        await store_statistical(key, data, environment=environment)


async def get_preferred_tools(environment: str | None = None) -> list[dict[str, Any]]:
    rows = await fetch_all("SELECT * FROM preference_memories ORDER BY priority DESC")
    results = []
    for r in rows:
        if environment and r.get("environment") and r["environment"] != environment:
            continue
        results.append({"key": r["key"], "value": json.loads(r["value_json"]), "environment": r.get("environment")})
    return results


async def get_failure_patterns(tool_id: str | None = None) -> list[dict[str, Any]]:
    if tool_id:
        rows = await fetch_all("SELECT * FROM episodic_memories WHERE episode_type = 'failure' AND details_json LIKE ? ORDER BY created_at DESC", [f"%{tool_id}%"])
    else:
        rows = await fetch_all("SELECT * FROM episodic_memories WHERE episode_type = 'failure' ORDER BY created_at DESC LIMIT 100")
    return [{"id": r["id"], "summary": r["summary"], "outcome": r["outcome"], "details": json.loads(r["details_json"]), "created_at": r["created_at"]} for r in rows]
