"""
Extract command examples from cheat.sheets into AutoTest tool files.

cheat.sheets format: flat text files with # comments + command pairs.
Each file is a single tool's cheat sheet, no YAML frontmatter.

Usage:
  python3 src/scripts/enrichment/extract-cheatsheets.py
"""
import json
from io import StringIO
from pathlib import Path

from ruamel.yaml import YAML

yaml = YAML()
yaml.preserve_quotes = True
yaml.indent(mapping=2, sequence=4, offset=2)

CHEATSHEETS_DIR = Path("Database/cheat.sheets/sheets")
TOOLS_DIR = Path("src/content/tools")
OUTPUT_PATH = Path("data/enrichment/cheatsheets-matches.json")

SHEET_TO_TOOL_ID = {
    "awk": "text-process-awk",
    "bash": "system-shell-bash",
    "cat": "system-file-cat",
    "chmod": "system-file-chmod",
    "curl": "network-http-curl",
    "dd": "system-file-dd",
    "df": "system-storage-df",
    "dig": "network-dns-dig",
    "du": "system-storage-du",
    "find": "system-file-find",
    "git": "dev-vcs-git",
    "hexdump": "system-file-hexdump",
    "ifconfig": "network-config-ifconfig",
    "ip": "network-config-ip",
    "jq": "text-process-jq",
    "mount": "system-storage-mount",
    "nc": "network-socket-nc",
    "netcat": "network-socket-nc",
    "nmap": "security-recon-nmap",
    "ping": "network-diagnostic-ping",
    "route": "network-config-route",
    "scp": "network-transfer-scp",
    "sed": "text-process-sed",
    "sort": "system-file-sort",
    "ssh": "network-remote-ssh",
    "stat": "system-file-stat",
    "systemctl": "system-service-systemctl",
    "tar": "system-archive-tar",
    "tcpdump": "network-capture-tcpdump",
    "tee": "system-io-tee",
    "telnet": "network-remote-telnet",
    "tmux": "system-terminal-tmux",
    "traceroute": "network-diagnostic-traceroute",
    "wget": "network-http-wget",
    "whois": "security-intel-whois",
    "xargs": "system-file-xargs",
}


def parse_cheatsheet(path: Path) -> list[dict]:
    """Parse a cheat.sheets file into list of {description, command} dicts."""
    lines = path.read_text().splitlines()
    examples: list[dict] = []
    comment_lines: list[str] = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#"):
            text = stripped.lstrip("#").strip()
            if text:
                comment_lines.append(text)
        elif stripped and not stripped.startswith("#"):
            desc = " ".join(comment_lines) if comment_lines else f"cheat.sheets: {path.name}"
            examples.append({"description": desc, "command": stripped})
            comment_lines = []
        else:
            comment_lines = []

    return examples


def extract_all() -> dict:
    """Return {tool_id: {examples: [...]}} from cheat.sheets."""
    results: dict = {}

    for f in sorted(CHEATSHEETS_DIR.iterdir()):
        if not f.is_file() or f.name.startswith("_") or f.name in ("_info.yaml",):
            continue
        tool_id = SHEET_TO_TOOL_ID.get(f.name)
        if not tool_id:
            continue

        examples = parse_cheatsheet(f)
        if examples:
            if tool_id not in results:
                results[tool_id] = {"examples": []}
            results[tool_id]["examples"].extend(examples)

    return results


def merge_into_tools(extracted: dict):
    """Merge cheat.sheets examples into tool .md files via ruamel.yaml."""
    merged_count = 0
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
        new_ex = data.get("examples", [])
        if not new_ex:
            continue

        existing_cmds = {e["command"] for e in (fm.get("examples", []) or [])}
        to_add = [e for e in new_ex if e["command"] not in existing_cmds]
        if not to_add:
            continue

        existing_list = list(fm.get("examples", []) or [])
        fm["examples"] = existing_list + to_add
        ex_count += len(to_add)
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

    print(f"cheat.sheets merge: enriched {merged_count} tool files")
    print(f"  examples:  {ex_count} values injected")


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    extracted = extract_all()
    OUTPUT_PATH.write_text(json.dumps(extracted, indent=2))

    print(f"cheat.sheets extraction: {len(extracted)} tools matched")
    for tid, data in sorted(extracted.items()):
        print(f"  {tid:<35} examples={len(data['examples'])}")

    merge_into_tools(extracted)


if __name__ == "__main__":
    main()
