---
id: security-reverse-ropgadget
namespace: security:reverse:ropgadget
name: ropgadget
description: Tool for finding ROP (Return-Oriented Programming) gadgets in binaries for building ROP chains.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - rop.gadget.find
  - binary.analysis
  - exploit.development
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
  - pwntools
  - pwndbg
  - ropper
workflow_edges:
  produces:
    - rop-gadgets
    - rop-chain
  consumes:
    - binary
contract:
  inputs:
    - type: file.binary
      description: Binary to search for gadgets
  outputs:
    - type: rop.gadget.list
      description: List of ROP gadgets found
      mime: text/plain
    - type: rop.gadget.json
      description: ROP gadgets in JSON format
      mime: application/json
  side_effects: []
  resource_cost:
    cpu: medium
    memory_mb: 256
    network: low
    disk_io: low
resource_profile:
  cpu: medium
  memory_mb: 256
  network: low
  disk_io: low
allowed-tools:
  - ROPgadget
  - python3
  - Bash
  - execFile
parameters:
  - name: binary
    type: string
    required: false
    description: "Binary file to analyze for gadgets"
    aliases:
      - --binary
  - name: rawArch
    type: string
    required: false
    description: "Raw architecture (e.g., x86, arm, mips)"
    aliases:
      - --rawArch
  - name: rawMode
    type: string
    required: false
    description: "Raw mode (e.g., 32, 64)"
    aliases:
      - --rawMode
  - name: opcode
    type: string
    required: false
    description: "Only search for specific opcodes"
    aliases:
      - --opcode
  - name: all
    type: boolean
    required: false
    description: "Show all gadgets (not just unique)"
    aliases:
      - --all
  - name: badbytes
    type: string
    required: false
    description: "Bytes to exclude from gadgets"
    aliases:
      - --badbytes
  - name: depth
    type: integer
    required: false
    description: "Maximum gadget depth in instructions"
    aliases:
      - --depth
  - name: thumb
    type: boolean
    required: false
    description: "Use ARM Thumb mode"
    aliases:
      - --thumb
  - name: json
    type: boolean
    required: false
    description: "Output in JSON format"
    aliases:
      - --json
  - name: console
    type: boolean
    required: false
    description: "Use interactive console"
    aliases:
      - --console
execution:
  template: "ROPgadget --binary {binary}"
  sandbox: execFile
  timeout_seconds: 300
  shell: false
global_vars:
  binary: ""
examples:
  - description: "Find all gadgets in a binary"
    command: ROPgadget --binary /bin/ls
  - description: "Filter gadgets excluding bad bytes"
    command: ROPgadget --binary /bin/ls --badbytes 0a
  - description: "Raw mode gadget search for ARM"
    command: ROPgadget --rawArch arm --rawMode 32 --binary firmware.bin
  - description: "Output gadgets as JSON"
    command: ROPgadget --binary /bin/ls --json
  - description: "Search for specific opcodes"
    command: ROPgadget --binary /bin/ls --opcode c3
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

# ROPgadget — ROP Gadget Finder

ROPgadget scans executables and libraries to find useful gadgets for Return-Oriented Programming (ROP) exploits. It supports ELF, PE, Mach-O, and raw binary formats across multiple architectures.

## Example Output

```
0x0000000000410ff3 : add byte ptr [rax], al ; jmp 0x410ff0
0x0000000000411dbf : pop rax ; ret
0x0000000000411dc0 : pop rdi ; ret
0x0000000000411dc2 : pop rsi ; ret
0x0000000000411dc4 : pop rdx ; ret
```

## Usage Tips

- Use `--badbytes` to filter out gadgets containing null bytes or newlines
- Combine with pwntools' `ROP()` class for automated chain building
- Use `--depth` to find longer gadget sequences
