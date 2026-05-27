---
id: security-recon-fierce
namespace: security:recon:fierce
name: fierce
description: DNS reconnaissance tool for locating non-contiguous IP space, subdomain
  brute forcing, and reverse DNS lookups.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - network.discovery.dns
  - network.discovery.subdomain
  - security.recon.dns
  - network.discovery.ip-range
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
  - dnsenum
  - dnsrecon
  - amass
  - subfinder
artifacts:
  - type: security.recon.dns.records
    description: Discovered DNS records and IP space
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - dns-records
    - ip-ranges
    - subdomains
  consumes:
    - domain
contract:
  inputs:
    - type: network.target.domain
      description: Target domain name
  outputs:
    - type: security.recon.dns.records
      description: DNS records and discovered IP space
      mime: text/plain
  side_effects:
    - network_traffic
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
  - fierce
  - Bash
  - execFile
parameters:
  - name: domain
    type: string
    required: false
    description: "Domain name to test"
    aliases:
      - --domain
  - name: connect
    type: boolean
    required: false
    description: "Attempt HTTP connection to non-RFC 1918 hosts"
    aliases:
      - --connect
  - name: wide
    type: boolean
    required: false
    description: "Scan entire class C of discovered records"
    aliases:
      - --wide
  - name: traverse
    type: integer
    required: false
    description: "Scan N IPs before and after discovered records"
    aliases:
      - --traverse
  - name: search
    type: string
    required: false
    description: "Filter on these domains when expanding lookup"
    aliases:
      - --search
  - name: range
    type: string
    required: false
    description: "Scan an internal IP range in CIDR notation"
    aliases:
      - --range
  - name: delay
    type: integer
    required: false
    description: "Time to wait between lookups (seconds)"
    aliases:
      - --delay
  - name: subdomains
    type: string
    required: false
    description: "Use these subdomains"
    aliases:
      - --subdomains
  - name: subdomain-file
    type: file
    required: false
    description: "Use subdomains from this file (one per line)"
    aliases:
      - --subdomain-file
  - name: dns-servers
    type: string
    required: false
    description: "Use these DNS servers for reverse lookups"
    aliases:
      - --dns-servers
  - name: dns-file
    type: file
    required: false
    description: "Use DNS servers from this file"
    aliases:
      - --dns-file
  - name: tcp
    type: boolean
    required: false
    description: "Use TCP instead of UDP for DNS queries"
    aliases:
      - --tcp
execution:
  template: "fierce --domain {domain}"
  sandbox: execFile
  timeout_seconds: 300
  shell: false
global_vars:
  target: domain
  domain: "example.com"
examples:
  - description: "Basic DNS reconnaissance"
    command: fierce --domain example.com
  - description: "Wide scan across entire class C ranges"
    command: fierce --domain example.com --wide
  - description: "With HTTP connection checking"
    command: fierce --domain example.com --connect
  - description: "Scan internal IP range"
    command: fierce --range 10.10.10.0/24
  - description: "Custom subdomain wordlist"
    command: fierce --domain example.com --subdomain-file subdomains.txt
  - description: "Use specific DNS servers"
    command: fierce --domain example.com --dns-servers 8.8.8.8 1.1.1.1
  - description: "Traverse N addresses around discovered records"
    command: fierce --domain example.com --traverse 10
  - description: "Use TCP for DNS queries"
    command: fierce --domain example.com --tcp
references:
  - label: "Fierce GitHub"
    url: "https://github.com/mschwager/fierce"
  - label: "Fierce Kali docs"
    url: "https://www.kali.org/tools/fierce/"
phase: enumeration
techniques:
  - discovery
  - enumeration
items:
  - NoCreds
services: []
attack_types:
  - Enumeration
---

# Fierce — DNS Reconnaissance

Fierce is a DNS recon tool originally written by RSnake and rewritten in Python. It locates non-contiguous IP space by performing DNS zone transfers, subdomain brute forcing, and reverse DNS lookups to map a target's network footprint.

## Key Capabilities

- **Subdomain discovery**: Brute forces common subdomain names
- **IP space mapping**: Identifies non-contiguous IP ranges
- **Wide scanning**: Expands to scan entire class C networks
- **Reverse DNS**: Maps IP blocks back to hostnames
- **Internal scanning**: Scan RFC 1918 ranges for host discovery

## Usage Examples

```bash
# Basic recon
fierce --domain example.com

# Wide scan with connectivity check
fierce --domain example.com --wide --connect

# Internal range scanning
fierce --range 10.10.10.0/24 --dns-servers 192.168.1.1
```
