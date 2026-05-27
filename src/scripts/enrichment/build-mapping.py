"""
Build a mapping table between our 82 tools and entries in each Database repo.
Outputs data/enrichment/mapping.json
"""
import json
import os
import re
import yaml
from pathlib import Path

REPO_BASE = Path("Database")
ENRICHMENT_DIR = Path("data/enrichment")
TOOLS_DIR = Path("src/content/tools")

# Load our tool list
def load_our_tools():
    tools = {}
    for f in sorted(TOOLS_DIR.glob("*.md")):
        content = f.read_text()
        parts = content.split("---", 2)
        if len(parts) < 3:
            continue
        fm = yaml.safe_load(parts[1])
        if not fm:
            continue
        tools[fm["id"]] = {
            "id": fm["id"],
            "name": fm["name"],
            "namespace": fm.get("namespace", ""),
        }
    return tools


# --- LOLBAS ---
def scan_lolbas(tools):
    lolbas_dir = REPO_BASE / "LOLBAS" / "yml"
    matches = {}
    binary_to_id = {t["name"].lower(): tid for tid, t in tools.items()}

    for subdir in ["OSBinaries", "OSLibraries", "OSScripts", "OtherMSBinaries"]:
        d = lolbas_dir / subdir
        if not d.is_dir():
            continue
        for yf in d.glob("*.yml"):
            name_stem = yf.stem.lower()
            # Try exact name match
            if name_stem in binary_to_id:
                tid = binary_to_id[name_stem]
                with open(yf) as f:
                    data = yaml.safe_load(f)
                mitre_ids = set()
                contributor = data.get("Author", "")
                commands = data.get("Commands", []) or []
                for cmd in commands:
                    mid = cmd.get("MitreID", "")
                    if mid:
                        mitre_ids.add(mid)
                matches[tid] = {
                    "lolbas": {
                        "file": str(yf.relative_to(REPO_BASE)),
                        "mitre_ids": sorted(mitre_ids),
                        "contributor": contributor,
                        "category": data.get("Category", ""),
                    }
                }
    return matches


# --- GTFOArgs ---
def scan_gtfoargs(tools):
    gtfo_dir = REPO_BASE / "GTFOArgs.github.io" / "_gtfoargs"
    matches = {}
    name_to_id = {t["name"].lower(): tid for tid, t in tools.items()}

    for mdf in gtfo_dir.glob("*.md"):
        content = mdf.read_text()
        parts = content.split("---", 2)
        if len(parts) < 3:
            continue
        fm = yaml.safe_load(parts[1])
        if not fm:
            continue
        title = fm.get("title", "").lower()
        if title in name_to_id:
            tid = name_to_id[title]
            functions = fm.get("functions", {}) or {}
            features = list(functions.keys())
            # Build examples from function code
            examples = []
            for fname, finfo in functions.items():
                if isinstance(finfo, list):
                    for entry in finfo:
                        if isinstance(entry, dict) and entry.get("code"):
                            examples.append({
                                "description": entry.get("description", fname),
                                "command": entry["code"],
                            })
                elif isinstance(finfo, dict):
                    desc = finfo.get("description", fname)
                    code = finfo.get("code", "")
                    if code:
                        examples.append({"description": desc, "command": code})
            matches[tid] = {
                "gtfoargs": {
                    "file": str(mdf.relative_to(REPO_BASE)),
                    "features": features,
                    "examples": examples[:5],
                }
            }
    return matches


# --- WADComs ---
def scan_wadcoms(tools):
    wadcoms_dir = REPO_BASE / "WADComs.github.io" / "_wadcoms"
    matches = {}
    name_to_id = {t["name"].lower(): tid for tid, t in tools.items()}

    if not wadcoms_dir.is_dir():
        wadcoms_dir = REPO_BASE / "WADComs" / "_wadcoms"

    if wadcoms_dir.is_dir():
        for mdf in wadcoms_dir.glob("*.md"):
            content = mdf.read_text()
            parts = content.split("---", 2)
            if len(parts) < 3:
                continue
            fm = yaml.safe_load(parts[1])
            if not fm:
                continue
            desc = (fm.get("description", "") or "").lower()
            # Try matching tool name in description
            for tname, tid in name_to_id.items():
                if tname in desc:
                    matches.setdefault(tid, {})
                    matches[tid]["wadcoms"] = {
                        "file": str(mdf.relative_to(REPO_BASE)),
                        "items": fm.get("items", []),
                        "services": fm.get("services", []),
                        "attack_types": fm.get("attack_types", []),
                        "os": fm.get("OS", []),
                    }
                    break
    return matches


# --- NetRunners ---
def scan_netrunners(tools):
    nr_file = REPO_BASE / "NetRunners" / "src" / "data" / "commands.json"
    matches = {}
    name_to_id = {t["name"].lower(): tid for tid, t in tools.items()}

    if nr_file.exists():
        data = json.loads(nr_file.read_text())
        for category, phases in data.items():
            for phase, commands in phases.items():
                if not isinstance(commands, list):
                    continue
                for cmd_entry in commands:
                    if isinstance(cmd_entry, dict):
                        cmd_str = cmd_entry.get("command", "")
                    else:
                        cmd_str = str(cmd_entry)
                    cmd_str = cmd_str.lower()
                    for tname, tid in name_to_id.items():
                        if tname in cmd_str:
                            matches.setdefault(tid, {})
                            matches[tid].setdefault("netrunners", {})
                            matches[tid]["netrunners"].setdefault("phases", set()).add(phase)
                            matches[tid]["netrunners"]["category"] = category
    # Convert sets to lists
    for tid in matches:
        if "phases" in matches[tid].get("netrunners", {}):
            matches[tid]["netrunners"]["phases"] = sorted(matches[tid]["netrunners"]["phases"])
    return matches


# --- LOOBins (macOS) ---
def scan_loobins(tools):
    loobins_dir = REPO_BASE / "LOOBins" / "LOOBins"
    matches = {}
    name_to_id = {t["name"].lower(): tid for tid, t in tools.items()}

    if loobins_dir.is_dir():
        for yf in loobins_dir.glob("*.yaml"):
            with open(yf) as f:
                data = yaml.safe_load(f)
            if not data:
                continue
            bname = data.get("name", "").lower()
            if bname in name_to_id:
                tid = name_to_id[bname]
                tactics = set()
                use_cases = data.get("example_use_cases", []) or []
                for uc in use_cases:
                    for t in (uc.get("tactics", []) or []):
                        tactics.add(t)
                matches[tid] = {
                    "loobins": {
                        "file": str(yf.relative_to(REPO_BASE)),
                        "techniques": sorted(tactics),
                    }
                }
    return matches


# --- Reference cheat sheets ---
def scan_reference(tools):
    ref_dir = REPO_BASE / "reference" / "source" / "_posts"
    matches = {}
    name_to_id = {t["name"].lower(): tid for tid, t in tools.items()}

    if ref_dir.is_dir():
        for mdf in ref_dir.glob("*.md"):
            content = mdf.read_text()
            parts = content.split("---", 2)
            if len(parts) < 3:
                continue
            fm = yaml.safe_load(parts[1])
            if not fm:
                continue
            title = (fm.get("title", "") or "").lower()
            for tname, tid in name_to_id.items():
                if tname == title or tname in title or title in tname:
                    matches.setdefault(tid, {})
                    matches[tid].setdefault("reference", {})
                    matches[tid]["reference"]["file"] = str(mdf.relative_to(REPO_BASE))
                    matches[tid]["reference"]["title"] = fm.get("title", "")
                    # Extract code blocks as examples
                    body = parts[2]
                    code_blocks = re.findall(r'```(?:\w+)?\n(.*?)```', body, re.DOTALL)
                    examples = []
                    for cb in code_blocks[:5]:
                        lines = [l.strip() for l in cb.strip().split("\n") if l.strip()]
                        for line in lines[:3]:
                            if line.startswith(("[", "http", "#", "/*")):
                                continue
                            examples.append({"description": f"From {fm.get('title', '')}", "command": line})
                    if examples:
                        matches[tid]["reference"]["examples"] = examples[:5]
                    break
    return matches


def main():
    ENRICHMENT_DIR.mkdir(parents=True, exist_ok=True)

    tools = load_our_tools()
    print(f"Loaded {len(tools)} tools")

    all_matches = {}

    print("Scanning LOLBAS...")
    for tid, data in scan_lolbas(tools).items():
        all_matches.setdefault(tid, {}).update(data)

    print("Scanning GTFOArgs...")
    for tid, data in scan_gtfoargs(tools).items():
        all_matches.setdefault(tid, {}).update(data)

    print("Scanning WADComs...")
    for tid, data in scan_wadcoms(tools).items():
        all_matches.setdefault(tid, {}).update(data)

    print("Scanning NetRunners...")
    for tid, data in scan_netrunners(tools).items():
        all_matches.setdefault(tid, {}).update(data)

    print("Scanning LOOBins...")
    for tid, data in scan_loobins(tools).items():
        all_matches.setdefault(tid, {}).update(data)

    print("Scanning Reference...")
    for tid, data in scan_reference(tools).items():
        all_matches.setdefault(tid, {}).update(data)

    # Output
    output = {}
    for tid in sorted(all_matches):
        entry = tools.get(tid, {})
        output[tid] = {
            "name": entry.get("name", ""),
            "matches": all_matches[tid],
        }

    out_path = ENRICHMENT_DIR / "mapping.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nMatched {len(output)} tools across all repos")
    print(f"Mapping written to {out_path}")

    # Summary
    for tid, data in sorted(output.items()):
        repos = list(data["matches"].keys())
        extra = ""
        if "lolbas" in data["matches"]:
            mids = data["matches"]["lolbas"].get("mitre_ids", [])
            extra = f" (mitre_ids={mids})"
        print(f"  {tid:<30} matched: {repos}{extra}")


if __name__ == "__main__":
    main()
