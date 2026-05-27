---
id: security-honeypot-endlessh
namespace: security:honeypot:endlessh
name: endlessh
description: SSH tar pit that slowly sends an endless banner to keep SSH clients connected, consuming their resources and preventing brute force attacks.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - honeypot.ssh.tarpit
  - honeypot.ssh.attract
  - defense.ssh.rate-limit
platforms:
  - linux
  - bsd
  - cross-platform
risk_level: low
trust_level: verified
execution_policy: enabled
architectures:
  - amd64
  - arm64
dependencies: []
related_tools:
  - cowrie
  - kippo
artifacts:
  - type: honeypot.log
    description: Connection logs
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - connection-log
  consumes:
    - target-port
contract:
  inputs:
    - type: network.port
      description: SSH port to listen on
  outputs:
    - type: honeypot.log
      description: Log file with connection attempts
      mime: text/plain
  side_effects:
    - network_traffic
  resource_cost:
    cpu: low
    memory_mb: 32
    network: low
    disk_io: low
resource_profile:
  cpu: low
  memory_mb: 32
  network: low
  disk_io: low
allowed-tools:
  - endlessh
  - Bash
  - execFile
parameters:
  - name: flag-port
    type: integer
    required: false
    description: "Port to listen on (default 22)"
    aliases:
      - -p
      - --port
  - name: flag-bind
    type: string
    required: false
    description: "Address to bind to (default all)"
    aliases:
      - -b
      - --bind
  - name: flag-ms
    type: integer
    required: false
    description: "Milliseconds to sleep between lines (default 100)"
    aliases:
      - -m
      - --ms
  - name: flag-verbose
    type: boolean
    required: false
    description: "Log IP addresses"
    aliases:
      - -v
      - --verbose
  - name: flag-log
    type: string
    required: false
    description: "Log file path"
    aliases:
      - -l
      - --log
  - name: flag-version
    type: boolean
    required: false
    description: "Print version and exit"
    aliases:
      - -V
      - --version
execution:
  template: "endlessh {flag-port} {flag-bind} {flag-ms} {flag-verbose} {flag-log}"
  sandbox: execFile
  timeout_seconds: 60
  shell: false
examples:
  - description: "Run with default settings"
    command: endlessh
  - description: "Listen on port 2222 with verbose logging"
    command: endlessh -p 2222 -v
  - description: "Custom bind address and log file"
    command: endlessh -b 192.168.1.100 -l /var/log/endlessh.log
  - description: "Slow response (500ms delay)"
    command: endlessh -m 500
references:
  - label: "endlessh GitHub"
    url: "https://github.com/skeeto/endlessh"
phase: defense-evasion
techniques:
  - defense-evasion
  - monitoring
items:
  - NoCreds
services:
  - SSH
attack_types:
  - DefenseEvasion
---

# endlessh — SSH Tar Pit

endlessh is a minimalist SSH tar pit that keeps clients occupied with an endless banner, consuming their resources without providing a usable shell. It's useful for frustrating automated brute-force scanners and reducing SSH login attempts.

## Usage

```bash
# Default: listen on port 22, log to stderr
endlessh

# Listen on custom port with verbose logging
endlessh -p 2222 -v

# Bind to specific address and log to file
endlessh -b 192.168.1.100 -l /var/log/endlessh.log

# Slow response (500ms between lines)
endlessh -m 500
```