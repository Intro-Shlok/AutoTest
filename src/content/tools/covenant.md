---
id: security-exploit-covenant
namespace: security:exploit:covenant
name: covenant
description: .NET command and control framework for red teaming with real-time collaboration and multi-user support.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - agent.communication
  - post.exploitation
  - payload.generation
  - realtime.collaboration
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
  - dotnet
related_tools:
  - metasploit
  - empire
  - sliver
workflow_edges:
  produces:
    - agent-session
    - grunt-stager
    - harvested-credentials
  consumes:
    - target-ip
    - listener-config
    - grunt-template
contract:
  inputs:
    - type: network.target.ip
      description: Listener bind address
    - type: network.port.number
      description: Listener port
    - type: credential.username
      description: Admin username
    - type: credential.password
      description: Admin password
  outputs:
    - type: agent.session
      description: Grunt agent session
      mime: application/octet-stream
    - type: payload.binary
      description: Generated stager/grunt binary
      mime: application/octet-stream
  side_effects:
    - network_traffic
    - process_spawn
    - filesystem_write
  resource_cost:
    cpu: high
    memory_mb: 512
    network: high
    disk_io: medium
resource_profile:
  cpu: high
  memory_mb: 512
  network: high
  disk_io: medium
allowed-tools:
  - covenant
  - Bash
  - execFile
parameters:
  - name: flag-config
    type: string
    required: false
    description: "Config file path"
    aliases:
      - --config
  - name: flag-port
    type: integer
    required: false
    description: "HTTP server port"
    aliases:
      - --port
  - name: flag-username
    type: string
    required: false
    description: "Admin account username"
    aliases:
      - --username
  - name: flag-password
    type: string
    required: false
    description: "Admin account password"
    aliases:
      - --password
  - name: flag-server
    type: boolean
    required: false
    description: "Run as server only"
    aliases:
      - --server
  - name: flag-https
    type: boolean
    required: false
    description: "Enable HTTPS"
    aliases:
      - --https
  - name: flag-cert
    type: string
    required: false
    description: "SSL certificate path"
    aliases:
      - --cert
  - name: flag-verbose
    type: boolean
    required: false
    description: "Verbose logging"
    aliases:
      - --verbose
  - name: flag-debug
    type: boolean
    required: false
    description: "Debug mode"
    aliases:
      - --debug
  - name: flag-open-browser
    type: boolean
    required: false
    description: "Open browser on startup"
    aliases:
      - --open-browser
execution:
  template: "covenant"
  sandbox: execFile
  timeout_seconds: 600
  shell: false
global_vars:
  lport: "7443"
  username: "admin"
  password: "admin123"
examples:
  - description: "Start Covenant with default settings"
    command: covenant
  - description: "Start Covenant on custom port"
    command: covenant --port 8443
  - description: "Start Covenant with HTTPS"
    command: covenant --https --cert /path/to/cert.pfx
  - description: "Start Covenant with credentials"
    command: covenant --username redteam --password SecurePass123
  - description: "Start Covenant in server-only mode"
    command: covenant --server --port 7443
  - description: "Start Covenant with debug logging"
    command: covenant --debug --verbose
  - description: "Start Covenant and open browser"
    command: covenant --open-browser
references:
  - label: "Covenant GitHub"
    url: "https://github.com/cobbr/Covenant"
  - label: "Covenant Wiki"
    url: "https://github.com/cobbr/Covenant/wiki"
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
    - method: git
      repo_url: "https://github.com/cobbr/Covenant.git"
      commands:
        - "git clone https://github.com/cobbr/Covenant.git"
---
# Covenant — .NET C2 Framework

Covenant is a .NET-based command and control framework designed for red team operations. It features a web-based UI, real-time collaboration, and comprehensive post-exploitation capabilities through its "grunt" agents.

## Key Features

- **Web-based UI**: Full graphical interface for C2 operations
- **Grunt agents**: .NET-based agents with extensive capabilities
- **Multi-user**: Real-time collaboration with chat and shared sessions
- **Dynamic compilation**: On-the-fly payload compilation
- **Task system**: Parallel task execution across grunts
- **Listener types**: HTTP, HTTPS, and Bridge listeners
