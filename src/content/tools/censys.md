---
id: security-intel-censys
namespace: security:intel:censys
name: censys
description: Command-line interface to the Censys internet asset search engine for discovering exposed devices, certificates, and services across the global internet.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - security.intel.osint
  - security.recon.passive
  - network.discovery.host
  - security.fingerprint.service
  - network.discovery.certificate
platforms:
  - linux
  - macos
  - cross-platform
risk_level: low
trust_level: verified
execution_policy: enabled
architectures:
  - amd64
  - arm64
dependencies:
  - python3
related_tools:
  - shodan
  - zoomEye
artifacts:
  - type: security.intel.search.query
    description: Censys search results
    mime: application/json
    trust_level: verified
  - type: security.intel.shodan.host
    description: Censys host information
    mime: application/json
    trust_level: verified
workflow_edges:
  produces:
    - search-results
    - host-info
    - certificate-data
  consumes:
    - search-query
    - ip-address
contract:
  inputs:
    - type: security.intel.search.query
      description: Censys search query
    - type: network.target.ip
      description: IP address to query
  outputs:
    - type: security.intel.search.query
      description: Search result data
      mime: application/json
    - type: network.scan.json
      description: Host and port information
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
  - censys
  - Bash
  - execFile
parameters:
  - name: search
    type: string
    required: false
    description: "Search query for hosts, certificates, or services"
    aliases:
      - search
  - name: flag-i
    type: string
    required: false
    description: "Query by IP address"
    aliases:
      - -i
      - --ip
  - name: flag-a
    type: boolean
    required: false
    description: "Query by Autonomous System Number"
    aliases:
      - -a
      - --asn
  - name: flag-d
    type: string
    required: false
    description: "Query by domain name"
    aliases:
      - -d
      - --domain
  - name: flag-c
    type: string
    required: false
    description: "Query by certificate SHA-256 fingerprint"
    aliases:
      - -c
      - --certificate
  - name: flag-O
    type: string
    required: false
    description: "Output file for results"
    aliases:
      - -O
      - --output
  - name: flag-j
    type: boolean
    required: false
    description: "Output in JSON format"
    aliases:
      - -j
      - --json
  - name: flag-h
    type: boolean
    required: false
    description: "Show help message"
    aliases:
      - -h
      - --help
execution:
  template: "censys {search} {flags}"
  sandbox: execFile
  timeout_seconds: 60
  shell: false
examples:
  - description: "Search for exposed SSH servers"
    command: 'censys search "services.service_name: SSH"'
  - description: "Lookup IP address information"
    command: censys view 8.8.8.8
  - description: "Search for certificates for a domain"
    command: 'censys search "names: example.com" --index certificates'
  - description: "Export results as JSON"
    command: 'censys search "services.port: 443" --output results.json'
references:
  - label: "Censys CLI Documentation"
    url: "https://search.censys.io/"
phase: recon
techniques:
  - recon
  - discovery
items:
  - NoCreds
services: []
attack_types:
  - Enumeration
  - Discovery
install:
    - method: pip
      package_name: "censys"
      commands:
        - "pip install censys"
---

# Censys — Internet Asset Search Engine

Censys provides a command-line interface to query the Censys internet intelligence platform for discovering exposed devices, open ports, services, and TLS certificates across the public internet. It can be used for attack surface management, asset discovery, and reconnaissance.

## Search Queries

| Pattern | Description |
|---------|-------------|
| `services.service_name: SSH` | Find SSH servers |
| `services.port: 443` | Find HTTPS services |
| `names: example.com` | Search by domain |
| `location.country: Japan` | Filter by country |
| `labels: {cdn,cloud}` | Filter by infrastructure |

## Common Searches

```bash
# Search for exposed databases
censys search "services.service_name: MongoDB"

# Search for all services on a specific IP
censys view 198.51.100.1

# Search for certificates by organization
censys search "organization: Example" --index certificates

# Search with geographic filter
censys search "services.service_name: RDP AND location.country: US"

# Output as JSON
censys search "services.port: 22" --json
```

## Automation

```bash
# Batch query multiple IPs
cat ips.txt | xargs -I{} censys view {} > results.json
```
