---
id: security-recon-masscan
namespace: security:recon:masscan
name: masscan
description: High-speed TCP port scanner capable of scanning the entire internet in
  minutes, supporting banner grab, configurable rate limits, and multiple output formats.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - network.scan.port
  - network.discovery.host
  - security.fingerprint.service
  - security.evasion.firewall
  - network.scan.banner
platforms:
  - linux
  - macos
  - cross-platform
risk_level: medium
trust_level: verified
execution_policy: enabled
architectures:
  - amd64
  - arm64
dependencies: []
related_tools:
  - nmap
  - rustscan
  - zenmap
artifacts:
  - type: network.scan.binary
    description: Binary scan results for later processing
    mime: application/octet-stream
    trust_level: verified
  - type: network.scan.xml
    description: XML-formatted scan results
    mime: application/xml
    trust_level: verified
  - type: network.scan.json
    description: JSON-formatted scan results
    mime: application/json
    trust_level: verified
workflow_edges:
  produces:
    - scan-results
    - open-ports
    - host-list
  consumes:
    - target-ip
    - target-range
contract:
  inputs:
    - type: network.target.ip
      description: Target IP address or CIDR range
    - type: network.target.range
      description: IP range in CIDR notation
    - type: network.port.range
      description: Port range or comma-separated ports
  outputs:
    - type: network.scan.json
      description: Scan results as JSON
      mime: application/json
    - type: network.scan.xml
      description: Scan results as XML
      mime: application/xml
  side_effects:
    - network_traffic
    - raw_socket_access
  resource_cost:
    cpu: medium
    memory_mb: 64
    network: high
    disk_io: low
resource_profile:
  cpu: medium
  memory_mb: 64
  network: high
  disk_io: low
allowed-tools:
  - masscan
  - Bash
  - execFile
parameters:
  - name: flag-p
    type: string
    required: false
    description: "Ports to scan (e.g. -p80, -p1-65535)"
    aliases:
      - -p
      - --ports
  - name: rate
    type: integer
    required: false
    description: "Packets per second (default 100)"
    default_value: "100"
    aliases:
      - --rate
  - name: flag-oJ
    type: string
    required: false
    description: "Output to JSON file"
    aliases:
      - -oJ
      - --output-json
  - name: flag-oX
    type: string
    required: false
    description: "Output to XML file"
    aliases:
      - -oX
      - --output-xml
  - name: flag-oB
    type: string
    required: false
    description: "Output to binary file"
    aliases:
      - -oB
      - --output-binary
  - name: adapter-ip
    type: string
    required: false
    description: "IP address of the network adapter"
    aliases:
      - --adapter-ip
  - name: adapter-port
    type: string
    required: false
    description: "Source port for outgoing packets"
    aliases:
      - --adapter-port
  - name: adapter-mac
    type: string
    required: false
    description: "MAC address of the network adapter"
    aliases:
      - --adapter-mac
  - name: router-mac
    type: string
    required: false
    description: "MAC address of the gateway router"
    aliases:
      - --router-mac
  - name: exclude
    type: string
    required: false
    description: "IP addresses to exclude from scan"
    aliases:
      - --exclude
  - name: excludefile
    type: file
    required: false
    description: "File with IPs to exclude"
    aliases:
      - --excludefile
  - name: banners
    type: boolean
    required: false
    description: "Grab banners from open ports"
    aliases:
      - --banners
  - name: nmap
    type: boolean
    required: false
    description: "List options compatible with nmap"
    aliases:
      - --nmap
execution:
  template: "masscan {target} -p{ports} --rate={rate}"
  sandbox: execFile
  timeout_seconds: 600
  shell: false
global_vars:
  target: ip
  ports: "80,443"
  rate: "10000"
examples:
  - description: "Scan a subnet for web servers"
    command: masscan 10.0.0.0/8 -p80,443 --rate=10000
  - description: "Scan specific IP for all ports with banners"
    command: masscan 192.168.1.1 -p1-65535 --banners --rate=1000
  - description: "Output results to JSON file"
    command: masscan 10.0.0.0/24 -p22,80,443 -oJ scan.json --rate=1000
  - description: "Scan with custom adapter settings"
    command: masscan 10.0.0.0/8 -p80 --adapter-ip 192.168.1.100 --adapter-mac 00-11-22-33-44-55 --router-mac 66-55-44-33-22-11
  - description: "Exclude specific IPs from a range scan"
    command: masscan 10.0.0.0/8 -p443 --exclude 10.0.0.1 --rate=10000
  - description: "Binary output for later reprocessing"
    command: masscan 10.0.0.0/8 -p80,443 --banners -oB session.scan --rate=10000
  - description: "Read binary scan results and convert to XML"
    command: masscan --open --banners --readscan session.scan -oX results.xml
  - description: "List nmap-compatible options"
    command: masscan --nmap
references:
  - label: "Masscan GitHub"
    url: "https://github.com/robertdavidgraham/masscan"
  - label: "Masscan documentation"
    url: "https://github.com/robertdavidgraham/masscan/wiki"
phase: enumeration
techniques:
  - discovery
  - enumeration
items:
  - NoCreds
services: []
attack_types:
  - Enumeration
---

# Masscan — High-Speed Port Scanner

Masscan is the fastest TCP port scanner available, capable of scanning the entire internet in about 5 minutes when sent at 10 million packets per second. It uses asynchronous transmission similar to `nmap -sS` but with a custom TCP/IP stack for maximum performance.

## Key Features

- **Massively parallel**: Scans the entire IPv4 internet in minutes
- **Banner grab**: Captures service banners from open ports  
- **Multiple output formats**: Binary, XML, JSON, grepable
- **Nmap compatibility**: Many options mirror nmap syntax
- **Config file support**: Save and reuse scan configurations

## Basic Scan Types

| Scan Type | Command | Description |
|-----------|---------|-------------|
| Single port | `masscan target -p80` | Scan a single port on target |
| Port range | `masscan target -p1-65535` | Scan all 65535 ports |
| Multiple ports | `masscan target -p22,80,443,8080` | Scan specific ports |
| CIDR range | `masscan 10.0.0.0/8 -p443` | Scan an entire subnet |
| With banners | `masscan target -p80 --banners` | Grab service banners |

## Output Formats

```bash
# Binary (compact, for later reprocessing)
masscan target -p80 -oB session.scan

# XML (machine-parseable)
masscan target -p80 -oX scan.xml

# JSON (structured)
masscan target -p80 -oJ scan.json

# Grepable (text)
masscan target -p80 > scan.txt
```

## Performance Tuning

- `--rate=100000` — target 100,000 packets per second (default: 100)
- `--adapter-ip` — specify source IP for load balancing across interfaces
- `--shard N/M` — split scan across M machines (this is shard N)

## Operational Security

- Masscan generates extremely high network traffic; use rate limiting responsibly
- Root privileges are required for SYN scans
- Scanning without authorization is illegal in many jurisdictions
- Use `--excludefile` to avoid scanning sensitive IP ranges
