from dataclasses import dataclass, field
from typing import Any
import time


@dataclass
class Event:
    type: str
    data: dict[str, Any]
    timestamp: float = field(default_factory=time.time)


class WorkflowCreated(Event):
    def __init__(self, workflow_id: str, goal: str, dag: dict[str, Any]) -> None:
        super().__init__("workflow.created", {"workflow_id": workflow_id, "goal": goal, "dag": dag})


class WorkflowStarted(Event):
    def __init__(self, workflow_id: str) -> None:
        super().__init__("workflow.started", {"workflow_id": workflow_id})


class WorkflowCompleted(Event):
    def __init__(self, workflow_id: str, result: dict[str, Any]) -> None:
        super().__init__("workflow.completed", {"workflow_id": workflow_id, "result": result})


class WorkflowFailed(Event):
    def __init__(self, workflow_id: str, reason: str) -> None:
        super().__init__("workflow.failed", {"workflow_id": workflow_id, "reason": reason})


class TaskStarted(Event):
    def __init__(self, task_id: str, workflow_id: str, tool_id: str) -> None:
        super().__init__("task.started", {"task_id": task_id, "workflow_id": workflow_id, "tool_id": tool_id})


class TaskCompleted(Event):
    def __init__(self, task_id: str, workflow_id: str, result: dict[str, Any]) -> None:
        super().__init__("task.completed", {"task_id": task_id, "workflow_id": workflow_id, "result": result})


class TaskFailed(Event):
    def __init__(self, task_id: str, workflow_id: str, reason: str) -> None:
        super().__init__("task.failed", {"task_id": task_id, "workflow_id": workflow_id, "reason": reason})


class TaskRetrying(Event):
    def __init__(self, task_id: str, workflow_id: str, attempt: int, max_retries: int) -> None:
        super().__init__("task.retrying", {"task_id": task_id, "workflow_id": workflow_id, "attempt": attempt, "max_retries": max_retries})


class ArtifactCreated(Event):
    def __init__(self, artifact_id: str, workflow_id: str, task_id: str, artifact_type: str) -> None:
        super().__init__("artifact.created", {"artifact_id": artifact_id, "workflow_id": workflow_id, "task_id": task_id, "type": artifact_type})


class ApprovalRequested(Event):
    def __init__(self, request_id: str, workflow_id: str, task_id: str, risk_level: str) -> None:
        super().__init__("approval.requested", {"request_id": request_id, "workflow_id": workflow_id, "task_id": task_id, "risk_level": risk_level})


class ApprovalDecided(Event):
    def __init__(self, request_id: str, decision: str, decided_by: str) -> None:
        super().__init__("approval.decided", {"request_id": request_id, "decision": decision, "decided_by": decided_by})


class PolicyDenied(Event):
    def __init__(self, task_id: str, workflow_id: str, rule: str, reason: str) -> None:
        super().__init__("policy.denied", {"task_id": task_id, "workflow_id": workflow_id, "rule": rule, "reason": reason})


class MemoryUpdated(Event):
    def __init__(self, memory_type: str, key: str, value: Any) -> None:
        super().__init__("memory.updated", {"type": memory_type, "key": key, "value": value})
