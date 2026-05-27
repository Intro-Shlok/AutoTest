from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass
from typing import Any

from src.orchestrator.db import fetch_all

logger = logging.getLogger("adaptive_cost")


@dataclass
class ToolStats:
    tool_id: str
    sample_count: int
    avg_runtime_ms: float
    p95_runtime_ms: float
    success_rate: float
    total_runtime_ms: float
    successes: int
    last_seen: float

    @property
    def avg_runtime_seconds(self) -> float:
        return self.avg_runtime_ms / 1000.0

    @property
    def confidence(self) -> float:
        return compute_confidence(self.sample_count)


def compute_confidence(sample_count: int) -> float:
    if sample_count <= 0:
        return 0.0
    if sample_count < 5:
        return 0.3
    if sample_count < 20:
        return 0.6
    return min(0.95, 0.6 + 0.35 * (1.0 - 20.0 / sample_count))


def blend_cost(declared: float, observed: float, sample_count: int) -> float:
    if sample_count <= 0:
        return declared
    alpha = min(0.3 + 0.4 * (sample_count / 20.0), 0.7)
    return alpha * observed + (1.0 - alpha) * declared


class AdaptiveCostProvider:
    def __init__(self) -> None:
        self.tool_stats: dict[str, ToolStats] = {}
        self.last_refresh: float = 0.0
        self.refresh_count: int = 0

    async def refresh_from_db(self) -> int:
        try:
            rows = await fetch_all(
                "SELECT * FROM statistical_memories WHERE key LIKE 'reliability:%'"
            )
        except Exception:
            logger.warning("Could not query statistical_memories (DB not ready)")
            return 0

        count = 0
        for row in rows:
            key: str = row.get("key", "")
            if not key.startswith("reliability:"):
                continue
            tool_id = key[len("reliability:"):]
            try:
                data = json.loads(row.get("value_json", "{}"))
            except (json.JSONDecodeError, TypeError):
                continue
            sample_count = data.get("executions", 0)
            if sample_count <= 0:
                continue
            total_runtime_ms = data.get("total_runtime_ms", 0.0)
            successes = data.get("successes", 0)
            avg_runtime_ms = data.get("avg_runtime_ms", 0.0)
            success_rate = data.get("success_rate", 0.0)
            if avg_runtime_ms <= 0 and sample_count > 0:
                avg_runtime_ms = total_runtime_ms / sample_count

            self.tool_stats[tool_id] = ToolStats(
                tool_id=tool_id,
                sample_count=sample_count,
                avg_runtime_ms=avg_runtime_ms,
                p95_runtime_ms=data.get("p95_runtime_ms", avg_runtime_ms),
                success_rate=success_rate,
                total_runtime_ms=total_runtime_ms,
                successes=successes,
                last_seen=row.get("updated_at", time.time()),
            )
            count += 1

        self.last_refresh = time.time()
        self.refresh_count += 1
        logger.info("Refreshed adaptive costs: %d tool stats loaded", count)
        return count

    def get_tool_stats(self, tool_id: str) -> ToolStats | None:
        return self.tool_stats.get(tool_id)

    def get_observed_latency(self, tool_id: str, default_latency_seconds: float = 5.0) -> float | None:
        stats = self.tool_stats.get(tool_id)
        if stats is None or stats.sample_count <= 0:
            return None
        return stats.avg_runtime_seconds

    def get_observed_reliability(self, tool_id: str) -> float | None:
        stats = self.tool_stats.get(tool_id)
        if stats is None or stats.sample_count <= 0:
            return None
        return stats.success_rate

    def get_confidence(self, tool_id: str) -> float:
        stats = self.tool_stats.get(tool_id)
        if stats is None:
            return 0.0
        return stats.confidence

    def blend_latency(self, tool_id: str, declared_latency_seconds: float) -> float:
        stats = self.tool_stats.get(tool_id)
        if stats is None or stats.sample_count <= 0:
            return declared_latency_seconds
        return blend_cost(declared_latency_seconds, stats.avg_runtime_seconds, stats.sample_count)

    def to_dict(self) -> dict[str, Any]:
        return {
            "last_refresh": self.last_refresh,
            "refresh_count": self.refresh_count,
            "tool_count": len(self.tool_stats),
            "tools": {
                tid: {
                    "sample_count": s.sample_count,
                    "avg_runtime_ms": s.avg_runtime_ms,
                    "success_rate": s.success_rate,
                    "confidence": s.confidence,
                }
                for tid, s in sorted(self.tool_stats.items(), key=lambda x: -x[1].sample_count)
            },
        }
