from __future__ import annotations

import logging
from typing import Any

from src.planner.cost import CostEstimator, CostVector
from src.planner.objectives import ObjectiveProfile, resolve_objective

logger = logging.getLogger("scoring")


def score_plan(
    plan: dict[str, Any],
    objective: ObjectiveProfile | str | dict[str, Any],
    estimator: CostEstimator | None = None,
) -> float:
    obj = resolve_objective(objective)
    if obj is None:
        return 0.0
    cost = estimator.plan_cost(plan) if estimator else CostVector()
    return cost.weighted_score(obj.weights)


def rank_plans(
    plans: list[dict[str, Any]],
    objective: ObjectiveProfile | str | dict[str, Any],
    estimator: CostEstimator,
) -> list[tuple[float, int, dict[str, Any]]]:
    obj = resolve_objective(objective)
    if obj is None:
        return [(0.0, i, p) for i, p in enumerate(plans)]

    scored: list[tuple[float, int, dict[str, Any]]] = []
    for i, plan in enumerate(plans):
        cost = estimator.plan_cost(plan)
        score = cost.weighted_score(obj.weights)
        scored.append((score, i, plan))

    scored.sort(key=lambda x: x[0])
    return scored


def best_plan(
    plans: list[dict[str, Any]],
    objective: ObjectiveProfile | str | dict[str, Any],
    estimator: CostEstimator,
) -> dict[str, Any] | None:
    ranked = rank_plans(plans, objective, estimator)
    if not ranked:
        return None
    return ranked[0][2]
