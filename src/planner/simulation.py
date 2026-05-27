from __future__ import annotations

import logging
from typing import Any

from src.planner.planner import Planner
from src.planner.cost import CostEstimator
from src.planner.objectives import ObjectiveProfile, resolve_objective, list_objectives

logger = logging.getLogger("simulation")


class SimulationMode:
    def __init__(self, planner: Planner) -> None:
        self.planner = planner

    def dry_run(
        self,
        goal: str,
        constraints: dict[str, Any] | None = None,
        objective: str | dict[str, Any] | ObjectiveProfile | None = None,
    ) -> dict[str, Any]:
        plan = self.planner.plan_from_goal(goal, constraints, objective=objective)
        plan["mode"] = "simulation"
        plan["disclaimer"] = "Dry-run: no workflows, tasks, or artifacts were created"
        plan["risk_assessment"] = self._assess_risk(plan)
        plan["fidelity_assessment"] = self._assess_fidelity(plan)

        cost_est = CostEstimator(self.planner.commands)
        cost = cost_est.plan_cost(plan)
        plan["cost_estimate"] = {
            "cost_vector": cost.to_dict(),
            "breakdown": {
                "node_summary": self._node_cost_summary(plan, cost_est),
            },
        }

        if objective:
            obj = resolve_objective(objective)
            if obj:
                plan["cost_estimate"]["objective"] = obj.name
                plan["cost_estimate"]["weighted_score"] = round(cost.weighted_score(obj.weights), 4)

        return plan

    def _node_cost_summary(self, plan: dict[str, Any], estimator: CostEstimator) -> list[dict[str, Any]]:
        dag = plan.get("dag", {})
        nodes = dag.get("nodes", {})
        summary: list[dict[str, Any]] = []
        for nid, node in nodes.items():
            ntype = node.get("node_type", "tool")
            if ntype == "tool":
                ns = node.get("tool_namespace", "")
                c = estimator.tool_cost(namespace=ns)
                summary.append({
                    "node_id": nid,
                    "label": node.get("label", ""),
                    "type": "tool",
                    "cost": c.to_dict(),
                })
            elif ntype == "transform":
                tf = node.get("transform_def")
                c = estimator.transform_cost(tf)
                summary.append({
                    "node_id": nid,
                    "label": node.get("label", ""),
                    "type": "transform",
                    "cost": c.to_dict(),
                })
        return summary

    def _assess_risk(self, plan: dict[str, Any]) -> dict[str, Any]:
        dag = plan.get("dag", {})
        max_risk = "low"
        risk_count = {"low": 0, "medium": 0, "high": 0, "critical": 0}

        for nid, node in dag.get("nodes", {}).items():
            tool_ns = node.get("tool_namespace", "")
            cmd = self.planner.by_namespace.get(tool_ns, {})
            risk = cmd.get("risk_level", "low")
            risk_count[risk] = risk_count.get(risk, 0) + 1
            if {"low": 0, "medium": 1, "high": 2, "critical": 3}.get(risk, 0) > {"low": 0, "medium": 1, "high": 2, "critical": 3}.get(max_risk, 0):
                max_risk = risk

        return {
            "max_risk_level": max_risk,
            "risk_distribution": risk_count,
            "requires_approval": max_risk in ("high", "critical"),
        }

    def _assess_fidelity(self, plan: dict[str, Any]) -> dict[str, Any]:
        dag = plan.get("dag", {})
        nodes = dag.get("nodes", {})
        lossy_nodes: list[dict[str, Any]] = []
        min_score = 1.0
        degradation_warnings: list[dict[str, Any]] = []

        for nid, node in nodes.items():
            if node.get("node_type") != "transform":
                continue
            tf = node.get("transform_def")
            if not tf:
                continue
            fid = tf.get("fidelity", {})
            score = fid.get("score", 1.0)
            if score < 1.0:
                min_score = min(min_score, score)
                entry: dict[str, Any] = {
                    "node_id": nid,
                    "label": node.get("label", ""),
                    "fidelity_score": score,
                    "loss_type": fid.get("loss_type", "unknown"),
                }
                bd = fid.get("breakdown")
                if bd:
                    entry["breakdown"] = bd
                lossy_nodes.append(entry)
                notes = fid.get("degradation_notes", [])
                if isinstance(notes, list):
                    for note in notes:
                        degradation_warnings.append({
                            "node_id": nid,
                            "message": note,
                        })
                elif notes:
                    degradation_warnings.append({
                        "node_id": nid,
                        "message": str(notes),
                    })

        return {
            "min_fidelity_score": min_score if lossy_nodes else 1.0,
            "lossy_node_count": len(lossy_nodes),
            "lossy_nodes": lossy_nodes,
            "degradation_warnings": degradation_warnings,
        }

    def estimate_cost(self, plan: dict[str, Any]) -> dict[str, Any]:
        dag = plan.get("dag", {})
        total_memory = 0
        total_nodes = len(dag.get("nodes", {}))
        network_intensive = 0

        for nid, node in dag.get("nodes", {}).items():
            tool_ns = node.get("tool_namespace", "")
            cmd = self.planner.by_namespace.get(tool_ns, {})
            rp = cmd.get("resource_profile", {})
            total_memory += rp.get("memory_mb", 0)
            if rp.get("network", "low") == "high":
                network_intensive += 1

        return {
            "estimated_memory_mb": total_memory,
            "node_count": total_nodes,
            "network_intensive_nodes": network_intensive,
            "estimated_complexity": "simple" if total_nodes <= 3 else "moderate" if total_nodes <= 7 else "complex",
        }
