"""
Production-grade RedTeaming-Tactics extractor.

Architecture:
  Phase 1 — DFS repository traversal (prune .git/, .gitbook/, etc.)
  Phase 2 — Dual MITRE ID extraction (filename regex primary, {% embed %} fallback)
  Phase 3 — State-machine lexer (track in_code_block across ``` and {% code %} boundaries)
  Phase 4 — Aho-Corasick multi-pattern search within code blocks only
  Phase 5 — Contextualization (directory→techniques, reconciliation table overlap)
  Phase 6 — Serialization (tool_id → {techniques, mitre_ids})

Usage:
  python3 src/scripts/enrichment/extract-redteaming.py
"""
import argparse
import json
import re
import sys
from pathlib import Path

import ahocorasick

REPO_BASE = Path("Database/RedTeaming-Tactics-and-Techniques")
TOOLS_DIR = Path("src/content/tools")
OUTPUT_PATH = Path("data/enrichment/redteaming-matches.json")
RECON_PATH = Path("data/enrichment/mitre-reconciliation.json")

# Directories to prune from traversal
PRUNE_DIRS = {".git", ".gitbook", "community", "node_modules", "theme", "assets", "images", "files", "lab", "miscellaneous-reversing-forensics"}

# Map RedTeaming directory names → our techniques enum
DIR_TO_TECHNIQUES = {
    "initial-access": ["execution"],
    "code-execution": ["execution"],
    "code-injection-process-injection": ["process-manip", "execution"],
    "credential-access-and-credential-dumping": ["credential-access"],
    "defense-evasion": ["defense-evasion"],
    "enumeration-and-discovery": ["enumeration", "discovery"],
    "exfiltration": ["exfiltration"],
    "lateral-movement": ["lateral-movement"],
    "persistence": ["persistence"],
    "privilege-escalation": ["privilege-escalation"],
    "red-team-infrastructure": ["command-and-control"],
    "t1055-process-injection": ["process-manip"],
    "active-directory-kerberos-abuse": ["credential-access", "privilege-escalation"],
    "windows-services-abuse": ["privilege-escalation", "persistence"],
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

# Common English words to exclude from tool matching
COMMON_WORDS = {
    "file", "sort", "tr", "wc", "comm", "head", "cut", "cp", "mv",
    "dd", "od", "tee", "nice", "free", "top", "ps", "kill", "less",
    "cat", "ip", "df", "du", "ln", "rm", "tr", "stat", "watch",
    "timeout", "patch", "diff", "tail", "find", "xargs",
}


class ToolMatcher:
    """Aho-Corasick automaton for multi-pattern tool name matching."""

    def __init__(self, tool_names: dict[str, str]):
        self.automaton = ahocorasick.Automaton(key_type=ahocorasick.KEY_STRING, store_type=ahocorasick.STORE_ANY)
        self.tool_names = tool_names  # {lowercase_name: tool_id}

        for name, tid in tool_names.items():
            # Add both bare name and .exe variant
            self.automaton.add_word(name.lower(), (name.lower(), tid))
            if not name.lower().endswith(".exe"):
                self.automaton.add_word(name.lower() + ".exe", (name.lower(), tid))

        self.automaton.make_automaton()

    def search(self, text: str) -> set[str]:
        """Return set of tool_ids found in text using Aho-Corasick."""
        found = set()
        text_lower = text.lower()
        for end_idx, (matched_name, tid) in self.automaton.iter(text_lower):
            # Check word boundary: character before and after must not be alphanumeric
            start = end_idx - len(matched_name) + 1
            before = text_lower[start - 1] if start > 0 else " "
            after = text_lower[end_idx + 1] if end_idx + 1 < len(text_lower) else " "
            if not before.isalnum() and not after.isalnum() and before != "_":
                if matched_name not in COMMON_WORDS:
                    found.add(tid)
        return found


class StateMachineLexer:
    """
    State-machine lexer for GitBook Markdown.

    Tracks in_code_block across:
      - Standard fenced code blocks (```)
      - GitBook {% code %}...{% endcode %} tags
    Skips:
      - {% hint %}...{% endhint %}
      - {% file %} tags
    Fail-safe: reset on any markdown header (#, ##, ###)
    """

    def __init__(self, tool_matcher: ToolMatcher):
        self.matcher = tool_matcher
        self.in_code_block = False
        self.in_hint = False
        self.found_tools: set[str] = set()

        # Patterns
        self.code_open_re = re.compile(r"^(```)|({%\s*code\s)")
        self.code_close_re = re.compile(r"^(```)|({%\s*endcode\s*})")
        self.hint_open_re = re.compile(r"({%\s*hint\s)")
        self.hint_close_re = re.compile(r"({%\s*endhint\s*})")
        self.header_re = re.compile(r"^#{1,6}\s")
        self.embed_re = re.compile(r'{%\s*embed\s+url="(.*?)"\s*%}')

    def parse(self, text: str) -> set[str]:
        """Parse document text and return set of tool_ids found in code blocks."""
        self.found_tools = set()
        self.in_code_block = False
        self.in_hint = False

        for line in text.split("\n"):
            stripped = line.strip()

            # Fail-safe: headers reset code block state
            if self.header_re.match(stripped):
                self.in_code_block = False
                continue

            # Hint block handling
            if self.hint_open_re.search(stripped):
                self.in_hint = True
                continue
            if self.hint_close_re.search(stripped):
                self.in_hint = False
                continue
            if self.in_hint:
                continue

            # Code block boundary detection
            if self.code_open_re.search(stripped):
                self.in_code_block = True
                continue
            if self.code_close_re.search(stripped):
                self.in_code_block = False
                continue

            # Extract MITRE embed URLs regardless of code block state
            # (handled separately)

            # Only search within code blocks
            if self.in_code_block:
                matched = self.matcher.search(stripped)
                self.found_tools.update(matched)

        return self.found_tools


def extract_mitre_ids_from_filename(filename: str) -> list[str]:
    """Primary heuristic: extract T-code from filename prefix."""
    m = re.search(r"(?i)^t(\d{4}(?:\.\d{3})?)", filename)
    if m:
        return ["T" + m.group(1)]
    return []


def extract_mitre_ids_from_embeds(text: str) -> list[str]:
    """Secondary heuristic: extract T-code from {% embed %} tags."""
    ids = []
    for m in re.finditer(r'{%\s*embed\s+url="[^"]*/T(\d{4}(?:\.\d{3})?)\s*"', text, re.IGNORECASE):
        ids.append("T" + m.group(1))
    return ids


def load_reconciliation_table() -> dict:
    """Load T-code → [techniques] mapping for tactic overlap resolution."""
    if RECON_PATH.exists():
        return json.loads(RECON_PATH.read_text())
    return {}


def load_tool_names(tools_dir: Path) -> dict[str, str]:
    """Return {lowercase_name: tool_id} for all our tools."""
    import yaml
    mapping = {}
    for f in sorted(tools_dir.glob("*.md")):
        content = f.read_text()
        parts = content.split("---", 2)
        if len(parts) < 3:
            continue
        fm = yaml.safe_load(parts[1])
        if fm:
            name = fm.get("name", "").lower().strip()
            tid = fm.get("id", "")
            if name and tid:
                mapping[name] = tid
    return mapping


def scan_repository(
    repo_base: Path,
    tool_matcher: ToolMatcher,
    lexer: StateMachineLexer,
    recon_table: dict,
) -> dict:
    """DFS traversal of repository, returning {tool_id: {techniques, mitre_ids}}."""
    results: dict[str, dict] = {}

    if not repo_base.is_dir():
        print(f"Repo not found: {repo_base}")
        return results

    # Walk offensive-security/ and offensive-security-experiments/
    search_dirs = ["offensive-security", "offensive-security-experiments"]
    for search_name in search_dirs:
        search_dir = repo_base / search_name
        if not search_dir.is_dir():
            continue
        print(f"Traversing {search_dir.relative_to(repo_base)}...")

        for mdf in search_dir.rglob("*.md"):
            # Prune unwanted dirs
            if any(p.name in PRUNE_DIRS for p in mdf.relative_to(repo_base).parents):
                continue

            rel_path = mdf.relative_to(repo_base)
            parent_dir = mdf.parent.name.lower()

            # Extract MITRE IDs (dual heuristic)
            mitre_ids = extract_mitre_ids_from_filename(mdf.stem)
            text = mdf.read_text(errors="replace")
            if not mitre_ids:
                mitre_ids = extract_mitre_ids_from_embeds(text)

            # Validate mitre_ids against reconciliation table (filters out non-standard IDs)
            if mitre_ids:
                mitre_ids = [mid for mid in mitre_ids if mid in recon_table]

    # Derive techniques from parent directory
            techniques = DIR_TO_TECHNIQUES.get(parent_dir, [])

            # Extend techniques via reconciliation table if we have T-codes
            for tid_code in mitre_ids:
                parent = tid_code if "." not in tid_code else tid_code.rsplit(".", 1)[0]
                if tid_code in recon_table:
                    techniques.extend(recon_table[tid_code])
                elif parent in recon_table:
                    techniques.extend(recon_table[parent])

            # Deduplicate techniques
            techniques = list(dict.fromkeys(t for t in techniques if t in VALID_TECHNIQUES))

            # Skip if no techniques and we're not in a mapped directory
            if not techniques and parent_dir not in DIR_TO_TECHNIQUES:
                continue

            # Scan code blocks for tool names using state-machine lexer
            found_tools = lexer.parse(text)
            if not found_tools:
                continue

            # Accumulate results per tool
            for tool_id in found_tools:
                if tool_id not in results:
                    results[tool_id] = {"techniques": set(), "mitre_ids": set()}
                results[tool_id]["techniques"].update(techniques)
                results[tool_id]["mitre_ids"].update(mitre_ids)

    # Convert sets to sorted lists
    output = {}
    for tid in sorted(results):
        techs = sorted(results[tid]["techniques"])
        mids = sorted(results[tid]["mitre_ids"], key=lambda x: (x.split(".")[0].lstrip("T"), x))
        if techs or mids:
            output[tid] = {}
            if techs:
                output[tid]["techniques"] = techs
            if mids:
                output[tid]["mitre_ids"] = mids

    return output


def main():
    parser = argparse.ArgumentParser(description="Extract tools and MITRE IDs from RedTeaming-Tactics repo")
    parser.add_argument("--repo", type=str, default=str(REPO_BASE),
                        help=f"Path to RedTeaming repo (default: {REPO_BASE})")
    args = parser.parse_args()

    repo_path = Path(args.repo)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Load tool names
    tool_names = load_tool_names(TOOLS_DIR)
    print(f"Loaded {len(tool_names)} tool names")

    # Build Aho-Corasick automaton
    matcher = ToolMatcher(tool_names)
    print(f"Built Aho-Corasick automaton with {len(tool_names)} patterns")

    # Build state-machine lexer
    lexer = StateMachineLexer(matcher)

    # Load reconciliation table
    recon_table = load_reconciliation_table()
    print(f"Loaded reconciliation table: {len(recon_table)} T-codes")

    # Scan repository
    results = scan_repository(repo_path, matcher, lexer, recon_table)

    # Write output
    with open(OUTPUT_PATH, "w") as f:
        json.dump(results, f, indent=2)

    # Summary
    techniques_count = sum(1 for v in results.values() if "techniques" in v)
    mitre_count = sum(1 for v in results.values() if "mitre_ids" in v)
    total_injections = sum(len(v.get("techniques", [])) + len(v.get("mitre_ids", [])) for v in results.values())

    print(f"\n— RedTeaming Extraction Complete —")
    print(f"  Tools matched:       {len(results)}")
    print(f"  With techniques:     {techniques_count}")
    print(f"  With mitre_ids:      {mitre_count}")
    print(f"  Total field values:  {total_injections}")

    for tid, data in sorted(results.items()):
        techs = ",".join(data.get("techniques", []))
        mids = ",".join(data.get("mitre_ids", []))
        print(f"  {tid:<30} techs=[{techs}]  mitre=[{mids}]")


if __name__ == "__main__":
    main()
