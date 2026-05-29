---
id: security-exploit-havoc
namespace: security:exploit:havoc
name: havoc
description: Modern post-exploitation command and control framework with a GUI interface, supporting agent communication, payload generation, and team collaboration.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - agent.communication
  - implant.generation
  - post.exploitation
  - command.control.c2
  - adversary.simulation
platforms:
  - linux
  - windows
  - cross-platform
risk_level: high
trust_level: verified
execution_policy: enabled
architectures:
  - amd64
dependencies: []
related_tools:
  - sliver
  - covenant
  - empire
  - mythic
workflow_edges:
  produces:
    - implant-binary
    - agent-session
    - c2-listener
  consumes:
    - target-ip
    - target-port
    - implant-profile
contract:
  inputs:
    - type: network.target.ip
      description: Listener bind address
    - type: network.port.number
      description: Listener bind port
    - type: payload.type
      description: Payload type (dll, exe, shellcode)
  outputs:
    - type: agent.session
      description: Active agent session
      mime: application/octet-stream
    - type: implant.binary
      description: Generated implant payload
      mime: application/octet-stream
  side_effects:
    - network_traffic
    - process_spawn
    - filesystem_write
  resource_cost:
    cpu: medium
    memory_mb: 256
    network: high
    disk_io: low
resource_profile:
  cpu: medium
  memory_mb: 256
  network: high
  disk_io: low
allowed-tools:
  - havoc
  - Bash
  - execFile
parameters:
  - name: teamserver-host
    type: string
    required: false
    description: "Team server host address"
    aliases:
      - --teamserver-host
  - name: teamserver-port
    type: integer
    required: false
    description: "Team server port"
    aliases:
      - --teamserver-port
  - name: flag-v
    type: boolean
    required: false
    description: "Verbose output"
    aliases:
      - -v
      - --verbose
  - name: profile
    type: string
    required: false
    description: "C2 profile configuration file"
    aliases:
      - --profile
execution:
  template: "havoc {flags}"
  sandbox: execFile
  timeout_seconds: 3600
  shell: false
examples:
  - description: "Start the Havoc team server"
    command: havoc server --profile havoc.yaotl
  - description: "Start the Havoc client GUI"
    command: havoc client
  - description: "Generate a default HTTP implant"
    command: havoc generate --listener http --target https://example.com
references:
  - label: "Havoc GitHub"
    url: "https://github.com/HavocFramework/Havoc"
  - label: "Havoc Documentation"
    url: "https://havocframework.com/docs"
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
install:
    - method: git
      repo_url: "https://github.com/HavocFramework/Havoc.git"
      commands:
        - "git clone https://github.com/HavocFramework/Havoc.git"
        - "cd Havoc && make"
---

# Havoc — Modern C2 Framework

Havoc is a modern post-exploitation command and control framework with a native GUI client and team server architecture. It supports multiple agent types, encrypted C2 channels, and integrated reporting for red team operations.

## Architecture

- **Team Server** — Central orchestrator managing agents and operators
- **Client** — GUI-based operator interface (Qt-based)
- **Agent** — Implant running on compromised hosts
- **Listener** — C2 endpoint for agent callbacks

## Common Commands

```bash
# Start team server
havoc server --profile config.yaotl

# Launch client
havoc client

# Generate agent
havoc generate --listener https --target https://c2.example.com
```
