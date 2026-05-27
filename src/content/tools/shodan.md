---
id: security-intel-shodan-cli
namespace: security:intel:shodan
name: shodan
description: Command-line interface to the Shodan search engine for discovering internet-connected
  devices, open ports, and service banners.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - security.intel.osint
  - security.recon.passive
  - network.discovery.host
  - security.fingerprint.service
  - security.intel.vulnerability
  - network.discovery.iot
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
  - censys
  - zoomEye
  - recon-ng
  - theharvester
artifacts:
  - type: security.intel.shodan.search
    description: Shodan search results
    mime: application/json
    trust_level: verified
  - type: security.intel.shodan.host
    description: Shodan host information
    mime: application/json
    trust_level: verified
workflow_edges:
  produces:
    - host-info
    - search-results
    - port-banners
  consumes:
    - ip-address
    - search-query
contract:
  inputs:
    - type: network.target.ip
      description: IP address to query
    - type: security.intel.search.query
      description: Search query string
  outputs:
    - type: security.intel.shodan.host
      description: Host information including ports and banners
      mime: application/json
    - type: security.intel.shodan.search
      description: Search results
      mime: application/json
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
  - shodan
  - Bash
  - execFile
parameters:
  - name: command
    type: string
    required: true
    description: "Shodan command (search, host, count, download, scan, etc.)"
  - name: args
    type: string
    required: false
    description: "Arguments for the subcommand"
execution:
  template: "shodan {command} {args}"
  sandbox: execFile
  timeout_seconds: 60
  shell: false
global_vars:
  target: ip
  command: "host"
  args: "8.8.8.8"
examples:
  - description: "Initialize Shodan with API key"
    command: shodan init YOUR_API_KEY
  - description: "Search for devices running Apache"
    command: shodan search apache
  - description: "View host information for an IP"
    command: shodan host 8.8.8.8
  - description: "Count results for a search query"
    command: shodan count "product:nginx"
  - description: "Download search results to a file"
    command: shodan download results.json.gz "port:22 country:US"
  - description: "Parse downloaded results"
    command: shodan parse results.json.gz
  - description: "Scan an IP or netblock"
    command: shodan scan submit 10.0.0.0/24
  - description: "Check if an IP is a honeypot"
    command: shodan honeyscore 185.220.101.1
  - description: "My public IP info"
    command: shodan myip
  - description: "Monitor network with alerts"
    command: shodan alert create "My Alert" 10.0.0.0/24
references:
  - label: "Shodan CLI Documentation"
    url: "https://cli.shodan.io/"
  - label: "Shodan Website"
    url: "https://www.shodan.io/"
phase: enumeration
techniques:
  - discovery
  - enumeration
  - recon
items:
  - NoCreds
services: []
attack_types:
  - Enumeration
---

# Shodan CLI — Internet Device Search Engine

Shodan is a search engine for internet-connected devices. The CLI tool provides programmatic access to the Shodan database, allowing you to search for specific technologies, view host details, download datasets, and set up continuous monitoring.

## Search Filters

| Filter | Description | Example |
|--------|-------------|---------|
| `port` | Filter by port number | `port:22` |
| `country` | Filter by country code | `country:US` |
| `org` | Filter by organization | `org:"Google"` |
| `product` | Filter by product name | `product:nginx` |
| `os` | Filter by operating system | `os:Linux` |
| `vuln` | Filter by vulnerability | `vuln:CVE-2021-41773` |

## Usage

```bash
# Search with filters
shodan search "port:443 product:Apache country:JP"

# Host summary
shodan host 8.8.8.8

# Download and parse
shodan download data "port:22" --limit 1000
shodan parse data.json.gz
```
