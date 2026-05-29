---
id: security-ioc-loki
namespace: security:ioc:loki
name: loki
description: IOC (Indicator of Compromise) scanner that checks files and systems against threat intelligence feeds and YARA rules for malware detection.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - ioc.scan.file
  - ioc.scan.system
  - ioc.detect.malware
  - ioc.yara.match
  - ioc.threat-intel
platforms:
  - linux
  - macos
  - windows
  - cross-platform
risk_level: medium
trust_level: verified
execution_policy: enabled
architectures:
  - amd64
  - arm64
dependencies:
  - python3
related_tools:
  - yara
  - grep
  - threatstream
artifacts:
  - type: ioc.scan.report
    description: IOC scan results
    mime: text/plain
    trust_level: verified
  - type: ioc.scan.json
    description: JSON format scan results
    mime: application/json
    trust_level: verified
workflow_edges:
  produces:
    - ioc-findings
    - scan-report
  consumes:
    - target-path
    - ioc-rules
contract:
  inputs:
    - type: file.path
      description: Path to scan (file or directory)
    - type: ioc.rules
      description: Path to IOC rules or YARA rules
  outputs:
    - type: ioc.scan.report
      description: Scan results with matched IOCs
      mime: text/plain
    - type: ioc.scan.json
      description: JSON format findings
      mime: application/json
  side_effects: []
  resource_cost:
    cpu: medium
    memory_mb: 256
    network: low
    disk_io: medium
resource_profile:
  cpu: medium
  memory_mb: 256
  network: low
  disk_io: medium
allowed-tools:
  - loki
  - python3
  - Bash
  - execFile
parameters:
  - name: path
    type: string
    required: true
    description: "Path to scan (file or directory)"
    aliases:
      - -p
      - --path
  - name: flag-rules
    type: string
    required: false
    description: "Path to custom rules directory"
    aliases:
      - -r
      - --rules
  - name: flag-yara
    type: string
    required: false
    description: "YARA rule file or directory"
    aliases:
      - -y
      - --yara-rules
  - name: flag-ioc
    type: string
    required: false
    description: "IOC checkbox file"
    aliases:
      - --ioc
  - name: flag-score
    type: integer
    required: false
    description: "Minimum score threshold"
    aliases:
      - -s
      - --score
  - name: flag-output
    type: string
    required: false
    description: "Output file path"
    aliases:
      - -o
      - --output
  - name: flag-format
    type: string
    required: false
    description: "Output format (text, json, syslog)"
    aliases:
      - -f
      - --format
  - name: flag-nobeeps
    type: boolean
    required: false
    description: "Disable beep on alert"
    aliases:
      - --nobeeps
  - name: flag-no-progress
    type: boolean
    required: false
    description: "Disable progress bar"
    aliases:
      - --no-progress
  - name: flag-verbose
    type: boolean
    required: false
    description: "Verbose output"
    aliases:
      - -v
      - --verbose
execution:
  template: "python3 loki.py {flag-yara} {flag-rules} {flag-ioc} {flag-score} {flag-output} {flag-format} {flag-nobeeps} {flag-no-progress} {flag-verbose} -p {path}"
  sandbox: execFile
  timeout_seconds: 600
  shell: false
examples:
  - description: "Basic scan with default rules"
    command: python3 loki.py -p /path/to/scan
  - description: "Scan with custom YARA rules"
    command: python3 loki.py -p /path/to/scan -y rules.yar
  - description: "Scan with custom IOC rules"
    command: python3 loki.py -p /path/to/scan -r /path/to/ioc-rules
  - description: "JSON output with score threshold"
    command: python3 loki.py -p /path/to/scan -s 100 -f json -o results.json
references:
  - label: "Loki IOC Scanner GitHub"
    url: "https://github.com/Neo23x0/Loki"
phase: enumeration
techniques:
  - discovery
  - collection
items:
  - NoCreds
services: []
attack_types:
  - Discovery
  - Enumeration
install:
    - method: git
      repo_url: "https://github.com/Neo23x0/Loki.git"
      commands:
        - "git clone https://github.com/Neo23x0/Loki.git"
        - "cd Loki && pip install -r requirements.txt"
---

# Loki — IOC Scanner

Loki is an IOC (Indicator of Compromise) scanner that checks files and systems against threat intelligence feeds, YARA rules, and other IOC sources. It's designed for incident response and malware detection.

## Usage

```bash
# Basic scan
python3 loki.py -p /path/to/scan

# With custom YARA rules
python3 loki.py -p /path/to/scan -y rules.yar

# With custom IOC rules directory
python3 loki.py -p /path/to/scan -r /path/to/ioc-rules

# JSON output with minimum score
python3 loki.py -p /path/to/scan -s 100 -f json -o results.json
```