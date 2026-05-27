---
id: security-exploit-pupy
namespace: security:exploit:pupy
name: pupy
description: Cross-platform remote administration and post-exploitation framework written in Python, supporting in-memory execution, multiple transports, and extensible modules.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - agent.communication
  - command.control.c2
  - post.exploitation
  - remote.administration
  - inmemory.execution
platforms:
  - linux
  - windows
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
  - sliver
  - empire
  - merlin
  - metasploit
workflow_edges:
  produces:
    - agent-session
    - c2-listener
    - harvested-credentials
  consumes:
    - target-ip
    - target-port
    - payload-type
contract:
  inputs:
    - type: network.target.ip
      description: Pupy server bind address
    - type: network.port.number
      description: Listener port
    - type: payload.type
      description: Payload type (Windows/Linux/Android)
  outputs:
    - type: agent.session
      description: Pupy agent session
      mime: application/octet-stream
    - type: credential.data
      description: Extracted credentials
      mime: text/plain
  side_effects:
    - network_traffic
    - process_spawn
    - filesystem_write
  resource_cost:
    cpu: medium
    memory_mb: 128
    network: high
    disk_io: low
resource_profile:
  cpu: medium
  memory_mb: 128
  network: high
  disk_io: low
allowed-tools:
  - pupy
  - python3
  - Bash
  - execFile
parameters:
  - name: flag-l
    type: string
    required: false
    description: "Listener bind address"
    aliases:
      - -l
      - --listen
  - name: flag-p
    type: integer
    required: false
    description: "Listener port"
    aliases:
      - -p
      - --port
  - name: flag-t
    type: string
    required: false
    description: "Transport type (ssl, http, https, dns, rsa)"
    aliases:
      - -t
      - --transport
  - name: flag-s
    type: string
    required: false
    description: "Script or module to execute"
    aliases:
      - -s
      - --script
execution:
  template: "pupysh {flags}"
  sandbox: execFile
  timeout_seconds: 3600
  shell: false
examples:
  - description: "Start Pupy server"
    command: pupysh
  - description: "Generate Windows payload with SSL transport"
    command: pupy --transport ssl -l 0.0.0.0 -p 8443
  - description: "Generate Android payload"
    command: pupy --transport ssl -l 0.0.0.0 -p 8443 --platform android
references:
  - label: "Pupy GitHub"
    url: "https://github.com/n1nj4sec/pupy"
phase: exploitation
techniques:
  - command-and-control
  - execution
items:
  - Shell
  - Hash
services: []
attack_types:
  - Exploitation
  - Execution
---

# Pupy — Remote Administration C2 Framework

Pupy is a cross-platform remote administration and post-exploitation framework written entirely in Python. It supports in-memory execution, multiple transport protocols (SSL, HTTP, HTTPS, DNS, RSA), and runs on Windows, Linux, macOS, and Android.

## Key Features

- In-memory payload execution
- Multi-transport support (SSL, HTTP, HTTPS, DNS, RSA)
- Reflective DLL injection on Windows
- Linux payload support
- Android agent support
- Extensible module system

## Common Commands

```bash
# Start the Pupy shell interface
pupysh

# Generate a staged payload
pupy --transport ssl -l 0.0.0.0 -p 8443

# Interactive shell access
# Once the agent checks in, list sessions with 'sessions'
# Interact with 'sessions -i <id>'
```
