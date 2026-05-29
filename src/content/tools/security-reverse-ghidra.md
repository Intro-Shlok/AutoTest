---
id: security-reverse-ghidra
namespace: security:reverse:ghidra
name: ghidra
description: NSA's reverse engineering framework with disassembly, decompilation, debugging, and scriptable analysis.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - reverse.disassembly
  - reverse.decompilation
  - reverse.debugging
  - reverse.analysis
  - reverse.scripting
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
  - radare2
  - cutter
  - gdb
  - ida
workflow_edges:
  produces:
    - disassembly
    - decompiled-code
    - analysis-results
  consumes:
    - binary
contract:
  inputs:
    - type: file.binary
      description: Binary file for analysis
  outputs:
    - type: analysis.decompiled
      description: Decompiled source code
      mime: text/plain
    - type: analysis.disassembly
      description: Disassembled instruction listing
      mime: text/plain
  side_effects:
    - filesystem_write
    - process_spawn
  resource_cost:
    cpu: high
    memory_mb: 4096
    network: low
    disk_io: high
resource_profile:
  cpu: high
  memory_mb: 4096
  network: low
  disk_io: high
allowed-tools:
  - ghidra
  - Bash
  - execFile
parameters:
  - name: import
    type: string
    required: false
    description: "Import a binary file into a new project"
    aliases:
      - -import
  - name: process
    type: string
    required: false
    description: "Process a specific program in an existing project"
    aliases:
      - -process
  - name: analysisTimeoutPerFile
    type: integer
    required: false
    description: "Timeout in seconds for analysis per file"
    aliases:
      - -analysisTimeoutPerFile
  - name: recursive
    type: boolean
    required: false
    description: "Recursively import files in directories"
    aliases:
      - -recursive
  - name: readOnly
    type: boolean
    required: false
    description: "Open project in read-only mode"
    aliases:
      - -readOnly
  - name: preScript
    type: string
    required: false
    description: "Script to run before analysis"
    aliases:
      - -preScript
  - name: postScript
    type: string
    required: false
    description: "Script to run after analysis"
    aliases:
      - -postScript
  - name: scriptPath
    type: string
    required: false
    description: "Path to script directories"
    aliases:
      - -scriptPath
  - name: propertiesPath
    type: string
    required: false
    description: "Path to project properties file"
    aliases:
      - -propertiesPath
  - name: maxMemory
    type: string
    required: false
    description: "Maximum memory for the JVM (e.g. 4G)"
    aliases:
      - -maxMemory
  - name: ghidraRun
    type: string
    required: false
    description: "Path to the ghidraRun script (launcher)"
    aliases:
      - ghidraRun
  - name: ghidraHeadless
    type: string
    required: false
    description: "Path to the headless analyzer script"
    aliases:
      - ghidraHeadless
execution:
  template: "ghidra"
  sandbox: execFile
  timeout_seconds: 3600
  shell: false
global_vars:
  binary: ""
  project: ""
  output_dir: "./ghidra_out"
examples:
  - description: "Launch Ghidra GUI"
    command: ghidra
  - description: "Headless import and analyze a binary"
    command: ghidraHeadless /tmp/project TestProject -import /bin/ls -analysisTimeoutPerFile 300
  - description: "Headless analysis with pre and post scripts"
    command: ghidraHeadless /tmp/project TestProject -process /bin/ls -preScript PreScript.java -postScript PostScript.java -scriptPath /scripts
  - description: "Recursive import with read-only mode"
    command: ghidraHeadless /tmp/project TestProject -recursive -readOnly -import /firmware/dir
  - description: "Run with custom memory limit"
    command: ghidra -maxMemory 8G
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
install:
    - method: git
      repo_url: "https://github.com/NationalSecurityAgency/ghidra.git"
      commands:
        - "git clone https://github.com/NationalSecurityAgency/ghidra.git"
---

# Ghidra — NSA Reverse Engineering Framework

Ghidra is a full-featured reverse engineering platform developed by the NSA. It provides disassembly, decompilation, debugging, and scriptable program analysis capabilities with support for multiple processor architectures and file formats.

## Key Features

- **Decompiler**: Converts assembly to pseudo-C for easier analysis
- **Multi-architecture**: x86, ARM, MIPS, PowerPC, RISC-V, and many more
- **Scriptable**: Python and Java scripting APIs for automation
- **Collaborative**: Multi-user project support for team analysis
- **Headless mode**: Automated batch analysis without GUI

## Modes

| Mode | Command | Description |
|------|---------|-------------|
| GUI | `ghidra` | Launch the graphical interface |
| Headless | `ghidraHeadless <project> <name> -import <file>` | Batch analysis without GUI |
| Scripting | `ghidraHeadless ... -preScript <script>` | Automated script execution |

## Common Headless Workflow

```bash
# Create project and import binary
ghidraHeadless /tmp/proj MyProject -import target.bin

# Analyze with custom scripts
ghidraHeadless /tmp/proj MyProject -process target.bin -preScript analyze.py
```
