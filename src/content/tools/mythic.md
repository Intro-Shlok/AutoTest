---
id: security-exploit-mythic
namespace: security:exploit:mythic
name: mythic
description: Collaborative red team C2 framework with a web UI, multi-agent support, and extensible payload agents for post-exploitation operations.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - agent.communication
  - command.control.c2
  - implant.generation
  - post.exploitation
  - adversary.simulation
  - team.collaboration
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
  - docker
  - python3
related_tools:
  - sliver
  - covenant
  - empire
  - havoc
  - merlin
workflow_edges:
  produces:
    - implant-binary
    - agent-session
    - c2-listener
    - harvested-credentials
  consumes:
    - target-ip
    - target-port
    - implant-profile
    - payload-type
contract:
  inputs:
    - type: network.target.ip
      description: Callback IP/C2 domain
    - type: network.port.number
      description: Listener port
    - type: payload.type
      description: Agent payload type (apollo, poseidon, etc.)
  outputs:
    - type: agent.session
      description: Active Mythic agent session
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
    memory_mb: 512
    network: high
    disk_io: medium
resource_profile:
  cpu: medium
  memory_mb: 512
  network: high
  disk_io: medium
allowed-tools:
  - mythic
  - Bash
  - execFile
parameters:
  - name: flag-start
    type: boolean
    required: false
    description: "Start Mythic services"
    aliases:
      - --start
  - name: flag-stop
    type: boolean
    required: false
    description: "Stop Mythic services"
    aliases:
      - --stop
  - name: flag-status
    type: boolean
    required: false
    description: "Check Mythic service status"
    aliases:
      - --status
  - name: flag-restart
    type: boolean
    required: false
    description: "Restart Mythic services"
    aliases:
      - --restart
execution:
  template: "./mythic-cli {flags}"
  sandbox: execFile
  timeout_seconds: 3600
  shell: false
examples:
  - description: "Start Mythic server and all services"
    command: ./mythic-cli start
  - description: "Stop Mythic services"
    command: ./mythic-cli stop
  - description: "Check Mythic service status"
    command: ./mythic-cli status
  - description: "Restart Mythic services"
    command: ./mythic-cli restart
references:
  - label: "Mythic GitHub"
    url: "https://github.com/its-a-feature/Mythic"
  - label: "Mythic Documentation"
    url: "https://docs.mythic-c2.net/"
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
      repo_url: "https://github.com/its-a-feature/Mythic.git"
      commands:
        - "git clone https://github.com/its-a-feature/Mythic.git"
        - "cd Mythic && make"
---

# Mythic — Collaborative Red Team C2 Framework

Mythic is a web-based, multi-agent C2 framework designed for red team collaboration. It uses a Docker-based architecture with a web UI, REST API, and supports multiple agent payloads for cross-platform post-exploitation.

## Key Features

- Web-based user interface for real-time collaboration
- Multi-agent support (Apollo, Poseidon, Athena, etc.)
- Docker-based service architecture
- WebSockets for live agent communication
- Extensible payload types and C2 profiles

## Mythic Agents

| Agent | Platform | Language |
|-------|----------|----------|
| Apollo | Windows | C# |
| Poseidon | macOS | Swift |
| Athena | Linux | Golang |
| Medusa | All | Python |

## Common Commands

```bash
# Navigate to Mythic install directory
cd Mythic/

# Start the framework
./mythic_cli start

# Access the web UI at https://localhost:7443
# Generate payloads and manage agents through the GUI
```
