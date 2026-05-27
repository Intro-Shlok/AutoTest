"""
Extract examples from NetRunners pentest toolkit into AutoTest tool files.

NetRunners format: JSON with commands organized by category/subcategory.
Commands have template variables like {{IP}}, {{USER}}, {{PASSWORD}}.

We map overlapping tools and merge commands as parameterized examples.

Usage:
  python3 src/scripts/enrichment/extract-netrunners.py
"""
import json
from io import StringIO
from pathlib import Path

from ruamel.yaml import YAML

yaml = YAML()
yaml.preserve_quotes = True
yaml.indent(mapping=2, sequence=4, offset=2)

NETRUNNERS_PATH = Path("Database/NetRunners/src/data/commands.json")
TOOLS_DIR = Path("src/content/tools")
OUTPUT_PATH = Path("data/enrichment/netrunners-matches.json")

# Map NetRunners tool name (first word of command) -> our tool id
TOOL_MAP = {
    "bash": "system-shell-bash",
    "find": "system-file-find",
    "ftp": "network-transfer-ftp",
    "grep": "text-search-grep",
    "nc": "network-socket-nc",
    "nc.exe": "network-socket-nc",
    "nmap": "security-recon-nmap",
    "python3": "dev-runtime-python3",
    "ssh": "network-remote-ssh",
    "wget": "network-http-wget",
}


def extract_all() -> dict:
    """Parse NetRunners commands.json and return {tool_id: {examples: [...]}}."""
    with open(NETRUNNERS_PATH) as f:
        data = json.load(f)

    results: dict = {}

    for category, subcats in data.items():
        if not isinstance(subcats, dict):
            continue
        for subcategory, cmds in subcats.items():
            for cmd_str in cmds:
                cmd_str = cmd_str.strip()
                if not cmd_str:
                    continue

                # Extract first word as tool name
                first_word = cmd_str.split()[0].lower() if cmd_str else ""
                # Handle paths like python3 /path/to/script.py
                if "/" in first_word:
                    first_word = first_word.rsplit("/", 1)[-1]

                tool_id = TOOL_MAP.get(first_word)
                if not tool_id:
                    continue

                description = f"NetRunners {category}/{subcategory}"

                if tool_id not in results:
                    results[tool_id] = {"examples": []}

                results[tool_id]["examples"].append({
                    "description": description,
                    "command": cmd_str,
                })

    return results


def merge_into_tools(extracted: dict):
    """Merge NetRunners examples into tool .md files."""
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

    print(f"NetRunners merge: enriched {merged_count} tool files")
    print(f"  examples:  {example_count} values injected")


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    extracted = extract_all()
    OUTPUT_PATH.write_text(json.dumps(extracted, indent=2))

    print(f"NetRunners extraction: {len(extracted)} tools matched")
    for tid, data in sorted(extracted.items()):
        exs = len(data["examples"])
        print(f"  {tid:<35}  examples={exs}")

    merge_into_tools(extracted)


if __name__ == "__main__":
    main()
