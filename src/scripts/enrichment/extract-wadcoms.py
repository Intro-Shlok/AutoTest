"""
Extract items, services, attack_types from WADComs into AutoTest tool files.

WADComs format: Jekyll markdown with YAML frontmatter covering AD tools.
We map overlapping tools (primarily nmap) and merge the structured metadata.

Usage:
  python3 src/scripts/enrichment/extract-wadcoms.py
"""
import json
from io import StringIO
from pathlib import Path

import yaml as pyyaml
from ruamel.yaml import YAML

yaml = YAML()
yaml.preserve_quotes = True
yaml.indent(mapping=2, sequence=4, offset=2)

WADCOMS_DIR = Path("Database/WADComs.github.io/_wadcoms")
TOOLS_DIR = Path("src/content/tools")
OUTPUT_PATH = Path("data/enrichment/wadcoms-matches.json")

# Map WADComs filename (without .md) -> our tool id
FILENAME_TO_TOOL_ID = {
    "nmap": "security-recon-nmap",
    "Nmap-Krb5-Enum-Users": "security-recon-nmap",
}

# Map WADComs items -> our items enum
ITEM_MAP = {
    "Username": "Username",
    "Password": "Password",
    "Hash": "Hash",
    "TGS": "TGS",
    "TGT": "TGT",
    "PFX": "PFX",
    "Shell": "Shell",
    "No_Creds": "NoCreds",
    "NoCreds": "NoCreds",
}

# Map WADComs services -> our services enum
SERVICE_MAP = {
    "SMB": "SMB",
    "WMI": "WMI",
    "DCOM": "DCOM",
    "Kerberos": "Kerberos",
    "RPC": "RPC",
    "LDAP": "LDAP",
    "NTLM": "NTLM",
    "DNS": "DNS",
}

# Map WADComs attack_types -> our attack_types enum
ATTACK_TYPE_MAP = {
    "Enumeration": "Enumeration",
    "Exploitation": "Exploitation",
    "Persistence": "Persistence",
    "PrivEsc": "PrivilegeEscalation",
    "PrivilegeEscalation": "PrivilegeEscalation",
    "CredentialAccess": "CredentialAccess",
    "DefenseEvasion": "DefenseEvasion",
    "Discovery": "Discovery",
    "LateralMovement": "LateralMovement",
    "Collection": "Collection",
}

# Valid enums for validation
VALID_ITEMS = {"Username", "Password", "Hash", "TGS", "TGT", "PFX", "Shell", "NoCreds"}
VALID_SERVICES = {"SMB", "WMI", "DCOM", "Kerberos", "RPC", "LDAP", "NTLM", "DNS"}
VALID_ATTACK_TYPES = {"Enumeration", "Exploitation", "Persistence", "PrivilegeEscalation", "DefenseEvasion", "CredentialAccess", "Discovery", "LateralMovement", "Collection"}


def extract_all() -> dict:
    """Return {tool_id: {items, services, attack_types, examples}} from WADComs."""
    results: dict = {}
    for f in sorted(WADCOMS_DIR.glob("*.md")):
        stem = f.stem
        tool_id = FILENAME_TO_TOOL_ID.get(stem)
        if not tool_id:
            continue

        raw = f.read_text()
        parts = raw.split("---", 2)
        if len(parts) < 3:
            continue
        fm = pyyaml.safe_load(parts[1])
        if not fm:
            continue

        if tool_id not in results:
            results[tool_id] = {"items": set(), "services": set(), "attack_types": set(), "examples": []}

        # Map items
        for item in fm.get("items", []):
            mapped = ITEM_MAP.get(item)
            if mapped:
                results[tool_id]["items"].add(mapped)

        # Map services
        for svc in fm.get("services", []):
            mapped = SERVICE_MAP.get(svc)
            if mapped:
                results[tool_id]["services"].add(mapped)

        # Map attack_types
        for at in fm.get("attack_types", []):
            mapped = ATTACK_TYPE_MAP.get(at)
            if mapped:
                results[tool_id]["attack_types"].add(mapped)

        # Extract example command if not already present
        command = fm.get("command", "").strip()
        if command:
            description = fm.get("description", "").strip()
            # Take first sentence of description for example label
            first_sentence = description.split(".")[0].strip() if description else f"WADComs: {stem}"
            results[tool_id]["examples"].append({
                "description": first_sentence,
                "command": command,
            })

    # Convert sets to sorted lists
    output = {}
    for tid, data in results.items():
        entry = {}
        if data["items"]:
            entry["items"] = sorted(data["items"])
        if data["services"]:
            entry["services"] = sorted(data["services"])
        if data["attack_types"]:
            entry["attack_types"] = sorted(data["attack_types"])
        if data["examples"]:
            entry["examples"] = data["examples"]
        if entry:
            output[tid] = entry

    return output


def merge_into_tools(extracted: dict):
    """Merge WADComs data into tool .md files."""
    merged_count = 0
    item_count = 0
    svc_count = 0
    at_count = 0
    ex_count = 0

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

        # Merge items (set union)
        new_items = data.get("items", [])
        if new_items:
            existing = set(fm.get("items", []) or [])
            to_add = [v for v in new_items if v not in existing]
            if to_add:
                fm["items"] = list(existing) + to_add
                item_count += len(to_add)
                changed = True

        # Merge services (set union)
        new_svcs = data.get("services", [])
        if new_svcs:
            existing = set(fm.get("services", []) or [])
            to_add = [v for v in new_svcs if v not in existing]
            if to_add:
                fm["services"] = list(existing) + to_add
                svc_count += len(to_add)
                changed = True

        # Merge attack_types (set union)
        new_at = data.get("attack_types", [])
        if new_at:
            existing = set(fm.get("attack_types", []) or [])
            to_add = [v for v in new_at if v not in existing]
            if to_add:
                fm["attack_types"] = list(existing) + to_add
                at_count += len(to_add)
                changed = True

        # Merge examples (dedup by command)
        new_ex = data.get("examples", [])
        if new_ex:
            existing_cmds = {e["command"] for e in (fm.get("examples", []) or [])}
            to_add = [e for e in new_ex if e["command"] not in existing_cmds]
            if to_add:
                existing_list = list(fm.get("examples", []) or [])
                fm["examples"] = existing_list + to_add
                ex_count += len(to_add)
                changed = True

        if not changed:
            continue

        merged_count += 1

        body = "---\n"
        buf = StringIO()
        yaml.dump(fm, buf)
        body += buf.getvalue().strip()
        body += "\n---\n\n"
        body += parts[2].strip()
        if not body.endswith("\n"):
            body += "\n"
        f.write_text(body)

    print(f"WADComs merge: enriched {merged_count} tool files")
    print(f"  items:         {item_count} values injected")
    print(f"  services:      {svc_count} values injected")
    print(f"  attack_types:  {at_count} values injected")
    print(f"  examples:      {ex_count} values injected")


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    extracted = extract_all()
    OUTPUT_PATH.write_text(json.dumps(extracted, indent=2))

    print(f"WADComs extraction: {len(extracted)} tools matched")
    for tid, data in sorted(extracted.items()):
        items = ",".join(data.get("items", []))
        svcs = ",".join(data.get("services", []))
        ats = ",".join(data.get("attack_types", []))
        exs = len(data.get("examples", []))
        print(f"  {tid:<35} items=[{items}]  svcs=[{svcs}]  ats=[{ats}]  exs={exs}")

    merge_into_tools(extracted)


if __name__ == "__main__":
    main()
