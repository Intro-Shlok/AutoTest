"""
Extract examples + capabilities + injection parameters from GTFOArgs.

GTFOArgs format: Jekyll markdown with YAML frontmatter.
  title: tool_name
  functions:
    shell|command|file-upload|file-download|file-read|file-write|sudo|suid:
      - description: text
        code: command snippet

Pass 1: code snippets → examples[] (existing)
Pass 2: function types → capabilities[] + techniques[] + features[] + parameters[]

Usage:
  python3 src/scripts/enrichment/extract-gtfoargs.py
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

GTFOARGS_DIR = Path("Database/GTFOArgs.github.io/_gtfoargs")
TOOLS_DIR = Path("src/content/tools")
OUTPUT_PATH = Path("data/enrichment/gtfoargs-matches.json")

# Map GTFOArgs title -> our tool id
TITLE_TO_TOOL_ID = {
    "awk": "text-process-awk",
    "curl": "network-http-curl",
    "dig": "network-dns-dig",
    "file": "system-file-file",
    "find": "system-file-find",
    "git": "dev-vcs-git",
    "make": "dev-build-make",
    "socat": "network-socket-socat",
    "ssh": "network-remote-ssh",
    "tar": "system-archive-tar",
    "wget": "network-http-wget",
}

# Map GTFOArgs function types -> our capabilities
FUNCTION_TO_CAPABILITIES = {
    "shell": ["security.privilege-escalation.shell"],
    "command": ["security.execution.command"],
    "file-read": ["system.file.read"],
    "file-write": ["system.file.write"],
    "file-upload": ["network.transfer.upload"],
    "file-download": ["network.transfer.download"],
    "sudo": ["security.privilege-escalation.sudo"],
    "suid": ["security.privilege-escalation.suid"],
    "non-interactive": ["security.execution.command"],
    "limited-suid": ["security.privilege-escalation.suid"],
}

# Map GTFOArgs function types -> our techniques
FUNCTION_TO_TECHNIQUES = {
    "shell": ["privilege-escalation"],
    "command": ["execution"],
    "file-read": ["collection"],
    "file-write": ["data-manipulation"],
    "file-upload": ["exfiltration"],
    "file-download": ["exfiltration"],
    "sudo": ["privilege-escalation"],
    "suid": ["privilege-escalation"],
}

# Map GTFOArgs function types -> our features
FUNCTION_TO_FEATURES = {
    "shell": ["process-manip"],
    "command": ["process-manip"],
    "file-read": ["file-system"],
    "file-write": ["file-system"],
    "sudo": ["requires-root"],
    "suid": ["file-system"],
}

# Injection flags to extract from code snippets (tool -> [(flag, description)])
# These are well-known GTFO abuse flags not currently in our parameters
INJECTION_FLAGS = {
    "tar": [
        ("checkpoint", "Execute command at checkpoint during archive creation (GTFO abuse)"),
        ("checkpoint-action", "Action to execute at checkpoint (e.g., exec=command)"),
        ("use-compress-program", "External compression program (abuse for shell/file-read)"),
        ("to-command", "Pipe extracted files to a command"),
        ("rsh-command", "Remote shell command for SSH-based archive transfer"),
        ("record-size", "Set record size for tape operations"),
        ("info-script", "Run script at volume rotation"),
        ("new-volume-script", "Alias for info-script"),
    ],
    "find": [
        ("exec", "Execute a command on each matched file"),
        ("ok", "Like -exec but prompts before each execution"),
        ("execdir", "Execute command from the directory of the matched file"),
        ("fprintf", "Print formatted output to a file"),
        ("perm", "Find files with specific permissions (e.g., /4000 for SUID)"),
        ("user", "Find files owned by a specific user"),
        ("mmin", "Find files modified N minutes ago"),
        ("size", "Find files of a specific size"),
    ],
    "awk": [
        ("exec-expression", "Execute shell command via system() or print|/bin/sh"),
        ("getline-variable", "Read file content into variable via getline < file"),
    ],
    "git": [
        ("worktree-add", "Add a worktree with a specific path"),
        ("config-path", "Set a config value pointing to a script path"),
       ("hooks-path", "Override hooks directory path"),
    ],
    "make": [
        ("eval-expression", "Evaluate arbitrary make expression via $(shell cmd)"),
        ("include-file", "Include an arbitrary file into the Makefile parse"),
    ],
}

# Human-readable labels for function types
FUNCTION_LABELS = {
    "shell": "Argument injection: spawn interactive shell",
    "command": "Argument injection: execute arbitrary command",
    "file-upload": "Argument injection: upload file",
    "file-download": "Argument injection: download file",
    "file-read": "Argument injection: read local file",
    "file-write": "Argument injection: write to local file",
    "sudo": "Argument injection: sudo privilege escalation",
    "suid": "Argument injection: SUID privilege escalation",
}


def extract_all() -> dict:
    """Return {tool_id: {examples, capabilities, techniques, features, parameters}}."""
    results: dict = {}
    for f in sorted(GTFOARGS_DIR.glob("*.md")):
        raw = f.read_text()
        parts = raw.split("---", 2)
        if len(parts) < 3:
            continue
        fm = pyyaml.safe_load(parts[1])
        if not fm:
            continue

        title = fm.get("title", "")
        if not title:
            continue

        tool_id = TITLE_TO_TOOL_ID.get(title.lower())
        if not tool_id:
            continue

        functions = fm.get("functions", {})
        examples = []
        seen_func_types = set()

        for func_type, entries in functions.items():
            seen_func_types.add(func_type)
            label = FUNCTION_LABELS.get(func_type, f"Argument injection: {func_type}")
            for entry in entries:
                desc = entry.get("description", "")
                code = entry.get("code", "").strip()
                if not code:
                    continue
                examples.append({
                    "description": f"{label}: {desc}",
                    "command": code,
                })

        # Derive capabilities from function types
        capabilities = set()
        techniques = set()
        features = set()
        for ft in seen_func_types:
            for cap in FUNCTION_TO_CAPABILITIES.get(ft, []):
                capabilities.add(cap)
            for tech in FUNCTION_TO_TECHNIQUES.get(ft, []):
                techniques.add(tech)
            for feat in FUNCTION_TO_FEATURES.get(ft, []):
                features.add(feat)

        # Derive injection parameters
        injection_params = INJECTION_FLAGS.get(title.lower(), [])

        entry = {}
        if examples:
            entry["examples"] = examples
        if capabilities:
            entry["capabilities"] = sorted(capabilities)
        if techniques:
            entry["techniques"] = sorted(techniques)
        if features:
            entry["features"] = sorted(features)
        if injection_params:
            entry["parameters"] = [
                {"name": name, "description": desc, "type": "string"}
                for name, desc in injection_params
            ]

        if entry:
            results[tool_id] = entry

    return results


def merge_into_tools(extracted: dict):
    """Merge GTFOArgs data into tool .md files."""
    merged_count = 0
    example_count = 0
    cap_count = 0
    tech_count = 0
    feat_count = 0
    param_count = 0

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

        # Merge examples
        new_examples = data.get("examples", [])
        if new_examples:
            existing_cmds = {e["command"] for e in (fm.get("examples", []) or [])}
            to_add = [e for e in new_examples if e["command"] not in existing_cmds]
            if to_add:
                existing = list(fm.get("examples", []) or [])
                fm["examples"] = existing + to_add
                example_count += len(to_add)
                changed = True

        # Merge capabilities
        new_caps = data.get("capabilities", [])
        if new_caps:
            existing = set(fm.get("capabilities", []) or [])
            to_add = [c for c in new_caps if c not in existing]
            if to_add:
                fm["capabilities"] = list(existing) + to_add
                cap_count += len(to_add)
                changed = True

        # Merge techniques
        new_techs = data.get("techniques", [])
        if new_techs:
            existing = set(fm.get("techniques", []) or [])
            to_add = [t for t in new_techs if t not in existing]
            if to_add:
                fm["techniques"] = list(existing) + to_add
                tech_count += len(to_add)
                changed = True

        # Merge features
        new_feats = data.get("features", [])
        if new_feats:
            existing = set(fm.get("features", []) or [])
            to_add = [f for f in new_feats if f not in existing]
            if to_add:
                fm["features"] = list(existing) + to_add
                feat_count += len(to_add)
                changed = True

        # Merge injection parameters (by name dedup)
        new_params = data.get("parameters", [])
        if new_params:
            existing_names = {p.get("name", "") for p in (fm.get("parameters", []) or [])}
            to_add = [p for p in new_params if p["name"] not in existing_names]
            if to_add:
                existing_list = list(fm.get("parameters", []) or [])
                fm["parameters"] = existing_list + to_add
                param_count += len(to_add)
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

    print(f"GTFOArgs merge: enriched {merged_count} tool files")
    print(f"  examples:    {example_count} values injected")
    print(f"  capabilities: {cap_count} values injected")
    print(f"  techniques:  {tech_count} values injected")
    print(f"  features:    {feat_count} values injected")
    print(f"  parameters:  {param_count} values injected")


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    extracted = extract_all()
    OUTPUT_PATH.write_text(json.dumps(extracted, indent=2))

    print(f"GTFOArgs extraction: {len(extracted)} tools matched")
    for tid, data in sorted(extracted.items()):
        parts = []
        if "examples" in data:
            parts.append(f"ex={len(data['examples'])}")
        if "capabilities" in data:
            parts.append(f"caps={len(data['capabilities'])}")
        if "techniques" in data:
            parts.append(f"techs={len(data['techniques'])}")
        if "features" in data:
            parts.append(f"feats={len(data['features'])}")
        if "parameters" in data:
            parts.append(f"params={len(data['parameters'])}")
        print(f"  {tid:<35}  {', '.join(parts)}")

    merge_into_tools(extracted)


if __name__ == "__main__":
    main()
