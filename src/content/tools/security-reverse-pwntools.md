---
id: security-reverse-pwntools
namespace: security:reverse:pwntools
name: pwntools
description: Python CTF framework and exploit development library for binary exploitation, shellcode generation, and ROP chain building.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - exploit.development
  - shellcode.generation
  - rop.chain
  - binary.analysis
  - reverse.patching
platforms:
  - linux
  - macos
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
  - gdb
  - ropgadget
  - checksec
  - pwndbg
workflow_edges:
  produces:
    - exploit-script
    - shellcode
    - rop-chain
  consumes:
    - binary
contract:
  inputs:
    - type: file.binary
      description: Binary to analyze
  outputs:
    - type: exploit.script
      description: Python exploit script
      mime: text/x-python
    - type: exploit.shellcode
      description: Generated shellcode bytes
      mime: application/octet-stream
  side_effects:
    - process_spawn
    - network_traffic
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
  - python3
  - Bash
  - execFile
parameters:
  - name: checksec
    type: boolean
    required: false
    description: "Check binary security hardening (via checksec script)"
    aliases:
      - checksec
  - name: asm
    type: string
    required: false
    description: "Assemble instructions to bytes"
    aliases:
      - asm
  - name: disasm
    type: string
    required: false
    description: "Disassemble bytes to instructions"
    aliases:
      - disasm
  - name: cyclic
    type: integer
    required: false
    description: "Generate cyclic pattern of given length"
    aliases:
      - cyclic
  - name: hex
    type: string
    required: false
    description: "Convert bytes to hex string"
    aliases:
      - hex
  - name: unhex
    type: string
    required: false
    description: "Convert hex string to bytes"
    aliases:
      - unhex
  - name: constgrep
    type: string
    required: false
    description: "Search for constants by regex"
    aliases:
      - constgrep
  - name: errno
    type: string
    required: false
    description: "Look up errno values"
    aliases:
      - errno
  - name: update
    type: boolean
    required: false
    description: "Update pwntools to the latest version"
    aliases:
      - update
execution:
  template: "python3 -c \"from pwn import *; {command}\""
  sandbox: execFile
  timeout_seconds: 120
  shell: false
global_vars:
  binary: ""
  command: ""
examples:
  - description: "Check binary security mitigations"
    command: python3 -m pwn checksec /bin/ls
  - description: "Generate cyclic pattern"
    command: python3 -c "from pwn import *; print(cyclic(100))"
  - description: "Disassemble bytes"
    command: python3 -c "from pwn import *; print(disasm(b'\\x90\\x90'))"
  - description: "Assemble instructions"
    command: python3 -c "from pwn import *; print(asm('nop'))"
  - description: "Convert hex to bytes and back"
    command: python3 -c "from pwn import *; print(unhex('48656c6c6f')); print(hex(b'Hello'))"
  - description: "Build and send a ROP chain"
    command: python3 exploit.py
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

# pwntools — CTF Exploit Development Framework

pwntools is a Python library designed for CTF (Capture The Flag) binary exploitation. It streamlines common tasks such as assembling shellcode, building ROP chains, connecting to remote services, and debugging exploits locally.

## Key Modules

| Module | Purpose |
|--------|---------|
| `pwn.asm` | Assemble and disassemble instructions |
| `pwn.elf` | ELF binary parsing and patching |
| `pwn.rop` | Automatic ROP chain building |
| `pwn.shellcraft` | Shellcode template generation |
| `pwn.cyclic` | Pattern generation for offset discovery |

## Common Pattern

```python
from pwn import *

elf = ELF('./vuln')
rop = ROP(elf)
rop.call('system', [next(elf.search(b'/bin/sh'))])
io = process('./vuln')
io.sendline(rop.chain())
io.interactive()
```
