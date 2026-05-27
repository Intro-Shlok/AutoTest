"""
Parse --help output text files into structured parameter definitions.

Instead of regex-based line matching, uses whitespace-gap heuristic:
- Find the first wide gap (3+ spaces) after a flag-like prefix
- Left side = flags, right side = description
- Parse flags for short (-s) and long (--long) variants
"""

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
HELP_DIR = REPO_ROOT / "data" / "help_texts"
OUT_DIR = REPO_ROOT / "data" / "parsed_params"

INVALID_FLAG = re.compile(r"invalid option|unknown option|unrecognized|error while", re.IGNORECASE)
DEFAULT_RE = re.compile(r"(?:\(default:\s*([^)]+)\)|\[default:\s*([^\]]+)\]|default:\s+([^.\n]+?)(?:\.|,|;|$))", re.IGNORECASE)

# Flag pattern: starts with - or --, handles various formats
# Long: --flag, --flag=ARG, --flag <arg>, --flag ARG
# Short: -s, -s/other (nmap style like -sS/sT/sA)
FLAG_TOKENS = re.compile(
    r"(--[a-zA-Z0-9][a-zA-Z0-9_-]*(?:[= ]<[^>;]+>|[= ]\[[^\]]+\]|[= ][A-Z_]+)?)"  # long
    r"|"
    r"(-[a-zA-Z0-9?](?:/[a-zA-Z0-9?]+)*)"  # short with optional / aliases
)

# Enum extraction
ENUM_END_RE = re.compile(r"\(([^)]+)\)\s*$")
ENUM_BRACE_RE = re.compile(r"\{([^}]+)\}")


def infer_type(arg_text: str | None, desc: str) -> str:
    if arg_text:
        a = re.sub(r"[<>\[\]{}]", "", arg_text).upper().strip()
        if a in ("N", "NUM", "NUMERIC", "COUNT", "SIZE", "PORT", "PORTS", "NUMBER", "INT", "INTEGER", "LEVEL", "TIMES", "BYTES", "KB", "MB", "GB", "SECONDS", "MSEC", "MAX", "MIN", "LIMIT", "DEPTH", "WIDTH", "HEIGHT", "COLUMNS", "ROWS", "ITERATIONS", "WORKERS", "THREADS", "CONNECTIONS", "RETRIES", "RANGE"):
            return "integer"
        if a in ("FLOAT", "TIME", "DELAY", "INTERVAL", "TIMEOUT_SECONDS", "RATE", "THRESHOLD", "PROBABILITY"):
            return "number"
        if a in ("URL", "URI", "URLS"):
            return "url"
        if a in ("FILE", "DIR", "DIRECTORY", "PATH", "OUTFILE", "INFILE", "INPUT", "OUTPUT", "LOG", "LOGFILE", "CACHE", "CACHE_FILE", "CAFILE", "KEY_FILE", "CERT_FILE", "CONFIG", "CONFIG_FILE", "RC_FILE", "PATTERN_FILE", "EXCLUDE_FILE", "INCLUDE_FILE"):
            return "file"
        if a in ("LIST", "ARRAY", "VALUES", "ITEMS"):
            return "array"
    d = desc.lower()
    if re.search(r"port\s+number|numeric|integer|number\s+of", d):
        return "integer"
    if re.search(r"url\s|uri\s|http", d):
        return "url"
    if re.search(r"file\s+path|directory|filename|path\s+to|file\s+to|output\s+file|input\s+file", d):
        return "file"
    if re.search(r"comma.separated|list of|one or more|space.separated|delimited", d):
        return "array"
    if re.search(r"seconds?|milliseconds?|timeout|interval", d) and not re.search(r"string", d):
        return "number"
    return "string"


def extract_enum(desc: str) -> list[str] | None:
    # {a|b|c} syntax
    m = ENUM_BRACE_RE.search(desc)
    if m:
        parts = [p.strip() for p in m.group(1).split("|") if p.strip()]
        if parts:
            return parts
    # Trailing parens: "(a, b, c)" at end of description
    m = ENUM_END_RE.search(desc.rstrip())
    if m:
        content = m.group(1)
        candidates = [p.strip() for p in re.split(r"[,|/]", content) if p.strip()]
        if len(candidates) >= 2:
            if not any(kw in content.lower() for kw in ["default", "deprecated", "e.g.", "i.e.", "see also", "or more"]):
                return [c for c in candidates if not re.match(r"^(and|or|for|the|of|to|in|with|by)$", c, re.I)]
    return None


def extract_default(desc: str) -> str | None:
    m = DEFAULT_RE.search(desc)
    if m:
        return (m.group(1) or m.group(2) or m.group(3)).strip().rstrip(".)],;")
    return None


def make_param_name(longs: list[str], shorts: list[str], desc: str) -> str:
    if longs:
        raw = longs[0].lstrip("-")
        # Strip <arg> or [arg] suffixes (handles nested brackets)
        raw = re.sub(r"\s*[<\[].*$", "", raw).strip()
        # Replace underscores and spaces with hyphens
        name = raw.replace("_", "-")
        # Remove trailing digits that look like dedup artifacts
        name = re.sub(r"-\d+$", "", name)
        if name and not name[0].isdigit():
            return name
    if shorts:
        return f"flag-{shorts[0].lstrip('-')}"
    words = desc.split()
    if words:
        return words[0].lower().strip(".,:;").replace("_", "-")
    return "unknown"


def split_flags_desc(line: str) -> tuple[str, str] | None:
    """Split an indented line into (flags_block, description) using gap heuristic.

    Finds the first gap of 3+ spaces or a tab that appears after a flag-like prefix.
    """
    stripped = line.strip()
    if not stripped:
        return None
    
    if not (stripped.startswith("-") or stripped.startswith("--")):
        return None

    # Normalize tabs to spaces for consistent splitting
    normalized = line.replace("\t", "    ")

    # Find wide gaps (3+ spaces) in the normalized line
    for m in re.finditer(r"  {3,}", normalized):
        gap_start = m.start()
        prefix = normalized[:gap_start].strip()
        suffix = normalized[m.end():].strip()
        if prefix.startswith("-") or prefix.startswith("--"):
            return prefix, suffix

    # Try 2-space gap as fallback
    for m in re.finditer(r"  {2,}", normalized):
        gap_start = m.start()
        prefix = normalized[:gap_start].strip()
        suffix = normalized[m.end():].strip()
        if prefix.startswith("-") or prefix.startswith("--"):
            return prefix, suffix

    # Try tab-split as another fallback (for tools that use tabs)
    if "\t" in line:
        parts = line.split("\t")
        if len(parts) >= 2:
            prefix = parts[0].strip()
            suffix = "\t".join(parts[1:]).strip()
            if prefix.startswith("-") or prefix.startswith("--"):
                return prefix, suffix

    # Colon-separated: -sS/sT: Description (nmap style)
    colon_match = re.match(r"^(\s*(?:-[a-zA-Z0-9?][a-zA-Z0-9?/.,\[\]<>]*(?:\s*,\s*|\s+)?)+):\s*(.*)", stripped)
    if colon_match:
        prefix = colon_match.group(1).strip().rstrip(":")
        suffix = colon_match.group(2).strip()
        if prefix.startswith("-") or re.match(r"[A-Z][a-z]", prefix):
            return prefix, suffix

    return None


def parse_help_file(tool: str) -> list[dict]:
    path = HELP_DIR / f"{tool}.txt"
    if not path.exists():
        return []
    text = path.read_text()
    # Strip ANSI escape sequences (common in GNU coreutils help texts)
    text = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', text)
    text = re.sub(r'\x1b\][0-9;]*\x1b\\', '', text)  # OSC sequences (hyperlinks)
    text = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', text)
    text = text.replace('\x1b\\', '').replace('\x1b]', '')
    lines = text.split("\n")

    params = []
    seen_names = set()
    i = 0
    while i < len(lines):
        original = lines[i].rstrip()
        if not original.strip():
            i += 1
            continue

        # Try to split into flags and description
        split = split_flags_desc(original)
        flags_block = None
        desc_raw = ""
        if split:
            flags_block, desc_raw = split
            # Skip section header-like lines
            if len(flags_block) < 4 and flags_block.isupper():
                i += 1
                continue
        else:
            # Check if this is a flag-only line (starts with - or -- with no inline description)
            # Format like "  -c, --changes" with description on next line
            stripped_check = original.strip()
            if stripped_check.startswith("-") and FLAG_TOKENS.search(stripped_check):
                flags_block = stripped_check
                desc_raw = ""
            else:
                i += 1
                continue

        if INVALID_FLAG.search(desc_raw):
            i += 1
            continue

        # Extract flags from the flags block
        shorts = []
        longs = []
        for fm in FLAG_TOKENS.finditer(flags_block):
            if fm.group(2):  # short flag: -s
                shorts.append(fm.group(2).lstrip("-"))
            else:  # long flag: --something
                long_full = fm.group(1)
                longs.append(long_full.split("=")[0])  # strip =ARG

        if not shorts and not longs:
            i += 1
            continue

        # Extract argument name from long flags with =ARG
        arg = None
        for fm in FLAG_TOKENS.finditer(flags_block):
            if fm.group(1) and "=" in fm.group(1):
                arg_part = fm.group(1).split("=", 1)[1]
                arg = arg_part.strip()
            elif fm.group(1) and " " in fm.group(1) and len(fm.group(1)) > 20:
                pass

        if not arg and longs:
            long_full = [fm.group(1) for fm in FLAG_TOKENS.finditer(flags_block) if fm.group(1)]
            if long_full:
                for lf in long_full:
                    la = re.search(r" ([A-Z_]+|<[^>]+>|\[[^\]]+\])$", lf)
                    if la:
                        arg = la.group(1)

        desc = desc_raw.strip()
        # If description is empty/short, collect continuation lines
        if not desc or len(desc) < 3:
            desc_parts = []
            while i + 1 < len(lines):
                next_line = lines[i + 1].rstrip()
                # Next flagged line or section header ends continuation
                if not next_line or next_line.startswith("  -") or next_line.startswith("  --"):
                    break
                if next_line.startswith("     ") or next_line.startswith("\t"):
                    desc_parts.append(next_line.strip())
                    i += 1
                else:
                    break
            desc = " ".join(desc_parts).strip()

        # Name
        name = make_param_name(longs, shorts, desc)
        if name in seen_names:
            idx = 2
            alt_name = f"{name}-{idx}"
            while alt_name in seen_names:
                idx += 1
                alt_name = f"{name}-{idx}"
            name = alt_name

        param_type = infer_type(arg, desc)
        aliases = [f"-{s}" for s in shorts] + [f"--{l}" for l in longs]
        # Clean malformed aliases: ----flag → --flag, ---flag → --flag
        aliases = [re.sub(r"^-{3,}", "--", a) for a in aliases]
        enum_values = extract_enum(desc)
        default_val = extract_default(desc)

        # Clean description
        clean = desc
        clean = DEFAULT_RE.sub("", clean).strip()
        clean = re.sub(r"\s+", " ", clean).strip(".,; ")

        param = {
            "name": name,
            "template_key": re.sub(r"[^a-z0-9-]", "", name.lower().replace(" ", "-")).strip("-") or name,
            "type": param_type,
            "required": False,
            "default_value": default_val if param_type != "boolean" else None,
            "description": clean or desc[:200],
            "aliases": aliases if aliases else None,
        }
        if enum_values:
            ev_lower = {v.lower() for v in enum_values}
            if ev_lower <= {"true", "false", "yes", "no", "on", "off", "enabled", "disabled"}:
                param["type"] = "boolean"
                param["default_value"] = param.get("default_value")
            else:
                param["enum"] = enum_values

        seen_names.add(name)
        params.append(param)
        i += 1

    # Deduplicate
    seen_dedup: dict[str, dict] = {}
    for p in params:
        name = p["name"]
        if name not in seen_dedup:
            seen_dedup[name] = p
        else:
            existing = seen_dedup[name]
            e_score = sum(1 for v in existing.values() if v not in (None, "", [], False))
            n_score = sum(1 for v in p.values() if v not in (None, "", [], False))
            if n_score > e_score:
                seen_dedup[name] = p

    return list(seen_dedup.values())


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    total = 0
    for help_file in sorted(HELP_DIR.glob("*.txt")):
        tool = help_file.stem
        params = parse_help_file(tool)
        out_path = OUT_DIR / f"{tool}.json"
        with open(out_path, "w") as f:
            json.dump(params, f, indent=2)
        print(f"  {tool:20s} {len(params):3d} parameters")
        total += len(params)
    count = len(list(HELP_DIR.glob("*.txt")))
    print(f"\n=== Summary: {count} tools, {total} total parameters ===")


if __name__ == "__main__":
    main()
