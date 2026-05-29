---
id: text-process-sed
namespace: text:process:sed
name: sed
description: Stream editor for parsing and transforming text using pattern matching
  and substitution operations.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - text.transform.substitute
  - text.transform.delete
  - text.transform.insert
  - text.transform.append
  - text.filter.line
  - text.process.stream
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
  - cut
  - grep
  - tr
  - awk
  - system-file-tr
  - text-process-awk
  - text-search-grep
artifacts:
  - type: text.transformed
    description: Text after sed transformation
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - transformed-text
  consumes:
    - input-text
contract:
  inputs:
    - type: text.plain
      description: Input text stream to transform
  outputs:
    - type: text.transformed
      description: Text after applying sed script
      mime: text/plain
  side_effects: []
  resource_cost:
    cpu: low
    memory_mb: 8
    network: none
    disk_io: low
resource_profile:
  cpu: low
  memory_mb: 8
  network: none
  disk_io: low
allowed-tools:
  - sed
  - Bash
  - execFile

parameters:
  - name: quiet
    type: string
    required: false
    description: "suppress automatic printing of pattern space --debug annotate program
      execution"
    aliases:
      - -n
      - --quiet
      - --silent
  - name: expression
    type: string
    required: false
    description: "add the script to the commands to be executed"
    aliases:
      - -e
      - --expression
  - name: file
    type: file
    required: false
    description: "add the contents of script-file to the commands to be executed"
    aliases:
      - -f
      - -f
      - -f
      - --file
  - name: follow-symlinks
    type: string
    required: false
    description: "follow symlinks when processing in place"
    aliases:
      - --follow-symlinks
  - name: in-place
    type: string
    required: false
    description: "edit files in place (makes backup if SUFFIX supplied)"
    aliases:
      - -i
      - --in-place
  - name: line-length
    type: integer
    required: false
    description: "specify the desired line-wrap length for the `l' command"
    aliases:
      - -l
      - --line-length
  - name: posix
    type: string
    required: false
    description: "disable all GNU extensions"
    aliases:
      - --posix
  - name: regexp-extended
    type: string
    required: false
    description: "use extended regular expressions in the script (for portability
      use POSIX -E)"
    aliases:
      - -E
      - -r
      - --regexp-extended
  - name: separate
    type: string
    required: false
    description: "consider files as separate rather than as a single, continuous long
      stream. --sandbox operate in sandbox mode (disable e/r/w commands)"
    aliases:
      - -s
      - --separate
  - name: unbuffered
    type: file
    required: false
    description: "load minimal amounts of data from the input files and flush the
      output buffers more often"
    aliases:
      - -u
      - --unbuffered
  - name: null-data
    type: string
    required: false
    description: "separate lines by NUL characters --help display this help and exit
      --version output version information and exit"
    aliases:
      - -z
      - --null-data
features:
  - local
  - pipes-stdin
  - pipes-stdout
  - batch
  - process-manip
techniques:
  - data-manipulation
  - analysis
execution:
  template: "sed {quiet} {expression} {file} {follow-symlinks} {in-place}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
examples:
  - description: "Find and replace first occurrence per line"
    command: "sed 's/old/new/' file.txt"
  - description: "Global find and replace all occurrences"
    command: "sed 's/old/new/g' file.txt"
  - description: "In-place edit with backup"
    command: "sed -i.bak 's/foo/bar/g' config.txt"
  - description: "Delete lines matching a pattern"
    command: "sed '/^#/d' config.conf"
  - description: "Print lines 10-20"
    command: "sed -n '10,20p' file.txt"
  - description: "Delete trailing whitespace"
    command: "sed 's/[[:space:]]*$//' file.txt"
  - description: 'Darkiros UTILS: Replace multiple space to one'
    command: sed -e 's/  */ /g'
  - description: 'Darkiros UTILS: Remove the last char'
    command: sed 's/.$//'
  - description: Preview a file edit, via substitution.
    command: sudo sed 's/Name=Xfce Session/Name=Xfce_Session/' FILE
  - description: Replace the same string more than once per line (g flag)
    command: sudo sed 's/Name=Xfce Session/Name=Xfce_Session/g' FILE
  - description: Edit a file (adding -i flag), in-place; changes are made to the file(s).
    command: sudo sed -i 's/Name=Xfce Session/Name=Xfce_Session/' FILE
  - description: It can become necessary to escape special characters in your string.
    command: sed -i 's/\/path\/to\/somewhere\//\/path\/to\/anotherplace\//' FILE
  - description: Change your sed delimiter to a pipe to avoid escaping slashes.
    command: sed -i 's|/path/to/somewhere/|/path/to/anotherplace/|' FILE
  - description: Print 2nd line
    command: sed -n '2p' FILE
  - description: Print lines from 2 till 9
    command: sed -n '2,9p' FILE
  - description: Print lines starting from one having pattern "any" till line number
      17
    command: sed -n '/any/,17p' FILE
  - description: Print lines starting from the beginning, quit after printing 3rd
      line
    command: sed -n 'p;3q'
  - description: Print and quit at 5th line
    command: sed -n '5{p;q}' FILE
  - description: Print lines starting from the one having pattern "strstart" till
      the line having pattern "strend"
    command: sed -n '/strstart/,/strend/p' FILE
  - description: Print the last line
    command: sed -n '$p' FILE
  - description: Replace tabs with 4 spaces (changes are written to file itself)
    command: sed -i 's/\t/    /g' FILE
  - description: Replace CRLF with LF (convert DOS/Windows line endings to Linux line
      endings)
    command: sed -i  's/\r$//g' FILE
  - description: Insert CR (carriage return) character before LF (line feed) character
      (Linux to DOS/Windows line endings conversion)
    command: sed -i 's/$/\r/' FILE
  - description: Remove trailing spaces (changes are written to file itself)
    command: sed -i -E "s/\s+$//g" FILE
  - description: Remove empty lines (changes are written to file itself)
    command: sed -i -E "/^\s*$/d" FILE
  - description: Anonymize original MAC address of an Ethernet device in ifconfig's
      output (match 6 pairs of hexadecimal numbers with an optional trailing ":")
    command: ifconfig | sed -E "/ether/ s/([0-9a-f]{2}:{0,1}){6}/00:00:00:00:00:00/g"
  - description: Rearrange order of %Y,%m,%d in `date`s output by matching groups
      of characters
    command: date '+%Y-%m-%d' | sed -E "s/([0-9]{4})-([0-9]{2})-([0-9]{2})/\3-\2-\1/"
references:
  - label: "GNU Sed manual"
    url: "https://www.gnu.org/software/sed/manual/"
  - label: "Sed one-liners"
    url: "https://sed.sourceforge.io/sed1line.txt"
install:
    - method: apt
      package_name: "sed"
      commands:
        - "apt-get install -y sed"
    - method: brew
      package_name: "gnu-sed"
      commands:
        - "brew install gnu-sed"
---

# Sed — Stream Editor

Sed is a non-interactive stream editor that performs text transformations on input streams. It's ideal for automated text processing in scripts and pipelines, particularly find-and-replace operations.

## Substitution

```bash
# Basic substitution (first match per line)
sed 's/pattern/replacement/' file.txt

# Global substitution (all matches)
sed 's/pattern/replacement/g' file.txt

# Case-insensitive
sed 's/pattern/replacement/gi' file.txt

# Replace only on specific lines
sed '3s/pattern/replacement/' file.txt
sed '10,20s/pattern/replacement/g' file.txt
```

## Line Operations

```bash
# Delete lines
sed '5d' file.txt               # Delete line 5
sed '/^$/d' file.txt             # Delete empty lines
sed '/^#/d' file.txt             # Delete comments

# Print specific lines
sed -n '5p' file.txt             # Print line 5 only
sed -n '/error/p' file.txt       # Print lines containing 'error'

# Insert and append
sed '2i\inserted line' file.txt  # Insert before line 2
sed '2a\appended line' file.txt  # Append after line 2
```

## In-Place Editing

```bash
# Edit file directly (BSD/macOS requires space)
sed -i '' 's/foo/bar/g' file.txt     # macOS
sed -i 's/foo/bar/g' file.txt         # Linux

# Create backup
sed -i.bak 's/foo/bar/g' file.txt
```

## Multiple Commands

```bash
# Chain with -e
sed -e 's/foo/bar/' -e '/^$/d' file.txt

# Chain with semicolons
sed 's/foo/bar/; /^$/d' file.txt

# From a script file
sed -f script.sed file.txt
```

## Related Tools

- **[awk](../process/awk.md)** — Field-oriented text processing
- **[grep](../../search/grep.md)** — Pattern search and filtering
- **[tr](../../transform/tr.md)** — Character translation
- **[cut](../../transform/cut.md)** — Field extraction
