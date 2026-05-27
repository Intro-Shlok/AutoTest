"""
Merge enrichment data from mapping.json into tool .md files.
Uses ruamel.yaml to preserve existing YAML formatting.
"""
import json
import re
from io import StringIO
from pathlib import Path

from ruamel.yaml import YAML

yaml = YAML()
yaml.preserve_quotes = True
yaml.indent(mapping=2, sequence=4, offset=2)

TOOLS_DIR = Path("src/content/tools")
MAPPING_PATH = Path("data/enrichment/mapping.json")

PHASE_MAP = {
    "enumeration": "enumeration",
    "exploitation": "exploitation",
    "post-exploitation": "post-exploitation",
    "recon": "recon",
}

FEATURE_MAP = {
    "file-read": "output-json",
    "file-write": "file-system",
    "file-download": "network-intensive",
    "file-upload": "network-intensive",
    "command-execution": "process-manip",
    "library-load": "process-manip",
    "suid-execution": "local",
    "sudo": "local",
    "reverse-shell": "remote",
    "bind-shell": "remote",
    "non-interactive-reverse-shell": "remote",
}

def merge_enrichment():
    mapping = json.loads(MAPPING_PATH.read_text())
    merged_count = 0
    total_fields = {}

    for f in sorted(TOOLS_DIR.glob("*.md")):
        content = f.read_text()
        parts = content.split("---", 2)
        if len(parts) < 3:
            continue

        fm = yaml.load(parts[1])
        if fm is None:
            continue

        tid = fm.get("id", "")
        if tid not in mapping:
            continue

        data = mapping[tid]
        matches = data.get("matches", {})
        if not matches:
            continue

        changed = False

        # mitre_ids from LOLBAS
        if "lolbas" in matches and not fm.get("mitre_ids"):
            mids = matches["lolbas"].get("mitre_ids", [])
            if mids:
                fm["mitre_ids"] = mids
                changed = True
                total_fields.setdefault("mitre_ids", 0)
                total_fields["mitre_ids"] += len(mids)

        # contributor from LOLBAS
        if "lolbas" in matches and not fm.get("contributor"):
            c = matches["lolbas"].get("contributor", "")
            if c:
                fm["contributor"] = c
                changed = True
                total_fields.setdefault("contributor", 0)
                total_fields["contributor"] += 1

        # phase from NetRunners
        if "netrunners" in matches and not fm.get("phase"):
            phases = matches["netrunners"].get("phases", [])
            for p in phases:
                pl = p.lower()
                if pl in PHASE_MAP:
                    fm["phase"] = PHASE_MAP[pl]
                    changed = True
                    total_fields.setdefault("phase", 0)
                    total_fields["phase"] += 1
                    break

        # features from GTFOArgs
        if "gtfoargs" in matches:
            existing = set(fm.get("features", []) or [])
            mapped = set()
            for fname in matches["gtfoargs"].get("features", []):
                m = FEATURE_MAP.get(fname)
                if m and m not in existing:
                    mapped.add(m)
            if mapped:
                fm["features"] = list(existing) + sorted(mapped)
                changed = True
                total_fields.setdefault("features", 0)
                total_fields["features"] += len(mapped)

        # examples from GTFOArgs
        if "gtfoargs" in matches:
            existing_examples = fm.get("examples", []) or []
            existing_descs = {e.get("description", "") for e in existing_examples}
            new_examples = []
            for ex in matches["gtfoargs"].get("examples", []):
                desc = ex.get("description", "")
                cmd = ex.get("command", "")
                if desc not in existing_descs and cmd:
                    new_examples.append(ex)
                    existing_descs.add(desc)
            if new_examples:
                fm["examples"] = existing_examples + new_examples
                changed = True
                total_fields.setdefault("examples", 0)
                total_fields["examples"] += len(new_examples)

        if changed:
            body = "---\n"
            buf = StringIO()
            yaml.dump(fm, buf)
            body += buf.getvalue().strip()
            body += "\n---\n\n"
            body += parts[2].strip()
            if not body.endswith("\n"):
                body += "\n"
            f.write_text(body)
            merged_count += 1

    print(f"Merged enrichment into {merged_count} tool files")
    for field, count in sorted(total_fields.items()):
        print(f"  {field}: {count} values injected")


if __name__ == "__main__":
    merge_enrichment()
