---
id: security-recon-assetfinder
namespace: security:recon:assetfinder
name: assetfinder
description: Command-line tool that finds domains and subdomains potentially related
  to a given domain using passive sources.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - network.discovery.subdomain
  - security.recon.passive
  - network.discovery.domain
platforms:
  - linux
  - macos
  - cross-platform
risk_level: low
trust_level: community
execution_policy: enabled
architectures:
  - amd64
  - arm64
dependencies: []
related_tools:
  - subfinder
  - amass
  - findomain
artifacts:
  - type: security.recon.domain.list
    description: List of related domains and subdomains
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - subdomains
    - related-domains
  consumes:
    - domain
contract:
  inputs:
    - type: network.target.domain
      description: Target domain name
  outputs:
    - type: security.recon.domain.list
      description: Related domains and subdomains
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
  - assetfinder
  - Bash
  - execFile
parameters:
  - name: domain
    type: string
    required: true
    description: "Target domain to find assets for"
  - name: subs-only
    type: boolean
    required: false
    description: "Only show subdomains, exclude related domains"
    aliases:
      - --subs-only
  - name: flag-f
    type: boolean
    required: false
    description: "Filter out unverified domains"
    aliases:
      - -f
      - --filter
    default_value: "false"
execution:
  template: "assetfinder {domain}"
  sandbox: execFile
  timeout_seconds: 120
  shell: false
global_vars:
  target: domain
  domain: "example.com"
examples:
  - description: "Basic domain asset discovery"
    command: assetfinder example.com
  - description: "Show only subdomains (exclude related domains)"
    command: assetfinder --subs-only example.com
  - description: "Filter output for verified domains only"
    command: assetfinder --subs-only example.com | sort -u
references:
  - label: "Assetfinder GitHub"
    url: "https://github.com/tomnomnom/assetfinder"
phase: enumeration
techniques:
  - discovery
items:
  - NoCreds
services: []
attack_types:
  - Enumeration
---

# Assetfinder — Domain & Subdomain Discovery

Assetfinder is a lightweight tool that finds domains and subdomains potentially related to a given domain. It sources data from certificate transparency logs, DNS records, and other public intelligence sources.

## Usage

```bash
# Basic discovery
assetfinder example.com

# Subdomains only
assetfinder --subs-only example.com

# Pipe to httpx for live host verification
assetfinder example.com | httpx -silent
```
