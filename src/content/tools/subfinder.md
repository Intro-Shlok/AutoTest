---
id: security-recon-subfinder
namespace: security:recon:subfinder
name: subfinder
description: Fast passive subdomain discovery tool from ProjectDiscovery that queries
  dozens of online sources to find valid subdomains for target domains.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - network.discovery.subdomain
  - security.recon.passive
  - network.discovery.dns
  - network.discovery.dns-resolve
platforms:
  - linux
  - macos
  - windows
  - cross-platform
risk_level: low
trust_level: verified
execution_policy: enabled
architectures:
  - amd64
  - arm64
dependencies: []
related_tools:
  - amass
  - assetfinder
  - dnsenum
  - fierce
  - httpx
artifacts:
  - type: security.recon.subdomain.list
    description: List of discovered subdomains
    mime: text/plain
    trust_level: verified
  - type: security.recon.subdomain.json
    description: Subdomains in JSONL format
    mime: application/json
    trust_level: verified
workflow_edges:
  produces:
    - subdomains
    - resolved-ips
  consumes:
    - domain
contract:
  inputs:
    - type: network.target.domain
      description: Target domain name
    - type: network.target.domain.list
      description: File containing multiple domains
  outputs:
    - type: security.recon.subdomain.list
      description: List of discovered subdomains
      mime: text/plain
    - type: security.recon.subdomain.json
      description: JSONL output with source metadata
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
  - subfinder
  - Bash
  - execFile
parameters:
  - name: flag-d
    type: string
    required: false
    description: "Target domain to find subdomains for"
    aliases:
      - -d
      - -domain
  - name: flag-dL
    type: file
    required: false
    description: "File containing list of domains"
    aliases:
      - -dL
      - -list
  - name: flag-s
    type: string
    required: false
    description: "Specific sources to use for discovery"
    aliases:
      - -s
      - -sources
  - name: flag-es
    type: string
    required: false
    description: "Sources to exclude from enumeration"
    aliases:
      - -es
      - -exclude-sources
  - name: all
    type: boolean
    required: false
    description: "Use all sources for enumeration (slow)"
    aliases:
      - -all
  - name: recursive
    type: boolean
    required: false
    description: "Use only recursive-capable sources"
    aliases:
      - -recursive
  - name: flag-m
    type: string
    required: false
    description: "Subdomains to match (file or comma separated)"
    aliases:
      - -m
      - -match
  - name: flag-f
    type: string
    required: false
    description: "Subdomains to filter (file or comma separated)"
    aliases:
      - -f
      - -filter
  - name: flag-rl
    type: integer
    required: false
    description: "Maximum HTTP requests per second"
    aliases:
      - -rl
      - -rate-limit
  - name: flag-t
    type: integer
    required: false
    description: "Number of concurrent goroutines"
    default_value: "10"
    aliases:
      - -t
  - name: flag-o
    type: string
    required: false
    description: "File to write output to"
    aliases:
      - -o
      - -output
  - name: flag-oJ
    type: boolean
    required: false
    description: "Write output in JSONL format"
    aliases:
      - -oJ
      - -json
  - name: flag-oD
    type: string
    required: false
    description: "Directory to write output (-dL only)"
    aliases:
      - -oD
      - -output-dir
  - name: flag-nW
    type: boolean
    required: false
    description: "Display active subdomains only"
    aliases:
      - -nW
      - -active
  - name: flag-r
    type: string
    required: false
    description: "Comma separated list of resolvers to use"
    aliases:
      - -r
  - name: silent
    type: boolean
    required: false
    description: "Show only subdomains in output"
    aliases:
      - -silent
  - name: version
    type: boolean
    required: false
    description: "Show version of subfinder"
    aliases:
      - -version
  - name: flag-ls
    type: boolean
    required: false
    description: "List all available sources"
    aliases:
      - -ls
      - -list-sources
  - name: flag-config
    type: file
    required: false
    description: "Config file path"
    aliases:
      - -config
  - name: timeout
    type: integer
    required: false
    description: "Seconds to wait before timing out"
    default_value: "30"
    aliases:
      - -timeout
  - name: max-time
    type: integer
    required: false
    description: "Minutes to wait for enumeration results"
    default_value: "10"
    aliases:
      - -max-time
execution:
  template: "subfinder -d {domain} -o {output}"
  sandbox: execFile
  timeout_seconds: 600
  shell: false
global_vars:
  target: domain
  domain: "example.com"
  output: "subdomains.txt"
examples:
  - description: "Basic subdomain enumeration for a single domain"
    command: subfinder -d example.com
  - description: "Use all available sources"
    command: subfinder -d example.com -all
  - description: "Save output to a file"
    command: subfinder -d example.com -o results.txt
  - description: "JSON output for pipeline integration"
    command: subfinder -d example.com -oJ
  - description: "Silent mode — only print subdomains"
    command: subfinder -d example.com -silent
  - description: "Use specific sources only"
    command: subfinder -d example.com -s crtsh,github
  - description: "Exclude certain sources"
    command: subfinder -d example.com -es alienvault,zoomeyeapi
  - description: "Rate limit to 10 requests per second"
    command: subfinder -d example.com -rl 10
  - description: "Active subdomain resolution"
    command: subfinder -d example.com -nW
  - description: "Enumerate multiple domains from a file"
    command: subfinder -dL domains.txt
  - description: "List all available data sources"
    command: subfinder -ls
references:
  - label: "Subfinder GitHub"
    url: "https://github.com/projectdiscovery/subfinder"
  - label: "Subfinder Documentation"
    url: "https://docs.projectdiscovery.io/opensource/subfinder/overview"
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
    - method: go
      repo_url: "github.com/projectdiscovery/subfinder/v2/cmd/subfinder"
      commands:
        - "go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest"
    - method: apt
      package_name: "subfinder"
      commands:
        - "apt-get install -y subfinder"
---

# Subfinder — Passive Subdomain Discovery

Subfinder is a fast passive subdomain enumeration tool from ProjectDiscovery. It queries over 40 online sources including certificate transparency logs, search engines, and threat intelligence platforms to discover valid subdomains without actively probing the target.

## Features

- **40+ passive sources**: Certificate transparency, DNS datasets, search engines, APIs
- **Fast and stealthy**: No direct contact with target infrastructure
- **Easy integration**: STDIN/STDOUT for pipeline workflows
- **Configurable**: Per-source rate limiting, source selection, proxy support

## Basic Usage

```bash
# Standard subdomain enumeration
subfinder -d example.com

# Full results with all sources
subfinder -d example.com -all -oJ

# Pipe to httpx for HTTP probing
subfinder -d example.com -silent | httpx -title -status-code
```
