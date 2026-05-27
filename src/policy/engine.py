from __future__ import annotations

import json
import logging
import time
from typing import Any

from src.orchestrator.db import insert, update, fetch_one, fetch_all
from src.ulid import prefixed_ulid

logger = logging.getLogger("policy")

DEFAULT_POLICIES: list[dict[str, Any]] = [
    {"rule": "deny_outbound_network", "condition": {"field": "resource_profile.network", "eq": "none"}, "action": "block", "enabled": True},
    {"rule": "warn_experimental", "condition": {"field": "trust_level", "eq": "experimental"}, "action": "warn", "enabled": True},
    {"rule": "require_approval_high_risk", "condition": {"field": "risk_level", "eq": "high"}, "action": "require_approval", "enabled": True},
    {"rule": "deny_disabled_tools", "condition": {"field": "execution_policy", "eq": "disabled"}, "action": "block", "enabled": True},
]


def resolve_field(obj: dict[str, Any], dotted_path: str) -> Any:
    value = obj
    for part in dotted_path.split("."):
        if isinstance(value, dict):
            value = value.get(part)
        else:
            return None
    return value


def _prefix_matches(needle: str, haystack: list[str]) -> bool:
    for h in haystack:
        if h == needle:
            return True
        if h.startswith(needle + "."):
            return True
    return False


class PolicyEngine:
    def __init__(self, policies: list[dict[str, Any]] | None = None) -> None:
        self.policies = policies or [dict(p) for p in DEFAULT_POLICIES]

    def evaluate(self, tool: dict[str, Any]) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        for policy in self.policies:
            if not policy.get("enabled", True):
                continue
            cond = policy.get("condition", {})

            capability_filter = cond.get("capability")
            if capability_filter:
                tool_caps = tool.get("capabilities", [])
                if not _prefix_matches(capability_filter, tool_caps):
                    continue

            risk_min = cond.get("risk_min")
            if risk_min:
                risk_rank = {"low": 0, "medium": 1, "high": 2, "critical": 3}
                tool_risk = risk_rank.get(tool.get("risk_level", "low"), 0)
                if tool_risk < risk_rank.get(risk_min, 0):
                    continue

            field = cond.get("field", "")
            if not field:
                continue
            expected = cond.get("eq")
            actual = resolve_field(tool, field)
            if actual == expected:
                results.append({
                    "rule": policy["rule"],
                    "action": policy["action"],
                    "matched": True,
                    "field": field,
                    "expected": expected,
                    "actual": actual,
                    "capability_match": capability_filter,
                })
        return results

    def is_blocked(self, tool: dict[str, Any]) -> tuple[bool, str]:
        results = self.evaluate(tool)
        for r in results:
            if r["action"] == "block":
                return True, r["rule"]
        return False, ""

    def requires_approval(self, tool: dict[str, Any]) -> bool:
        results = self.evaluate(tool)
        return any(r["action"] == "require_approval" for r in results)

    def add_policy(self, policy: dict[str, Any]) -> None:
        self.policies.append(policy)
        logger.info("Added policy: %s", policy["rule"])

    def remove_policy(self, rule_name: str) -> bool:
        before = len(self.policies)
        self.policies = [p for p in self.policies if p["rule"] != rule_name]
        return len(self.policies) < before

    def to_dict(self) -> list[dict[str, Any]]:
        return list(self.policies)

    @classmethod
    def from_dict(cls, policies: list[dict[str, Any]]) -> PolicyEngine:
        return cls(policies)

    async def load_from_db(self) -> None:
        rows = await fetch_all("SELECT * FROM policies WHERE enabled = 1 ORDER BY rowid")
        if not rows:
            return
        loaded = []
        for row in rows:
            rule = json.loads(row["rule_json"])
            rule["enabled"] = True
            loaded.append(rule)
        if loaded:
            self.policies = loaded
            logger.info("Loaded %d policies from database", len(loaded))

    async def save_to_db(self, policy: dict[str, Any]) -> str:
        pid = prefixed_ulid("pol")
        now = time.time()
        await insert("policies", {
            "id": pid,
            "name": policy["rule"],
            "rule_json": json.dumps(policy),
            "enabled": 1,
            "created_at": now,
        })
        self.add_policy(policy)
        return pid
