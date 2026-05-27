"""
Extract detections, commands, and MITRE IDs from LOLBAS into AutoTest tool files.

LOLBAS format: Collection of .yml files, one per Windows LOLBin.
We map overlapping tools (bash, ftp, sftp, ssh, tar) and merge:
  - Detection[] -> our detections[]
  - Commands[] -> our examples[]
  - MitreID per command -> union merge into our mitre_ids[]

Usage:
  python3 src/scripts/enrichment/extract-lolbas.py
"""
import json
import re
from io import StringIO
from pathlib import Path

import yaml as pyyaml
from ruamel.yaml import YAML

yaml = YAML()
yaml.preserve_quotes = True
yaml.indent(mapping=2, sequence=4, offset=2)

LOLBAS_DIR = Path("Database/LOLBAS/yml")
TOOLS_DIR = Path("src/content/tools")
OUTPUT_PATH = Path("data/enrichment/lolbas-matches.json")

# Map LOLBAS Name -> our tool id (dash-separated kebab-case)
# LOLBAS names always have .exe suffix; keys here are case-insensitive
NAME_TO_TOOL_ID = {
    "bash.exe": "system-shell-bash",
    "ftp.exe": "network-transfer-ftp",
    "sftp.exe": "network-transfer-sftp",
    "ssh.exe": "network-remote-ssh",
    "tar.exe": "system-archive-tar",
}

# Match detection strings like "Sigma: URL", "Elastic: URL", "IOC: text"
DETECTION_RE = re.compile(r"^(sigma|elastic|splunk|ioc|blockrule|yara|clamav|sysmon|wdac)\s*:\s*(.+)$", re.IGNORECASE)

CATEGORY_TO_TECHNIQUE = {
    "download": "command-and-control",
    "upload": "exfiltration",
    "execute": "execution",
    "ads": "defense-evasion",
    "copy": "collection",
    "encode": "defense-evasion",
    "decode": "defense-evasion",
    "bypass": "defense-evasion",
    "awl bypass": "defense-evasion",
    "recon": "discovery",
    "deception": "defense-evasion",
    "compromise": "execution",
}

VALID_TECHNIQUES = {
    "recon", "enumeration", "exfiltration", "privilege-escalation",
    "persistence", "lateral-movement", "discovery", "collection",
    "command-and-control", "credential-access", "defense-evasion",
    "execution", "impact", "data-manipulation", "monitoring",
    "backup", "forensics", "analysis", "network-manipulation",
    "process-discovery", "process-termination", "network-sniffing",
    "remote-services", "encryption", "process-manip",
}

VALID_DETECTION_TYPES = {"sigma", "elastic", "splunk", "ioc", "blockrule", "yara", "clamav", "sysmon", "wdac"}


def parse_detection(item) -> dict | None:
    """Parse a single LOLBAS detection item into our detections format.

    LOLBAS detection items can be either:
      - A single-key dict: {"Sigma": "URL"} or {"IOC": "text"}
      - A string: "Sigma: URL" (rare variant)
    """
    if isinstance(item, dict):
        for key, value in item.items():
            dtype = key.lower().strip()
            if dtype in VALID_DETECTION_TYPES:
                val = str(value).strip()
                if dtype in ("sigma", "elastic", "splunk", "blockrule", "yara", "clamav", "sysmon", "wdac"):
                    return {"type": dtype, "url": val}
                elif dtype == "ioc":
                    return {"type": "ioc", "description": val}
        return None
    elif isinstance(item, str):
        m = DETECTION_RE.match(item.strip())
        if m:
            dtype = m.group(1).lower()
            value = m.group(2).strip()
            if dtype in ("sigma", "elastic", "splunk", "blockrule", "yara", "clamav", "sysmon", "wdac"):
                return {"type": dtype, "url": value}
            elif dtype == "ioc":
                return {"type": "ioc", "description": value}
    return None


def extract_all() -> dict:
    """Scan all LOLBAS .yml files and return {tool_id: {mitre_ids, examples, detections, techniques}}."""
    results: dict = {}
    for yml_file in sorted(LOLBAS_DIR.rglob("*.yml")):
        with open(yml_file) as f:
            data = pyyaml.safe_load(f)

        name = data.get("Name", "")
        if not name:
            continue

        tool_id = NAME_TO_TOOL_ID.get(name.lower())
        if not tool_id:
            continue

        mitre_ids: set[str] = set()
        examples: list[dict] = []
        techniques: set[str] = set()

        # Extract commands -> examples + mitre_ids + techniques
        for cmd in data.get("Commands", []):
            cmd_str = cmd.get("Command", "")
            desc = cmd.get("Description", "")
            usecase = cmd.get("Usecase", "")
            category = cmd.get("Category", "")
            mid = cmd.get("MitreID", "")

            # Build example description
            ex_desc = usecase if usecase else desc
            if ex_desc:
                examples.append({"description": ex_desc, "command": cmd_str})

            # Collect MITRE IDs
            if mid:
                mitre_ids.add(mid)

            # Derive technique from category
            tech = CATEGORY_TO_TECHNIQUE.get(category.lower().strip())
            if tech and tech in VALID_TECHNIQUES:
                techniques.add(tech)

        # Extract detections
        detections: list[dict] = []
        for det_text in data.get("Detection", []):
            parsed = parse_detection(det_text)
            if parsed:
                detections.append(parsed)

        if not any([mitre_ids, examples, detections, techniques]):
            continue

        results[tool_id] = {}
        if sorted(mitre_ids):
            results[tool_id]["mitre_ids"] = sorted(mitre_ids)
        if techniques:
            results[tool_id]["techniques"] = sorted(techniques)
        if examples:
            results[tool_id]["examples"] = examples
        if detections:
            results[tool_id]["detections"] = detections

    return results


def merge_into_tools(extracted: dict):
    """Merge extracted data into tool .md files using ruamel.yaml set-union."""
    merged_count = 0
    tech_count = 0
    mitre_count = 0
    example_count = 0
    detection_count = 0

    for f in sorted(TOOLS_DIR.glob("*.md")):
        content = f.read_text()
        parts = content.split("---", 2)
        if len(parts) < 3:
            continue

        fm = yaml.load(parts[1])
        if fm is None:
            continue

        tid = fm.get("id", "")
        if tid not in extracted:
            continue

        data = extracted[tid]
        changed = False

        # Merge mitre_ids (set union)
        new_ids = data.get("mitre_ids", [])
        if new_ids:
            existing = set(fm.get("mitre_ids", []) or [])
            to_add = [m for m in new_ids if m not in existing]
            if to_add:
                fm["mitre_ids"] = list(existing) + to_add
                mitre_count += len(to_add)
                changed = True

        # Merge techniques (set union)
        new_techs = data.get("techniques", [])
        if new_techs:
            existing = set(fm.get("techniques", []) or [])
            to_add = [t for t in new_techs if t not in existing]
            if to_add:
                fm["techniques"] = list(existing) + to_add
                tech_count += len(to_add)
                changed = True

        # Merge examples (append new ones, dedup by command string)
        new_examples = data.get("examples", [])
        if new_examples:
            existing_cmds = {e["command"] for e in (fm.get("examples", []) or [])}
            to_add = [e for e in new_examples if e["command"] not in existing_cmds]
            if to_add:
                existing_examples = list(fm.get("examples", []) or [])
                fm["examples"] = existing_examples + to_add
                example_count += len(to_add)
                changed = True

        # Merge detections (append new ones, dedup by type+url)
        new_detections = data.get("detections", [])
        if new_detections:
            existing_dets = set()
            for d in (fm.get("detections", []) or []):
                # Create a unique key: type + url_or_description
                key = (d.get("type", ""), d.get("url", ""), d.get("description", ""))
                existing_dets.add(key)
            to_add = []
            for d in new_detections:
                key = (d["type"], d.get("url", ""), d.get("description", ""))
                if key not in existing_dets:
                    to_add.append(d)
                    existing_dets.add(key)
            if to_add:
                existing_list = list(fm.get("detections", []) or [])
                fm["detections"] = existing_list + to_add
                detection_count += len(to_add)
                changed = True

        if not changed:
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

    print(f"LOLBAS merge: enriched {merged_count} tool files")
    print(f"  mitre_ids:   {mitre_count} values injected")
    print(f"  techniques:  {tech_count} values injected")
    print(f"  examples:    {example_count} values injected")
    print(f"  detections:  {detection_count} values injected")


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    extracted = extract_all()
    OUTPUT_PATH.write_text(json.dumps(extracted, indent=2))

    print(f"LOLBAS extraction: {len(extracted)} tools matched")
    for tid, data in sorted(extracted.items()):
        mids = ",".join(data.get("mitre_ids", []))
        dets = len(data.get("detections", []))
        exs = len(data.get("examples", []))
        techs = ",".join(data.get("techniques", []))
        print(f"  {tid:<35} mids=[{mids}]  techs=[{techs}]  dets={dets}  exs={exs}")

    merge_into_tools(extracted)


if __name__ == "__main__":
    main()
