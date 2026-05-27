from __future__ import annotations

import json
import logging
import os
import fnmatch
from dataclasses import dataclass
from pathlib import Path
from typing import Any

logger = logging.getLogger("transforms")

TRANSFORMS_PATH = Path(__file__).resolve().parent.parent.parent / "schemas" / "transforms-default.json"

FIDELITY_LOSSLESS = "lossless"
FIDELITY_TRUNCATION = "truncation"
FIDELITY_STRUCTURAL = "structural"
FIDELITY_SEMANTIC = "semantic"
FIDELITY_FULL = "full"

LOSS_TYPE_ORDER = {
    FIDELITY_LOSSLESS: 0,
    FIDELITY_TRUNCATION: 1,
    FIDELITY_STRUCTURAL: 2,
    FIDELITY_SEMANTIC: 3,
    FIDELITY_FULL: 4,
}

_DEFAULT_FIDELITY_LOSSLESS: dict[str, Any] = {
    "score": 1.0,
    "loss_type": FIDELITY_LOSSLESS,
    "breakdown": {"structural": 1.0, "semantic": 1.0, "content": 1.0},
}

_DEFAULT_FIDELITY_FULL_LOSS: dict[str, Any] = {
    "score": 0.0,
    "loss_type": FIDELITY_FULL,
    "breakdown": {"structural": 0.0, "semantic": 0.0, "content": 0.0},
}


def _convert_legacy_lossy(lossy: bool | None) -> dict[str, Any]:
    if lossy is True:
        return dict(_DEFAULT_FIDELITY_FULL_LOSS)
    return dict(_DEFAULT_FIDELITY_LOSSLESS)


def _normalize_fidelity(fidelity: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {
        "score": fidelity.get("score", 1.0),
        "loss_type": fidelity.get("loss_type", FIDELITY_LOSSLESS),
    }
    breakdown = fidelity.get("breakdown")
    if breakdown is not None:
        result["breakdown"] = {
            "structural": breakdown.get("structural", 1.0),
            "semantic": breakdown.get("semantic", 1.0),
            "content": breakdown.get("content", 1.0),
        }
    notes = fidelity.get("degradation_notes")
    if notes:
        result["degradation_notes"] = notes
    return result


@dataclass
class TransformDef:
    source: str
    target: str
    method: str
    lossy: bool = False
    converter_tool: str | None = None
    command_template: str | None = None
    description: str = ""
    fidelity: dict[str, Any] | None = None

    def __post_init__(self) -> None:
        if self.fidelity is None:
            self.fidelity = _convert_legacy_lossy(self.lossy if self.lossy else None)

    @property
    def fidelity_score(self) -> float:
        return self.fidelity.get("score", 1.0) if self.fidelity else 1.0

    @property
    def loss_type(self) -> str:
        return self.fidelity.get("loss_type", FIDELITY_LOSSLESS) if self.fidelity else FIDELITY_LOSSLESS

    @property
    def is_lossless(self) -> bool:
        return self.fidelity_score >= 1.0

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "source": self.source,
            "target": self.target,
            "method": self.method,
            "lossy": not self.is_lossless,
            "fidelity": self.fidelity,
            "converter_tool": self.converter_tool,
            "command_template": self.command_template,
            "description": self.description,
        }
        return d

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> TransformDef:
        return cls(
            source=d["source"],
            target=d["target"],
            method=d["method"],
            lossy=d.get("lossy", False),
            converter_tool=d.get("converter_tool"),
            command_template=d.get("command_template"),
            description=d.get("description", ""),
            fidelity=d.get("fidelity"),
        )


class TransformCatalog:
    def __init__(self, transforms: list[TransformDef] | None = None) -> None:
        self.transforms: list[TransformDef] = transforms or []

    def add(self, t: TransformDef) -> None:
        self.transforms.append(t)
        logger.debug("Added transform: %s -> %s (%s)", t.source, t.target, t.method)

    def find(self, source_type: str, target_type: str) -> list[TransformDef]:
        results: list[TransformDef] = []
        for t in self.transforms:
            src_match = fnmatch.fnmatch(source_type, t.source) or t.source == "*"
            tgt_match = fnmatch.fnmatch(target_type, t.target) or t.target == "*"
            if src_match and tgt_match:
                results.append(t)
        results.sort(key=lambda x: (
            -x.fidelity_score,
            0 if x.method == "pipe" else 1 if x.method == "redirect" else 2,
        ))
        return results

    def find_best(self, source_type: str, target_type: str) -> TransformDef | None:
        matches = self.find(source_type, target_type)
        if not matches:
            return None
        for m in matches:
            if (m.source == source_type or m.source == "*") and (m.target == target_type or m.target == "*"):
                return m
        return matches[0]

    def find_best_fidelity(self, source_type: str, target_type: str, min_score: float = 0.0) -> TransformDef | None:
        matches = self.find(source_type, target_type)
        filtered = [m for m in matches if m.fidelity_score >= min_score]
        if not filtered:
            return None
        return filtered[0]

    def has_direct(self, source_type: str, target_type: str) -> bool:
        return self.find_best(source_type, target_type) is not None

    def to_list(self) -> list[dict[str, Any]]:
        return [t.to_dict() for t in self.transforms]

    @classmethod
    def load_default(cls) -> TransformCatalog:
        if TRANSFORMS_PATH.exists():
            with open(TRANSFORMS_PATH) as f:
                data = json.load(f)
            transforms = [TransformDef.from_dict(t) for t in data.get("transforms", [])]
            logger.info("Loaded %d default transforms", len(transforms))
            return cls(transforms)
        logger.warning("No default transforms file at %s", TRANSFORMS_PATH)
        return cls()

    @classmethod
    def load(cls, path: str | Path) -> TransformCatalog:
        with open(path) as f:
            data = json.load(f)
        transforms = [TransformDef.from_dict(t) for t in data.get("transforms", [])]
        return cls(transforms)
