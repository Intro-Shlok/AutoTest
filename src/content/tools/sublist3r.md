---
id: security-recon-sublist3r
namespace: security:recon:sublist3r
name: sublist3r
description: OSINT subdomain enumeration tool that uses search engines, DNS services, and certificate transparency logs to discover subdomains of a target domain.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - dns.enum.subdomain
  - osint.discovery.subdomain
  - osint.search.engine
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
  - amass
  - subfinder
  - assetfinder
  - dnsrecon
  - fierce
artifacts:
  - type: dns.subdomain.list
    description: Discovered subdomains list
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - subdomain-list
  consumes:
    - target-domain
contract:
  inputs:
    - type: domain.name
      description: Target domain name
  outputs:
    - type: dns.subdomain.list
      description: List of discovered subdomains
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
  - sublist3r
  - python3
  - Bash
  - execFile
parameters:
  - name: domain
    type: string
    required: true
    description: "Target domain name"
    aliases:
      - -d
      - --domain
  - name: flag-ports
    type: string
    required: false
    description: "Ports to scan for HTTP/HTTPS on discovered subdomains"
    aliases:
      - -p
      - --ports
  - name: flag-threads
    type: integer
    required: false
    description: "Number of threads for enumeration"
    aliases:
      - -t
      - --threads
  - name: flag-engines
    type: string
    required: false
    description: "Comma-separated list of search engines to use"
    aliases:
      - -e
      - --engines
  - name: flag-no-color
    type: boolean
    required: false
    description: "Disable colored output"
    aliases:
      - -n
      - --no-color
  - name: flag-bruteforce
    type: boolean
    required: false
    description: "Enable subdomain bruteforce"
    aliases:
      - -b
      - --bruteforce
  - name: flag-output
    type: string
    required: false
    description: "Output file for results"
    aliases:
      - -o
      - --output
  - name: flag-verbose
    type: boolean
    required: false
    description: "Verbose output"
    aliases:
      - -v
      - --verbose
execution:
  template: "sublist3r {flag-verbose} {flag-no-color} {flag-bruteforce} {flag-threads} {flag-ports} {flag-engines} {flag-output} -d {domain}"
  sandbox: execFile
  timeout_seconds: 300
  shell: false
examples:
  - description: "Basic subdomain enumeration"
    command: sublist3r -d example.com
  - description: "Save results to file with verbose output"
    command: sublist3r -d example.com -o subdomains.txt -v
  - description: "Use specific search engines only"
    command: sublist3r -d example.com -e baidu,yahoo,google
  - description: "Enable bruteforce with 50 threads"
    command: sublist3r -d example.com -b -t 50
references:
  - label: "Sublist3r GitHub"
    url: "https://github.com/aboul3la/Sublist3r"
phase: recon
techniques:
  - recon
  - discovery
items:
  - NoCreds
services:
  - DNS
attack_types:
  - Discovery
  - Enumeration
---

# Sublist3r — Subdomain Enumeration Tool

Sublist3r is an OSINT-based subdomain enumeration tool designed for penetration testers and security researchers. It leverages multiple search engines (Google, Yahoo, Bing, Baidu, Ask) and other sources like Netcraft, DNSDumpster, and VirusTotal to discover subdomains.

## Usage

```bash
# Basic enumeration
sublist3r -d example.com

# Save to file
sublist3r -d example.com -o subdomains.txt

# Enable bruteforce
sublist3r -d example.com -b

# Specify engines
sublist3r -d example.com -e google,yahoo

# Increase threads
sublist3r -d example.com -t 100
```
