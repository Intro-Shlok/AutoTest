---
id: security-reverse-checksec
namespace: security:reverse:checksec
name: checksec
description: Binary hardening checker that reports PIE, NX, RELRO, Stack Canary, and other security mitigations on ELF binaries.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - binary.security.check
  - hardening.analysis
  - mitigation.detection
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
  - pwntools
  - ropgadget
  - gdb
workflow_edges:
  produces:
    - security-report
    - mitigation-summary
  consumes:
    - binary
contract:
  inputs:
    - type: file.binary
      description: ELF binary to check
  outputs:
    - type: report.security
      description: Security mitigation analysis
      mime: text/plain
    - type: report.json
      description: Security report in JSON
      mime: application/json
  side_effects: []
  resource_cost:
    cpu: low
    memory_mb: 32
    network: low
    disk_io: low
resource_profile:
  cpu: low
  memory_mb: 32
  network: low
  disk_io: low
allowed-tools:
  - checksec
  - python3
  - Bash
  - execFile
parameters:
  - name: file
    type: string
    required: false
    description: "Check security on a specific binary file"
    aliases:
      - --file
  - name: elf
    type: integer
    required: false
    description: "Check security of a process by PID"
    aliases:
      - --elf
  - name: proc
    type: integer
    required: false
    description: "Check /proc/PID/exe security"
    aliases:
      - --proc
  - name: debug
    type: boolean
    required: false
    description: "Enable debug output"
    aliases:
      - --debug
  - name: kernel
    type: boolean
    required: false
    description: "Check kernel security mitigations"
    aliases:
      - --kernel
  - name: output
    type: string
    required: false
    description: "Write output to file"
    aliases:
      - --output
  - name: format
    type: string
    required: false
    description: "Output format (json or csv)"
    aliases:
      - --format
  - name: listCheck
    type: boolean
    required: false
    description: "List all available checks"
    aliases:
      - --list-check
execution:
  template: "checksec --file={binary}"
  sandbox: execFile
  timeout_seconds: 30
  shell: false
global_vars:
  binary: ""
examples:
  - description: "Check security of a binary"
    command: checksec --file=/bin/ls
  - description: "Check running process security"
    command: checksec --proc 1234
  - description: "Output JSON format"
    command: checksec --file=/bin/ls --format=json
  - description: "Check kernel security mitigations"
    command: checksec --kernel
  - description: "Check multiple binaries"
    command: checksec --file=/bin/ls --file=/bin/bash --format=json
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
    - method: pip
      package_name: "checksec"
      commands:
        - "pip install checksec"
---

# checksec — Binary Security Hardening Checker

checksec analyzes ELF binaries and reports on the security mitigations they employ. It is essential for understanding which exploitation techniques may be viable against a given target.

## Mitigations Checked

| Mitigation | Description | Bypass Difficulty |
|------------|-------------|-------------------|
| PIE | Position Independent Executable | Medium |
| NX | Non-Executable Stack | Medium |
| RELRO | Relocation Read-Only | Low-High |
| Stack Canary | Stack Overflow Protection | Medium |
| FORTIFY | Fortified Source Functions | Low |

## Example Output

```
RELRO           STACK CANARY      NX            PIE             RPATH    RUNPATH    Symbols         FORTIFY    Fortified    Fortifiable    FILE
Full RELRO      Canary found      NX enabled    PIE enabled     No RPATH No RUNPATH   76) Symbols      Yes       5            18             /bin/ls
```
