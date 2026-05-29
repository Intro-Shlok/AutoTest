---
id: security-exploit-empire
namespace: security:exploit:empire
name: empire
description: PowerShell-based post-exploitation framework for staged and stageless payloads with encrypted C2 communication.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - post.exploitation
  - agent.communication
  - payload.generation
  - credential.dumping
  - privilege.escalation
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
  - metasploit
  - sliver
  - covenant
  - starkiller
workflow_edges:
  produces:
    - agent-session
    - listener
    - stager-payload
    - harvested-credentials
  consumes:
    - target-ip
    - listener-profile
    - stager-type
contract:
  inputs:
    - type: network.target.ip
      description: Listener IP address
    - type: network.port.number
      description: Listener port
    - type: stager.type
      description: Stager type (dll, launcher, macro, etc.)
  outputs:
    - type: command.session
      description: Encrypted C2 agent session
      mime: application/octet-stream
    - type: credential.data
      description: Dumped credentials
      mime: application/json
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
  - empire
  - Bash
  - execFile
parameters:
  - name: subcommand
    type: string
    required: true
    description: "Subcommand: server, client, reset, --help"
    aliases: []
  - name: username
    type: string
    required: false
    description: "Username for authentication"
    aliases:
      - --username
  - name: password
    type: string
    required: false
    description: "Password for authentication"
    aliases:
      - --password
  - name: port
    type: integer
    required: false
    description: "Server listener port"
    aliases:
      - --port
  - name: flag-c
    type: string
    required: false
    description: "Config file path"
    aliases:
      - -c
      - --config
  - name: flag-d
    type: boolean
    required: false
    description: "Debug mode"
    aliases:
      - -d
      - --debug
  - name: flag-v
    type: boolean
    required: false
    description: "Verbose output"
    aliases:
      - -v
      - --verbose
  - name: restip
    type: string
    required: false
    description: "RESTful API bind IP"
    aliases:
      - --restip
  - name: headless
    type: boolean
    required: false
    description: "Run without interactive console"
    aliases:
      - --headless
  - name: launcher
    type: string
    required: false
    description: "Launcher stager type"
    aliases:
      - --launcher
  - name: flag-ip
    type: string
    required: false
    description: "Listener IP address"
    aliases:
      - --ip
  - name: profile
    type: string
    required: false
    description: "Listener profile name"
    aliases:
      - --profile
execution:
  template: "empire server"
  sandbox: execFile
  timeout_seconds: 600
  shell: false
global_vars:
  lhost: "0.0.0.0"
  lport: "1337"
examples:
  - description: "Start Empire server"
    command: empire server
  - description: "Start Empire client"
    command: empire client
  - description: "Start server with custom port"
    command: empire server --port 443
  - description: "Start server in headless mode"
    command: empire server --headless
  - description: "Start client with credentials"
    command: empire client --username empireadmin --password password123
  - description: "Server with debug output"
    command: empire server -d -v
  - description: "Server with REST API on custom IP"
    command: empire server --restip 10.0.0.1
references:
  - label: "Empire GitHub"
    url: "https://github.com/BC-SECURITY/Empire"
  - label: "Empire Documentation"
    url: "https://bc-security.gitbook.io/empire-wiki/"
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
      repo_url: "https://github.com/BC-SECURITY/Empire.git"
      commands:
        - "git clone https://github.com/BC-SECURITY/Empire.git"
        - "cd Empire && ./setup/install.sh"
---
# Empire — PowerShell Post-Exploitation Framework

Empire (now maintained as PowerShell Empire) is a pure PowerShell post-exploitation agent framework. It provides encrypted C2 communication, modular stagers, and extensive post-exploitation capabilities built on PowerShell scripting.

## Key Features

- **Encrypted C2**: Encrypted communication between agents and server
- **Multiple stagers**: Dll, launcher, macro, and more
- **Module system**: Extensive post-exploitation modules
- **Starkiller UI**: Graphical front-end for Empire
- **Multi-platform agents**: PowerShell (Windows) and Python (Linux/OSX)
- **Listener profiles**: HTTP, HTTPS, and SMB listeners

## Architecture

- **Server**: Python-based RESTful C2 server
- **Client**: PowerShell or python-based agents
- **Starkiller**: Vue.js GUI for Empire management
- **Modules**: Post-exploitation, credential theft, lateral movement
