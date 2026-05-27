---
id: security-recon-spiderfoot
namespace: security:recon:spiderfoot
name: spiderfoot
description: Open-source intelligence automation tool that queries over 200 data sources
  for email, domain, IP, and web footprinting.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - security.intel.osint
  - security.recon.passive
  - security.intel.email
  - network.discovery.subdomain
  - security.intel.vulnerability
  - security.intel.breach
  - security.recon.framework
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
  - recon-ng
  - maltego
  - theharvester
  - shodan
artifacts:
  - type: security.recon.report
    description: SpiderFoot scan report
    mime: text/html
    trust_level: verified
  - type: security.recon.events
    description: SpiderFoot event data
    mime: application/json
    trust_level: community
workflow_edges:
  produces:
    - recon-data
    - scan-results
    - correlated-events
  consumes:
    - domain
    - ip-address
    - email
    - url
contract:
  inputs:
    - type: network.target.domain
      description: Target domain name
    - type: network.target.ip
      description: Target IP address
    - type: security.target.email
      description: Email address
    - type: network.target.url
      description: Target URL
  outputs:
    - type: security.recon.report
      description: Scan report with OSINT findings
      mime: text/html
    - type: security.recon.events
      description: Event data as JSON
      mime: application/json
  side_effects:
    - network_traffic
    - network_traffic
    - network_traffic
  resource_cost:
    cpu: medium
    memory_mb: 256
    network: medium
    disk_io: low
resource_profile:
  cpu: medium
  memory_mb: 256
  network: medium
  disk_io: low
allowed-tools:
  - spiderfoot
  - Bash
  - execFile
parameters:
  - name: flag-s
    type: string
    required: false
    description: "Target for the scan"
    aliases:
      - -s
  - name: flag-t
    type: string
    required: false
    description: "Event types to collect (modules selected automatically)"
    aliases:
      - -t
  - name: flag-u
    type: string
    required: false
    description: "Select modules by use case (all, footprint, investigate, passive)"
    aliases:
      - -u
  - name: flag-o
    type: string
    required: false
    description: "Output format (tab, csv, json)"
    default_value: "tab"
    aliases:
      - -o
  - name: flag-l
    type: string
    required: false
    description: "IP and port to listen on (web UI)"
    aliases:
      - -l
  - name: flag-d
    type: boolean
    required: false
    description: "Enable debug output"
    aliases:
      - -d
      - --debug
  - name: flag-m
    type: string
    required: false
    description: "Modules to enable (comma-separated)"
    aliases:
      - -m
  - name: flag-M
    type: boolean
    required: false
    description: "List available modules"
    aliases:
      - -M
      - --modules
  - name: flag-T
    type: boolean
    required: false
    description: "List available event types"
    aliases:
      - -T
      - --types
  - name: flag-x
    type: boolean
    required: false
    description: "Strict mode — only enable directly-consumable modules"
    aliases:
      - -x
  - name: flag-q
    type: boolean
    required: false
    description: "Disable logging"
    aliases:
      - -q
  - name: flag-C
    type: string
    required: false
    description: "Run correlation rules against a scan ID"
    aliases:
      - -C
      - --correlate
  - name: max-threads
    type: integer
    required: false
    description: "Max number of modules to run concurrently"
    aliases:
      - -max-threads
execution:
  template: "spiderfoot -s {target}"
  sandbox: execFile
  timeout_seconds: 3600
  shell: false
global_vars:
  target: domain
  domain: "example.com"
examples:
  - description: "Basic footprint scan on a domain"
    command: spiderfoot -s example.com
  - description: "Full scan with all modules"
    command: spiderfoot -s example.com -u all
  - description: "Passive only scan (no direct contact)"
    command: spiderfoot -s example.com -u passive
  - description: "Investigate an IP address"
    command: spiderfoot -s 8.8.8.8 -u investigate
  - description: "Specific event types only"
    command: spiderfoot -s example.com -t "DOMAIN_NAME,IP_ADDRESS"
  - description: "JSON output for pipeline processing"
    command: spiderfoot -s example.com -o json
  - description: "Launch web UI on custom port"
    command: spiderfoot -l 127.0.0.1:5001
  - description: "List all available modules"
    command: spiderfoot -M
  - description: "Run correlation rules against a completed scan"
    command: spiderfoot -C SCAN_ID
references:
  - label: "SpiderFoot GitHub"
    url: "https://github.com/smicallef/spiderfoot"
  - label: "SpiderFoot Documentation"
    url: "https://www.spiderfoot.net/documentation/"
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

# SpiderFoot — OSINT Automation

SpiderFoot is an open-source intelligence automation tool that queries over 200 data sources to build comprehensive profiles of domains, IP addresses, email addresses, and URLs. It operates in both CLI and web UI modes.

## Scan Types

| Use Case | Description |
|----------|-------------|
| `passive` | No direct contact with target infrastructure |
| `footprint` | Broad information gathering |
| `investigate` | Deep investigation of target |
| `all` | All available modules |

## Data Sources Over 200

- Search engines (Google, Bing, Yahoo)
- Threat intelligence (AlienVault, VirusTotal, Shodan)
- Certificate transparency logs
- DNS records and whois
- Data breach databases
- Social media platforms
- Code repositories
