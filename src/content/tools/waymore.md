---
id: security-recon-waymore
namespace: security:recon:waymore
name: waymore
description: Enhanced wayback machine URL fetcher that retrieves historical URLs from Internet Archive and filters results using customizable patterns.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - web.recon.historical-url
  - osint.discovery.url
  - web.recon.wayback
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
  - waybackurls
  - gau
  - unfurl
  - katana
artifacts:
  - type: web.url.list
    description: Historical URLs from Wayback Machine
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - historical-urls
    - url-list
  consumes:
    - target-domain
contract:
  inputs:
    - type: domain.name
      description: Target domain name
  outputs:
    - type: web.url.list
      description: Discovered historical URLs
      mime: text/plain
  side_effects:
    - network_traffic
  resource_cost:
    cpu: low
    memory_mb: 128
    network: medium
    disk_io: low
resource_profile:
  cpu: low
  memory_mb: 128
  network: medium
  disk_io: low
allowed-tools:
  - waymore
  - python3
  - Bash
  - execFile
parameters:
  - name: target
    type: string
    required: true
    description: "Target domain name"
    aliases:
      - -i
      - --input
  - name: flag-output
    type: string
    required: false
    description: "Output directory for results"
    aliases:
      - -o
      - --output
  - name: flag-mode
    type: string
    required: false
    description: "Filter mode (only-urls, only-params, both)"
    aliases:
      - -m
      - --mode
  - name: flag-fetch
    type: boolean
    required: false
    description: "Fetch status codes for discovered URLs"
    aliases:
      - -f
      - --fetch
  - name: flag-pull
    type: boolean
    required: false
    description: "Pull page content from archive"
    aliases:
      - -p
      - --pull
  - name: flag-verbose
    type: boolean
    required: false
    description: "Verbose output"
    aliases:
      - -v
      - --verbose
execution:
  template: "waymore {flag-mode} {flag-fetch} {flag-pull} {flag-verbose} -i {target} {flag-output}"
  sandbox: execFile
  timeout_seconds: 300
  shell: false
examples:
  - description: "Basic URL discovery"
    command: waymore -i example.com
  - description: "Fetch URL status codes"
    command: waymore -i example.com -f
  - description: "Only URLs with parameters"
    command: waymore -i example.com -m only-params
references:
  - label: "waymore GitHub"
    url: "https://github.com/xnl-h4ck3r/waymore"
phase: recon
techniques:
  - recon
  - discovery
items:
  - NoCreds
services:
  - HTTP
attack_types:
  - Discovery
  - Enumeration
---

# waymore — Wayback Machine URL Enumerator

waymore is a Python-based tool for fetching historical URLs from the Internet Archive (Wayback Machine). It extends basic wayback URL fetching with filtering, status code checking, and content retrieval capabilities.

## Usage

```bash
# Basic URL discovery
waymore -i example.com

# Fetch status codes
waymore -i example.com -f

# Filter URLs with parameters only
waymore -i example.com -m only-params

# Save to custom directory
waymore -i example.com -o ./results
```
