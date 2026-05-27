---
id: security-web-paramspider
namespace: security:web:paramspider
name: paramspider
description: Tool for mining parameters from web archives to discover hidden endpoints, GET/POST parameters, and potential injection points.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - web.discovery.endpoint
  - web.enumeration.parameter
  - security.recon.passive
  - web.archive.url
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
  - gau
  - waybackurls
  - arjun
  - katana
artifacts:
  - type: crawl.txt
    description: Discovered parameterized URLs
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - param-list
    - url-list
  consumes:
    - target-domain
contract:
  inputs:
    - type: network.target.domain
      description: Target domain to mine parameters from
  outputs:
    - type: crawl.txt
      description: List of URLs with discovered parameters
      mime: text/plain
  side_effects:
    - network_traffic
  resource_cost:
    cpu: low
    memory_mb: 64
    network: low
    disk_io: low
resource_profile:
  cpu: low
  memory_mb: 64
  network: low
  disk_io: low
allowed-tools:
  - paramspider
  - Bash
  - execFile
parameters:
  - name: domain
    type: string
    required: false
    description: "Target domain name"
    aliases:
      - -d
      - --domain
  - name: flag-o
    type: string
    required: false
    description: "Output file path"
    aliases:
      - -o
      - --output
  - name: flag-level
    type: string
    required: false
    description: "Filter level (high, low)"
    aliases:
      - -l
      - --level
  - name: flag-exclude
    type: string
    required: false
    description: "Exclude file extensions (comma separated)"
    aliases:
      - -e
      - --exclude
  - name: flag-priority
    type: boolean
    required: false
    description: "Only show URLs with parameters"
    aliases:
      - -p
      - --priority
  - name: flag-silent
    type: boolean
    required: false
    description: "Silent mode"
    aliases:
      - -s
      - --silent
execution:
  template: "paramspider {flags} {domain}"
  sandbox: execFile
  timeout_seconds: 120
  shell: false
examples:
  - description: "Mine parameters for a domain"
    command: paramspider -d example.com
  - description: "Mine with custom output file"
    command: paramspider -d example.com -o results.txt
  - description: "Exclude image file extensions"
    command: paramspider -d example.com --exclude png,jpg,gif,css,js
  - description: "High-level filtering for cleaner results"
    command: paramspider -d example.com --level high --priority
  - description: "Silent mode for pipeline"
    command: paramspider -d example.com --silent | httpx -status-code -title
references:
  - label: "ParamSpider GitHub"
    url: "https://github.com/devanshbatham/ParamSpider"
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

# ParamSpider — Web Archive Parameter Mining

ParamSpider mines parameters from web archive sources to discover hidden GET/POST parameters and potential injection points for web applications. It helps identify attack surface that may be missed by traditional crawling.

## Workflow

```bash
# Mine parameters and test with ffuf
paramspider -d target.com --silent | sort -u | ffuf -u "DOMAIN" -w - -mc 200

# Mine and probe live endpoints
paramspider -d target.com --silent | grep "\.php" | httpx -status-code

# Mine parameters with high-level filtering
paramspider -d target.com --level high --priority -o params.txt
```
