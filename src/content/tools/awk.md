---
id: text-process-awk
namespace: text:process:awk
name: awk
description: Pattern scanning and text processing language for field-oriented data
  extraction, reporting, and transformation.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - text.process.field
  - text.aggregate.count
  - text.aggregate.average
  - text.process.report
  - data.transform.column
  - text.transform.csv
  - text.aggregate.sum
  - security.execution.command
  - security.privilege-escalation.shell
  - system.file.read
  - system.file.write
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
  - perl
  - sed
  - tr
  - system-file-tr
  - text-process-sed
  - text-search-grep
artifacts:
  - type: text.transformed
    description: Processed text output
    mime: text/plain
    trust_level: verified
  - type: data.report
    description: Formatted report
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - processed-output
    - formatted-report
  consumes:
    - input-data
    - awk-script
contract:
  inputs:
    - type: text.plain
      description: Input text for processing
    - type: text.awk.script
      description: Awk script or expression
  outputs:
    - type: text.transformed
      description: Processed text output
      mime: text/plain
  side_effects: []
  resource_cost:
    cpu: low
    memory_mb: 16
    network: none
    disk_io: low
resource_profile:
  cpu: low
  memory_mb: 16
  network: none
  disk_io: low
allowed-tools:
  - awk
  - gawk
  - nawk
  - Bash
  - execFile

parameters:
  - name: flag-f
    type: string
    required: false
    description: "--file=progfile"
    aliases:
      - -f
  - name: flag-F
    template_key: flag-f
    type: string
    required: false
    description: "--field-separator=fs"
    aliases:
      - -F
  - name: flag-v
    type: string
    required: false
    description: "--assign=var=val"
    aliases:
      - -v
  - name: flag-b
    type: string
    required: false
    description: "--characters-as-bytes"
    aliases:
      - -b
  - name: flag-c
    type: string
    required: false
    description: "--traditional"
    aliases:
      - -c
  - name: flag-d
    type: string
    required: false
    description: "--dump-variables[=file]"
    aliases:
      - -d
  - name: flag-D
    template_key: flag-d
    type: string
    required: false
    description: "--debug[=file]"
    aliases:
      - -D
  - name: flag-e
    type: string
    required: false
    description: "--source='program-text'"
    aliases:
      - -e
      - -t
  - name: flag-E
    template_key: flag-e
    type: string
    required: false
    description: "--exec=file"
    aliases:
      - -E
  - name: flag-g
    type: string
    required: false
    description: "--gen-pot"
    aliases:
      - -g
  - name: flag-h
    type: string
    required: false
    description: "--help"
    aliases:
      - -h
  - name: flag-i
    type: string
    required: false
    description: "--include=includefile"
    aliases:
      - -i
  - name: flag-k
    type: string
    required: false
    description: "--csv"
    aliases:
      - -k
  - name: flag-l
    type: string
    required: false
    description: "--load=library"
    aliases:
      - -l
  - name: flag-L
    template_key: flag-l
    type: string
    required: false
    description: "--lint[=fatal|invalid|no-ext]"
    aliases:
      - -L
      - -e
  - name: flag-n
    type: string
    required: false
    description: "--non-decimal-data"
    aliases:
      - -n
  - name: flag-o
    type: string
    required: false
    description: "--pretty-print[=file]"
    aliases:
      - -o
  - name: flag-p
    type: string
    required: false
    description: "--profile[=file]"
    aliases:
      - -p
  - name: flag-r
    type: number
    required: false
    description: "--re-interval"
    aliases:
      - -r
  - name: flag-s
    type: string
    required: false
    description: "--no-optimize"
    aliases:
      - -s
  - name: flag-t
    type: string
    required: false
    description: "--lint-old"
    aliases:
      - -t
  - name: exec-expression
    description: Execute shell command via system() or print|/bin/sh
    type: string
  - name: getline-variable
    description: Read file content into variable via getline < file
    type: string
features:
  - batch
  - pipes-stdout
  - process-manip
  - local
  - pipes-stdin
  - file-system
  - output-json
techniques:
  - analysis
  - data-manipulation
  - command-and-control
  - collection
  - execution
  - privilege-escalation
execution:
  template: "awk {flag-f} {flag-f} {flag-v} {flag-b} {flag-c}"
  sandbox: execFile
  timeout_seconds: 60
  shell: false
examples:
  - description: "Print specific columns from a file"
    command: "awk '{print $1, $3}' file.txt"
  - description: "Print with custom field separator (CSV)"
    command: "awk -F',' '{print $1, $2}' data.csv"
  - description: "Filter rows by column value"
    command: "awk '$3 > 100 {print $1, $3}' data.txt"
  - description: "Compute sum of a column"
    command: "awk '{sum += $2} END {print sum}' data.txt"
  - description: "Print formatted report with headers"
    command: "awk 'BEGIN {print \"Name\\tScore\"} {print $1 \"\\t\" $2}' data.txt"
  - description: "Count lines per category"
    command: "awk '{count[$1]++} END {for (c in count) print c, count[c]}' data.txt"
  - description: Can be used to execute arbitrary commands on a system and spawn shells.
    command: awk 'BEGIN{system("/bin/sh")}'
  - description: Can be used to execute arbitrary commands on a system.
    command: "awk 'BEGIN {system(\"ls\"); exit}' /dev/null\n"
  - description: The file must exist and command will be executed as many rows there
      are in the file.
    command: "awk 'system(\"ls\")' /etc/passwd\n"
  - description: If spaces cannot be inserted, we can use `sprintf(%c,32)` to emulate
      them.
    command: "awk '//{}BEGIN{system(sprintf(\"uname%c-aa\",32))}'\n"
  - description: Read an arbitrary file.
    command: "awk 'BEGIN{while((getline line<\"/etc/passwd\")>0){print line}}' /dev/null\n"
  - description: 'Argument injection: execute arbitrary command: Can be used to execute
      arbitrary commands on a system.'
    command: awk 'BEGIN {system("ls"); exit}' /dev/null
  - description: 'Argument injection: execute arbitrary command: The file must exist
      and command will be executed as many rows there are in the file.'
    command: awk 'system("ls")' /etc/passwd
  - description: 'Argument injection: execute arbitrary command: If spaces cannot
      be inserted, we can use `sprintf(%c,32)` to emulate them.'
    command: awk '//{}BEGIN{system(sprintf("uname%c-aa",32))}'
  - description: 'Argument injection: read local file: Read an arbitrary file.'
    command: awk 'BEGIN{while((getline line<"/etc/passwd")>0){print line}}' /dev/null
  - description: 'Argument injection: read local file: Print the contents of multiple
      files.'
    command: awk '//' /etc/passwd /etc/hostname /root/.ssh/id_rsa
  - description: 'Argument injection: write to local file: Write to an arbitrary file'
    command: awk 'BEGIN{print "ssh-rsa ..." > "/root/.ssh/authorized_keys}' /dev/null
  - description: Sum integers from a file or STDIN, one integer per line.
    command: printf '1\n2\n3\n' | awk '{sum += $1} END {print sum}'
  - description: Using specific character as separator to sum integers from a file
      or STDIN.
    command: printf '1:2:3' | awk -F ":" '{print $1+$2+$3}'
  - description: Print line number 12 of file.txt
    command: awk 'NR==12' file.txt
  - description: Print first field for each record in file.txt
    command: awk '{print $1}' file.txt
  - description: 'cheat.sheets: awk'
    command: Print only lines that match regex in file.txt
  - description: 'cheat.sheets: awk'
    command: awk '/regex/' file.txt
  - description: Print only lines that do not match regex in file.txt
    command: awk '!/regex/' file.txt
  - description: Print any line where field 2 is equal to "foo" in file.txt
    command: awk '$2 == "foo"' file.txt
  - description: Print lines where field 2 is NOT equal to "foo" in file.txt
    command: awk '$2 != "foo"' file.txt
  - description: Print line if field 1 matches regex in file.txt
    command: awk '$1 ~ /regex/' file.txt
  - description: Print line if field 1 does NOT match regex in file.txt
    command: awk '$1 !~ /regex/' file.txt
  - description: Print lines with more than 80 characters in file.txt
    command: awk 'length > 80' file.txt
  - description: Print a multiplication table.
    command: awk -v RS='' '
  - description: 'cheat.sheets: awk'
    command: '{'
  - description: 'cheat.sheets: awk'
    command: for(i=1;i<=NF;i++){
  - description: 'cheat.sheets: awk'
    command: printf("%dx%d=%d%s", i, NR, i*NR, i==NR?"\n":"\t")
  - description: 'cheat.sheets: awk'
    command: '}'
  - description: 'cheat.sheets: awk'
    command: '}'
  - description: 'cheat.sheets: awk'
    command: "' <<< \"$(seq 9 | sed 'H;g')\""
  - description: Specify output separator character.
    command: printf '1 2 3' | awk 'BEGIN {OFS=":"}; {print $1,$2,$3}'
  - description: Search paragraph for the given REGEX match. Paragraphs will be collapsed
      together.
    command: awk -v RS='' '/42B/' file
  - description: Search paragraph for the given REGEX match. Paragraphs will be separated
      with a new line.
    command: awk -v RS= ORS='\n\n' '/42B/' file
  - description: Display only first field in text taken from STDIN.
    command: echo 'Field_1  Field_2  Field_3' | awk '{print $1}'
  - description: Use AWK solo; without the need for something via STDIN.
    command: awk 'BEGIN {print("Example text.")}'
  - description: Access environment variables from within AWK.
    command: awk 'BEGIN {print ENVIRON["LS_COLORS"]}'
  - description: Count number of lines taken from STDIN.
    command: free | awk '{L++} END {print(L)}'
  - description: Cleaner, more efficient approach to the above.
    command: free | awk 'END {print(NR)}'
  - description: Output unique list of available sections under which to create a
      DEB package.
    command: awk '!A[$1]++ {print($1)}' <<< "$(dpkg-query --show -f='${Section}\n')"
  - description: Using process substitution (`<()` is NOT command substitution), with
      AWK and its associative array variables, we can print just column 2 for lines
      whose first column is equal to what's between the double-quotes.
    command: awk '{NR != 1 && A[$1]=$2} END {print(A["Mem:"])}' <(free -h)
  - description: While below is an easier and simpler solution to the above, it's
      not at all the same, and in other cases, the above is definitely preferable.
    command: awk '/^Mem:/ {print($2)}' <(free -h)
  - description: Output list of unique uppercase-only, sigil-omitted variables used
      in FILE.
    command: awk '
  - description: 'cheat.sheets: awk'
    command: '{'
  - description: 'cheat.sheets: awk'
    command: for(F=0; F<NF; F++){
  - description: 'cheat.sheets: awk'
    command: if($F~/^\$[A-Z_]+$/){
  - description: 'cheat.sheets: awk'
    command: A[$F]++
  - description: 'cheat.sheets: awk'
    command: '}'
  - description: 'cheat.sheets: awk'
    command: '}'
  - description: 'cheat.sheets: awk'
    command: '}'
  - description: 'cheat.sheets: awk'
    command: END {
  - description: 'cheat.sheets: awk'
    command: for(I in A){
  - description: 'cheat.sheets: awk'
    command: X=substr(I, 2, length(I))
  - description: 'cheat.sheets: awk'
    command: printf("%s\n", X)
  - description: 'cheat.sheets: awk'
    command: '}'
  - description: 'cheat.sheets: awk'
    command: '}'
  - description: 'cheat.sheets: awk'
    command: "' FILE"
  - description: Output only lines from FILE between PATTERN_1 and PATTERN_2. Good
      for logs.
    command: awk '/PATTERN_1/,/PATTERN_2/ {print}' FILE
  - description: Pretty-print a table of an overview of the non-system users on the
      system.
    command: awk -F ':' '
  - description: 'cheat.sheets: awk'
    command: BEGIN {
  - description: 'cheat.sheets: awk'
    command: printf("%-17s %-4s %-4s %-s\n", "NAME", "UID", "GID", "SHELL")
  - description: 'cheat.sheets: awk'
    command: '}'
  - description: 'cheat.sheets: awk'
    command: $3 >= 1000 && $1 != "nobody" {
  - description: 'cheat.sheets: awk'
    command: printf("%-17s %-d %-d %-s\n", $1, $3, $4, $7)
  - description: 'cheat.sheets: awk'
    command: '}'
  - description: 'cheat.sheets: awk'
    command: "' /etc/passwd"
  - description: Display the total amount of MiB of RAM available in the machine.
      This is also a painful but useful workaround to get the units comma-separated,
      as would be doable with Bash's own `printf` built-in.
    command: awk '/^MemTotal:/ {printf("%'"'"'dMiB\n", $2 / 1024)}'
  - description: It's possible to sort strings in AWK, as well as uniq-ing, meaning
      you can replace uniq(1) and sort(1) calls with just the one call of AWK. Granted,
      you can use `sort -u` to do both, but AWK offers much more functionality. Unlike
      when using AWK to uniq-ify, uniq(1) only works by adjacency, meaning the duplicate
      lines must be adjacent to one another for them to be handled.
    command: awk '
  - description: 'cheat.sheets: awk'
    command: '{'
  - description: 'cheat.sheets: awk'
    command: '!Lines[$0]++'
  - description: 'cheat.sheets: awk'
    command: '}'
  - description: 'cheat.sheets: awk'
    command: END {
  - description: 'cheat.sheets: awk'
    command: asorti(Lines, Sorted)
  - description: 'cheat.sheets: awk'
    command: for (Line in Sorted) {
  - description: 'cheat.sheets: awk'
    command: print(Sorted[Line])
  - description: 'cheat.sheets: awk'
    command: '}'
  - description: 'cheat.sheets: awk'
    command: '}'
  - description: 'cheat.sheets: awk'
    command: "' FILE"
  - description: Remove duplicate lines
    command: awk '!seen[$0]++' file.txt
  - description: Remove all empty lines
    command: awk 'NF > 0' file.txt
references:
  - label: "GNU Awk manual"
    url: "https://www.gnu.org/software/gawk/manual/"
  - label: "Awk one-liners"
    url: "https://awk.info/?tip/oneliner"
---

# Awk — Text Processing Language

Awk is a powerful text processing language designed for field-oriented data extraction, reporting, and transformation. It's ideal for processing structured text files like logs, CSVs, and tables.

## Core Concepts

Awk programs follow the pattern: `pattern { action }`

- **pattern** — Condition that determines which records to process
- **action** — What to do with matching records

### Built-in Variables

| Variable | Meaning |
|----------|---------|
| `$0` | Entire current line |
| `$1`, `$2`, ... | First, second, ... field |
| `NF` | Number of fields in current record |
| `NR` | Current record number (line number) |
| `FS` | Field separator (default: whitespace) |
| `OFS` | Output field separator |

## Common Patterns

### Field Extraction
```bash
# Print columns 1, 3, and last
awk '{print $1, $3, $NF}' file.txt

# With header
awk 'BEGIN {print "Name\tValue"} {print $1, $2}' data.txt

# Custom separator
awk -F: '{print $1, $3}' /etc/passwd
```

### Filtering
```bash
# Lines where column 3 > 100
awk '$3 > 100' data.txt

# Lines matching regex
awk '/error/' log.txt

# Combined conditions
awk '$1 ~ /^192\.168/ && $3 > 1000' access.log
```

### Aggregation
```bash
# Sum column
awk '{sum += $2} END {print sum}' data.txt

# Average
awk '{sum += $2; count++} END {print sum/count}' data.txt

# Group by category
awk '{count[$1]++} END {for (k in count) print k, count[k]}' data.txt
```

## Related Tools

- **[sed](../process/sed.md)** — Stream editor for substitutions
- **[grep](../../search/grep.md)** — Pattern search
- **[cut](../../transform/cut.md)** — Simple column extraction
- **[jq](../process/jq.md)** — JSON-specific processor
