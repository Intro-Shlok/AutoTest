---
id: security-exploit-setoolkit
namespace: security:exploit:setoolkit
name: setoolkit
description: Social Engineer Toolkit for automating credential harvesting, phishing campaigns, and payload generation.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - social.engineering
  - credential.harvesting
  - phishing.campaign
  - payload.generation
  - website.clone
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
  - python3
related_tools:
  - beef
  - metasploit
  - gophish
workflow_edges:
  produces:
    - phishing-url
    - harvested-credentials
    - malicious-payload
    - cloned-website
  consumes:
    - target-email
    - target-url
    - lhost
    - lport
contract:
  inputs:
    - type: network.target.email
      description: Target email address for phishing
    - type: network.url
      description: URL to clone for credential harvesting
    - type: network.lhost
      description: Local IP for reverse connections
    - type: network.lport
      description: Local port for reverse connections
  outputs:
    - type: credential.data
      description: Harvested credentials
      mime: application/json
    - type: payload.binary
      description: Generated malicious payload
      mime: application/octet-stream
  side_effects:
    - network_traffic
    - network_traffic
    - network_traffic
  resource_cost:
    cpu: medium
    memory_mb: 128
    network: medium
    disk_io: low
resource_profile:
  cpu: medium
  memory_mb: 128
  network: medium
  disk_io: low
allowed-tools:
  - setoolkit
  - Bash
  - execFile
parameters:
  - name: menu-1
    type: string
    required: false
    description: "Option 1: Social-Engineering Attacks"
    aliases: []
  - name: menu-2
    type: string
    required: false
    description: "Option 2: Penetration Testing"
    aliases: []
  - name: menu-3
    type: string
    required: false
    description: "Option 3: Third Party Modules"
    aliases: []
  - name: menu-4
    type: string
    required: false
    description: "Option 4: Update SET"
    aliases: []
  - name: menu-99
    type: string
    required: false
    description: "Option 99: Exit"
    aliases: []
execution:
  template: "setoolkit"
  sandbox: execFile
  timeout_seconds: 600
  shell: false
global_vars:
  lhost: "10.0.0.1"
  lport: "4444"
examples:
  - description: "Launch SET main menu"
    command: setoolkit
  - description: "Website attack vectors - credential harvesting"
    command: "setoolkit (then navigate: 1) Social-Engineering Attacks > 2) Website Attack Vectors > 3) Credential Harvester Attack Method > 2) Site Cloner)"
  - description: "Generate malicious payload with Metasploit"
    command: "setoolkit (then navigate: 1) Social-Engineering Attacks > 4) Infectious Media Generator)"
  - description: "Phishing email campaign"
    command: "setoolkit (then navigate: 1) Social-Engineering Attacks > 5) Mass Mailer Attack)"
  - description: "Quick penetration testing tools"
    command: "setoolkit (then navigate: 2) Penetration Testing)"
references:
  - label: "SET GitHub"
    url: "https://github.com/trustedsec/social-engineer-toolkit"
  - label: "SET Documentation"
    url: "https://www.social-engineer.org/toolkit/"
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
# SET — Social Engineer Toolkit

The Social-Engineer Toolkit (SET) is an open-source penetration testing framework designed for social engineering. It automates credential harvesting, phishing campaigns, website cloning, and payload generation.

## Attack Vectors

| Menu | Category | Description |
|------|----------|-------------|
| 1 | Social-Engineering Attacks | Phishing, credential harvesting, payload delivery |
| 2 | Penetration Testing | Quick access to Metasploit and other tools |
| 3 | Third Party Modules | Community-contributed modules |
| 4 | Update SET | Update the toolkit to latest version |
| 99 | Exit | Exit the framework |

## Social-Engineering Attack Types

1. Spear-Phishing Attack Vectors
2. Website Attack Vectors (credential harvesting, web jacking)
3. Infectious Media Generator
4. Create a Payload and Listener
5. Mass Mailer Attack
6. Arduino-Based Attack Vector
7. SMS Spoofing Attack Vector
8. Wireless Access Point Attack Vector
9. QRCode Generator Attack Vector
10. Powershell Attack Vectors
11. Third Party Modules
