"""
Generate/update all 83 tool .md files by merging parsed parameters with domain knowledge.

For existing 26 tools: reads current .md, replaces parameters section, adds features/techniques.
For 57 new tools: generates complete .md files from templates + parsed parameters.
"""

import json
import os
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TOOLS_DIR = REPO_ROOT / "src" / "content" / "tools"
PARSED_DIR = REPO_ROOT / "data" / "parsed_params"
HELP_DIR = REPO_ROOT / "data" / "help_texts"

# ─── Domain taxonomy for new tools ───
# (tool_name, domain, category, namespace_short, description)
TOOL_TAXONOMY = {
    # New network tools
    "scp":     ("network", "transfer", "scp", "Secure copy over SSH protocol"),
    "sftp":    ("network", "transfer", "sftp", "Secure file transfer over SSH"),
    "ftp":     ("network", "transfer", "ftp", "File transfer protocol client"),
    "telnet":  ("network", "remote", "telnet", "Telnet protocol client for remote connections"),
    "tcpdump": ("network", "capture", "tcpdump", "Dump traffic on a network interface"),
    "nc":      ("network", "socket", "nc", "Netcat - arbitrary TCP/UDP connections and listening"),
    # New system tools
    "find":    ("system", "file", "find", "Search for files in a directory hierarchy"),
    "xargs":   ("system", "file", "xargs", "Build and execute command lines from standard input"),
    "sort":    ("system", "file", "sort", "Sort lines of text files"),
    "uniq":    ("system", "file", "uniq", "Report or omit repeated lines"),
    "cut":     ("system", "file", "cut", "Remove sections from each line of files"),
    "tr":      ("system", "file", "tr", "Translate or delete characters"),
    "wc":      ("system", "file", "wc", "Print newline, word, and byte counts"),
    "comm":    ("system", "file", "comm", "Compare two sorted files line by line"),
    "head":    ("system", "file", "head", "Output the first part of files"),
    "tail":    ("system", "file", "tail", "Output the last part of files"),
    "less":    ("system", "file", "less", "View file contents page by page"),
    "cat":     ("system", "file", "cat", "Concatenate files and print to standard output"),
    "diff":    ("system", "file", "diff", "Compare files line by line"),
    "patch":   ("system", "file", "patch", "Apply diff patches to files"),
    "strings": ("system", "file", "strings", "Find printable strings in binary files"),
    "base64":  ("system", "file", "base64", "Base64 encode/decode data"),
    "xxd":     ("system", "file", "xxd", "Hex dump or reverse hex dump"),
    "hexdump": ("system", "file", "hexdump", "Display file contents in hexadecimal"),
    "od":      ("system", "file", "od", "Dump files in octal and other formats"),
    "file":    ("system", "file", "file", "Determine file type"),
    "stat":    ("system", "file", "stat", "Display file or filesystem status"),
    "md5sum":  ("system", "file", "md5sum", "Compute and check MD5 message digest"),
    "sha256sum": ("system", "file", "sha256sum", "Compute and check SHA-256 message digest"),
    "sha1sum": ("system", "file", "sha1sum", "Compute and check SHA-1 message digest"),
    # System file management
    "cp":      ("system", "file", "cp", "Copy files and directories"),
    "mv":      ("system", "file", "mv", "Move/rename files and directories"),
    "rm":      ("system", "file", "rm", "Remove files or directories"),
    "ln":      ("system", "file", "ln", "Create hard and symbolic links"),
    "chmod":   ("system", "file", "chmod", "Change file mode bits"),
    "chown":   ("system", "file", "chown", "Change file owner and group"),
    "dd":      ("system", "file", "dd", "Convert and copy a file"),
    # System process
    "ps":      ("system", "process", "ps", "Report process status"),
    "kill":    ("system", "process", "kill", "Send signals to processes"),
    "nice":    ("system", "process", "nice", "Run a program with modified scheduling priority"),
    "ionice":  ("system", "process", "ionice", "Set/get I/O scheduling class and priority"),
    "timeout": ("system", "process", "timeout", "Run a command with a time limit"),
    "watch":   ("system", "process", "watch", "Execute a program periodically"),
    "top":     ("system", "process", "top", "Display Linux processes"),
    "free":    ("system", "process", "free", "Display amount of free and used memory"),
    "df":      ("system", "storage", "df", "Report filesystem disk space usage"),
    "du":      ("system", "storage", "du", "Estimate file space usage"),
    # System service
    "systemctl": ("system", "service", "systemctl", "Control the systemd system and service manager"),
    "journalctl": ("system", "service", "journalctl", "Query the systemd journal"),
    "cron":   ("system", "scheduler", "cron", "Daemon to execute scheduled commands"),
    # System mount
    "mount":  ("system", "storage", "mount", "Mount a filesystem"),
    # System shell
    "bash":   ("system", "shell", "bash", "GNU Bourne-Again SHell"),
    # Network config
    "iptables": ("network", "firewall", "iptables", "Administration tool for IPv4 firewall rules"),
    "ip":     ("network", "config", "ip", "Show/manipulate routing, devices, policy routing and tunnels"),
    "ifconfig": ("network", "config", "ifconfig", "Configure network interfaces"),
    "route":  ("network", "config", "route", "Show/manipulate the IP routing table"),
    "tmux":   ("system", "terminal", "tmux", "Terminal multiplexer"),
    "socat":  ("network", "socket", "socat", "Multipurpose relay for bidirectional data transfer"),
    "git":    ("dev", "vcs", "git", "Distributed version control system"),
    "make":   ("dev", "build", "make", "GNU Make - build automation tool"),
    "python3": ("dev", "runtime", "python3", "Python programming language interpreter"),
    "awk":    ("text", "process", "awk", "Pattern scanning and processing language"),
    "sed":    ("text", "process", "sed", "Stream editor for filtering and transforming text"),
    "grep":   ("text", "search", "grep", "Print lines matching a pattern"),
    "jq":     ("text", "process", "jq", "Command-line JSON processor"),
}

# Existing tools that already have .md files
EXISTING_TOOLS = {"curl", "docker", "nmap", "tar", "jq", "tee", "git", "python3",
                  "ssh", "ping", "dig", "traceroute", "netcat", "wget", "openssl",
                  "whois", "grep", "sed", "awk", "rsync", "gzip", "docker-compose",
                  "socat", "tmux", "make", "kubectl"}

# Feature rules by domain
def infer_features(domain: str, category: str, tool_name: str = "") -> list[str]:
    features = []
    if domain == "network":
        features += ["remote", "network-intensive"]
    if domain == "system" and category in ("file", "file-manage", "shell", "terminal"):
        features += ["local"]
    if domain == "system" and category in ("process", "service", "scheduler", "storage"):
        features += ["local"]
    if domain == "text":
        features += ["local", "pipes-stdin", "pipes-stdout", "batch"]
    if domain == "dev":
        features += ["local", "batch"]
    if category in ("file", "file-manage", "archive"):
        features += ["file-system"]
    if category in ("shell", "terminal"):
        features += ["interactive"]
    if category in ("firewall", "config"):
        features += ["requires-root", "network-intensive"]
    if category == "process":
        features += ["process-manip"]
    if category in ("service", "scheduler"):
        features += ["requires-root"]
    if category == "capture":
        features += ["requires-root", "network-intensive", "streaming"]
    if category == "transfer":
        features += ["remote", "encryption"]
    if tool_name in ("openssl", "sha256sum", "sha1sum", "md5sum", "base64", "xxd"):
        features += ["encryption", "batch"]
    if tool_name in ("jq",):
        features += ["output-json"]
    if tool_name in ("curl",):
        features += ["output-json", "streaming"]
    if tool_name in ("top", "htop", "watch"):
        features += ["streaming"]
    if tool_name in ("scp", "sftp"):
        features += ["encryption", "remote"]
    if tool_name in ("cat", "less", "head", "tail"):
        features += ["pipes-stdin", "pipes-stdout"]
    # Deduplicate
    return list(dict.fromkeys(features))


def infer_techniques(domain: str, category: str, tool_name: str = "") -> list[str]:
    techniques = []
    if domain == "network":
        if category in ("http", "transfer"):
            techniques += ["exfiltration", "collection"]
        if category in ("recon", "dns", "diagnose", "capture"):
            techniques += ["recon", "discovery"]
        if category in ("firewall", "config"):
            techniques += ["defense-evasion", "discovery"]
        if category in ("socket", "remote"):
            techniques += ["command-and-control", "lateral-movement"]
    if domain == "system":
        if category in ("file", "file-manage"):
            techniques += ["collection", "data-manipulation"]
        if category == "process":
            techniques += ["execution", "impact"]
        if category in ("service", "scheduler"):
            techniques += ["execution", "persistence"]
        if category == "storage":
            techniques += ["discovery"]
    if domain == "text":
        techniques += ["data-manipulation", "analysis"]
    if domain == "dev":
        techniques += ["execution", "analysis"]
    if domain == "security":
        techniques += ["recon", "credential-access"]
    if tool_name in ("openssl",):
        techniques += ["credential-access", "encryption"]
    if tool_name in ("ssh",):
        techniques += ["lateral-movement", "remote-services"]
    if tool_name in ("tcpdump",):
        techniques += ["network-sniffing", "discovery"]
    if tool_name in ("ps",):
        techniques += ["discovery", "process-discovery"]
    if tool_name in ("kill",):
        techniques += ["impact", "process-termination"]
    if tool_name in ("iptables", "ip", "route", "ifconfig"):
        techniques += ["defense-evasion", "network-manipulation"]
    return list(dict.fromkeys(techniques))


def infer_capabilities(domain: str, category: str, tool: str) -> list[str]:
    """Generate hierarchical capability namespacing."""
    caps = [f"{domain}.{category}.{tool}"]
    if domain == "network":
        if category == "http":
            caps.append(f"{domain}.http.fetch")
            caps.append(f"{domain}.http.inspect")
        if category == "transfer":
            caps.append(f"{domain}.transfer.download")
            caps.append(f"{domain}.transfer.upload")
        if category == "socket":
            caps.append(f"{domain}.socket.connect")
            caps.append(f"{domain}.socket.listen")
        if category == "dns":
            caps.append(f"{domain}.dns.lookup")
        if category == "diagnose":
            caps.append(f"{domain}.diagnose.trace")
            caps.append(f"{domain}.diagnose.ping")
        if category == "capture":
            caps.append(f"{domain}.capture.packet")
            caps.append(f"{domain}.capture.sniff")
        if category == "remote":
            caps.append(f"{domain}.remote.shell")
    if domain == "system":
        if category == "file":
            caps.append(f"{domain}.file.search")
            caps.append(f"{domain}.file.process")
            caps.append(f"{domain}.file.copy")
            caps.append(f"{domain}.file.move")
            caps.append(f"{domain}.file.delete")
        if category == "process":
            caps.append(f"{domain}.process.list")
            caps.append(f"{domain}.process.signal")
            caps.append(f"{domain}.process.monitor")
        if category == "storage":
            caps.append(f"{domain}.storage.usage")
            caps.append(f"{domain}.storage.mount")
        if category == "scheduler":
            caps.append(f"{domain}.scheduler.cron")
    if domain == "text":
        if category == "search":
            caps.append(f"{domain}.search.pattern")
        if category == "process":
            caps.append(f"{domain}.process.transform")
    if tool == "bash":
        caps.append("system.shell.command")
    if tool == "python3":
        caps.append("dev.runtime.execute")
    if tool == "git":
        caps.append("dev.vcs.commit")
    return caps


def param_to_yaml(p: dict, indent: int = 4) -> str:
    """Convert a parameter dict to YAML string."""
    prefix = " " * indent
    param_name = str(p['name'])
    # Quote YAML reserved words
    if param_name.lower() in ("null", "true", "false", "yes", "no", "on", "off"):
        param_name = f'"{param_name}"'
    lines = [f"{prefix}- name: {param_name}"]
    # template_key
    tk = p.get("template_key")
    if tk and tk != p.get("name"):
        lines.append(f"{prefix}  template_key: {tk}")
    lines.append(f"{prefix}  type: {p['type']}")
    lines.append(f"{prefix}  required: {'true' if p.get('required') else 'false'}")
    dv = p.get("default_value")
    if dv is not None:
        dv_str = str(dv).strip("`'\"")
        # Escape YAML-special characters in default values
        if not dv_str.replace('.','',1).isdigit():
            dv_str = dv_str.replace('"', '\\"')
            dv_str = f'"{dv_str}"'
        lines.append(f"{prefix}  default_value: {dv_str}")
    desc = p.get('description', '')
    if not desc or not desc.strip():
        desc = f"Set the {p.get('name', 'unknown')} parameter"
    desc = desc.strip()
    # Remove man page formatting artifacts (overstrike, backspace, etc.)
    desc = re.sub(r'.\x08', '', desc)  # Remove char+backspace sequences
    desc = desc.replace('\x08', '')     # Remove orphan backspaces
    # Remove leading flag patterns from description (parser artifact)
    desc = re.sub(r'^-[a-zA-Z0-9?]+\s', '', desc)
    desc = desc.replace('\\', '\\\\').replace('"', '\\"')
    # Truncate very long descriptions
    if len(desc) > 200:
        desc = desc[:197] + "..."
    lines.append(f'{prefix}  description: "{desc}"')
    aliases = p.get("aliases")
    if aliases:
        clean = []
        for a in aliases:
            a = str(a).strip()
            # Fix malformed aliases (e.g., ----flag -> --flag)
            if a.startswith("---"):
                a = "--" + a.lstrip("-")
            if a.startswith("-") and len(a) >= 2:
                # Quote if it looks like a number (e.g., -1)
                if re.match(r'^-?\d+(\.\d+)?$', a):
                    a = f'"{a}"'
                clean.append(a)
        if clean:
            alias_lines = "\n".join(f"{prefix}    - {a}" for a in clean)
            lines.append(f"{prefix}  aliases:\n{alias_lines}")
    ev = p.get("enum")
    if ev:
        clean_ev = []
        for e in ev:
            e_str = str(e)
            if e_str.lower() in ("null", "true", "false", "yes", "no", "on", "off"):
                e_str = f'"{e_str}"'
            elif re.match(r'^-?\d+(\.\d+)?$', e_str):
                e_str = f'"{e_str}"'
            clean_ev.append(e_str)
        enum_lines = "\n".join(f"{prefix}    - {e}" for e in clean_ev)
        lines.append(f"{prefix}  enum:\n{enum_lines}")
    return "\n".join(lines)


def make_tool_id(domain: str, category: str, tool: str) -> str:
    return f"{domain}-{category}-{tool}"


def make_namespace(domain: str, category: str, tool: str) -> str:
    return f"{domain}:{category}:{tool}"


def safe_name(tool: str) -> str:
    return tool.replace("_", "-")


def decide_risk(tool: str, domain: str, category: str) -> str:
    if tool in ("rm", "dd", "iptables", "kill"):
        return "high"
    if category in ("firewall", "file-manage") and tool not in ("ln",):
        return "medium"
    if domain == "system" and category in ("service", "scheduler"):
        return "medium"
    if tool in ("openssl", "scp", "sftp"):
        return "medium"
    return "low"


def decide_trust(tool: str) -> str:
    return "verified"


def default_execution_template(tool: str, params: list[dict]) -> str:
    """Generate a basic execution template from parameters."""
    if not params:
        return tool
    parts = [tool]
    for p in params[:5]:
        key = p.get("template_key") or p["name"]
        parts.append(f"{{{key}}}")
    return " ".join(parts)


def generate_examples(tool: str, params: list[dict]) -> list[dict]:
    """Generate basic examples from parsed parameters."""
    examples = []
    if params:
        first = params[0]
        if first["type"] == "string":
            examples.append({
                "description": f"Basic usage with {first['name']}",
                "command": f"{tool} ${{{first['name']}}}"
            })
        if first.get("enum"):
            examples.append({
                "description": f"Use {first['name']} flag",
                "command": f"{tool} {first['enum'][0]}"
            })
    # Always add --help example
    examples.append({
        "description": "Display help message",
        "command": f"{tool} --help"
    })
    return examples


def read_current_frontmatter(tool: str) -> dict | None:
    """Read the existing .md file frontmatter."""
    path = TOOLS_DIR / f"{tool}.md"
    if not path.exists():
        return None
    
    # Read raw YAML frontmatter block
    text = path.read_text()
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return None
    
    yaml_block = m.group(1)
    # Simple YAML parsing for known keys (not using yaml library)
    result = {}
    current_key = None
    current_list = None
    for line in yaml_block.split("\n"):
        # Top-level key
        kv_match = re.match(r"^([a-zA-Z_-][a-zA-Z0-9_-]*):\s*(.*)", line)
        if kv_match:
            current_key = kv_match.group(1)
            val = kv_match.group(2).strip()
            if val == "":
                # Starts a block (list or dict)
                current_list = []
                result[current_key] = current_list
            else:
                # Simple value
                if val.startswith('"') and val.endswith('"'):
                    val = val[1:-1]
                elif val.startswith("'") and val.endswith("'"):
                    val = val[1:-1]
                result[current_key] = val
                current_key = None
                current_list = None
        elif line.startswith("  - "):
            if current_list is not None:
                val = line.strip("- ").strip()
                if val.startswith('"') and val.endswith('"'):
                    val = val[1:-1]
                current_list.append(val)
        elif current_key and current_list is not None and line.startswith("    "):
            # Sub-key in a dict
            pass
    
    return result


def build_tool_file(tool: str) -> str:
    """Generate the complete .md content for a tool."""
    # Load parsed params
    parsed_path = PARSED_DIR / f"{tool}.json"
    params = []
    if parsed_path.exists():
        params = json.loads(parsed_path.read_text())
    
    # Limit to top 30 params to keep files manageable
    if len(params) > 30:
        # Keep first 30, prefer those with aliases (more important flags)
        with_aliases = [p for p in params if p.get("aliases")]
        without = [p for p in params if not p.get("aliases")]
        params = (with_aliases + without)[:30]
    
    # Get taxonomy
    is_existing = tool in EXISTING_TOOLS
    existing_fm = read_current_frontmatter(tool) if is_existing else None
    
    if is_existing and existing_fm:
        # Use existing file, just update parameters + add features/techniques
        path = TOOLS_DIR / f"{tool}.md"
        text = path.read_text()
        
        # Remove old parameters section and everything after it until next top-level key
        # Let's just inject new params before the 'execution' line
        param_yaml = "\n".join(param_to_yaml(p) for p in params) if params else " []"
        
        # Replace or add parameters
        param_section = f"parameters:\n{param_yaml}" if params else "parameters: []"
        old_param = re.search(r"^parameters:\n(?:  .*\n?)*", text, re.MULTILINE)
        
        # Add features and techniques if not present
        domain, category = "", ""
        for t, (d, c, _, _) in TOOL_TAXONOMY.items():
            if t == tool:
                domain, category = d, c
                break
        
        features = infer_features(domain, category, tool)
        techniques = infer_techniques(domain, category, tool)

        # Strip existing features/techniques/parameters sections to avoid duplicates
        # Use a loop to handle adjacent sections (after strip, next one has no leading \n)
        for section in ["features:", "techniques:", "parameters:"]:
            while True:
                new_text = re.sub(r"(\n?)" + re.escape(section) + r"\n(?:  .*\n?)*", "\n", text)
                if new_text == text:
                    break
                text = new_text

        lines = []
        added_extra = False
        for line in text.split("\n"):
            # Skip stripped sections (parameters, features, techniques — already removed by regex above)
            if line.startswith("parameters:") or line.startswith("features:") or line.startswith("techniques:"):
                continue
            if not added_extra and line.startswith("execution:"):
                # Inject parameters, features, techniques before execution
                if params:
                    lines.append("parameters:")
                    for p_yaml in [param_to_yaml(p) for p in params]:
                        lines.append(p_yaml)
                if features:
                    lines.append("features:")
                    for f in features:
                        lines.append(f"  - {f}")
                if techniques:
                    lines.append("techniques:")
                    for t in techniques:
                        lines.append(f"  - {t}")
                added_extra = True
                lines.append(line)  # Keep the "execution:" line
                continue
            # Override the template line if we just passed execution:
            if added_extra and line.strip().startswith("template:"):
                if params:
                    new_tmpl = default_execution_template(tool, params)
                    lines.append(f'  template: "{new_tmpl}"')
                else:
                    lines.append(line)
                continue

            lines.append(line)

        return "\n".join(lines)
    
    else:
        # New tool - generate from scratch
        # Find the taxonomy entry
        if tool not in TOOL_TAXONOMY:
            print(f"  SKIP {tool}: no taxonomy entry")
            return ""
        
        domain, category, ns_short, desc = TOOL_TAXONOMY[tool]
        tool_id = make_tool_id(domain, category, tool)
        namespace = make_namespace(domain, category, tool)
        caps = infer_capabilities(domain, category, tool)
        features = infer_features(domain, category, tool)
        techniques = infer_techniques(domain, category, tool)
        risk = decide_risk(tool, domain, category)
        trust = decide_trust(tool)
        examples = generate_examples(tool, params)
        
        # Build YAML
        lines = ["---"]
        lines.append(f"id: {tool_id}")
        lines.append(f"namespace: {namespace}")
        lines.append(f"name: {tool}")
        lines.append(f"description: {desc}")
        lines.append('author: "Repository Maintainers"')
        lines.append('version: "1.0.0"')
        
        if caps:
            lines.append("capabilities:")
            for c in caps:
                lines.append(f"  - {c}")
        
        lines.append("platforms:")
        lines.append("  - linux")
        if tool in ("python3", "curl", "git", "bash", "make"):
            lines.append("  - macos")
            lines.append("  - windows")
        lines.append("risk_level: " + risk)
        lines.append("trust_level: " + trust)
        lines.append("execution_policy: enabled")
        lines.append("architectures:")
        lines.append("  - amd64")
        lines.append("  - arm64")
        
        if features:
            lines.append("features:")
            for f in features:
                lines.append(f"  - {f}")
        if techniques:
            lines.append("techniques:")
            for t in techniques:
                lines.append(f"  - {t}")
        
        if params:
            lines.append("parameters:")
            for p in params:
                lines.append(param_to_yaml(p, indent=4))
        else:
            lines.append("parameters: []")
        
        # Execution template
        tmpl = tool
        if params:
            flags = []
            for p in params[:5]:
                key = p.get("template_key") or p["name"]
                if p.get("aliases"):
                    flag = p["aliases"][0] if p["type"] == "boolean" else f"{p['aliases'][0]} {{{key}}}"
                    flags.append(flag)
                else:
                    flags.append(f"{{{key}}}")
            flags_str = " ".join(flags)
            if flags_str:
                tmpl = f"{tool} {flags_str}"
        
        lines.append("execution:")
        lines.append(f"  template: \"{tmpl}\"")
        lines.append("  sandbox: execFile")
        lines.append("  timeout_seconds: 30")
        lines.append("  shell: false")
        
        if examples:
            lines.append("examples:")
            for ex in examples:
                lines.append(f"  - description: \"{ex['description']}\"")
                lines.append(f"    command: \"{ex['command']}\"")
        
        lines.append("---")
        lines.append("")
        lines.append(f"# {tool} — {desc}")
        lines.append("")
        lines.append("## Overview")
        lines.append("")
        lines.append(f"`{tool}` is a command-line utility for {desc.lower()}.")
        lines.append("")
        lines.append("## Usage")
        lines.append("")
        lines.append(f"```")
        lines.append(f"{tmpl}")
        lines.append(f"```")
        
        return "\n".join(lines)


def main():
    # Collect all tools (existing + new)
    all_tools = set(EXISTING_TOOLS)
    for tool in TOOL_TAXONOMY:
        all_tools.add(tool)
    
    # Remove tools without help text files
    existing = []
    new = []
    
    for tool in sorted(all_tools):
        if tool == "kubectl":
            continue  # Not installed
        
        content = build_tool_file(tool)
        if not content:
            continue
        
        out_path = TOOLS_DIR / f"{tool}.md"
        out_path.write_text(content)
        
        if tool in EXISTING_TOOLS:
            existing.append(tool)
        else:
            new.append(tool)
        print(f"  {'UPDATE' if tool in EXISTING_TOOLS else 'CREATE'} {tool}.md")
    
    print(f"\n=== Summary ===")
    print(f"Updated: {len(existing)} existing tools")
    print(f"Created: {len(new)} new tools")
    print(f"Total:   {len(existing) + len(new)}")


if __name__ == "__main__":
    main()
