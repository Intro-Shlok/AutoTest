from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger("objectives")

BUILTIN_OBJECTIVES: dict[str, dict[str, Any]] = {
    "minimize_latency": {
        "name": "minimize_latency",
        "weights": {
            "latency": 1.0,
            "cpu": 0.0,
            "memory_mb": 0.0,
            "network": 0.0,
            "storage": 0.0,
            "fidelity_loss": 0.0,
            "trust_risk": 0.0,
            "transform_cost": 0.1,
        },
        "description": "Optimize for fastest execution by minimizing total latency and transform overhead.",
    },
    "maximize_fidelity": {
        "name": "maximize_fidelity",
        "weights": {
            "fidelity_loss": 1.0,
            "latency": 0.0,
            "cpu": 0.0,
            "memory_mb": 0.0,
            "network": 0.0,
            "storage": 0.0,
            "trust_risk": 0.0,
            "transform_cost": 0.0,
        },
        "description": "Optimize for maximum information preservation. Prefers lossless transforms.",
    },
    "minimize_trust_risk": {
        "name": "minimize_trust_risk",
        "weights": {
            "trust_risk": 1.0,
            "cpu": 0.0,
            "memory_mb": 0.0,
            "network": 0.0,
            "storage": 0.0,
            "latency": 0.0,
            "fidelity_loss": 0.0,
            "transform_cost": 0.0,
        },
        "description": "Optimize for safest tool selection. Prefers verified tools, avoids experimental and AI-generated.",
    },
    "minimize_resource": {
        "name": "minimize_resource",
        "weights": {
            "cpu": 0.25,
            "memory_mb": 0.3,
            "network": 0.3,
            "storage": 0.15,
            "latency": 0.0,
            "fidelity_loss": 0.0,
            "trust_risk": 0.0,
            "transform_cost": 0.0,
        },
        "description": "Optimize for cheapest resource usage. Prefers tools with low CPU, memory, and network footprints.",
    },
    "balanced": {
        "name": "balanced",
        "weights": {
            "cpu": 0.125,
            "memory_mb": 0.125,
            "network": 0.125,
            "storage": 0.125,
            "latency": 0.125,
            "fidelity_loss": 0.125,
            "trust_risk": 0.125,
            "transform_cost": 0.125,
        },
        "description": "Equal weight across all cost dimensions. General-purpose optimization.",
    },
    "minimize_cost": {
        "name": "minimize_cost",
        "weights": {
            "cpu": 0.1,
            "memory_mb": 0.3,
            "network": 0.4,
            "storage": 0.2,
            "latency": 0.0,
            "fidelity_loss": 0.0,
            "trust_risk": 0.0,
            "transform_cost": 0.0,
        },
        "description": "Optimize for monetary execution cost. Network and memory are primary cost drivers.",
    },
}

ALL_OBJECTIVE_NAMES = set(BUILTIN_OBJECTIVES.keys())


@dataclass
class ObjectiveProfile:
    name: str
    weights: dict[str, float]
    description: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "weights": dict(self.weights),
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> ObjectiveProfile:
        return cls(
            name=d.get("name", "custom"),
            weights=d.get("weights", {}),
            description=d.get("description", "Custom objective"),
        )


def load_objective(name: str) -> ObjectiveProfile | None:
    spec = BUILTIN_OBJECTIVES.get(name)
    if spec is None:
        logger.warning("Unknown objective '%s', falling back to balanced", name)
        return None
    return ObjectiveProfile.from_dict(spec)


def list_objectives() -> list[dict[str, Any]]:
    return [ObjectiveProfile.from_dict(spec).to_dict() for spec in BUILTIN_OBJECTIVES.values()]


def resolve_objective(obj: str | dict[str, Any] | ObjectiveProfile | None) -> ObjectiveProfile | None:
    if obj is None:
        return None
    if isinstance(obj, ObjectiveProfile):
        return obj
    if isinstance(obj, dict):
        return ObjectiveProfile.from_dict(obj)
    if isinstance(obj, str):
        return load_objective(obj)
    return None
