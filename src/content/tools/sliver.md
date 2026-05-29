---
id: security-exploit-sliver
namespace: security:exploit:sliver
name: sliver
description: Implant-based C2 framework for adversary simulation, red team operations, and post-exploitation.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - agent.communication
  - implant.generation
  - post.exploitation
  - adversary.simulation
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
dependencies: []
related_tools:
  - metasploit
  - empire
  - covenant
  - cobalt-strike
workflow_edges:
  produces:
    - implant-binary
    - agent-session
    - c2-listener
    - loot-data
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
    - type: implant.config
      description: Implant configuration profile
  outputs:
    - type: agent.session
      description: Active agent session
      mime: application/octet-stream
    - type: implant.binary
      description: Generated implant binary
      mime: application/octet-stream
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
  - sliver
  - Bash
  - execFile
parameters:
  - name: subcommand
    type: string
    required: true
    description: "Subcommand: client, server, operator, --help"
    aliases: []
  - name: flag-config
    type: string
    required: false
    description: "Config file path"
    aliases:
      - --config
  - name: lhost
    type: string
    required: false
    description: "Listener host/IP"
    aliases:
      - --lhost
  - name: lport
    type: integer
    required: false
    description: "Listener port"
    aliases:
      - --lport
  - name: flag-profile
    type: string
    required: false
    description: "Implant profile"
    aliases:
      - --profile
  - name: flag-save
    type: string
    required: false
    description: "Save output to file"
    aliases:
      - --save
  - name: flag-mtls
    type: string
    required: false
    description: "mTLS listener (host:port)"
    aliases:
      - --mtls
  - name: flag-http
    type: string
    required: false
    description: "HTTP listener (host:port)"
    aliases:
      - --http
  - name: flag-https
    type: string
    required: false
    description: "HTTPS listener (host:port)"
    aliases:
      - --https
  - name: flag-dns
    type: string
    required: false
    description: "DNS listener (host:port)"
    aliases:
      - --dns
  - name: flag-daemon
    type: boolean
    required: false
    description: "Daemonize server"
    aliases:
      - --daemon
  - name: flag-armory
    type: boolean
    required: false
    description: "Enable armory for community extensions"
    aliases:
      - --armory
execution:
  template: "sliver-client"
  sandbox: execFile
  timeout_seconds: 600
  shell: false
global_vars:
  lhost: "0.0.0.0"
  lport: "443"
examples:
  - description: "Start Sliver server"
    command: sliver-server --daemon
  - description: "Start Sliver client"
    command: sliver-client
  - description: "Generate mTLS implant"
    command: generate --mtls 10.0.0.1:443 --os windows --arch amd64 --save implant.exe
  - description: "Start HTTP listener"
    command: sliver-client --http 0.0.0.0:80
  - description: "Start HTTPS listener"
    command: sliver-client --https 0.0.0.0:443
  - description: "Enable armory extensions"
    command: sliver-client --armory
  - description: "Generate with custom profile"
    command: generate --profile windows-defender-evasion --save beacon.exe
references:
  - label: "Sliver GitHub"
    url: "https://github.com/BishopFox/sliver"
  - label: "Sliver Documentation"
    url: "https://sliver.sh/docs"
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
install:
    - method: go
      repo_url: "github.com/BishopFox/sliver"
      commands:
        - "go install github.com/BishopFox/sliver@latest"
---
# Sliver — Implant-Based C2 Framework

Sliver is an open-source, implant-based C2 (Command and Control) framework designed for adversary simulation, red team operations, and post-exploitation. It supports multiple communication protocols including mTLS, HTTP, HTTPS, DNS, and named pipes.

## Key Features

- **Multi-protocol C2**: mTLS, HTTP(S), DNS, TCP, named pipes
- **Dynamic implants**: Fully customizable implant generation
- **Armory**: Community extension marketplace
- **Operators**: Multi-user collaboration with role-based access
- **Encrypted comms**: End-to-end encryption for all communication
- **Cross-platform**: Server on Linux/macOS, implants on Windows/Linux/macOS
