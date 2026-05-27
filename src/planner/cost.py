from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger("cost")

CPU_NORM = {"low": 0.25, "medium": 0.5, "high": 1.0}
NETWORK_NORM = {"none": 0.0, "low": 0.25, "medium": 0.5, "high": 1.0}
DISK_IO_NORM = {"none": 0.0, "low": 0.15, "medium": 0.4, "high": 0.8}
TRUST_RISK = {"verified": 0.0, "community": 0.25, "experimental": 0.6, "ai-generated": 1.0}
TRANSFORM_METHOD_COST = {"passthrough": 0.0, "pipe": 0.1, "redirect": 0.2, "copy": 0.3, "convert": 0.5}


@dataclass
class CostVector:
    cpu: float = 0.0
    memory_mb: int = 0
    network: float = 0.0
    storage: float = 0.0
    latency: float = 0.0
    fidelity_loss: float = 0.0
    trust_risk: float = 0.0
    transform_cost: float = 0.0

    def __add__(self, other: CostVector) -> CostVector:
        return CostVector(
            cpu=max(self.cpu, other.cpu),
            memory_mb=self.memory_mb + other.memory_mb,
            network=max(self.network, other.network),
            storage=max(self.storage, other.storage),
            latency=self.latency + other.latency,
            fidelity_loss=max(self.fidelity_loss, other.fidelity_loss),
            trust_risk=max(self.trust_risk, other.trust_risk),
            transform_cost=self.transform_cost + other.transform_cost,
        )

    def weighted_score(self, weights: dict[str, float]) -> float:
        score = 0.0
        for dim, w in weights.items():
            val = getattr(self, dim, 0.0)
            score += val * w
        return score

    def to_dict(self) -> dict[str, Any]:
        return {
            "cpu": round(self.cpu, 4),
            "memory_mb": self.memory_mb,
            "network": round(self.network, 4),
            "storage": round(self.storage, 4),
            "latency": round(self.latency, 4),
            "fidelity_loss": round(self.fidelity_loss, 4),
            "trust_risk": round(self.trust_risk, 4),
            "transform_cost": round(self.transform_cost, 4),
        }


class CostEstimator:
    def __init__(self, commands: list[dict[str, Any]] | None = None, adaptive_provider: Any | None = None) -> None:
        self.commands = commands or []
        self.by_namespace: dict[str, dict[str, Any]] = {}
        for cmd in self.commands:
            ns = cmd.get("namespace", "")
            if ns:
                self.by_namespace[ns] = cmd
        self.adaptive_provider = adaptive_provider
        self._cost_cache: dict[str, CostVector] = {}

    def clear_cache(self) -> None:
        self._cost_cache.clear()

    def tool_cost(self, tool: dict[str, Any] | None = None, namespace: str = "") -> CostVector:
        cmd = tool or self.by_namespace.get(namespace, {})
        if not cmd:
            return CostVector()

        rp = cmd.get("resource_profile", {})
        rc = cmd.get("contract", {}).get("resource_cost", {})
        risk = cmd.get("risk_level", "low")
        trust = cmd.get("trust_level", "community")

        cpu_s = rc.get("cpu") or rp.get("cpu", "medium")
        mem = rc.get("memory_mb") or rp.get("memory_mb", 64)
        net_s = rc.get("network") or rp.get("network", "low")
        disk_s = rc.get("disk_io") or rp.get("disk_io", "low")
        cost_est = cmd.get("cost_estimate", {})

        declared_latency = cost_est.get("avg_execution_seconds", 5.0)
        if declared_latency <= 0:
            declared_latency = 5.0

        if self.adaptive_provider and namespace:
            blended = self.adaptive_provider.blend_latency(namespace, declared_latency)
            latency_used = blended
        else:
            latency_used = declared_latency

        base_latency = latency_used / 60.0
        if risk == "low":
            base_latency *= 1.0
        elif risk == "medium":
            base_latency *= 1.5
        elif risk == "high":
            base_latency *= 3.0
        elif risk == "critical":
            base_latency *= 5.0

        return CostVector(
            cpu=CPU_NORM.get(cpu_s, 0.5),
            memory_mb=mem,
            network=NETWORK_NORM.get(net_s, 0.25),
            storage=DISK_IO_NORM.get(disk_s, 0.15),
            latency=min(base_latency, 1.0),
            fidelity_loss=0.0,
            trust_risk=TRUST_RISK.get(trust, 0.25),
            transform_cost=0.0,
        )

    def transform_cost(self, transform_def: dict[str, Any] | None) -> CostVector:
        if not transform_def:
            return CostVector()
        steps = transform_def.get("steps", [])
        if not steps:
            return CostVector()

        fidelity = transform_def.get("fidelity", {})
        score = fidelity.get("score", 1.0)
        fidelity_loss = 1.0 - score

        total_transform = 0.0
        total_latency = 0.0
        peak_cpu = 0.0
        peak_network = 0.0

        for step in steps:
            method = step.get("method", "convert")
            cost = TRANSFORM_METHOD_COST.get(method, 0.5)
            total_transform += cost
            total_latency += cost * 0.5
            peak_cpu = max(peak_cpu, CPU_NORM.get("low", 0.25))
            if method == "convert":
                peak_cpu = max(peak_cpu, CPU_NORM.get("medium", 0.5))
            if method == "network":
                peak_network = max(peak_network, NETWORK_NORM.get("medium", 0.5))

        return CostVector(
            cpu=peak_cpu,
            memory_mb=0,
            network=peak_network,
            storage=0.0,
            latency=min(total_latency, 1.0),
            fidelity_loss=fidelity_loss,
            trust_risk=0.0,
            transform_cost=total_transform,
        )

    def edge_cost(self, artifact_type: str) -> CostVector:
        if not artifact_type:
            return CostVector()
        if "network" in artifact_type:
            return CostVector(network=0.2, latency=0.1)
        if "http" in artifact_type:
            return CostVector(network=0.3, latency=0.15)
        if "filesystem" in artifact_type:
            return CostVector(storage=0.1)
        return CostVector()

    def dag_cost(self, dag: dict[str, Any] | None, plan: dict[str, Any] | None = None) -> CostVector:
        if not dag:
            return CostVector()
        nodes = dag.get("nodes", {})
        edges = dag.get("edges", [])
        aggregated = CostVector()

        for nid, node in nodes.items():
            ntype = node.get("node_type", "tool")
            if ntype == "tool":
                ns = node.get("tool_namespace", "")
                aggregated += self.tool_cost(namespace=ns)
            elif ntype == "transform":
                tf = node.get("transform_def")
                aggregated += self.transform_cost(tf)
            elif ntype == "cache_fetch":
                aggregated += CostVector(latency=0.01, storage=0.05, transform_cost=0)

        for edge in edges:
            art_type = edge.get("artifact_type", "")
            aggregated += self.edge_cost(art_type)

        if plan:
            fa = plan.get("fidelity_assessment", {})
            plan_fidelity_loss = 1.0 - fa.get("min_fidelity_score", 1.0) if fa else 0.0
            aggregated.fidelity_loss = max(aggregated.fidelity_loss, plan_fidelity_loss)

        return aggregated

    def plan_cost(self, plan: dict[str, Any]) -> CostVector:
        dag = plan.get("dag", {})
        return self.dag_cost(dag, plan)

    def plan_confidence(self, plan: dict[str, Any]) -> float:
        if not self.adaptive_provider:
            return 1.0
        dag = plan.get("dag", {})
        nodes = dag.get("nodes", {})
        confidences: list[float] = []
        for node in nodes.values():
            if node.get("node_type") == "tool":
                ns = node.get("tool_namespace", "")
                confidences.append(self.adaptive_provider.get_confidence(ns))
            elif node.get("node_type") == "cache_fetch":
                confidences.append(1.0)
        if not confidences:
            return 1.0
        return sum(confidences) / len(confidences)
