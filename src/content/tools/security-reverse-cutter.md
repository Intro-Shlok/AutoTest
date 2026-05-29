---
id: security-reverse-cutter
namespace: security:reverse:cutter
name: cutter
description: Qt-based GUI for radare2 providing disassembly, decompilation (via Ghidra/rz-ghidra), and debugging capabilities.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - reverse.disassembly
  - reverse.decompilation
  - reverse.debugging
  - reverse.analysis
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
  - ghidra
  - gdb
workflow_edges:
  produces:
    - disassembly
    - decompiled-code
    - analysis-graphs
  consumes:
    - binary
contract:
  inputs:
    - type: file.binary
      description: Binary file to analyze
  outputs:
    - type: analysis.disassembly
      description: Disassembled instruction listing
      mime: text/plain
    - type: analysis.decompiled
      description: Decompiled pseudo-C code
      mime: text/plain
  side_effects:
    - process_spawn
  resource_cost:
    cpu: medium
    memory_mb: 512
    network: low
    disk_io: medium
resource_profile:
  cpu: medium
  memory_mb: 512
  network: low
  disk_io: medium
allowed-tools:
  - cutter
  - Bash
  - execFile
parameters:
  - name: autoAnalyze
    type: boolean
    required: false
    description: "Automatically analyze the binary on open"
    aliases:
      - -A
  - name: noSave
    type: boolean
    required: false
    description: "Do not save project on exit"
    aliases:
      - -z
  - name: writeMode
    type: boolean
    required: false
    description: "Open file in write mode for patching"
    aliases:
      - -w
  - name: arch
    type: string
    required: false
    description: "Set target architecture"
    aliases:
      - -a
  - name: bits
    type: integer
    required: false
    description: "Set CPU bits (32 or 64)"
    aliases:
      - -b
  - name: file
    type: string
    required: false
    description: "Binary file to open"
execution:
  template: "cutter {binary}"
  sandbox: execFile
  timeout_seconds: 600
  shell: false
global_vars:
  binary: ""
examples:
  - description: "Open binary in Cutter GUI"
    command: cutter /bin/ls
  - description: "Open with auto-analysis enabled"
    command: cutter -A /bin/ls
  - description: "Open in write mode for patching"
    command: cutter -w /bin/ls
  - description: "Open with specific architecture setting"
    command: cutter -a arm -b 32 firmware.bin
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
    - method: apt
      package_name: "cutter"
      commands:
        - "apt-get install -y cutter"
---

# Cutter — radare2 GUI

Cutter is a free and open-source reverse engineering platform powered by radare2. It provides a Qt-based graphical interface with disassembly, graph views, decompilation (via Ghidra's decompiler through rz-ghidra), and integrated debugging.

## Key Views

- **Disassembly**: Linear and graph-based instruction views
- **Decompiler**: Pseudo-C output via Ghidra decompiler integration
- **Hexdump**: Raw hex and structured data view
- **Debugger**: Integrated debugging with breakpoints and memory inspection

## Features

- Scriptable via Python and JavaScript
- Multiple architecture support through radare2 backend
- Project management for saving analysis state
- Plugin ecosystem for extensibility
