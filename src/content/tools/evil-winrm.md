---
id: security-exec-evil-winrm
namespace: security:exec:evil-winrm
name: evil-winrm
description: WinRM shell for remote Windows administration and post-exploitation,
  supporting plaintext, pass-the-hash, and Kerberos PKINIT authentication.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - security.exec.winrm
  - security.credential.pth
  - security.lateral.winrm
  - security.ad.krbauth
platforms:
  - linux
  - cross-platform
risk_level: high
trust_level: verified
execution_policy: enabled
architectures:
  - amd64
dependencies:
  - ruby
related_tools:
  - netexec
  - impacket
  - psexec
contract:
  inputs:
    - type: network.target.ip
      description: Target IP address
    - type: credential.username
      description: Windows username
    - type: credential.password
      description: Plaintext password or NTLM hash
  outputs:
    - type: shell.session
      description: Interactive WinRM shell session
  side_effects:
    - network_traffic
    - raw_socket_access
resource_profile:
  cpu: low
  memory_mb: 64
  network: low
  disk_io: low
allowed-tools:
  - evil-winrm
parameters:
  - name: target
    type: string
    required: true
    description: "Target IP address or hostname"
  - name: username
    type: string
    required: true
    description: "Username for authentication"
  - name: password
    type: string
    required: false
    description: "Password for plaintext auth"
  - name: hash
    type: string
    required: false
    description: "NTLM hash for pass-the-hash"
  - name: certificate
    type: file
    required: false
    description: "Public certificate file (PKINIT)"
  - name: private-key
    type: file
    required: false
    description: "Private key file (PKINIT)"
global_vars:
  target: ip
  username: user
execution:
  template: "evil-winrm -i {target} -u {username} -p {password}"
  sandbox: execFile
  timeout_seconds: 300
  shell: false
examples:
  - description: "Basic WinRM shell with password authentication"
    command: evil-winrm -i 10.10.10.1 -u john -p password123
  - description: "Pass-the-hash authentication"
    command: evil-winrm -i 10.10.10.1 -u john -H <NThash>
  - description: "PKINIT certificate authentication"
    command: evil-winrm -i 10.10.10.1 -c pub.pem -k priv.pem -S -r EVILCORP
  - description: "Authentication with SSL and relay domain"
    command: evil-winrm -i {{DOMAIN}} -u {{USER}} -p '{{PASSWORD}}'
  - description: "Kerberos-based authentication"
    command: evil-winrm -i {{DC.DOMAIN}} -k -u {{USER}} -r {{DOMAIN}}
references:
  - label: "evil-winrm GitHub"
    url: "https://github.com/Hackplayers/evil-winrm"
techniques:
  - lateral-movement
  - execution
  - credential-access
services:
  - WinRM
items:
  - Password
  - Hash
attack_types:
  - LateralMovement
  - Execution
---

# evil-winrm — WinRM Shell for Pentesting

evil-winrm provides an interactive PowerShell session on Windows targets via WinRM. It supports multiple authentication methods including plaintext, pass-the-hash (NTLM), and Kerberos PKINIT.

## Key Features

- **Upload/download** files to/from the target
- **Pass-the-hash** with NTLM hash
- **PKINIT** authentication with certificates
- **Scripts** loading from local and remote sources
- **Dynamic command completion** for common Windows tools

## Authentication Methods

| Method | Flags | Use Case |
|--------|-------|----------|
| Password | `-u user -p pass` | Plaintext credentials |
| Pass-the-Hash | `-u user -H <NThash>` | NTLM hash without password |
| PKINIT | `-c cert -k key -r domain` | Certificate-based authentication |
