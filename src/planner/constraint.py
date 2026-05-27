from __future__ import annotations

from typing import Any


def _prefix_match(needle: str, haystack: list[str]) -> bool:
    for h in haystack:
        if h == needle:
            return True
        if h.startswith(needle + "."):
            return True
    return False


def _contract_field(tool: dict[str, Any], field: str, default: Any = None) -> Any:
    contract = tool.get("contract", {})
    profile = tool.get("resource_profile", {})
    if contract:
        contract_rc = contract.get("resource_cost", {})
        if field in contract_rc:
            return contract_rc.get(field)
    return profile.get(field, default)


def filter_by_resource(
    tools: list[dict[str, Any]],
    max_memory_mb: int | None = None,
    max_cpu: str | None = None,
    network_required: bool | None = None,
) -> list[dict[str, Any]]:
    results = list(tools)
    if max_memory_mb is not None:
        results = [t for t in results if _contract_field(t, "memory_mb", 0) <= max_memory_mb]
    if max_cpu:
        cpu_rank = {"low": 1, "medium": 2, "high": 3}
        results = [t for t in results if cpu_rank.get(_contract_field(t, "cpu", "medium"), 2) <= cpu_rank[max_cpu]]
    if network_required is not None:
        if network_required:
            results = [t for t in results if _contract_field(t, "network", "low") != "none"]
        else:
            results = [t for t in results if _contract_field(t, "network", "low") == "none"]
    return results


def filter_by_trust(
    tools: list[dict[str, Any]],
    min_trust: str = "community",
) -> list[dict[str, Any]]:
    trust_rank = {"ai-generated": 0, "experimental": 1, "community": 2, "verified": 3}
    min_rank = trust_rank.get(min_trust, 2)
    return [t for t in tools if trust_rank.get(t.get("trust_level", "community"), 2) >= min_rank]


def filter_by_architecture(
    tools: list[dict[str, Any]],
    host_arch: str,
) -> list[dict[str, Any]]:
    return [t for t in tools if "cross-platform" in t.get("architectures", []) or host_arch in t.get("architectures", [])]


def filter_by_policy(
    tools: list[dict[str, Any]],
    policy: str = "enabled",
) -> list[dict[str, Any]]:
    return [t for t in tools if t.get("execution_policy", "enabled") == policy]


def filter_by_capability(
    tools: list[dict[str, Any]],
    capability: str,
) -> list[dict[str, Any]]:
    return [t for t in tools if _prefix_match(capability, t.get("capabilities", []))]


def filter_by_side_effect(
    tools: list[dict[str, Any]],
    side_effect: str,
    present: bool = True,
) -> list[dict[str, Any]]:
    results = []
    for t in tools:
        se = t.get("contract", {}).get("side_effects", [])
        if present and side_effect in se:
            results.append(t)
        elif not present and side_effect not in se:
            results.append(t)
    return results


def find_producers(
    tools: list[dict[str, Any]],
    artifact_type: str,
) -> list[dict[str, Any]]:
    results = []
    for t in tools:
        contract = t.get("contract", {})
        outputs = contract.get("outputs", [])
        if _prefix_match(artifact_type, [o.get("type", "") for o in outputs]):
            results.append(t)
        elif _prefix_match(artifact_type, t.get("workflow_edges", {}).get("produces", [])):
            results.append(t)
    return results


def find_consumers(
    tools: list[dict[str, Any]],
    artifact_type: str,
) -> list[dict[str, Any]]:
    results = []
    for t in tools:
        contract = t.get("contract", {})
        inputs = contract.get("inputs", [])
        if _prefix_match(artifact_type, [i.get("type", "") for i in inputs]):
            results.append(t)
        elif _prefix_match(artifact_type, t.get("workflow_edges", {}).get("consumes", [])):
            results.append(t)
    return results


def solve_chain(
    tools: list[dict[str, Any]],
    start_artifact: str | None = None,
    goal_artifact: str | None = None,
    max_depth: int = 5,
) -> list[list[str]]:
    tools_by_ns = {t.get("namespace", ""): t for t in tools}

    def _get_outputs(tool: dict[str, Any]) -> list[str]:
        contract = tool.get("contract", {})
        out = [o.get("type", "") for o in contract.get("outputs", [])]
        if not out:
            out = tool.get("workflow_edges", {}).get("produces", [])
        return out

    def _get_inputs(tool: dict[str, Any]) -> list[str]:
        contract = tool.get("contract", {})
        inputs = [i.get("type", "") for i in contract.get("inputs", [])]
        if not inputs:
            inputs = tool.get("workflow_edges", {}).get("consumes", [])
        return inputs

    all_produces: dict[str, list[str]] = {}
    for t in tools:
        ns = t.get("namespace", "")
        for art in _get_outputs(t):
            all_produces.setdefault(art, []).append(ns)
    all_consumes: dict[str, list[str]] = {}
    for t in tools:
        ns = t.get("namespace", "")
        for art in _get_inputs(t):
            all_consumes.setdefault(art, []).append(ns)

    chains: list[list[str]] = []

    def dfs(current_artifact: str, path: list[str], depth: int) -> None:
        if depth > max_depth:
            return
        if goal_artifact and current_artifact == goal_artifact:
            if path:
                chains.append(list(path))
            return
        producers = all_produces.get(current_artifact, [])
        for tool_ns in producers:
            if tool_ns not in path:
                path.append(tool_ns)
                for out_art in _get_outputs(tools_by_ns.get(tool_ns, {})):
                    dfs(out_art, path, depth + 1)
                path.pop()

    if start_artifact:
        dfs(start_artifact, [], 0)
    elif goal_artifact:
        consumers = all_consumes.get(goal_artifact, [])
        for tool_ns in consumers:
            chain = [tool_ns]
            preds = _get_inputs(tools_by_ns.get(tool_ns, {}))
            if preds:
                chains.append(chain)

    return chains


def match_capability_prefix(capability_prefix: str, tools: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [t for t in tools if _prefix_match(capability_prefix, t.get("capabilities", []))]
