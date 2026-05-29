---
id: security-reverse-gdb
namespace: security:reverse:gdb
name: gdb
description: GNU Project debugger for analyzing program execution, reverse engineering binaries, and debugging crashes.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - reverse.debugging
  - reverse.disassembly
  - reverse.analysis
  - debug.memory.inspect
  - debug.register.inspect
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
  - radare2
  - ltrace
  - strace
  - pwndbg
  - pwntools
workflow_edges:
  produces:
    - disassembly
    - stack-traces
    - register-dumps
  consumes:
    - binary
    - core-dump
contract:
  inputs:
    - type: file.binary
      description: Binary to debug
    - type: file.core
      description: Core dump file for post-mortem analysis
  outputs:
    - type: debug.backtrace
      description: Stack backtrace
      mime: text/plain
    - type: debug.disassembly
      description: Disassembled code
      mime: text/plain
  side_effects:
    - process_spawn
  resource_cost:
    cpu: medium
    memory_mb: 128
    network: low
    disk_io: low
resource_profile:
  cpu: medium
  memory_mb: 128
  network: low
  disk_io: low
allowed-tools:
  - gdb
  - Bash
  - execFile
parameters:
  - name: quiet
    type: boolean
    required: false
    description: "Suppress introductory banner and warnings"
    aliases:
      - -q
  - name: ex
    type: string
    required: false
    description: "Execute a single GDB command"
    aliases:
      - -ex
  - name: x
    type: string
    required: false
    description: "Execute GDB commands from file"
    aliases:
      - -x
  - name: pid
    type: integer
    required: false
    description: "Attach to a running process by PID"
    aliases:
      - -p
  - name: batch
    type: boolean
    required: false
    description: "Run in batch mode (no interactive shell)"
    aliases:
      - -batch
  - name: symbols
    type: string
    required: false
    description: "Read symbol table from file"
    aliases:
      - -s
      - --symbols
  - name: exec
    type: string
    required: false
    description: "Use specified file as the executable"
    aliases:
      - --exec
  - name: core
    type: string
    required: false
    description: "Use specified file as the core dump"
    aliases:
      - --core
  - name: cd
    type: string
    required: false
    description: "Change to directory before starting"
    aliases:
      - --cd
  - name: nx
    type: boolean
    required: false
    description: "Do not read .gdbinit file"
    aliases:
      - -nx
  - name: nh
    type: boolean
    required: false
    description: "Do not read .gdbearlyinit file"
    aliases:
      - -nh
  - name: tty
    type: string
    required: false
    description: "Set the terminal for GDB I/O"
    aliases:
      - --tty
execution:
  template: "gdb -q -ex \"{command}\" {binary}"
  sandbox: execFile
  timeout_seconds: 300
  shell: false
global_vars:
  binary: ""
  command: ""
examples:
  - description: "Attach to a running process"
    command: gdb -p 1234
  - description: "Analyze a core dump"
    command: gdb /bin/ls core.dump -batch -ex bt
  - description: "Disassemble main function in batch mode"
    command: gdb -q -batch -ex "disassemble main" /bin/ls
  - description: "Run with commands from a file"
    command: gdb -x commands.gdb /bin/ls
  - description: "Inspect registers and memory"
    command: gdb -q -ex "info registers" -ex "x/16xw \$rsp" -batch /bin/ls
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
      package_name: "gdb"
      commands:
        - "apt-get install -y gdb"
---

# GDB — GNU Debugger

GDB is the standard debugger for compiled Unix programs, supporting C, C++, Rust, Go, and many other languages. It enables instruction-level debugging, memory/register inspection, disassembly, and reverse engineering.

## Common Debugging Commands

| Command | Description |
|---------|-------------|
| `disassemble main` | Disassemble the main function |
| `info registers` | Show CPU register values |
| `x/16xw $rsp` | Examine 16 words on the stack |
| `bt` | Print backtrace |
| `break *0x400510` | Set breakpoint at address |
| `ni` | Execute next instruction |
| `si` | Step into instruction |

## Batch Analysis

```bash
gdb -q -batch -ex "file /bin/ls" -ex "disassemble main" -ex "info functions"
```
