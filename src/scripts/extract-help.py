"""
Extract --help output from all installed CLI tools in the AutoTest repository.
Outputs raw help text to data/help_texts/<tool>.txt for downstream parsing.
"""

import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
HELP_DIR = REPO_ROOT / "data" / "help_texts"

# Order: try --help first, then -h, then -help, then help subcommand, then man
HELP_FLAGS = [
    ("--help", None),
    ("-h", None),
    ("-help", None),
    ("help", None),
    ("--help-all", None),
]

# For tools that need special handling
SPECIAL_HELP = {
    "openssl": ["openssl", "help"],
    "ip": ["ip", "help"],
    "kill": ["bash", "-c", "help kill"],
    "cron": ["man", "cron"],
    "ftp": ["man", "ftp"],
    "scp": ["man", "scp"],
    "sftp": ["man", "sftp"],
    "ssh": ["man", "ssh"],
    "tmux": ["man", "tmux"],
    "ps": ["ps", "--help", "all"],
}

# Tool namespace for help text: all known installed tools from audit
TOOLS = [
    # Existing 26 tools (in repo)
    "curl", "docker", "nmap", "tar", "jq", "tee", "git", "python3",
    "ssh", "ping", "dig", "traceroute", "netcat", "wget", "openssl",
    "whois", "grep", "sed", "awk", "rsync", "gzip", "docker-compose",
    "socat", "tmux", "make",
    # Note: kubectl is NOT installed, skip it
    # 57 new tools to add
    "find", "xargs", "sort", "uniq", "cut", "tr", "diff", "patch",
    "head", "tail", "less", "cat", "bash", "chmod", "chown", "cp", "mv",
    "rm", "ln", "mount", "dd", "cron", "systemctl", "journalctl",
    "iptables", "ip", "ifconfig", "route", "tcpdump", "telnet", "ftp",
    "scp", "sftp", "du", "df", "free", "top", "ps", "kill", "nice",
    "ionice", "timeout", "watch", "objdump", "readelf", "strings",
    "base64", "xxd", "hexdump", "od", "file", "stat", "md5sum",
    "sha256sum", "sha1sum", "wc", "comm",
    # The remaining installed tools from the audit
    "nc",
]


def tool_exists(tool: str) -> bool:
    if tool in SPECIAL_HELP:
        return True
    result = subprocess.run(
        ["which", tool], capture_output=True, text=True, timeout=5
    )
    return result.returncode == 0


def strip_ansi(text: str) -> str:
    """Remove ANSI escape sequences including OSC 8 hyperlinks from text."""
    import re
    # Remove OSC 8 hyperlinks: ESC ] 8 ; ; <url> ESC \
    text = re.sub(r'\x1b\][^\x1b]*\x1b\\', '', text)
    # Remove ANSI CSI sequences: ESC [ <params> <letter>
    text = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', text)
    # Remove remaining escape characters
    text = text.replace('\x1b', '')
    return text


def extract_help(tool: str) -> str | None:
    if tool in SPECIAL_HELP:
        try:
            result = subprocess.run(
                SPECIAL_HELP[tool],
                capture_output=True,
                text=True,
                timeout=10,
                env={},
            )
            output = (result.stdout or "") + (result.stderr or "")
            return strip_ansi(output.strip()) if output.strip() else None
        except subprocess.TimeoutExpired:
            return None
        except Exception:
            return None

    for flag, _ in HELP_FLAGS:
        try:
            result = subprocess.run(
                [tool, flag] if flag else [tool],
                capture_output=True,
                text=True,
                timeout=10,
            )
            output = (result.stdout or "") + (result.stderr or "")
            text = strip_ansi(output.strip())
            if not text or len(text) <= 20:
                continue
            lower = text.lower()
            if any(phrase in lower for phrase in ["invalid option", "unknown option", "unrecognized option", "error while loading", "option requires"]):
                if result.returncode != 0:
                    continue
            # Prefer stdout over stderr
            stdout_clean = strip_ansi(result.stdout or "")
            if stdout_clean and len(stdout_clean) > 20:
                return stdout_clean
            return text
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            continue

    # Last resort: man page
    try:
        result = subprocess.run(
            ["man", tool],
            capture_output=True,
            text=True,
            timeout=10,
            env={},
        )
        if result.returncode == 0 and result.stdout.strip():
            return f"[MAN PAGE - {tool}]\n" + result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass

    return None


def main():
    HELP_DIR.mkdir(parents=True, exist_ok=True)
    found = []
    missing = []
    errors = []

    for tool in TOOLS:
        if not tool_exists(tool):
            missing.append(tool)
            continue

        help_text = extract_help(tool)
        if help_text:
            out_path = HELP_DIR / f"{tool}.txt"
            with open(out_path, "w") as f:
                f.write(help_text)
            found.append(tool)
            print(f"  OK  {tool} ({len(help_text)} chars)")
        else:
            errors.append(tool)
            print(f"  ??? {tool} (no help output)")

    print(f"\n=== Summary ===")
    print(f"Extracted: {len(found)}")
    print(f"Not found (missing binary): {len(missing)}")
    print(f"Found but no help output: {len(errors)}")
    if missing:
        print(f"Missing: {', '.join(missing)}")
    if errors:
        print(f"No help: {', '.join(errors)}")


if __name__ == "__main__":
    main()
