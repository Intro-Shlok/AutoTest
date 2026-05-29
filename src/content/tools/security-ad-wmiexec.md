---
id: security-ad-wmiexec
namespace: security:ad:wmiexec
name: wmiexec
description: Impacket tool for semi-interactive remote command execution over Windows Management Instrumentation (WMI) without deploying services or agents.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - security.lateral.wmi
  - security.execution.remote
  - security.shell.remote
  - security.ad.service.control
  - security.credential.pth
platforms:
  - linux
  - cross-platform
risk_level: high
trust_level: verified
execution_policy: enabled
architectures:
  - amd64
  - arm64
dependencies:
  - python3
  - impacket
related_tools:
  - impacket
  - psexec
  - evil-winrm
  - netexec
phase: exploitation
techniques:
  - execution
  - lateral-movement
items:
  - NoCreds
  - Hash
services:
  - SMB
  - RPC
attack_types:
  - Execution
  - LateralMovement
contract:
  inputs:
    - type: network.target.ip
      description: Target Windows host IP
    - type: credential.username
      description: Username for authentication
    - type: credential.password
      description: Plaintext password or NTLM hash
    - type: domain.name
      description: Target domain name
  outputs:
    - type: command.output
      description: Remote command execution output
      mime: text/plain
    - type: session.shell
      description: Semi-interactive shell session
      mime: text/plain
  side_effects:
    - network_traffic
    - process_spawn
  resource_cost:
    cpu: low
    memory_mb: 64
    network: low
    disk_io: none
resource_profile:
  cpu: low
  memory_mb: 64
  network: low
  disk_io: none
allowed-tools:
  - wmiexec
  - impacket
  - python3
  - Bash
  - execFile
parameters:
  - name: target
    type: string
    required: true
    description: "Target host in format: domain/username:password@host"
  - name: command
    type: string
    required: false
    description: "Command to execute (if omitted, opens a semi-interactive shell)"
  - name: flag-share
    type: string
    required: false
    description: "SMB share to use (default: ADMIN$)"
    aliases:
      - -share
  - name: flag-nooutput
    type: boolean
    required: false
    description: "Do not retrieve command output"
    aliases:
      - -nooutput
  - name: flag-comspec
    type: string
    required: false
    description: "Windows cmd.exe path (default: cmd.exe)"
    aliases:
      - -comspec
  - name: flag-silentcommand
    type: boolean
    required: false
    description: "Use silent command mode"
    aliases:
      - -silentcommand
execution:
  template: "python3 /usr/share/doc/python3-impacket/examples/wmiexec.py {target} {flags}"
  sandbox: execFile
  timeout_seconds: 300
  shell: false
examples:
  - description: "Open a semi-interactive shell"
    command: impacket-wmiexec domain/username:password@10.0.0.1
  - description: "Execute a single command"
    command: impacket-wmiexec domain/username:password@10.0.0.1 "whoami"
  - description: "Execute command with NTLM hash (pass-the-hash)"
    command: impacket-wmiexec -hashes LM:HASH domain/username@10.0.0.1 "whoami"
  - description: "Run with local admin account"
    command: impacket-wmiexec ./administrator:password@10.0.0.1
references:
  - label: "Impacket GitHub"
    url: "https://github.com/fortra/impacket"
  - label: "wmiexec.py Documentation"
    url: "https://www.secureauth.com/blog/impacket-wmiexec/"
install:
    - method: pip
      package_name: "impacket"
      commands:
        - "pip install impacket"
---

# wmiexec.py — WMI Remote Command Execution

wmiexec.py is an Impacket tool that provides semi-interactive command execution over Windows Management Instrumentation (WMI). Unlike psexec.py, it does not deploy any service or agent on the target, making it stealthier for lateral movement.

## Key Features

- Semi-interactive shell via WMI
- No service deployment (stealthier than psexec)
- Pass-the-hash support
- Supports local and domain authentication
- No binary dropped on disk

## Usage

```bash
# Basic shell
impacket-wmiexec domain/user:Pass@192.168.1.100

# Single command
impacket-wmiexec domain/user:Pass@192.168.1.100 "ipconfig"

# Pass-the-hash
impacket-wmiexec -hashes aad3b435b51404eeaad3b435b51404ee:NT_HASH user@192.168.1.100

# Local admin
impacket-wmiexec ./admin:Pass@192.168.1.100
```
