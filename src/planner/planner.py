from __future__ import annotations

import json
import logging
import re
from typing import Any

from src.planner.constraint import (
    filter_by_capability,
    filter_by_resource,
    filter_by_trust,
    filter_by_architecture,
    find_producers,
    find_consumers,
    match_capability_prefix,
)
from src.planner.cost import CostEstimator, CostVector
from src.planner.objectives import ObjectiveProfile, resolve_objective, list_objectives
from src.planner.scoring import score_plan, rank_plans, best_plan
from src.orchestrator.dag import WorkflowDAG, DAGNode, DAGEdge
from src.transforms.registry import TransformCatalog
from src.transforms.resolver import TransformResolver, TransformPath

logger = logging.getLogger("planner")


class Planner:
    def __init__(
        self,
        commands: list[dict[str, Any]],
        host_arch: str = "amd64",
        transform_catalog: TransformCatalog | None = None,
        adaptive_provider: Any | None = None,
        artifact_cache: Any | None = None,
    ) -> None:
        self.commands = commands
        self.host_arch = host_arch
        self.transform_catalog = transform_catalog or TransformCatalog.load_default()
        self.transform_resolver = TransformResolver(self.transform_catalog)
        self.cost_estimator = CostEstimator(commands, adaptive_provider=adaptive_provider)
        self.adaptive_provider = adaptive_provider
        self.artifact_cache = artifact_cache
        self._build_index()

    def _build_index(self) -> None:
        self.by_namespace: dict[str, dict[str, Any]] = {}
        self.by_capability: dict[str, list[dict[str, Any]]] = {}
        self.by_artifact_produced: dict[str, list[dict[str, Any]]] = {}
        self.by_artifact_consumed: dict[str, list[dict[str, Any]]] = {}

        for cmd in self.commands:
            ns = cmd.get("namespace", "")
            self.by_namespace[ns] = cmd
            for cap in cmd.get("capabilities", []):
                self.by_capability.setdefault(cap, []).append(cmd)
            for art in cmd.get("workflow_edges", {}).get("produces", []):
                self.by_artifact_produced.setdefault(art, []).append(cmd)
            for art in cmd.get("workflow_edges", {}).get("consumes", []):
                self.by_artifact_consumed.setdefault(art, []).append(cmd)

    def _build_cost_assessment(self, plan: dict[str, Any], objective: ObjectiveProfile | None) -> dict[str, Any]:
        cost = self.cost_estimator.plan_cost(plan)
        result: dict[str, Any] = {
            "cost_vector": cost.to_dict(),
        }
        if objective:
            result["objective"] = objective.name
            result["weighted_score"] = round(cost.weighted_score(objective.weights), 4)
        return result

    def _select_candidates(
        self,
        goal: str,
        constraints: dict[str, Any],
        max_candidates: int = 10,
    ) -> list[dict[str, Any]]:
        matched: list[tuple[int, dict[str, Any]]] = []
        for cmd in self.commands:
            score = self._score_goal_match(cmd, goal)
            if score > 0:
                matched.append((score, cmd))
        matched.sort(key=lambda x: -x[0])
        candidates = [m[1] for m in matched[:max_candidates]]
        candidates = filter_by_trust(candidates, constraints.get("min_trust", "community"))
        candidates = filter_by_architecture(candidates, constraints.get("arch", self.host_arch))
        candidates = filter_by_resource(
            candidates,
            max_memory_mb=constraints.get("max_memory_mb"),
            max_cpu=constraints.get("max_cpu"),
        )
        return candidates

    def plan_from_goal(
        self,
        goal: str,
        constraints: dict[str, Any] | None = None,
        objective: str | dict[str, Any] | ObjectiveProfile | None = None,
    ) -> dict[str, Any]:
        constraints = constraints or {}
        candidates = self._select_candidates(goal, constraints)

        dag = self._build_chain_dag(candidates, goal, constraints)
        plan: dict[str, Any] = {
            "goal": goal,
            "constraints": constraints,
            "candidate_count": len(candidates),
            "dag": dag.to_dict(),
            "node_count": len(dag.nodes),
            "edge_count": len(dag.edges),
        }

        fidelity_assessment = self._assess_fidelity(plan)
        if fidelity_assessment["lossy_node_count"] > 0:
            plan["fidelity_assessment"] = fidelity_assessment

        obj = resolve_objective(objective)
        plan["cost_assessment"] = self._build_cost_assessment(plan, obj)

        return plan

    def plan_optimal(
        self,
        goal: str,
        objective: str | dict[str, Any] | ObjectiveProfile = "balanced",
        constraints: dict[str, Any] | None = None,
        alternatives: int = 5,
    ) -> dict[str, Any]:
        constraints = constraints or {}
        obj = resolve_objective(objective)
        if obj is None:
            obj = resolve_objective("balanced")

        base_candidates = self._select_candidates(goal, constraints)
        if not base_candidates:
            return {
                "goal": goal,
                "objective": obj.name if obj else "unknown",
                "candidate_count": 0,
                "node_count": 0,
                "error": "No matching tools found for goal",
            }

        plans: list[dict[str, Any]] = []

        primary_dag = self._build_chain_dag(base_candidates, goal, constraints)
        primary_plan: dict[str, Any] = {
            "goal": goal,
            "constraints": constraints,
            "candidate_count": len(base_candidates),
            "dag": primary_dag.to_dict(),
            "node_count": len(primary_dag.nodes),
            "edge_count": len(primary_dag.edges),
            "_variant": "primary",
        }
        fa = self._assess_fidelity(primary_plan)
        if fa["lossy_node_count"] > 0:
            primary_plan["fidelity_assessment"] = fa
        plans.append(primary_plan)

        if alternatives > 1 and len(base_candidates) >= 2:
            relaxed_trust = filter_by_trust(base_candidates, constraints.get("min_trust", "experimental"))
            for i in range(1, min(alternatives, len(relaxed_trust))):
                subset = relaxed_trust[i:] + relaxed_trust[:i]
                dag = self._build_chain_dag(subset, goal, constraints)
                alt: dict[str, Any] = {
                    "goal": goal,
                    "constraints": constraints,
                    "candidate_count": len(subset),
                    "dag": dag.to_dict(),
                    "node_count": len(dag.nodes),
                    "edge_count": len(dag.edges),
                    "_variant": f"alt_{i}",
                }
                fa2 = self._assess_fidelity(alt)
                if fa2["lossy_node_count"] > 0:
                    alt["fidelity_assessment"] = fa2
                plans.append(alt)

        estimator = self.cost_estimator
        ranked = rank_plans(plans, obj, estimator)
        best_idx = ranked[0][1]
        best = plans[best_idx]

        best["objective"] = obj.name
        best["cost_assessment"] = self._build_cost_assessment(best, obj)
        best["alternatives_explored"] = len(ranked)

        alternatives_list = []
        for score, idx, p in ranked:
            if idx != best_idx:
                alt_cost = estimator.plan_cost(p)
                alternatives_list.append({
                    "variant": p.get("_variant", f"plan_{idx}"),
                    "weighted_score": round(score, 4),
                    "cost_vector": alt_cost.to_dict(),
                    "node_count": p.get("node_count", 0),
                })
        if alternatives_list:
            best["alternatives"] = alternatives_list

        best.pop("_variant", None)
        return best

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

    async def optimize_with_cache(self, plan: dict[str, Any]) -> dict[str, Any]:
        dag_data = plan.get("dag", {})
        if not dag_data or not self.artifact_cache:
            return plan

        constraints = plan.get("constraints", {})
        max_age = constraints.get("cache_max_age", 3600)
        min_trust = constraints.get("cache_min_trust", "community")

        nodes = dag_data.get("nodes", {})
        edges = dag_data.get("edges", [])

        for edge in edges:
            art_type = edge.get("artifact_type", "")
            if not art_type:
                continue
            source_id = edge.get("source_id", "")
            source_node = nodes.get(source_id)
            if not source_node or source_node.get("node_type", "tool") not in ("tool",):
                continue

            hit = await self.artifact_cache.find_cached(art_type, max_age, min_trust)
            if not hit:
                continue

            fetch_id = f"cache_{source_id}"
            nodes[fetch_id] = {
                "id": fetch_id,
                "tool_id": source_node.get("tool_id", ""),
                "tool_namespace": "",
                "node_type": "cache_fetch",
                "label": f"cache:{art_type}",
                "params": {"artifact_id": hit.artifact_id, "content_hash": hit.content_hash},
                "retry_policy": {"max_attempts": 1, "backoff": "exponential"},
            }
            del nodes[source_id]

            edge["source_id"] = fetch_id
            edge["artifact_id"] = hit.artifact_id
            edge["cache_hit"] = True
            logger.info(
                "Cache hit: %s → %s (%s)",
                art_type, hit.artifact_id,
                hit.content_hash[:12] if hit.content_hash else "no-hash",
            )

        plan["dag"] = dag_data
        plan["node_count"] = len(nodes)
        return plan

    def plan_from_artifacts(
        self,
        produces: list[str] | None = None,
        consumes: list[str] | None = None,
        constraints: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        constraints = constraints or {}
        dag = WorkflowDAG()
        used_tools: list[dict[str, Any]] = []

        if produces:
            for art in produces:
                producers = filter_by_trust(
                    filter_by_architecture(find_producers(self.commands, art), constraints.get("arch", self.host_arch)),
                    constraints.get("min_trust", "community"),
                )
                used_tools.extend(producers)

        if consumes:
            for art in consumes:
                consumers = filter_by_trust(
                    filter_by_architecture(find_consumers(self.commands, art), constraints.get("arch", self.host_arch)),
                    constraints.get("min_trust", "community"),
                )
                used_tools.extend(consumers)

        for i, tool in enumerate(used_tools):
            node = DAGNode(
                id=f"node_{i}",
                tool_id=tool.get("id", ""),
                tool_namespace=tool.get("namespace", ""),
                label=tool.get("name", ""),
            )
            dag.add_node(node)

        for i in range(len(used_tools) - 1):
            dag.add_edge(DAGEdge(source_id=f"node_{i}", target_id=f"node_{i + 1}"))

        plan = {
            "artifact_plan": {"produces": produces, "consumes": consumes},
            "dag": dag.to_dict(),
            "node_count": len(dag.nodes),
            "edge_count": len(dag.edges),
        }
        plan["cost_assessment"] = self._build_cost_assessment(plan, None)
        return plan

    def _score_goal_match(self, cmd: dict[str, Any], goal: str) -> int:
        goal_lower = goal.lower()
        score = 0
        for key in ("name", "description", "namespace"):
            val = str(cmd.get(key, "")).lower()
            if val in goal_lower:
                score += 10
        for cap in cmd.get("capabilities", []):
            if cap.lower() in goal_lower:
                score += 5
            parts = cap.lower().split(".")
            if any(p in goal_lower for p in parts):
                score += 2
        contract = cmd.get("contract", {})
        for inp in contract.get("inputs", []):
            if inp.get("type", "").lower() in goal_lower:
                score += 3
        for out in contract.get("outputs", []):
            if out.get("type", "").lower() in goal_lower:
                score += 3
        for art in cmd.get("workflow_edges", {}).get("produces", []):
            if art.lower() in goal_lower:
                score += 3
        for art in cmd.get("workflow_edges", {}).get("consumes", []):
            if art.lower() in goal_lower:
                score += 2
        for tag in cmd.get("tags", []):
            if tag.lower() in goal_lower:
                score += 4
        return score

    def _resolve_params(self, tool: dict[str, Any], goal: str) -> dict[str, Any]:
        """Auto-populate default params from parameter schema, then apply objective-based overrides."""
        params: dict[str, Any] = {}
        goal_lower = goal.lower()

        for p in tool.get("parameters", []):
            name = p.get("name", "")
            ptype = p.get("type", "string")
            dv = p.get("default_value")
            aliases = p.get("aliases", [])
            desc = (p.get("description", "") or "").lower()
            enum_vals = p.get("enum", [])

            # Set default from schema
            if dv is not None:
                params[name] = dv
            elif ptype == "boolean":
                params[name] = False
            elif enum_vals:
                params[name] = enum_vals[0]

            # Objective-based flag selection: match goal keywords against param metadata
            goal_words = set(goal_lower.split())
            desc_words = set(desc.split())

            # If goal mentions a keyword found in this param's description, boost it
            if goal_words & desc_words:
                if ptype == "boolean":
                    params[name] = True
                elif enum_vals:
                    # Pick the enum value most relevant to the goal
                    best = enum_vals[0]
                    best_score = 0
                    for ev in enum_vals:
                        ev_words = set(ev.lower().split("_"))
                        score = len(goal_words & ev_words)
                        if ev_words & goal_words:
                            score += 2
                        if score > best_score:
                            best_score = score
                            best = ev
                    if best_score > 0:
                        params[name] = best

            # If goal explicitly mentions the parameter name, activate it
            if name.replace("_", "-") in goal_lower or name.replace("_", " ") in goal_lower:
                if ptype == "boolean":
                    params[name] = True
                elif enum_vals:
                    params[name] = enum_vals[-1]  # Pick the most aggressive option

        # Resolve execution template into params["command"]
        template = (tool.get("execution", {}) or {}).get("template", "")
        if template:
            resolved = template
            # Build mapping: template_key/name → value
            for p in tool.get("parameters", []):
                pname = p.get("name", "")
                tkey = p.get("template_key") or pname
                val = params.get(pname)
                if val is not None:
                    val_str = str(val)
                    if " " in val_str and not val_str.startswith('"'):
                        val_str = f'"{val_str}"'
                    # Try {name}, {template_key}, {{name}}, {{template_key}}
                    for key in set([pname, tkey]):
                        for brace in (f"{{{key}}}", f"{{{{{key}}}}}"):
                            if brace in resolved:
                                resolved = resolved.replace(brace, val_str)
            # Replace remaining unfilled placeholders (both {x} and {{x}})
            resolved = re.sub(r"\{[^}]+\}", "", resolved)
            resolved = re.sub(r"\{{2}[^}]+\}{2}", "", resolved)
            # Collapse multiple spaces
            resolved = re.sub(r" +", " ", resolved).strip()
            params["command"] = resolved

        return params

    def _build_chain_dag(
        self,
        candidates: list[dict[str, Any]],
        goal: str,
        constraints: dict[str, Any],
    ) -> WorkflowDAG:
        dag = WorkflowDAG()
        goal_lower = goal.lower()
        min_transform_fidelity = constraints.get("min_transform_fidelity", 0.0)

        for i, tool in enumerate(candidates):
            retry_policy = constraints.get("retry_policy", {})
            params = self._resolve_params(tool, goal)
            node = DAGNode(
                id=f"node_{i}",
                tool_id=tool.get("id", ""),
                tool_namespace=tool.get("namespace", ""),
                node_type="tool",
                params=params,
                retry_policy={
                    "max_attempts": retry_policy.get("max_attempts", constraints.get("max_retries", 1) + 1),
                    "backoff": retry_policy.get("backoff", constraints.get("backoff", "exponential")),
                },
                label=tool.get("name", ""),
            )
            dag.add_node(node)

        def _get_outputs(t: dict) -> list[str]:
            return [o.get("type", "") for o in t.get("contract", {}).get("outputs", [])] or t.get("workflow_edges", {}).get("produces", [])

        def _get_inputs(t: dict) -> list[str]:
            return [i.get("type", "") for i in t.get("contract", {}).get("inputs", [])] or t.get("workflow_edges", {}).get("consumes", [])

        transform_counter = [0]

        def _make_transform_node(path, src_type, tgt_type) -> DAGNode:
            transform_counter[0] += 1
            idx = transform_counter[0]
            return DAGNode(
                id=f"transform_{idx}",
                tool_id="",
                tool_namespace="",
                node_type="transform",
                label=f"transform:{path.first_method}:{src_type}→{tgt_type}",
                transform_def=path.to_dict(),
            )

        lossy_count = 0
        max_lossy = constraints.get("max_lossy_transforms")

        for i in range(len(candidates) - 1):
            current = candidates[i]
            next_tool = candidates[i + 1]

            outputs = _get_outputs(current)
            inputs = _get_inputs(next_tool)

            shared = set(outputs) & set(inputs)
            if shared:
                dag.add_edge(DAGEdge(
                    source_id=f"node_{i}",
                    target_id=f"node_{i + 1}",
                    artifact_type=list(shared)[0],
                ))
            else:
                path: TransformPath | None = None
                if min_transform_fidelity > 0.0:
                    path = self.transform_resolver.resolve_best_fidelity(
                        outputs[0] if outputs else "",
                        inputs[0] if inputs else "",
                        min_score=min_transform_fidelity,
                    ) if outputs and inputs else None
                if not path:
                    path_tup = self.transform_resolver.best_pair(outputs, inputs)
                    path = path_tup[2] if path_tup else None

                if path:
                    if path.lossy:
                        lossy_count += 1
                        if max_lossy is not None and lossy_count > max_lossy:
                            logger.warning(
                                "Exceeded max_lossy_transforms=%d at edge %s→%s",
                                max_lossy, i, i + 1,
                            )
                            continue
                    src_type = outputs[0] if outputs else ""
                    tgt_type = inputs[0] if inputs else ""
                    t_node = _make_transform_node(path, src_type, tgt_type)
                    dag.add_node(t_node)
                    dag.add_edge(DAGEdge(
                        source_id=f"node_{i}",
                        target_id=t_node.id,
                        artifact_type=src_type,
                    ))
                    dag.add_edge(DAGEdge(
                        source_id=t_node.id,
                        target_id=f"node_{i + 1}",
                        artifact_type=tgt_type,
                    ))

        return dag

    def simulate(self, goal: str, constraints: dict[str, Any] | None = None, objective: str | dict[str, Any] | ObjectiveProfile | None = None) -> dict[str, Any]:
        plan = self.plan_from_goal(goal, constraints, objective=objective)
        plan["mode"] = "simulation"
        plan["disclaimer"] = "This is a dry-run plan. No workflows or tasks were created."
        return plan
