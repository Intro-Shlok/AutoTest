---
id: text-search-grep
namespace: text:search:grep
name: grep
description: Powerful text search utility for pattern matching using regular expressions
  across files and streams.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - text.search.regex
  - text.search.fixed
  - text.search.recursive
  - text.search.invert
  - text.search.context
  - data.extract.pattern
platforms:
  - linux
  - macos
  - cross-platform
risk_level: low
trust_level: verified
execution_policy: enabled
architectures:
  - amd64
  - arm64
  - cross-platform
dependencies: []
related_tools:
  - rg
  - ack
  - awk
  - sed
  - ag
  - system-file-tr
  - text-process-awk
  - text-process-sed
artifacts:
  - type: text.search.result
    description: Lines matching the search pattern
    mime: text/plain
    trust_level: verified
  - type: text.search.count
    description: Count of matching lines
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - matching-lines
    - match-count
  consumes:
    - input-text
    - search-pattern
contract:
  inputs:
    - type: text.plain
      description: Text input to search through
    - type: text.regex.pattern
      description: Regular expression or fixed string pattern
  outputs:
    - type: text.search.result
      description: Lines matching the search pattern
      mime: text/plain
  side_effects: []
  resource_cost:
    cpu: low
    memory_mb: 16
    network: none
    disk_io: medium
resource_profile:
  cpu: low
  memory_mb: 16
  network: none
  disk_io: medium
allowed-tools:
  - grep
  - egrep
  - fgrep
  - Bash
  - execFile

parameters:
  - name: extended-regexp
    type: string
    required: false
    description: "PATTERNS are extended regular expressions"
    aliases:
      - -E
      - --extended-regexp
  - name: fixed-strings
    type: string
    required: false
    description: "PATTERNS are strings"
    aliases:
      - -F
      - --fixed-strings
  - name: basic-regexp
    type: string
    required: false
    description: "PATTERNS are basic regular expressions"
    aliases:
      - -G
      - --basic-regexp
  - name: perl-regexp
    type: string
    required: false
    description: "PATTERNS are Perl regular expressions"
    aliases:
      - -P
      - --perl-regexp
  - name: regexp
    type: string
    required: false
    description: "use PATTERNS for matching"
    aliases:
      - -e
      - --regexp
  - name: file
    type: file
    required: false
    description: "take PATTERNS from FILE"
    aliases:
      - -f
      - --file
  - name: ignore-case
    type: string
    required: false
    description: "ignore case distinctions in patterns and data"
    aliases:
      - -i
      - --ignore-case
  - name: no-ignore-case
    type: string
    required: false
    description: "do not ignore case distinctions (default)"
    aliases:
      - --no-ignore-case
  - name: word-regexp
    type: string
    required: false
    description: "match only whole words"
    aliases:
      - -w
      - --word-regexp
  - name: line-regexp
    type: string
    required: false
    description: "match only whole lines"
    aliases:
      - -x
      - --line-regexp
  - name: null-data
    type: string
    required: false
    description: "a data line ends in 0 byte, not newline"
    aliases:
      - -z
      - --null-data
  - name: no-messages
    type: string
    required: false
    description: "suppress error messages"
    aliases:
      - -s
      - --no-messages
  - name: invert-match
    type: string
    required: false
    description: "select non-matching lines"
    aliases:
      - -v
      - --invert-match
  - name: version
    type: string
    required: false
    description: "display version information and exit"
    aliases:
      - -V
      - --version
  - name: help
    type: string
    required: false
    description: "display this help text and exit"
    aliases:
      - --help
  - name: max-count
    type: integer
    required: false
    description: "stop after NUM selected lines"
    aliases:
      - -m
      - --max-count
  - name: byte-offset
    type: string
    required: false
    description: "print the byte offset with output lines"
    aliases:
      - -b
      - --byte-offset
  - name: line-number
    type: string
    required: false
    description: "print line number with output lines"
    aliases:
      - -n
      - --line-number
  - name: line-buffered
    type: string
    required: false
    description: "flush output on every line"
    aliases:
      - --line-buffered
  - name: with-filename
    type: string
    required: false
    description: "print file name with output lines"
    aliases:
      - -H
      - --with-filename
  - name: no-filename
    type: string
    required: false
    description: "suppress the file name prefix on output"
    aliases:
      - -h
      - --no-filename
  - name: label
    type: file
    required: false
    description: "use LABEL as the standard input file name prefix"
    aliases:
      - --label
  - name: only-matching
    type: string
    required: false
    description: "show only nonempty parts of lines that match"
    aliases:
      - -o
      - --only-matching
  - name: quiet
    type: string
    required: false
    description: "suppress all normal output"
    aliases:
      - -q
      - --quiet
      - --silent
  - name: binary-files
    type: string
    required: false
    description: "assume that binary files are TYPE"
    aliases:
      - --binary-files
  - name: text
    type: string
    required: false
    description: "equivalent to --binary-files=text"
    aliases:
      - -a
      - --text
  - name: directories
    type: string
    required: false
    description: "ACTION is 'read', 'recurse', or 'skip'"
    aliases:
      - -d
      - --directories
  - name: devices
    type: string
    required: false
    description: "how to handle devices, FIFOs and sockets"
    aliases:
      - -D
      - --devices
  - name: recursive
    type: string
    required: false
    description: "like --directories=recurse"
    aliases:
      - -r
      - --recursive
  - name: dereference-recursive
    type: string
    required: false
    description: "--include=GLOB search only files that match GLOB (a file pattern)
      --exclude=GLOB skip files that match GLOB --exclude-from=FILE skip files that
      match any file pattern from FILE --exclude-dir=GLOB s..."
    aliases:
      - -R
      - --dereference-recursive
features:
  - local
  - pipes-stdin
  - pipes-stdout
  - batch
techniques:
  - analysis
  - data-manipulation
  - execution
  - process-manip
  - persistence
  - credential-access
  - privilege-escalation
execution:
  template: "grep {extended-regexp} {fixed-strings} {basic-regexp} {perl-regexp} {regexp}"
  sandbox: execFile
  timeout_seconds: 60
  shell: false
examples:
  - description: "Search for a pattern in a file"
    command: "grep 'error' logfile.txt"
  - description: "Case-insensitive recursive search"
    command: "grep -ri 'TODO' src/"
  - description: "Show context lines around matches"
    command: "grep -C 3 'Exception' app.log"
  - description: "Count matches per file"
    command: "grep -c 'function' *.py"
  - description: "Invert match (lines not containing pattern)"
    command: "grep -v '^#' config.conf"
  - description: "Extract IP addresses with regex"
    command: "grep -oE '\\b([0-9]{1,3}\\.){3}[0-9]{1,3}\\b' access.log"
  - description: 'Darkiros UTILS: Extract md5 hash ({32})'
    command: egrep -oE '(^|[^a-fA-F0-9])[a-fA-F0-9]{32}([^a-fA-F0-9]|$)' [file] |
      egrep -o '[a-fA-F0-9]{32}' > md5-hashes.txt
  - description: 'Darkiros UTILS: Extract sha1 hash ({40})'
    command: egrep -oE '(^|[^a-fA-F0-9])[a-fA-F0-9]{40}([^a-fA-F0-9]|$)' [file] |
      egrep -o '[a-fA-F0-9]{40}' > sha1-hashes.txt
  - description: 'Darkiros UTILS: Extract sha256 hash ({64})'
    command: egrep -oE '(^|[^a-fA-F0-9])[a-fA-F0-9]{64}([^a-fA-F0-9]|$)' [file] |
      egrep -o '[a-fA-F0-9]{64}' > sha256-hashes.txt
  - description: 'Darkiros UTILS: Extract sha512 hash ({128})'
    command: egrep -oE '(^|[^a-fA-F0-9])[a-fA-F0-9]{128}([^a-fA-F0-9]|$)' [file] |
      egrep -o '[a-fA-F0-9]{128}' > sha512-hashes.txt
  - description: 'Darkiros UTILS: Extract valid MySQL-old hash'
    command: grep -e "[0-7][0-9a-f]{7}[0-7][0-9a-f]{7}" [file] > mysql-old-hashes.txt
  - description: 'Darkiros UTILS: Extract valid blowfish hash'
    command: grep -e "$2a\\$\\08\\$(.){75}" [file] > blowfish-hashes.txt
  - description: 'Darkiros UTILS: Extract emails from file'
    command: grep -E -o "\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6}\\b" [file]
  - description: 'Darkiros UTILS: Extract IP from file'
    command: grep -E -o 
      "(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"
      file.txt
  - description: NetRunners usefull/shell
    command: grep -r --color=always 'password' .
references:
  - label: "GNU Grep manual"
    url: "https://www.gnu.org/software/grep/manual/"
  - label: "Regular expressions guide"
    url: "https://www.regular-expressions.info/"
mitre_ids:
  - T1208
---

# Grep — Text Pattern Search

Grep is one of the essential Unix tools. It searches files and streams for lines matching a pattern, making it invaluable for log analysis, code searching, and data extraction pipelines.

## Search Patterns

### Basic vs Extended Regex
```bash
# Basic regex (default): + and ? are literal
grep 'foo\+' file.txt

# Extended regex: + and ? are metacharacters
grep -E 'foo+' file.txt

# Fixed strings (no regex, faster)
grep -F 'foo+' file.txt
```

### Common Regex Patterns
```bash
# Lines starting with a pattern
grep '^error' file.txt

# Lines ending with a pattern
grep 'done$' file.txt

# Word boundaries
grep -w 'class' file.txt

# Character classes
grep '[0-9]\{3\}-[0-9]\{4\}' file.txt
```

## Pipelined Usage

```bash
# Chain with other tools
ps aux | grep python | grep -v grep

# Extract and count unique matches
grep -oP 'https?://[^\s"]+' file.txt | sort | uniq -c | sort -rn

# Find files containing pattern
grep -rl 'main' --include='*.py' src/
```

## Performance Tips

| Situation | Best Tool |
|-----------|-----------|
| Single file | `grep` is fast enough |
| Large codebase | `ripgrep (rg)` is 5-10x faster |
| Binary search | `grep -a` or `strings \| grep` |
| Compressed files | `zgrep` for .gz files |

## Related Tools

- **[ripgrep (rg)](../../search/rg.md)** — Faster recursive search
- **[sed](../process/sed.md)** — Stream editor for find-and-replace
- **[awk](../process/awk.md)** — Text processing and field extraction
