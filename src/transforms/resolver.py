from __future__ import annotations

import logging
import fnmatch
from typing import Any

from src.transforms.registry import TransformCatalog, TransformDef, FIDELITY_LOSSLESS, LOSS_TYPE_ORDER

logger = logging.getLogger("transforms")


class TransformPath:
    def __init__(self, steps: list[TransformDef], source_type: str, target_type: str) -> None:
        self.steps = steps
        self.source_type = source_type
        self.target_type = target_type

    @property
    def length(self) -> int:
        return len(self.steps)

    @property
    def lossy(self) -> bool:
        return any(not s.is_lossless for s in self.steps)

    @property
    def fidelity_score(self) -> float:
        if not self.steps:
            return 1.0
        return min(s.fidelity_score for s in self.steps)

    @property
    def loss_type(self) -> str:
        if not self.steps:
            return FIDELITY_LOSSLESS
        worst = max(self.steps, key=lambda s: LOSS_TYPE_ORDER.get(s.loss_type, 0))
        return worst.loss_type

    @property
    def fidelity_breakdown(self) -> dict[str, float]:
        if not self.steps:
            return {"structural": 1.0, "semantic": 1.0, "content": 1.0}
        breakdown: dict[str, float] = {"structural": 1.0, "semantic": 1.0, "content": 1.0}
        for s in self.steps:
            bd = s.fidelity.get("breakdown") if s.fidelity else None
            if bd:
                for k in breakdown:
                    val = bd.get(k)
                    if val is not None:
                        breakdown[k] = min(breakdown[k], val)
        return breakdown

    @property
    def first_method(self) -> str:
        return self.steps[0].method if self.steps else "none"

    @property
    def degradation_notes(self) -> list[str]:
        notes: list[str] = []
        for s in self.steps:
            if s.fidelity:
                note = s.fidelity.get("degradation_notes")
                if note:
                    notes.append(note)
        return notes

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_type": self.source_type,
            "target_type": self.target_type,
            "steps": [s.to_dict() for s in self.steps],
            "lossy": self.lossy,
            "length": self.length,
            "fidelity": {
                "score": self.fidelity_score,
                "loss_type": self.loss_type,
                "breakdown": self.fidelity_breakdown,
                "degradation_notes": self.degradation_notes,
            },
        }


class TransformResolver:
    def __init__(self, catalog: TransformCatalog) -> None:
        self.catalog = catalog

    def resolve(self, source_type: str, target_type: str, max_hops: int = 2) -> TransformPath | None:
        if max_hops < 1:
            return None
        direct = self.catalog.find_best(source_type, target_type)
        if direct:
            return TransformPath([direct], source_type, target_type)
        if max_hops >= 2:
            intermediates: set[str] = set()
            for t in self.catalog.transforms:
                if fnmatch.fnmatch(source_type, t.source) or t.source == "*":
                    if t.target != target_type:
                        intermediates.add(t.target)
                if fnmatch.fnmatch(target_type, t.target) or t.target == "*":
                    if t.source != source_type:
                        intermediates.add(t.source)
            for intermediate in intermediates:
                first = self.catalog.find_best(source_type, intermediate)
                second = self.catalog.find_best(intermediate, target_type)
                if first and second:
                    return TransformPath([first, second], source_type, target_type)
        return None

    def resolve_best_fidelity(
        self,
        source_type: str,
        target_type: str,
        min_score: float = 0.0,
        max_hops: int = 2,
    ) -> TransformPath | None:
        if max_hops < 1:
            return None

        candidates: list[TransformPath] = []

        direct = self.catalog.find_best_fidelity(source_type, target_type, min_score=min_score)
        if direct:
            candidates.append(TransformPath([direct], source_type, target_type))

        if max_hops >= 2:
            intermediates: set[str] = set()
            for t in self.catalog.transforms:
                if fnmatch.fnmatch(source_type, t.source) or t.source == "*":
                    if t.target != target_type:
                        intermediates.add(t.target)
                if fnmatch.fnmatch(target_type, t.target) or t.target == "*":
                    if t.source != source_type:
                        intermediates.add(t.source)
            for intermediate in intermediates:
                first = self.catalog.find_best_fidelity(source_type, intermediate, min_score=min_score)
                second = self.catalog.find_best_fidelity(intermediate, target_type, min_score=min_score)
                if first and second:
                    candidates.append(TransformPath([first, second], source_type, target_type))

        if not candidates:
            return None

        candidates.sort(key=lambda p: (-p.fidelity_score, p.length, 0 if p.first_method == "pipe" else 1))
        return candidates[0]

    def resolve_all(self, source_types: list[str], target_types: list[str]) -> dict[tuple[str, str], TransformPath | None]:
        results: dict[tuple[str, str], TransformPath | None] = {}
        for src in source_types:
            for tgt in target_types:
                results[(src, tgt)] = self.resolve(src, tgt)
        return results

    def best_pair(self, source_types: list[str], target_types: list[str]) -> tuple[str, str, TransformPath] | None:
        best_path: TransformPath | None = None
        best_src: str = ""
        best_tgt: str = ""
        for src in source_types:
            for tgt in target_types:
                path = self.resolve(src, tgt)
                if path:
                    if best_path is None:
                        best_path = path
                        best_src = src
                        best_tgt = tgt
                    else:
                        if path.fidelity_score > best_path.fidelity_score:
                            best_path = path
                            best_src = src
                            best_tgt = tgt
                        elif path.fidelity_score == best_path.fidelity_score and path.length < best_path.length:
                            best_path = path
                            best_src = src
                            best_tgt = tgt
        if best_path:
            return (best_src, best_tgt, best_path)
        return None


import fnmatch
