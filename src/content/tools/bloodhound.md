---
id: security-recon-bloodhound
namespace: security:recon:bloodhound
name: BloodHound
description: Active Directory graph-based enumeration tool that maps relationships
  between users, groups, computers, and permissions to identify attack paths to domain
  privilege escalation.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - security.ad.enum.users
  - security.ad.enum.groups
  - security.ad.enum.computers
  - security.ad.enum.gpos
  - security.ad.enum.ous
  - security.ad.attackpath
  - security.ad.kerberosabuse
  - security.ad.aclanalysis
  - security.ad.sessioncollection
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
  - neo4j
related_tools:
  - netexec
  - impacket
contract:
  inputs:
    - type: network.target.ip
      description: Domain controller or target IP
    - type: credential.username
      description: Domain username
    - type: credential.password
      description: Domain password
  outputs:
    - type: security.ad.graph
      description: BloodHound JSON files (users/groups/computers/sessions)
  side_effects:
    - network_traffic
resource_profile:
  cpu: low
  memory_mb: 256
  network: medium
  disk_io: medium
allowed-tools:
  - bloodhound
parameters:
  - name: target
    type: string
    required: true
    description: "Target domain controller IP or domain"
  - name: username
    type: string
    required: true
    description: "Domain username"
  - name: password
    type: string
    required: true
    description: "Domain password"
  - name: domain
    type: string
    required: false
    description: "Domain name (auto-detected if omitted)"
  - name: nameserver
    type: string
    required: false
    description: "DNS server IP for domain resolution"
  - name: collection-method
    type: string
    required: false
    default_value: "all"
    description: "Collection method: all, group, session, computeronly, etc."
global_vars:
  target: ip
  domain: domain
  username: user
  nameserver: ip
execution:
  template: "bloodhound-python -d {domain} -u {username} -p {password} -ns {nameserver} -c {collection-method}"
  sandbox: execFile
  timeout_seconds: 600
  shell: false
examples:
  - description: "Full AD enumeration with all collection methods"
    command: bloodhound-python -d {{DOMAIN}} -u {{USER}} -p '{{PASSWORD}}' -ns {{IP}} -c all
  - description: "Kerberos-based enumeration (no password needed on Linux)"
    command: bloodhound-python -d {{DOMAIN}} -u {{USER}} -k -no-pass -ns {{IP}} -c all
  - description: "BloodHound.py remote ingestion from LDAP (no credentials)"
    command: bloodhound.py -c LDAP -d evilcorp.local -dc-ip 10.10.10.1 -ns 10.10.10.1
  - description: "BloodHound.py with credentials via LDAP"
    command: bloodhound.py -u john -p password123 -d evilcorp.local -dc-ip 10.10.10.1 -ns 10.10.10.1 -c All
  - description: "SharpHound.exe PowerShell execution on Windows"
    command: Invoke-BloodHound -CollectionMethod All -Domain evilcorp.local -ZipFile output.zip
references:
  - label: "BloodHound GitHub"
    url: "https://github.com/BloodHoundAD/BloodHound"
  - label: "BloodHound.py GitHub"
    url: "https://github.com/fox-it/BloodHound.py"
techniques:
  - discovery
  - enumeration
  - privilege-escalation
attack_types:
  - Enumeration
---

# BloodHound — AD Attack Path Mapping

BloodHound is a single-page JavaScript web application that uses graph theory to reveal hidden relationships and attack paths in Active Directory environments. It ingests LDAP data and session information to build a comprehensive map of who-can-do-what.

## Collectors

| Collector | Platform | Command |
|-----------|----------|---------|
| BloodHound.py | Linux | `bloodhound-python -d DOMAIN -u USER -p PASS -c all` |
| SharpHound.exe | Windows | `SharpHound.exe -c All` |
| SharpHound.ps1 | PowerShell | `Invoke-BloodHound -CollectionMethod All` |

## Collection Methods

- **Group**: Group membership  
- **Session**: Active user sessions  
- **ComputerOnly**: Computer details  
- **LocalAdmin**: Local admin groups  
- **RDP**: Remote Desktop users  
- **DCOM**: DCOM users  
- **PSRemote**: PowerShell Remote users  
- **ACL**: Access control entries  
- **All**: Everything above  
