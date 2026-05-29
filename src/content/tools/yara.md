---
id: security-malware-yara
namespace: security:malware:yara
name: yara
description: Pattern matching swiss knife for malware researchers to identify and classify malware samples based on textual or binary patterns.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - malware.analyze
  - malware.classify
  - malware.detect
  - forensics.scan
  - binary.pattern.match
platforms:
  - linux
  - macos
  - windows
  - cross-platform
risk_level: low
trust_level: verified
execution_policy: enabled
architectures:
  - amd64
  - arm64
dependencies: []
related_tools:
  - binwalk
  - volatility
  - radare2
  - ghidra
artifacts:
  - type: report.txt
    description: YARA scan results
    mime: text/plain
    trust_level: verified
  - type: report.json
    description: YARA scan results in JSON
    mime: application/json
    trust_level: verified
workflow_edges:
  produces:
    - scan-results
    - matched-rules
  consumes:
    - target-file
    - rule-file
contract:
  inputs:
    - type: file.path
      description: File or directory to scan
    - type: security.rule.file
      description: YARA rule file to apply
  outputs:
    - type: report.txt
      description: Scan results with matched rules
      mime: text/plain
    - type: report.json
      description: Scan results in JSON format
      mime: application/json
  side_effects:
    - filesystem_write
  resource_cost:
    cpu: medium
    memory_mb: 256
    network: none
    disk_io: medium
resource_profile:
  cpu: medium
  memory_mb: 256
  network: none
  disk_io: medium
allowed-tools:
  - yara
  - Bash
  - execFile
parameters:
  - name: rule-file
    type: string
    required: true
    description: "YARA rule file or directory"
  - name: target
    type: string
    required: true
    description: "File, directory, or PID to scan"
  - name: flag-s
    type: boolean
    required: false
    description: "Print strings that matched"
    aliases:
      - -s
      - --print-strings
  - name: flag-m
    type: boolean
    required: false
    description: "Print meta data"
    aliases:
      - -m
      - --print-meta
  - name: flag-n
    type: boolean
    required: false
    description: "Print only rule names"
    aliases:
      - -n
      - --negate
  - name: flag-g
    type: integer
    required: false
    description: "Number of tags to print"
    aliases:
      - -g
      - --tag
  - name: flag-r
    type: boolean
    required: false
    description: "Recursive directory scan"
    aliases:
      - -r
      - --recursive
  - name: flag-c
    type: boolean
    required: false
    description: "Print count of matches"
    aliases:
      - -c
      - --count
  - name: flag-p
    type: integer
    required: false
    description: "Number of parallel threads"
    aliases:
      - -p
      - --threads
execution:
  template: "yara {flags} {rule-file} {target}"
  sandbox: execFile
  timeout_seconds: 300
  shell: false
examples:
  - description: "Scan a file with a YARA rule"
    command: yara rule.yara suspicious.exe
  - description: "Scan a directory recursively"
    command: yara -r malware_rules/ /samples/
  - description: "Print matched strings"
    command: yara -s myrule.yar sample.bin
  - description: "Scan with multiple rule files"
    command: yara -r rules/ -c sample.exe
  - description: "Scan a running process by PID"
    command: yara rule.yara <PID>
references:
  - label: "YARA Official Site"
    url: "https://virustotal.github.io/yara/"
  - label: "YARA GitHub"
    url: "https://github.com/VirusTotal/yara"
  - label: "YARA Documentation"
    url: "https://yara.readthedocs.io/"
phase: forensics
techniques:
  - analysis
  - discovery
items:
  - NoCreds
services: []
attack_types:
  - Discovery
install:
    - method: apt
      package_name: "yara"
      commands:
        - "apt-get install -y yara"
    - method: brew
      package_name: "yara"
      commands:
        - "brew install yara"
---

# YARA — Malware Pattern Matching

YARA is a pattern matching tool designed for malware researchers to create descriptions of malware families based on textual or binary patterns. Rules consist of strings definitions and boolean expressions that determine the logic.

## Rule Structure

```yara
rule ExampleRule {
    meta:
        description = "Example YARA rule"
        author = "Researcher"
    strings:
        $text_string = "malicious_string"
        $hex_string = { 4D 5A 90 00 }
        $byte_string = "This program" nocase
    condition:
        $text_string or $hex_string
}
```

## Common Commands

```bash
# Scan files with rules
yara -s rules.yara /path/to/malware.exe

# Recursive directory scan
yara -r /path/to/rules/ /samples/directory/

# Scan with metadata output
yara -m rules.yara suspicious.bin
```
