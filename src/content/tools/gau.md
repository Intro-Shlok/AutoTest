---
id: security-web-gau
namespace: security:web:gau
name: gau
description: Get All URLs (gau) fetches known URLs from AlienVault's OTX, WayBack Machine, and other public archives for passive endpoint discovery.
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
  - waybackurls
  - paramspider
  - katana
  - arjun
artifacts:
  - type: crawl.txt
    description: Collected historical URLs
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
      description: Target domain to gather URLs for
  outputs:
    - type: crawl.txt
      description: Aggregated list of historical URLs from multiple sources
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
  - gau
  - Bash
  - execFile
parameters:
  - name: flag-o
    type: string
    required: false
    description: "Output file path"
    aliases:
      - -o
      - --output
  - name: flag-providers
    type: string
    required: false
    description: "Comma-separated list of providers (wayback,otx,commoncrawl)"
    aliases:
      - -p
      - --providers
  - name: flag-subdomains
    type: boolean
    required: false
    description: "Include subdomain URLs"
    alises:
      - -s
      - --subdomains
  - name: flag-blacklist
    type: string
    required: false
    description: "File extensions to exclude"
    aliases:
      - -b
      - --blacklist
  - name: flag-threads
    type: integer
    required: false
    description: "Number of concurrent threads"
    aliases:
      - -t
      - --threads
  - name: flag-verbose
    type: boolean
    required: false
    description: "Verbose output"
    aliases:
      - -v
      - --verbose
execution:
  template: "gau {target} {flags}"
  sandbox: execFile
  timeout_seconds: 120
  shell: false
examples:
  - description: "Fetch all URLs for a domain"
    command: gau example.com
  - description: "Fetch URLs including subdomains"
    command: gau --subdomains example.com
  - description: "Fetch from specific providers only"
    command: gau --providers wayback,otx example.com
  - description: "Exclude common file extensions"
    command: gau --blacklist png,jpg,gif,css example.com
  - description: "Multiple domains from stdin"
    command: cat domains.txt | gau --subdomains
  - description: "Pipeline to probe live hosts"
    command: gau example.com | sort -u | httpx -status-code -title
references:
  - label: "gau GitHub"
    url: "https://github.com/lc/gau"
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

# gau — Get All URLs

gau (Get All URLs) collects URLs from multiple public sources including the Wayback Machine, AlienVault OTX, and CommonCrawl. It provides comprehensive passive endpoint discovery for web security assessments and bug bounty hunting.

## Common Pipelines

```bash
# Find parameters
gau target.com | grep "?.*=" | sort -u

# Find JavaScript files
gau target.com | grep "\.js$" | sort -u

# Pipeline probe live hosts
gau target.com | sort -u | httpx -status-code -title -json

# Full passive recon
echo target.com | gau --subdomains | sort -u | httpx -silent | nuclei -t cves/
```
