---
id: security-forensics-volatility
namespace: security:forensics:volatility
name: volatility
description: Advanced memory forensics framework for analyzing RAM dumps, extracting processes, network connections, registry hives, and artifacts.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - memory.analysis.process
  - memory.analysis.network
  - memory.analysis.registry
  - memory.analysis.dump
  - forensics.memory.acquisition
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
dependencies:
  - python3
related_tools:
  - autopsy
  - binwalk
  - foremost
artifacts:
  - type: memory.dump.raw
    description: Raw memory dump file
    mime: application/octet-stream
    trust_level: verified
  - type: forensics.report.json
    description: Volatility analysis results in JSON
    mime: application/json
    trust_level: verified
  - type: forensics.report.text
    description: Volatility analysis results in text
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - memory-analysis
    - process-list
    - network-connections
    - registry-hives
    - hash-dump
  consumes:
    - memory-dump
    - plugin-path
contract:
  inputs:
    - type: memory.dump.file
      description: Path to the memory dump file
    - type: forensics.plugin
      description: Volatility plugin to execute (e.g. windows.pslist)
    - type: directory.path
      description: Path to additional plugin directory
  outputs:
    - type: forensics.report.text
      description: Plugin output as plain text
      mime: text/plain
    - type: forensics.report.json
      description: Plugin output as JSON
      mime: application/json
  side_effects:
    - filesystem_write
    - filesystem_write
  resource_cost:
    cpu: high
    memory_mb: 2048
    network: none
    disk_io: high
resource_profile:
  cpu: high
  memory_mb: 2048
  network: none
  disk_io: high
allowed-tools:
  - volatility
  - Bash
  - execFile
parameters:
  - name: flag-f
    type: file
    required: true
    description: "Memory dump file to analyze"
    aliases:
      - -f
      - --file
  - name: flag-p
    type: string
    required: false
    description: "Additional plugin directory path"
    aliases:
      - -p
      - --plugin-path
  - name: flag-r
    type: integer
    required: false
    description: "Recursion depth for layered plugins"
    default_value: "0"
    aliases:
      - -r
      - --recursion
  - name: flag-v
    type: integer
    required: false
    description: "Verbosity level (1-5)"
    default_value: "1"
    aliases:
      - -v
      - --verbose
  - name: flag-q
    type: boolean
    required: false
    description: "Quiet mode — suppress output except errors"
    aliases:
      - -q
      - --quiet
  - name: flag-y
    type: string
    required: false
    description: "YARA rule file for scanning"
    aliases:
      - -y
      - --yara
  - name: flag-l
    type: boolean
    required: false
    description: "List all available plugins"
    aliases:
      - -l
      - --list-plugins
  - name: flag-s
    type: integer
    required: false
    description: "Session ID to resume or manage"
    aliases:
      - -s
      - --sessions
  - name: flag-c
    type: file
    required: false
    description: "Configuration file path"
    aliases:
      - -c
      - --config
  - name: flag-o
    type: string
    required: false
    description: "Output format (text, json, sqlite)"
    default_value: "text"
    aliases:
      - -o
      - --output
  - name: single-location
    type: string
    required: false
    description: "Single memory location to scan"
    aliases:
      - --single-location
  - name: physical
    type: boolean
    required: false
    description: "Use physical address space"
    aliases:
      - --physical
  - name: output-dir
    type: string
    required: false
    description: "Directory for output files"
    aliases:
      - --output-dir
  - name: flag-i
    type: boolean
    required: false
    description: "Display information about the memory dump"
    aliases:
      - -i
      - --info
  - name: plugin
    type: string
    required: false
    description: "Plugin to run (e.g. windows.pslist, windows.netscan)"
    aliases:
      - windows.info
      - windows.pslist
      - windows.netscan
      - windows.hivelist
      - windows.hashdump
      - linux.bash
      - linux.pslist
      - mac.pslist
execution:
  template: "volatility -f {memory-dump} {plugin}"
  sandbox: execFile
  timeout_seconds: 600
  shell: false
global_vars:
  memory-dump: memory.raw
  plugin: windows.pslist
examples:
  - description: "List running processes from a Windows memory dump"
    command: volatility -f memory.raw windows.pslist
  - description: "Scan network connections from a memory dump"
    command: volatility -f memory.raw windows.netscan
  - description: "Dump registry hives from a memory dump"
    command: volatility -f memory.raw windows.hivelist
  - description: "Extract password hashes from a memory dump"
    command: volatility -f memory.raw windows.hashdump
  - description: "List available plugins"
    command: volatility -l
  - description: "Show memory dump info and profile suggestion"
    command: volatility -f memory.raw windows.info
  - description: "List bash history from a Linux memory dump"
    command: volatility -f linux.mem linux.bash
  - description: "Use custom plugin directory"
    command: volatility -f memory.raw -p /opt/volatility_plugins windows.pslist
references:
  - label: "Volatility 3 GitHub"
    url: "https://github.com/volatilityfoundation/volatility3"
  - label: "Volatility Documentation"
    url: "https://volatility3.readthedocs.io/"
phase: enumeration
techniques:
  - discovery
items:
  - NoCreds
services: []
attack_types:
  - Discovery
---
# Volatility — Memory Forensics Framework

Volatility is an advanced open-source memory forensics framework written in Python. It analyzes RAM dumps from Windows, Linux, and macOS systems to extract running processes, open network connections, loaded kernel modules, registry hives, and other critical forensic artifacts.

## Key Features

- **Cross-platform**: Supports Windows, Linux, and macOS memory dumps
- **Plugin architecture**: Dozens of analysis plugins included
- **No dependency on live system**: Works entirely from a memory capture
- **Extensible**: Custom plugins can be written in Python

## Common Plugins

| Plugin | Purpose |
|--------|---------|
| `windows.pslist` | List running processes |
| `windows.netscan` | Scan network connections |
| `windows.hivelist` | Show registry hives |
| `windows.hashdump` | Extract password hashes |
| `windows.info` | Show dump metadata |
| `linux.bash` | Recover bash history |
| `mac.pslist` | List macOS processes |
