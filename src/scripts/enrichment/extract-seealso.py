"""
Extract related_tools from cheat.sheets see_also/ into AutoTest tool files.

cheat.sheets see_also format: one tool per line, self-reference first.
We strip the self-reference and only inject tools that exist in our set.

Usage:
  python3 src/scripts/enrichment/extract-seealso.py
"""
import json
from io import StringIO
from pathlib import Path

from ruamel.yaml import YAML

yaml = YAML()
yaml.preserve_quotes = True
yaml.indent(mapping=2, sequence=4, offset=2)

SEEALSO_DIR = Path("Database/cheat.sheets/see_also")
TOOLS_DIR = Path("src/content/tools")
OUTPUT_PATH = Path("data/enrichment/seealso-matches.json")


def build_tool_name_to_id() -> dict[str, str]:
    """Build mapping from tool filename (without .md) -> tool id."""
    mapping = {}
    for f in TOOLS_DIR.glob("*.md"):
        content = f.read_text()
        parts = content.split("---", 2)
        if len(parts) < 3:
            continue
        fm = yaml.load(parts[1])
        if fm and "id" in fm and "name" in fm:
            mapping[fm["name"].lower()] = fm["id"]
            mapping[f.stem.lower()] = fm["id"]
    return mapping


def build_id_to_name() -> dict[str, str]:
    """Build mapping from tool id -> tool filename stem."""
    mapping = {}
    for f in TOOLS_DIR.glob("*.md"):
        content = f.read_text()
        parts = content.split("---", 2)
        if len(parts) < 3:
            continue
        fm = yaml.load(parts[1])
        if fm and "id" in fm:
            mapping[fm["id"]] = f.stem
    return mapping


def extract_all() -> dict:
    """Return {tool_id: [related_tool_ids]} from see_also/."""
    name_to_id = build_tool_name_to_id()
    results: dict = {}

    for f in sorted(SEEALSO_DIR.iterdir()):
        if not f.is_file() or f.name.startswith("."):
            continue

        sheet_name = f.name.lower()
        tool_id = name_to_id.get(sheet_name)
        if not tool_id:
            continue

        # Read references, skip self-reference
        refs = []
        lines = f.read_text().splitlines()
        for line in lines:
            line = line.strip().lower()
            if line and line != sheet_name:
                ref_id = name_to_id.get(line)
                if ref_id:
                    refs.append(ref_id)

        if refs:
            results[tool_id] = sorted(set(refs))

    return results


def merge_into_tools(extracted: dict):
    """Merge see_also references into tool .md files."""
    merged_count = 0
    ref_count = 0

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

        existing = set(fm.get("related_tools", []) or [])
        to_add = [r for r in extracted[tid] if r not in existing]
        if not to_add:
            continue

        fm["related_tools"] = list(existing) + to_add
        ref_count += len(to_add)
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

    print(f"see_also merge: enriched {merged_count} tool files")
    print(f"  related_tools: {ref_count} values injected")


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    extracted = extract_all()
    OUTPUT_PATH.write_text(json.dumps(extracted, indent=2))

    print(f"see_also extraction: {len(extracted)} tools matched")
    for tid, refs in sorted(extracted.items()):
        print(f"  {tid:<35} {len(refs)} related tools")
    print()

    merge_into_tools(extracted)


if __name__ == "__main__":
    main()
