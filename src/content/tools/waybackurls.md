---
id: security-web-waybackurls
namespace: security:web:waybackurls
name: waybackurls
description: Tool for fetching historical URLs from the Wayback Machine archive for discovering endpoints, parameters, and attack surface of target domains.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - web.discovery.endpoint
  - web.archive.url
  - security.recon.passive
  - web.enumeration.parameter
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
dependencies: []
related_tools:
  - gau
  - paramspider
  - katana
  - arjun
artifacts:
  - type: crawl.txt
    description: Historical URLs from Wayback Machine
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - url-list
    - endpoint-list
  consumes:
    - target-domain
contract:
  inputs:
    - type: network.target.domain
      description: Target domain to fetch URLs for
  outputs:
    - type: crawl.txt
      description: List of discovered historical URLs
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
  - waybackurls
  - Bash
  - execFile
parameters:
  - name: dates
    type: boolean
    required: false
    description: "Include timestamp for each URL"
    aliases:
      - -dates
  - name: no-subs
    type: boolean
    required: false
    description: "Exclude subdomain URLs"
    aliases:
      - -no-subs
  - name: flag-s
    type: string
    required: false
    description: "File containing list of domains"
    aliases:
      - -s
      - --subs
execution:
  template: "waybackurls {target} {flags}"
  sandbox: execFile
  timeout_seconds: 60
  shell: false
examples:
  - description: "Fetch all historical URLs for a domain"
    command: waybackurls example.com
  - description: "Fetch URLs and include dates"
    command: waybackurls -dates example.com
  - description: "Fetch URLs from multiple domains"
    command: cat domains.txt | waybackurls
  - description: "Filter for JavaScript files"
    command: waybackurls example.com | grep "\.js$"
  - description: "Filter for parameters"
    command: waybackurls example.com | grep "?.*="
references:
  - label: "waybackurls GitHub"
    url: "https://github.com/tomnomnom/waybackurls"
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
---

# waybackurls — Wayback Machine URL Fetcher

waybackurls is a tool by TomNomNom that fetches historical URLs for a target domain from the Wayback Machine's CDX API, enabling passive discovery of endpoints, parameters, and hidden attack surface without directly interacting with the target.

## Common Pipelines

```bash
# Find JavaScript files
waybackurls target.com | grep "\.js$" | sort -u

# Find endpoints with parameters
waybackurls target.com | grep "?.*=" | sort -u

# Filter for specific file types
waybackurls target.com | grep -E "\.(php|asp|jsp)"

# Extract unique parameters
waybackurls target.com | grep -oP "[\?&]\K[^=]+" | sort -u

# Find Wayback URLs then probe with httpx
waybackurls target.com | sort -u | httpx -status-code -title
```
