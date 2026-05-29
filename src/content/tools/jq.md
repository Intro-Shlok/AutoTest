---
id: text-process-jq
namespace: text:process:jq
name: jq
description: Lightweight and flexible command-line JSON processor for querying, filtering,
  and transforming JSON data.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - text.transform.json
  - text.query.jsonpath
  - data.format.pretty
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
  - yq
  - jc
  - fx
artifacts:
  - type: application.json
    description: JSON input data for transformation
    mime: application/json
    trust_level: verified
  - type: text.plain
    description: Plain text output from JSON query
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - formatted-output
  consumes:
    - raw-json
contract:
  inputs:
    - type: application.json
      description: JSON data to query or transform
      mime: application/json
  outputs:
    - type: text.plain
      description: Query result as plain text
      mime: text/plain
    - type: application.json
      description: Transformed JSON output
      mime: application/json
  side_effects:
    - none
  resource_cost:
    cpu: low
    memory_mb: 64
    network: none
    disk_io: low
allowed-tools:
  - jq
  - Bash
  - execFile

parameters:
  - name: null-input
    type: string
    required: false
    description: "use `null` as the single input value"
    aliases:
      - -n
      - --null-input
  - name: raw-input
    type: string
    required: false
    description: "read each line as string instead of JSON"
    aliases:
      - -R
      - --raw-input
  - name: slurp
    type: string
    required: false
    description: "read all inputs into an array and use it as"
    aliases:
      - -s
      - --slurp
  - name: compact-output
    type: string
    required: false
    description: "compact instead of pretty-printed output"
    aliases:
      - -c
      - --compact-output
  - name: raw-output
    type: string
    required: false
    description: "output strings without escapes and quotes"
    aliases:
      - -r
      - --raw-output
  - name: raw-output0
    type: string
    required: false
    description: "implies -r and output NUL after each output"
    aliases:
      - --raw-output0
  - name: join-output
    type: string
    required: false
    description: "implies -r and output without newline after"
    aliases:
      - -j
      - --join-output
  - name: ascii-output
    type: string
    required: false
    description: "output strings by only ASCII characters"
    aliases:
      - -a
      - --ascii-output
  - name: sort-keys
    type: string
    required: false
    description: "sort keys of each object on output"
    aliases:
      - -S
      - --sort-keys
  - name: color-output
    type: string
    required: false
    description: "colorize JSON output"
    aliases:
      - -C
      - --color-output
  - name: monochrome-output
    type: string
    required: false
    description: "disable colored output"
    aliases:
      - -M
      - --monochrome-output
  - name: tab
    type: string
    required: false
    description: "use tabs for indentation"
    aliases:
      - --tab
  - name: indent
    type: string
    required: false
    description: "use n spaces for indentation (max 7 spaces)"
    aliases:
      - --indent
  - name: unbuffered
    type: string
    required: false
    description: "flush output stream after each output"
    aliases:
      - --unbuffered
  - name: stream
    type: string
    required: false
    description: "parse the input value in streaming fashion"
    aliases:
      - --stream
  - name: stream-errors
    type: string
    required: false
    description: "implies --stream and report parse error as"
    aliases:
      - --stream-errors
  - name: seq
    type: string
    required: false
    description: "parse input/output as application/json-seq"
    aliases:
      - --seq
  - name: from-file
    type: string
    required: false
    description: "load the filter from a file"
    aliases:
      - -f
      - --from-file
  - name: library-path
    type: file
    required: false
    description: "search modules from the directory"
    aliases:
      - -L
      - --library-path
  - name: arg
    type: string
    required: false
    description: "set $name to the string value"
    aliases:
      - --arg
  - name: argjson
    type: string
    required: false
    description: "--slurpfile name file set $name to an array of JSON values read
      from the file; --rawfile name file set $name to string contents of file; --args
      consume remaining arguments as positional string valu..."
    aliases:
      - --argjson
  - name: exit-status
    type: string
    required: false
    description: "set exit status code based on the output"
    aliases:
      - -e
      - --exit-status
  - name: version
    type: string
    required: false
    description: "show the version"
    aliases:
      - -V
      - --version
  - name: build-configuration
    type: string
    required: false
    description: "show jq's build configuration"
    aliases:
      - --build-configuration
  - name: help
    type: string
    required: false
    description: "show the help"
    aliases:
      - -h
      - --help
features:
  - local
  - pipes-stdin
  - pipes-stdout
  - batch
  - process-manip
  - output-json
techniques:
  - data-manipulation
  - analysis
execution:
  template: "jq {null-input} {raw-input} {slurp} {compact-output} {raw-output}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
examples:
  - description: "Extract specific fields from JSON array"
    command: "cat data.json | jq '.items[] | {id: .id, name: .name}'"
  - description: "Pretty-print JSON with colored output"
    command: "echo '{\"key\": \"value\"}' | jq ."
  - description: "Count items in a JSON array"
    command: "cat data.json | jq '.items | length'"
  - description: 'Output a JSON file, in pretty-print format:'
    command: jq
  - description: 'Output all elements from arrays (or all key-value pairs from objects)
      in a JSON file:'
    command: jq .[]
  - description: Use jq to pretty-print JSON
    command: jq '.' file.json
  - description: Filter JSON object by extracting a specific field
    command: jq '.fieldName' file.json
  - description: Filter JSON array to extract specific element by index
    command: jq '.[index]' file.json
  - description: Select multiple fields from JSON
    command: "jq '{field1: .field1, field2: .field2}' file.json"
  - description: Use jq to count the number of elements in an array
    command: jq '.arrayName | length' file.json
  - description: Apply a function to each element in a JSON array
    command: jq '.arrayName[] | .fieldName' file.json
  - description: Parse JSON from stdin
    command: cat file.json | jq '.fieldName'
  - description: Use jq to filter JSON objects by condition
    command: jq 'select(.fieldName == "value")' file.json
  - description: Modify JSON field value
    command: jq '.fieldName = "newValue"' file.json
  - description: Load JSON from URL
    command: curl -s "http://example.com/file.json" | jq '.fieldName'
  - description: Combine operations and select elements from different levels
    command: "jq '.[] | {id: .id, name: .info.name}' file.json"
  - description: Query nested JSON data
    command: jq '.outerField.innerField' file.json
  - description: Concatenate fields
    command: jq '.field1 + " " + .field2' file.json
  - description: Group by a particular field
    command: jq 'group_by(.fieldName)' file.json
  - description: Sort JSON objects by field
    command: jq 'sort_by(.fieldName)' file.json
  - description: Use jq to find unique values
    command: jq 'unique' file.json
  - description: Print keys and values of a JSON object
    command: "jq 'to_entries | .[] | \"\\(.key): \\(.value)\"' file.json"
  - description: Output compact JSON without whitespace
    command: jq -c '.' file.json
  - description: Use jq to delete a field
    command: jq 'del(.fieldName)' file.json
  - description: Combine data from two JSON files
    command: jq -s '.[0] + .[1]' file1.json file2.json
  - description: 'Read JSON objects from a file into an array, and output it (inverse
      of jq .[]):'
    command: jq --slurp
  - description: 'Output the first element in a JSON file:'
    command: jq .[0]
  - description: 'Output the value of a given key of the first element in a JSON file:'
    command: jq .[0].key_name
  - description: 'Output the value of a given key of each element in a JSON file:'
    command: jq 'map(.key_name)'
  - description: Extract as stream of values instead of a list
    command: jq '.[] | .foo'
  - description: Slicing
    command: jq '.[1:2]'
  - description: Dictionary subset shorthand
    command: jq 'map({ a, b })'
  - description: Converting arbitrary data to json
    command: jq -r '(map(keys) | add | unique | sort) as $cols \
  - description: 'cheat.sheets: jq'
    command: "| .[] as $row | $cols | map($row[.]) | @csv'"
  - description: Filter a list of objects
    command: jq 'map(select(.name == "foo"))'
  - description: Add + 1 to all items
    command: jq 'map(.+1)'
  - description: Delete 2 items
    command: jq 'del(.[1, 2])'
  - description: Concatenate arrays
    command: jq 'add'
  - description: Flatten an array
    command: jq 'flatten'
  - description: Create a range of numbers
    command: jq '[range(2;4)]'
  - description: Display the type of each item
    command: jq 'map(type)'
  - description: Sort an array of basic type
    command: jq 'sort'
  - description: Sort an array of objects
    command: jq 'sort_by(.foo)'
  - description: Sort lines of a file
    command: jq --slurp '. | sort | .[]'
  - description: Group by a key - opposite to flatten
    command: jq 'group_by(.foo)'
  - description: Minimum value of an array
    command: jq 'min'
  - description: Remove duplicates
    command: jq 'unique'
  - description: or
    command: jq 'unique_by(.foo)'
  - description: or
    command: jq 'unique_by(length)'
  - description: Reverse an array
    command: jq 'reverse'
  - description: URL Encode something
    command: date | jq -sRr @uri
  - description: 'To create proper JSON from a shell script and properly escape variables:'
    command: jq -n --arg foobaz "$FOOBAZ" '{"foobaz":$foobaz}'
  - description: To fill environment variables from JSON object keys (e.g. $FOO from
      jq query ".foo")
    command: export $(jq -r '@sh "FOO=\(.foo) BAZ=\(.baz)"')
  - description: Parsing json
    command: jq 'with_entries(.value |= fromjson)' --sort-keys
  - description: Serializing json
    command: jq 'with_entries(.value |= tojson)' --sort-keys
  - description: Converting to csv
    command: jq '.[] | [.foo, .bar] | @csv' -r
references:
  - label: "jq manual"
    url: "https://jqlang.github.io/jq/manual/"
  - label: "jq playground"
    url: "https://jqplay.org/"
install:
    - method: apt
      package_name: "jq"
      commands:
        - "apt-get install -y jq"
    - method: brew
      package_name: "jq"
      commands:
        - "brew install jq"
---

# jq — Command-line JSON Processor

jq is a lightweight and flexible command-line JSON processor. It uses a domain-specific language (DSL) for querying, filtering, and transforming JSON data with the power of functional programming constructs.

## Core Concepts

jq operates on a stream of JSON values, applying a filter expression to each input value. Filters can:

- **Select** specific fields: `.key`, `.[]`
- **Transform** structures: `{new: .old}`
- **Filter** arrays: `select(.age > 18)`
- **Aggregate**: `length`, `add`, `group_by`
- **Build** new objects: `{name, total: .items | length}`

## Pipeline Integration

jq is designed for Unix pipeline composition:

```bash
curl https://api.example.com/data | jq '.results[] | {id, name, status}' > results.txt
```

This makes jq the canonical converter between `application.json` and `text.plain` artifact types.

## Common Transform Patterns

| Pattern | Command | Description |
|---------|---------|-------------|
| Pretty-print | `jq .` | Format JSON with indentation |
| Extract field | `jq '.field'` | Get single field value |
| Array to lines | `jq -r '.[]'` | Output each element on its own line |
| Object projection | `jq '{id, name}'` | Create new object with subset of fields |
| Conditional | `jq 'select(.status == "ok")'` | Filter by condition |
