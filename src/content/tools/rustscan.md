---
id: security-recon-rustscan
namespace: security:recon:rustscan
name: rustscan
description: Lightning-fast port scanner written in Rust that automatically pipes results
  into Nmap for service detection and scripting.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - network.scan.port
  - network.discovery.host
  - security.fingerprint.service
platforms:
  - linux
  - macos
  - windows
  - cross-platform
risk_level: medium
trust_level: community
execution_policy: enabled
architectures:
  - amd64
  - arm64
dependencies:
  - nmap
related_tools:
  - nmap
  - masscan
  - naabu
artifacts:
  - type: network.scan.port.list
    description: List of open ports from fast scan
    mime: text/plain
    trust_level: verified
  - type: network.scan.nmap.xml
    description: Nmap XML output when piped to Nmap
    mime: application/xml
    trust_level: verified
workflow_edges:
  produces:
    - open-ports
    - scan-results
  consumes:
    - target-ip
    - target-range
contract:
  inputs:
    - type: network.target.ip
      description: Target IP address or hostname
    - type: network.target.range
      description: IP range or CIDR notation
  outputs:
    - type: network.scan.port.list
      description: Discovered open ports
      mime: text/plain
  side_effects:
    - network_traffic
  resource_cost:
    cpu: low
    memory_mb: 32
    network: medium
    disk_io: low
resource_profile:
  cpu: low
  memory_mb: 32
  network: medium
  disk_io: low
allowed-tools:
  - rustscan
  - Bash
  - execFile
parameters:
  - name: flag-a
    type: string
    required: true
    description: "Target IP address, hostname, or CIDR range"
    aliases:
      - -a
      - --address
  - name: flag-p
    type: string
    required: false
    description: "Ports to scan (e.g. 80,443 or 1-65535)"
    default_value: "1-65535"
    aliases:
      - -p
      - --ports
  - name: flag-b
    type: integer
    required: false
    description: "Batch size for port scanning"
    default_value: "4500"
    aliases:
      - -b
      - --batch
  - name: timeout
    type: integer
    required: false
    description: "Timeout in milliseconds (default 1500)"
    default_value: "1500"
    aliases:
      - --timeout
  - name: tries
    type: integer
    required: false
    description: "Number of tries before giving up on a port"
    default_value: "1"
    aliases:
      - --tries
  - name: flag-n
    type: boolean
    required: false
    description: "Do not run Nmap automatically"
    aliases:
      - -n
      - --no-nmap
  - name: range
    type: string
    required: false
    description: "CIDR range to scan"
    aliases:
      - --range
  - name: accessible
    type: boolean
    required: false
    description: "Only show accessible ports"
    aliases:
      - --accessible
  - name: greppable
    type: boolean
    required: false
    description: "Greppable output format"
    aliases:
      - -g
      - --greppable
  - name: flag-u
    type: boolean
    required: false
    description: "Scan UDP ports (experimental)"
    aliases:
      - -u
      - --udp
execution:
  template: "rustscan -a {target} -p {ports} --batch {batch} --timeout {timeout}"
  sandbox: execFile
  timeout_seconds: 300
  shell: false
global_vars:
  target: ip
  ports: "1-65535"
  batch: "4500"
  timeout: "1500"
examples:
  - description: "Scan all ports on a single target with default Nmap integration"
    command: rustscan -a 10.10.10.1
  - description: "Scan specific ports with custom batch size"
    command: rustscan -a 10.10.10.1 -p 22,80,443 -b 2000
  - description: "Scan without auto-Nmap"
    command: rustscan -a scanme.nmap.org -n
  - description: "Scan a CIDR range"
    command: rustscan -a 10.10.10.0/24 --range 1-1000
  - description: "Greppable output for scripting"
    command: rustscan -a 10.10.10.1 -g
  - description: "UDP scan (experimental)"
    command: rustscan -a 10.10.10.1 -u -p 53,161
references:
  - label: "RustScan GitHub"
    url: "https://github.com/RustScan/RustScan"
phase: enumeration
techniques:
  - discovery
  - enumeration
items:
  - NoCreds
services: []
attack_types:
  - Enumeration
install:
    - method: apt
      package_name: "rustscan"
      commands:
        - "apt-get install -y rustscan"
    - method: cargo
      package_name: "rustscan"
      commands:
        - "cargo install rustscan"
---

# RustScan — Fast Port Scanner with Nmap Integration

RustScan is a modern port scanner written in Rust that optimizes the scanning workflow by automatically piping all discovered open ports into Nmap for detailed service enumeration and NSE script execution.

## Key Features

- **Blazing fast**: Scans all 65k ports in ~3 seconds
- **Automatic Nmap integration**: Pipes results directly to Nmap
- **Adaptive batching**: Automatically adjusts batch size based on target responsiveness
- **Scriptable output**: Greppable format for easy parsing

## Basic Usage

```bash
# Basic scan with Nmap auto-integration
rustscan -a 10.10.10.1

# Fast port-only scan, skip Nmap
rustscan -a 10.10.10.1 -n

# Scan specific ports
rustscan -a 10.10.10.1 -p 22,80,443,8080
```

## Performance Tuning

- `-b` controls batch size (default: 4500); lower for unstable connections
- `--timeout` in milliseconds; increase for high-latency targets
- `--tries` increases reliability on lossy networks
