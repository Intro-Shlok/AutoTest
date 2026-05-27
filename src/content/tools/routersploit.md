---
id: security-exploit-routersploit
namespace: security:exploit:routersploit
name: routersploit
description: Router exploitation framework with modules for scanning, exploiting, and fuzzing embedded devices.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - embedded.exploitation
  - router.scanning
  - device.fuzzing
  - credential.brute-force
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
  - commix
workflow_edges:
  produces:
    - device-access
    - exploit-session
    - credential-list
  consumes:
    - target-ip
    - target-port
    - exploit-module
contract:
  inputs:
    - type: network.target.ip
      description: Target device IP address
    - type: network.port.number
      description: Target device port
    - type: exploit.module.name
      description: RouterSploit module to use
  outputs:
    - type: shell.session
      description: Shell access on device
      mime: text/plain
    - type: credential.data
      description: Found credentials
      mime: application/json
  side_effects:
    - network_traffic
    - network_traffic
  resource_cost:
    cpu: low
    memory_mb: 64
    network: medium
    disk_io: low
resource_profile:
  cpu: low
  memory_mb: 64
  network: medium
  disk_io: low
allowed-tools:
  - routersploit
  - Bash
  - execFile
parameters:
  - name: flag-t
    type: string
    required: false
    description: "Target IP address"
    aliases:
      - -t
      - --target
  - name: flag-p
    type: integer
    required: false
    description: "Target port"
    aliases:
      - -p
      - --port
  - name: flag-m
    type: string
    required: false
    description: "Module to use"
    aliases:
      - -m
      - --module
  - name: flag-s
    type: string
    required: false
    description: "Scanner module"
    aliases:
      - -s
      - --scanner
  - name: flag-e
    type: string
    required: false
    description: "Exploit module"
    aliases:
      - -e
      - --exploit
  - name: flag-f
    type: string
    required: false
    description: "Fuzzer module"
    aliases:
      - -f
      - --fuzzer
  - name: flag-c
    type: string
    required: false
    description: "Credentials (user:pass)"
    aliases:
      - -c
      - --credentials
  - name: flag-v
    type: boolean
    required: false
    description: "Verbose output"
    aliases:
      - -v
      - --verbose
  - name: flag-q
    type: boolean
    required: false
    description: "Quiet mode"
    aliases:
      - -q
      - --quiet
  - name: flag-o
    type: string
    required: false
    description: "Output file"
    aliases:
      - -o
      - --output
execution:
  template: "routersploit -t {target}"
  sandbox: execFile
  timeout_seconds: 300
  shell: false
global_vars:
  target: "192.168.1.1"
  port: "80"
examples:
  - description: "Scan target router for vulnerabilities"
    command: routersploit -t 192.168.1.1 -s
  - description: "Run a specific exploit module"
    command: routersploit -t 192.168.1.1 -e exploits/routers/dlink/dir_815_creds
  - description: "Fuzz a device on custom port"
    command: routersploit -t 192.168.1.1 -p 8080 -f
  - description: "Quick scan with specific module"
    command: routersploit -t 192.168.1.1 -m scanners/autopwn
  - description: "Test credentials against target"
    command: routersploit -t 192.168.1.1 -c admin:admin
  - description: "Verbose output for debugging"
    command: routersploit -t 192.168.1.1 -m exploits/routers/dlink/dir_859_exec -v
  - description: "Save output to file"
    command: routersploit -t 192.168.1.1 -s -o scan_results.txt
references:
  - label: "RouterSploit GitHub"
    url: "https://github.com/threat9/routersploit"
  - label: "RouterSploit Wiki"
    url: "https://github.com/threat9/routersploit/wiki"
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
# RouterSploit — Embedded Device Exploitation Framework

RouterSploit is an open-source exploitation framework dedicated to embedded devices. It provides modules for scanning, exploiting, and fuzzing vulnerabilities in routers, cameras, and other IoT/embedded systems.

## Module Categories

- **Exploits**: Pre-built exploits for router/device vulnerabilities
- **Scanners**: Service and vulnerability detection modules
- **Fuzzers**: Protocol and parameter fuzzing modules
- **Credentials**: Default credential checking against known devices
- **Payloads**: Payload delivery for device exploitation
