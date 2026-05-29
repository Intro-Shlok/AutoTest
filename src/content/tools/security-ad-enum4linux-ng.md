---
id: security-ad-enum4linux-ng
namespace: security:ad:enum4linux-ng
name: enum4linux-ng
description: Python reimplementation of enum4linux for comprehensive SMB and NetBIOS
  enumeration of Windows and Active Directory targets.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - security.ad.enum.users
  - security.ad.enum.shares
  - security.ad.enum.groups
  - security.ad.enum.passwordpolicy
  - security.ad.enum.osinfo
  - security.ad.enum.sessions
platforms:
  - linux
  - cross-platform
risk_level: low
trust_level: verified
execution_policy: enabled
architectures:
  - amd64
  - arm64
dependencies:
  - python3
related_tools:
  - smbclient
  - smbmap
  - rpcclient
  - impacket
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
      description: Optional username for authenticated queries
    - type: credential.password
      description: Optional password for authenticated queries
  outputs:
    - type: security.ad.enum.users
      description: List of domain/local users
    - type: security.ad.enum.shares
      description: Available SMB shares
    - type: security.ad.enum.groups
      description: Group memberships
    - type: security.ad.passwordpolicy
      description: Domain password policy
  side_effects:
    - network_traffic
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
  - enum4linux-ng
parameters:
  - name: target
    type: string
    required: true
    description: "Target IP address or hostname"
    aliases:
      - -t
      - --target
  - name: all
    type: boolean
    required: false
    default_value: false
    description: "Run all enumeration modules"
    aliases:
      - -A
      - --all
  - name: users
    type: boolean
    required: false
    default_value: false
    description: "Enumerate users"
    aliases:
      - -U
      - --users
  - name: shares
    type: boolean
    required: false
    default_value: false
    description: "Enumerate shares"
    aliases:
      - -S
      - --shares
  - name: password-policy
    type: boolean
    required: false
    default_value: false
    description: "Enumerate password policy"
    aliases:
      - -P
      - --password-policy
  - name: groups
    type: boolean
    required: false
    default_value: false
    description: "Enumerate groups"
    aliases:
      - -G
      - --groups
  - name: username
    type: string
    required: false
    description: "Username for authenticated enumeration"
    aliases:
      - -u
      - --username
  - name: password
    type: string
    required: false
    description: "Password for authenticated enumeration"
    aliases:
      - -p
      - --password
  - name: domain
    type: string
    required: false
    description: "Domain name for authentication"
    aliases:
      - -d
      - --domain
  - name: workgroup
    type: string
    required: false
    description: "Workgroup name (default: WORKGROUP)"
    aliases:
      - -w
      - --workgroup
  - name: output
    type: string
    required: false
    description: "Output directory for results"
    aliases:
      - -o
      - --output
  - name: timeout
    type: integer
    required: false
    default_value: 5
    description: "Timeout in seconds for network operations"
    aliases:
      - --timeout
execution:
  template: "enum4linux-ng -A {target}"
  sandbox: execFile
  timeout_seconds: 120
  shell: false
global_vars:
  target: ip
examples:
  - description: "Full enumeration with all modules"
    command: enum4linux-ng -A 10.10.10.1
  - description: "Enumerate users only"
    command: enum4linux-ng -U 10.10.10.1
  - description: "Authenticated enumeration with domain credentials"
    command: enum4linux-ng -A 10.10.10.1 -u jdoe -p Pass123 -d evilcorp.local
  - description: "Enumerate password policy and shares"
    command: enum4linux-ng -P -S 10.10.10.1
  - description: "Quiet mode with output to directory"
    command: enum4linux-ng -A 10.10.10.1 -q -o ./enum-results
references:
  - label: "enum4linux-ng GitHub"
    url: "https://github.com/cddmp/enum4linux-ng"
install:
    - method: pip
      package_name: "enum4linux-ng"
      commands:
        - "pip install enum4linux-ng"
---

# enum4linux-ng — SMB & NetBIOS Enumeration

enum4linux-ng is a Python rewrite of the original enum4linux.pl, providing comprehensive SMB and NetBIOS enumeration against Windows and Samba hosts.

## Enumeration Modules

| Module | Flag | Description |
|--------|------|-------------|
| OS Info | auto | Detect operating system and version |
| Users | `-U` | List domain and local users |
| Groups | `-G` | List groups and members |
| Shares | `-S` | List SMB shares and permissions |
| Password Policy | `-P` | Extract domain password policy |
| Printers | auto | Enumerate printer shares |
| Sessions | auto | Detect logged-in users |
| RID Cycling | auto | Brute-force RIDs for user enumeration |

## Authentication Modes

- **Null session** (no credentials): Limited information
- **Guest session**: Slightly more access
- **Authenticated**: Full enumeration with valid credentials
