"""
Extract reverse shell / bind shell / msfvenom payloads from
Database/reverse-shell-generator/js/data.js

Robust state-machine approach: properly handles escaped quotes,
template literals, nested braces, and JS comments.

Post-processes PowerShell Base64 variants: generates the Base64-encoded
command from the base payload's script (UTF-16LE → Base64).
"""
import base64
import json
import re
from pathlib import Path

DATA_JS = Path("Database/reverse-shell-generator/js/data.js")
OUTPUT_DIR = Path("data/enrichment")

# PowerShell Base64 variants to generate dynamically.
# Key = variant name (as it appears in source as a placeholder),
# Value = key in rsgData.specialCommands whose script is the base for encoding.
BASE64_VARIANTS: dict[str, str] = {
    "PowerShell #3 (Base64)": "PowerShell payload",
    "PowerShell #5 (stderr support) (Base64)": "PowerShell +stderr payload",
}


def generate_ps_base64_command(script: str) -> str:
    """Encode a raw PowerShell script as a Base64 oneliner command.

    PowerShell's ``-e`` / ``-EncodedCommand`` flag expects the script to be
    encoded as UTF-16LE then Base64.
    """
    encoded = base64.b64encode(script.encode("utf-16le")).decode()
    return f"powershell -nop -W hidden -noni -ep bypass -e {encoded}"


def skip_js_string(text: str, pos: int) -> tuple[str, int] | None:
    """Parse a JS string literal at text[pos] (quote char: ", ', or `).
    Returns (unescaped_content, end_pos_after_closing_quote) or None."""
    quote = text[pos]
    result = []
    i = pos + 1
    while i < len(text):
        ch = text[i]
        if ch == '\\':
            if i + 1 >= len(text):
                return None
            esc = text[i + 1]
            escape_map = {
                'n': '\n', 'r': '\r', 't': '\t',
                'b': '\b', 'f': '\f', 'v': '\v',
                '0': '\0',
            }
            if esc in escape_map:
                result.append(escape_map[esc])
                i += 2
            elif esc == 'x' and i + 3 < len(text):
                try:
                    result.append(chr(int(text[i+2:i+4], 16)))
                    i += 4
                except ValueError:
                    result.append(esc)
                    i += 2
            elif esc == 'u' and i + 5 < len(text):
                try:
                    result.append(chr(int(text[i+2:i+6], 16)))
                    i += 6
                except ValueError:
                    result.append(esc)
                    i += 2
            else:
                result.append(esc)
                i += 2
        elif ch == quote:
            return (''.join(result), i + 1)
        else:
            result.append(ch)
            i += 1
    return None


def find_matching(text: str, pos: int, open_char: str, close_char: str) -> int:
    """Find matching close_char for open_char at pos, respecting strings and comments."""
    if pos >= len(text) or text[pos] != open_char:
        return -1
    depth = 1
    i = pos + 1
    while i < len(text):
        ch = text[i]
        if ch in ('"', "'", '`'):
            parsed = skip_js_string(text, i)
            if parsed is None:
                return -1
            i = parsed[1]
            continue
        if ch == '/' and i + 1 < len(text):
            if text[i + 1] == '/':
                nl = text.find('\n', i)
                i = nl + 1 if nl >= 0 else len(text)
                continue
            if text[i + 1] == '*':
                end = text.find('*/', i + 2)
                i = end + 2 if end >= 0 else len(text)
                continue
        if ch == open_char:
            depth += 1
        elif ch == close_char:
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


def find_matching_brace(text: str, pos: int) -> int:
    return find_matching(text, pos, '{', '}')


def find_matching_bracket(text: str, pos: int) -> int:
    return find_matching(text, pos, '[', ']')


def extract_field_value(text: str, field_name: str) -> str | None:
    """Extract the string value for a named field from a JS object literal block.
    Returns the unescaped string, or None if not found."""
    match = re.search(r'"' + re.escape(field_name) + r'"\s*:', text)
    if not match:
        return None
    pos = match.end()
    while pos < len(text) and text[pos] in ' \t\n\r':
        pos += 1
    if pos >= len(text):
        return None
    if text[pos] in ('"', "'", '`'):
        parsed = skip_js_string(text, pos)
        if parsed is not None:
            return parsed[0]
    return None


def extract_meta_array(text: str) -> list[str]:
    """Extract the string array from "meta": [...]."""
    match = re.search(r'"meta"\s*:', text)
    if not match:
        return []
    pos = match.end()
    while pos < len(text) and text[pos] in ' \t\n\r':
        pos += 1
    if pos >= len(text) or text[pos] != '[':
        return []
    pos += 1
    meta = []
    while pos < len(text):
        while pos < len(text) and text[pos] in ' \t\n\r,':
            pos += 1
        if pos >= len(text) or text[pos] == ']':
            break
        if text[pos] in ('"', "'"):
            parsed = skip_js_string(text, pos)
            if parsed is None:
                break
            meta.append(parsed[0])
            pos = parsed[1]
        else:
            break
    return meta


def extract_objects_with_name_command(text: str) -> list[dict]:
    """Extract {name, command, meta} object literals from a JS code block.
    Handles nested braces, quoted strings with escapes, and JS comments."""
    results = []
    i = 0
    while i < len(text):
        ch = text[i]
        if ch in ('"', "'", '`'):
            parsed = skip_js_string(text, i)
            i = parsed[1] if parsed else i + 1
            continue
        if ch == '/' and i + 1 < len(text):
            if text[i + 1] == '/':
                nl = text.find('\n', i)
                i = nl + 1 if nl >= 0 else len(text)
                continue
            if text[i + 1] == '*':
                end = text.find('*/', i + 2)
                i = end + 2 if end >= 0 else len(text)
                continue
        if ch == '{':
            close = find_matching_brace(text, i)
            if close < 0:
                i += 1
                continue
            obj_block = text[i:close + 1]
            name = extract_field_value(obj_block, 'name')
            command = extract_field_value(obj_block, 'command')
            if name and command and command != name:
                meta = extract_meta_array(obj_block)
                results.append({
                    "name": name,
                    "command": command,
                    "meta": meta,
                    "platforms": meta[:],
                })
            i = close + 1
            continue
        i += 1
    return results


def extract_listeners(text: str) -> list[dict]:
    """Extract listener commands from rsgData object literal."""
    results = []
    start = text.find('listenerCommands:')
    if start < 0:
        return results
    chunk = text[start:]
    arr_start = chunk.find('[')
    if arr_start < 0:
        return results
    end = find_matching_bracket(chunk, arr_start)
    if end < 0:
        return results
    array_body = chunk[arr_start:end + 1]
    pairs = re.findall(r"""\[\s*'([^']*)'\s*,\s*'((?:[^'\\]|\\.)*)'\s*\]""", array_body)
    for name, command in pairs:
        results.append({"name": name, "command": command})
    pairs_dq = re.findall(r'\[\s*"([^"]*)"\s*,\s*"((?:[^"\\]|\\.)*)"\s*\]', array_body)
    for name, command in pairs_dq:
        if not any(r["name"] == name for r in results):
            results.append({"name": name, "command": command})
    return results


def extract_special_commands(text: str) -> dict[str, str]:
    """Extract the ``specialCommands: { … }`` object literal from ``rsgData``.

    Returns a dict mapping each friendly name (e.g. ``"PowerShell payload"``)
    to the raw script string.
    """
    start = text.find("specialCommands:")
    if start < 0:
        return {}
    obj_start = text.find("{", start)
    if obj_start < 0:
        return {}
    obj_end = find_matching_brace(text, obj_start)
    if obj_end < 0:
        return {}
    body = text[obj_start : obj_end + 1]
    result: dict[str, str] = {}
    i = 0
    while i < len(body):
        ch = body[i]
        if ch in ('"', "'", "`"):
            parsed = skip_js_string(body, i)
            if parsed is None:
                i += 1
                continue
            key = parsed[0]
            i = parsed[1]
            while i < len(body) and body[i] in " \t\n\r:":
                i += 1
            if i >= len(body):
                break
            if body[i] in ('"', "'", "`"):
                parsed_val = skip_js_string(body, i)
                if parsed_val is not None:
                    result[key] = parsed_val[0]
                    i = parsed_val[1]
                    continue
        i += 1
    return result


def categorize_objects(text: str, var_name: str, cat_id: str) -> list[dict]:
    """Extract objects that appear near a given variable name."""
    pattern = rf'(?:var|let|const)\s+{re.escape(var_name)}\s*='
    match = re.search(pattern, text)
    if not match:
        return []
    chunk = text[match.start():]
    arr_start = chunk.find('[')
    if arr_start < 0:
        return []
    end = find_matching_bracket(chunk, arr_start)
    if end < 0:
        return []
    array_body = chunk[arr_start:end + 1]
    return extract_objects_with_name_command(array_body)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if not DATA_JS.exists():
        print(f"ERROR: {DATA_JS} not found")
        return
    raw = DATA_JS.read_text()
    print(f"Extracting from {DATA_JS}...")
    categories = [
        ("reverse-shell", "reverseShellCommands"),
        ("bind-shell", "bindShellCommands"),
        ("msfvenom", "msfvenomCommands"),
        ("hoaxshell", "hoaxShellCommands"),
        ("assembled", "assembledCommands"),
    ]
    all_payloads = []
    all_listeners = extract_listeners(raw)
    print(f"  listeners: {len(all_listeners)} entries")
    for cat_id, var_name in categories:
        label_map = {
            "reverse-shell": "Reverse Shell",
            "bind-shell": "Bind Shell",
            "msfvenom": "MSFVenom",
            "hoaxshell": "HoaxShell",
            "assembled": "Assembled Shellcode",
        }
        objects = categorize_objects(raw, var_name, cat_id)
        for obj in objects:
            all_payloads.append({
                "name": obj.get("name", ""),
                "command": obj.get("command", ""),
                "category": cat_id,
                "label": label_map.get(cat_id, cat_id),
                "platforms": obj.get("platforms", []),
            })
        print(f"  {var_name} ({cat_id}): {len(objects)} payloads")
    # Post-process: generate PowerShell Base64 variants from specialCommands
    special_cmds = extract_special_commands(raw)
    if special_cmds:
        print(f"  specialCommands: {len(special_cmds)} entries")
    for var_name, special_key in BASE64_VARIANTS.items():
        script = special_cmds.get(special_key)
        if not script:
            print(f"  WARN: special command '{special_key}' not found — cannot generate '{var_name}'")
            continue
        ps_cmd = generate_ps_base64_command(script)
        # Preserve category/label from the existing placeholder entry (if any),
        # otherwise default to reverse-shell (source context).
        existing = [p for p in all_payloads if p["name"] == var_name]
        if existing:
            cat = existing[0]["category"]
            label = existing[0]["label"]
            platforms = existing[0].get("platforms", [])
        else:
            cat = "reverse-shell"
            label = "Reverse Shell"
            platforms = ["windows"]
        all_payloads.append({
            "name": var_name,
            "command": ps_cmd,
            "category": cat,
            "label": label,
            "platforms": platforms,
        })
        print(f"  GENERATED: '{var_name}' from specialCommands['{special_key}']")
    payloads_path = OUTPUT_DIR / "revshells-payloads.json"
    payloads_path.write_text(json.dumps(all_payloads, indent=2))
    listeners_path = OUTPUT_DIR / "revshells-listeners.json"
    listeners_path.write_text(json.dumps(all_listeners, indent=2))
    print(f"\n  Total: {len(all_payloads)} payloads, {len(all_listeners)} listeners")
    print(f"  Wrote {len(all_payloads)} payloads, {len(all_listeners)} listeners")


if __name__ == "__main__":
    main()
