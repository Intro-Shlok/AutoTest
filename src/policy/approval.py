from __future__ import annotations

import time
import logging
from typing import Any

from src.ulid import prefixed_ulid
from src.events import get_bus, ApprovalRequested, ApprovalDecided
from src.orchestrator.db import insert, update, fetch_one, fetch_all

logger = logging.getLogger("approval")


async def request_approval(
    workflow_id: str,
    task_id: str,
    risk_level: str,
    justification: str,
    expires_in: int = 3600,
) -> dict[str, Any]:
    request_id = prefixed_ulid("apr")
    now = time.time()
    await insert("approval_requests", {
        "id": request_id,
        "workflow_id": workflow_id,
        "task_id": task_id,
        "risk_level": risk_level,
        "justification": justification,
        "status": "pending",
        "expires_at": now + expires_in,
        "created_at": now,
    })
    bus = get_bus()
    await bus.publish(ApprovalRequested(request_id, workflow_id, task_id, risk_level))
    logger.info("Approval %s requested for task %s (risk: %s)", request_id, task_id, risk_level)
    return {"approval_id": request_id, "status": "pending"}


async def decide_approval(request_id: str, decision: str, decided_by: str) -> dict[str, Any]:
    if decision not in ("approved", "rejected"):
        return {"error": "Decision must be 'approved' or 'rejected'"}

    req = await fetch_one("SELECT * FROM approval_requests WHERE id = ?", [request_id])
    if not req:
        return {"error": "Approval request not found"}
    if req["status"] != "pending":
        return {"error": f"Approval already decided: {req['status']}"}
    if req["expires_at"] and time.time() > req["expires_at"]:
        await update("approval_requests", {"status": "expired"}, "id = ?", [request_id])
        return {"error": "Approval request has expired"}

    await update("approval_requests", {
        "status": decision,
        "decision": decision,
        "decided_by": decided_by,
    }, "id = ?", [request_id])

    bus = get_bus()
    await bus.publish(ApprovalDecided(request_id, decision, decided_by))
    logger.info("Approval %s: %s by %s", request_id, decision, decided_by)

    return {"approval_id": request_id, "decision": decision, "decided_by": decided_by}


async def get_pending_approvals(workflow_id: str | None = None) -> list[dict[str, Any]]:
    if workflow_id:
        return await fetch_all(
            "SELECT * FROM approval_requests WHERE status = 'pending' AND workflow_id = ? ORDER BY created_at",
            [workflow_id],
        )
    return await fetch_all(
        "SELECT * FROM approval_requests WHERE status = 'pending' AND (expires_at IS NULL OR expires_at > ?) ORDER BY created_at",
        [time.time()],
    )
