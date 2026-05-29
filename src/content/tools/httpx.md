---
id: security-web-httpx
namespace: security:web:httpx
name: httpx
description: Fast and multi-purpose HTTP toolkit from ProjectDiscovery for probing, analyzing, and fingerprinting web servers and services.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - web.discovery.endpoint
  - web.fingerprint.technology
  - web.probe.http
  - web.enumeration.asset
  - security.fingerprint.service
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
  - nuclei
  - katana
  - subfinder
  - ffuf
artifacts:
  - type: network.http.response
    description: HTTP probe response data
    mime: text/plain
    trust_level: verified
  - type: web.fingerprint.results
    description: Technology fingerprint results
    mime: application/json
    trust_level: verified
workflow_edges:
  produces:
    - live-hosts
    - tech-stack
    - response-headers
  consumes:
    - target-url
    - host-list
contract:
  inputs:
    - type: network.target.url
      description: Target URL to probe
    - type: network.target.domain.list
      description: File containing list of hosts/domains
    - type: network.target.ip
      description: Target IP address
  outputs:
    - type: web.fingerprint.results
      description: Live hosts with status codes and technologies
      mime: application/json
    - type: network.http.response
      description: Raw HTTP response data
      mime: text/plain
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
  - httpx
  - Bash
  - execFile
parameters:
  - name: list
    type: string
    required: false
    description: "File containing list of URLs or hosts"
    aliases:
      - -l
      - --list
  - name: target
    type: string
    required: false
    description: "Single target URL or host"
    aliases:
      - -t
      - --target
  - name: flag-sc
    type: boolean
    required: false
    description: "Include status code in output"
    aliases:
      - -sc
      - --status-code
  - name: flag-ct
    type: boolean
    required: false
    description: "Include content type in output"
    aliases:
      - -ct
      - --content-type
  - name: flag-location
    type: boolean
    required: false
    description: "Include redirect location in output"
    aliases:
      - -location
  - name: flag-favicon
    type: boolean
    required: false
    description: "Extract favicon hash for identifying services"
    aliases:
      - -favicon
  - name: flag-title
    type: boolean
    required: false
    description: "Extract page title"
    alises:
      - -title
  - name: flag-tech-detect
    type: boolean
    required: false
    description: "Enable technology detection using wappalyzer"
    aliases:
      - -tech-detect
  - name: flag-json
    type: boolean
    required: false
    description: "Output as JSON lines"
    aliases:
      - -json
  - name: flag-threads
    type: integer
    required: false
    description: "Number of concurrent threads"
    aliases:
      - -t
      - --threads
  - name: flag-probe
    type: boolean
    required: false
    description: "Probe hosts for HTTP/HTTPS"
    aliases:
      - -probe
  - name: flag-o
    type: string
    required: false
    description: "Output file path"
    aliases:
      - -o
      - --output
  - name: flag-follow-redirects
    type: boolean
    required: false
    description: "Follow redirects"
    aliases:
      - -follow-redirects
execution:
  template: "httpx {flags} {target}"
  sandbox: execFile
  timeout_seconds: 120
  shell: false
examples:
  - description: "Probe a single URL"
    command: echo "https://example.com" | httpx -status-code -title
  - description: "Probe multiple hosts from a file"
    command: httpx -l hosts.txt -status-code -tech-detect -json
  - description: "Probe with favicon hash extraction"
    command: cat live-hosts.txt | httpx -favicon -status-code -title
  - description: "Probe and follow redirects"
    command: cat urls.txt | httpx -status-code -location -follow-redirects
  - description: "Probe with technology detection"
    command: httpx -l urls.txt -tech-detect -json -o results.json
references:
  - label: "httpx GitHub"
    url: "https://github.com/projectdiscovery/httpx"
  - label: "httpx Documentation"
    url: "https://docs.projectdiscovery.io/tools/httpx"
phase: enumeration
techniques:
  - recon
  - discovery
items:
  - NoCreds
services:
  - HTTP
  - HTTPS
attack_types:
  - Enumeration
  - Discovery
install:
    - method: go
      repo_url: "github.com/projectdiscovery/httpx/cmd/httpx"
      commands:
        - "go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest"
---

# httpx — HTTP Probing Toolkit

httpx is a fast and versatile HTTP probing tool from ProjectDiscovery used to analyze web servers, detect technologies, capture response metadata, and filter live hosts from large target sets. It is commonly pipelined with other tools like subfinder and nuclei.

## Pipeline Usage

```bash
# Subfinder -> httpx -> nuclei
subfinder -d example.com | httpx -status-code -title | nuclei -t cves/

# MassDNS -> httpx -> screenshot
massdns -r resolvers.txt -t A domains.txt | httpx -silent | aquatone
```

## Common Probes

```bash
# Basic probing
cat hosts.txt | httpx -status-code -content-type -title

# Full technology detection
subfinder -d example.com | httpx -tech-detect -json

# Extract all alive hosts
cat urls.txt | httpx -silent -status-code

# Favicon hash for service identification
httpx -l urls.txt -favicon
```
