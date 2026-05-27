"""
Phase 2 merge: inject techniques + mitre_ids from RedTeaming-Tactics into tool .md files.
Uses ruamel.yaml for set-union merge that preserves formatting.
"""
import json
from io import StringIO
from pathlib import Path

from ruamel.yaml import YAML

yaml = YAML()
yaml.preserve_quotes = True
yaml.indent(mapping=2, sequence=4, offset=2)

TOOLS_DIR = Path("src/content/tools")
REDTEAMING_PATH = Path("data/enrichment/redteaming-matches.json")

VALID_TECHNIQUES = {
    "recon", "enumeration", "exfiltration", "privilege-escalation",
    "persistence", "lateral-movement", "discovery", "collection",
    "command-and-control", "credential-access", "defense-evasion",
    "execution", "impact", "data-manipulation", "monitoring",
    "backup", "forensics", "analysis", "network-manipulation",
    "process-discovery", "process-termination", "network-sniffing",
    "remote-services", "encryption", "process-manip",
}


def merge_techniques(fm: dict, new_techniques: list[str]) -> int:
    """Union-merge techniques field. Returns count of new values added."""
    existing = set(fm.get("techniques", []) or [])
    to_add = [t for t in new_techniques if t in VALID_TECHNIQUES and t not in existing]
    if to_add:
        fm["techniques"] = list(existing) + to_add
    return len(to_add)


def merge_mitre_ids(fm: dict, new_ids: list[str]) -> int:
    """Union-merge mitre_ids field. Returns count of new values added."""
    existing = set(fm.get("mitre_ids", []) or [])
    to_add = [m for m in new_ids if m not in existing]
    if to_add:
        fm["mitre_ids"] = list(existing) + to_add
    return len(to_add)


def merge():
    redteaming = json.loads(REDTEAMING_PATH.read_text())
    merged_count = 0
    tech_count = 0
    mitre_count = 0

    for f in sorted(TOOLS_DIR.glob("*.md")):
        content = f.read_text()
        parts = content.split("---", 2)
        if len(parts) < 3:
            continue

        fm = yaml.load(parts[1])
        if fm is None:
            continue

        tid = fm.get("id", "")
        if tid not in redteaming:
            continue

        data = redteaming[tid]

        # Merge techniques
        new_techs = data.get("techniques", [])
        if new_techs:
            count = merge_techniques(fm, new_techs)
            if count:
                tech_count += count

        # Merge mitre_ids
        new_ids = data.get("mitre_ids", [])
        if new_ids:
            count = merge_mitre_ids(fm, new_ids)
            if count:
                mitre_count += count

        if not new_techs and not new_ids:
            continue

        merged_count += 1

        # Re-serialize
        body = "---\n"
        buf = StringIO()
        yaml.dump(fm, buf)
        body += buf.getvalue().strip()
        body += "\n---\n\n"
        body += parts[2].strip()
        if not body.endswith("\n"):
            body += "\n"
        f.write_text(body)

    print(f"Phase 2 merge: enriched {merged_count} tool files")
    print(f"  techniques:  {tech_count} values injected")
    print(f"  mitre_ids:   {mitre_count} values injected")


if __name__ == "__main__":
    merge()
