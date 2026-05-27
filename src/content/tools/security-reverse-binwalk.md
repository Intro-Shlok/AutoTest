---
id: security-reverse-binwalk
namespace: security:reverse:binwalk
name: binwalk
description: Firmware analysis tool for extracting filesystems, identifying embedded files, and scanning binary blobs for signatures.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - firmware.analysis
  - file.extraction
  - signature.scanning
  - binary.forensics
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
dependencies: []
related_tools:
  - foremost
  - volatility
  - strings
  - hexdump
workflow_edges:
  produces:
    - extracted-files
    - firmware-report
    - entropy-graph
  consumes:
    - firmware-file
    - binary-blob
contract:
  inputs:
    - type: file.binary
      description: Firmware or binary blob to analyze
  outputs:
    - type: file.extracted
      description: Extracted files and filesystems
      mime: application/octet-stream
    - type: report.signature
      description: Signature scan report
      mime: text/plain
  side_effects:
    - filesystem_write
  resource_cost:
    cpu: medium
    memory_mb: 512
    network: low
    disk_io: high
resource_profile:
  cpu: medium
  memory_mb: 512
  network: low
  disk_io: high
allowed-tools:
  - binwalk
  - python3
  - Bash
  - execFile
parameters:
  - name: extract
    type: boolean
    required: false
    description: "Extract files automatically"
    aliases:
      - -e
  - name: matryoshka
    type: boolean
    required: false
    description: "Recursively extract embedded filesystems"
    aliases:
      - -M
  - name: remove
    type: boolean
    required: false
    description: "Remove extracted file after scanning"
    aliases:
      - -r
  - name: depth
    type: integer
    required: false
    description: "Maximum recursion depth"
    aliases:
      - -d
  - name: include
    type: string
    required: false
    description: "Only scan for matching signatures"
    aliases:
      - -y
  - name: exclude
    type: string
    required: false
    description: "Exclude matching signatures"
    aliases:
      - -x
  - name: signature
    type: boolean
    required: false
    description: "Perform signature scanning"
    aliases:
      - -S
      - --signature
  - name: entropy
    type: boolean
    required: false
    description: "Calculate file entropy"
    aliases:
      - --entropy
  - name: opcodes
    type: boolean
    required: false
    description: "Identify CPU opcodes in firmware"
    aliases:
      - --opcodes
  - name: dd
    type: string
    required: false
    description: "Dump region to file (type:offset:size)"
    aliases:
      - --dd
  - name: csv
    type: boolean
    required: false
    description: "Output in CSV format"
    aliases:
      - -c
  - name: json
    type: boolean
    required: false
    description: "Output in JSON format"
    aliases:
      - -j
execution:
  template: "binwalk -e {firmware-file}"
  sandbox: execFile
  timeout_seconds: 600
  shell: false
global_vars:
  firmware-file: ""
examples:
  - description: "Extract firmware filesystems"
    command: binwalk -e firmware.bin
  - description: "Recursive extraction with all nested filesystems"
    command: binwalk -Me firmware.bin
  - description: "Signature scan only, no extraction"
    command: binwalk firmware.bin
  - description: "Entropy analysis of firmware blob"
    command: binwalk --entropy firmware.bin
  - description: "Scan with opcode identification"
    command: binwalk --opcodes firmware.bin
  - description: "JSON output with entropy calculation"
    command: binwalk -j --entropy firmware.bin
phase: exploitation
techniques:
  - discovery
  - execution
items:
  - NoCreds
services: []
attack_types:
  - Exploitation
  - Discovery
---

# Binwalk — Firmware Analysis Tool

Binwalk is a firmware analysis tool that scans binary files for embedded files and filesystems using signature matching. It can extract filesystems (Squashfs, JFFS2, etc.), identify compression types, and perform entropy analysis.

## Key Features

- **Signature scanning**: Detects hundreds of file signatures
- **Filesystem extraction**: Automatically extracts Squashfs, Cramfs, JFFS2, and more
- **Entropy analysis**: Identifies encrypted or compressed regions
- **Opcode detection**: Identifies CPU architecture of embedded code

## Typical Workflow

```bash
# Step 1: Scan for signatures
binwalk firmware.bin

# Step 2: Extract discovered filesystems
binwalk -Me firmware.bin

# Step 3: Analyze entropy for hidden regions
binwalk --entropy firmware.bin
```
