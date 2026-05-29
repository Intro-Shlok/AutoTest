---
id: security-ad-sharphound
namespace: security:ad:sharphound
name: sharphound
description: BloodHound data collector written in C# that enumerates Active Directory relationships, ACLs, group memberships, and session information for attack path analysis.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - security.ad.enum.domain
  - security.ad.enum.users
  - security.ad.enum.groups
  - security.ad.enum.computers
  - security.ad.enum.sessions
  - security.ad.enum.acl
  - security.ad.graph
platforms:
  - windows
risk_level: medium
trust_level: verified
execution_policy: enabled
architectures:
  - amd64
dependencies: []
related_tools:
  - bloodhound
  - certipy
  - impacket
  - netexec
artifacts:
  - type: security.ad.graph
    description: BloodHound JSON data files
    mime: application/json
    trust_level: verified
workflow_edges:
  produces:
    - ad-graph-data
    - session-data
  consumes:
    - target-domain
    - credential-data
contract:
  inputs:
    - type: network.target.ip
      description: Domain controller IP address
    - type: credential.username
      description: Domain username
    - type: credential.password
      description: Password or NTLM hash
    - type: domain.name
      description: Target domain name
  outputs:
    - type: security.ad.graph
      description: Collected AD relationship data as JSON
      mime: application/json
  side_effects:
    - network_traffic
    - filesystem_write
  resource_cost:
    cpu: low
    memory_mb: 256
    network: medium
    disk_io: low
resource_profile:
  cpu: low
  memory_mb: 256
  network: medium
  disk_io: low
allowed-tools:
  - sharphound
  - Bash
  - execFile
parameters:
  - name: CollectionMethod
    type: string
    required: false
    description: "Data collection method (Default, Group, LocalGroup, RDP, DCOnly, All)"
    aliases:
      - -c
      - --CollectionMethod
  - name: Domain
    type: string
    required: false
    description: "Target domain"
    aliases:
      - -d
      - --Domain
  - name: LdapUsername
    type: string
    required: false
    description: "LDAP bind username"
    aliases:
      - -u
      - --Username
  - name: LdapPassword
    type: string
    required: false
    description: "LDAP bind password"
    aliases:
      - -p
      - --Password
  - name: SearchBase
    type: string
    required: false
    description: "LDAP search base DN"
    aliases:
      - -sb
      - --SearchBase
  - name: Stealth
    type: boolean
    required: false
    description: "Use stealth collection mode"
    aliases:
      - -s
      - --Stealth
  - name: ZipFilename
    type: string
    required: false
    description: "Output zip file name"
    aliases:
      - -z
      - --ZipFilename
  - name: flag-json
    type: boolean
    required: false
    description: "Output as JSON (not zip)"
    aliases:
      - -j
      - --json
execution:
  template: "SharpHound.exe {flags}"
  sandbox: execFile
  timeout_seconds: 600
  shell: false
examples:
  - description: "Run all collection methods"
    command: SharpHound.exe -c All -d example.com
  - description: "Run with credentials"
    command: SharpHound.exe -c All -d example.com -u USER -p PASS
  - description: "Stealth collection"
    command: SharpHound.exe -c Default,Group -d example.com --Stealth
  - description: "Collect only from domain controller"
    command: SharpHound.exe -c DCOnly -d example.com
references:
  - label: "SharpHound GitHub"
    url: "https://github.com/BloodHoundAD/SharpHound"
  - label: "BloodHound Documentation"
    url: "https://bloodhound.readthedocs.io/"
phase: enumeration
techniques:
  - discovery
  - collection
items:
  - NoCreds
services:
  - LDAP
attack_types:
  - Discovery
  - Collection
install:
    - method: git
      repo_url: "https://github.com/BloodHoundAD/SharpHound.git"
      commands:
        - "git clone https://github.com/BloodHoundAD/SharpHound.git"
---

# SharpHound — BloodHound AD Data Collector

SharpHound is the official C# data collector for BloodHound that enumerates Active Directory environments, collecting information about users, groups, computers, sessions, ACLs, and trust relationships for attack path analysis.

## Collection Methods

| Method | Data Collected |
|--------|---------------|
| Default | Groups, sessions, local groups |
| Group | Group membership only (fast) |
| LocalGroup | Local admin rights enumeration |
| RDP | Remote Desktop users |
| DCOnly | Domain controller queries only |
| All | Everything (slowest, most complete) |

## Usage

```powershell
# Transfer SharpHound.exe to target
# Run collection
SharpHound.exe -c All -d domain.local

# Transfer resulting ZIP to BloodHound
# Import ZIP file in BloodHound GUI
```
