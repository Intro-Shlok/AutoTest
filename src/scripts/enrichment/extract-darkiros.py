"""
Extract examples from Darkiros pentest helper into AutoTest tool files.

Darkiros format: JS file with 'var data = [{...}]' JSON array.
We map overlapping tools and merge commands as new examples.

Usage:
  python3 src/scripts/enrichment/extract-darkiros.py
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

DARKIROS_PATH = Path("Database/Darkiros.github.io/assets/js/cheatSheet.js")
TOOLS_DIR = Path("src/content/tools")
OUTPUT_PATH = Path("data/enrichment/darkiros-matches.json")

# Map Darkiros tool name (lowercase) -> our tool id
TOOL_MAP = {
    "docker": "container-runtime-docker",
    "nmap": "security-recon-nmap",
    "sed": "text-process-sed",
    "socat": "network-socket-socat",
    "ssh": "network-remote-ssh",
}

# Partial matches: multi-word tool names where one word maps to our tool
PARTIAL_MAP = {
    "linux bash": "system-shell-bash",
    "grep hash": "text-search-grep",
    "others grep": "text-search-grep",
}


def parse_entries() -> list[dict]:
    """Parse Darkiros JS file, returning list of {tool, category, information, command, link}."""
    raw = open(DARKIROS_PATH).read()

    # Extract from JS array using regex
    entries = []
    # Match complete objects: start with {, find balanced braces
    depth = 0
    start = -1
    i = raw.find('{')
    brace_count = 0
    obj_start = -1

    for i, ch in enumerate(raw):
        if ch == '{':
            if brace_count == 0:
                obj_start = i
            brace_count += 1
        elif ch == '}':
            brace_count -= 1
            if brace_count == 0 and obj_start >= 0:
                obj_str = raw[obj_start:i+1]
                obj_start = -1
                # Parse manually with regex (safer than JSON)
                tool = re.search(r'\"tool\":\s*\"([^\"]+)\"', obj_str)
                category = re.search(r'\"category\":\s*\"([^\"]+)\"', obj_str)
                info = re.search(r'\"information\":\s*\"([^\"]+)\"', obj_str)
                cmd = re.search(r'\"command\":\s*\"((?:[^\"\\]|\\.)*)\"', obj_str)
                link = re.search(r'\"link\":\s*\"([^\"]+)\"', obj_str)
                if tool and cmd:
                    entry = {
                        "tool": tool.group(1),
                        "category": category.group(1) if category else "",
                        "information": info.group(1) if info else "",
                        "command": cmd.group(1).replace('\\"', '"').replace('\\n', '\n'),
                        "link": link.group(1) if link else "",
                    }
                    entries.append(entry)
    return entries


def extract_all(entries: list[dict]) -> dict:
    """Return {tool_id: {examples: [...]}} from Darkiros entries."""
    results: dict = {}

    for entry in entries:
        tool_name = entry["tool"].strip().lower()
        command = entry["command"].strip()
        description = entry["information"].strip() or f"Darkiros: {entry['tool']}"

        # Map to our tool id
        tool_id = TOOL_MAP.get(tool_name)
        if not tool_id:
            tool_id = PARTIAL_MAP.get(tool_name)
        if not tool_id:
            continue

        if tool_id not in results:
            results[tool_id] = {"examples": []}

        results[tool_id]["examples"].append({
            "description": f"Darkiros {entry['category']}: {description}",
            "command": command,
        })

    return results


def merge_into_tools(extracted: dict):
    """Merge Darkiros examples into tool .md files."""
    merged_count = 0
    example_count = 0

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

        new_examples = extracted[tid].get("examples", [])
        if not new_examples:
            continue

        existing_cmds = {e["command"] for e in (fm.get("examples", []) or [])}
        to_add = [e for e in new_examples if e["command"] not in existing_cmds]
        if not to_add:
            continue

        existing_list = list(fm.get("examples", []) or [])
        fm["examples"] = existing_list + to_add
        example_count += len(to_add)
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

    print(f"Darkiros merge: enriched {merged_count} tool files")
    print(f"  examples:  {example_count} values injected")


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    entries = parse_entries()
    print(f"Darkiros extraction: parsed {len(entries)} entries")

    extracted = extract_all(entries)
    OUTPUT_PATH.write_text(json.dumps(extracted, indent=2))

    print(f"  tools matched: {len(extracted)}")
    for tid, data in sorted(extracted.items()):
        exs = len(data["examples"])
        print(f"    {tid:<35}  examples={exs}")

    merge_into_tools(extracted)


if __name__ == "__main__":
    main()
