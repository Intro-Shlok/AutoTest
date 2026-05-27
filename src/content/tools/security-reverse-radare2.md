---
id: security-reverse-radare2
namespace: security:reverse:radare2
name: radare2
description: Advanced reverse engineering framework for binary analysis, disassembly, debugging, and patching with scriptable console.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - reverse.disassembly
  - reverse.analysis
  - reverse.debugging
  - reverse.patching
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
  - cutter
  - ghidra
  - gdb
  - rizin
workflow_edges:
  produces:
    - disassembly
    - analysis-metadata
    - decompiled-code
  consumes:
    - binary
contract:
  inputs:
    - type: file.binary
      description: Binary file to analyze
  outputs:
    - type: analysis.disassembly
      description: Disassembled code listing
      mime: text/plain
    - type: analysis.metadata
      description: Binary analysis metadata
      mime: application/json
  side_effects:
    - filesystem_write
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
  - radare2
  - Bash
  - execFile
parameters:
  - name: analyze
    type: boolean
    required: false
    description: "Automatically analyze the binary after loading"
    aliases:
      - -A
  - name: debug
    type: boolean
    required: false
    description: "Start in debug mode"
    aliases:
      - -d
  - name: quiet
    type: boolean
    required: false
    description: "Quiet mode (suppress banners)"
    aliases:
      - -q
  - name: write
    type: boolean
    required: false
    description: "Open file in write mode for patching"
    aliases:
      - -w
  - name: script
    type: string
    required: false
    description: "Run commands from script file"
    aliases:
      - -i
  - name: command
    type: string
    required: false
    description: "Run a single command and exit"
    aliases:
      - -c
  - name: project
    type: string
    required: false
    description: "Use a project file"
    aliases:
      - -p
  - name: seek
    type: string
    required: false
    description: "Seek to a specific address"
    aliases:
      - -s
  - name: bits
    type: integer
    required: false
    description: "Set CPU bits (32 or 64)"
    aliases:
      - -b
  - name: arch
    type: string
    required: false
    description: "Set target architecture"
    aliases:
      - -a
  - name: eval
    type: string
    required: false
    description: "Evaluate a configuration variable"
    aliases:
      - -e
execution:
  template: "radare2 -A {binary}"
  sandbox: execFile
  timeout_seconds: 600
  shell: false
global_vars:
  binary: ""
  command: ""
examples:
  - description: "Analyze a binary and open interactive shell"
    command: radare2 -A /bin/ls
  - description: "Analyze and run commands non-interactively"
    command: radare2 -A -q -c "afl" /bin/ls
  - description: "Open binary in debug mode"
    command: radare2 -d /bin/ls
  - description: "Open with write mode for patching"
    command: radare2 -w /bin/ls
  - description: "Specify architecture and bits"
    command: radare2 -a arm -b 32 firmware.bin
  - description: "Run script against binary"
    command: radare2 -A -i analyze.r2 /bin/ls
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

# radare2 — Reverse Engineering Framework

radare2 is a portable reverse engineering framework providing a complete toolchain for binary analysis, disassembly, debugging, and patching. It features a powerful scriptable console, supports dozens of architectures, and can be extended via plugins.

## Key Commands

| Command | Action |
|---------|--------|
| `afl` | List all functions |
| `pdf @sym.main` | Print disassembly of main |
| `VV` | Visual graph mode |
| `pxr @ rsp` | Show stack references |
| `iz` | List strings in data section |

## Common Workflows

```bash
# Analyze and list functions
radare2 -A -q -c "afl" /bin/ls

# Disassemble main function
radare2 -A -q -c "s sym.main; pdf" /bin/ls
```
