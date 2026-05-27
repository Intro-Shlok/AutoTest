---
id: security-dns-dnsrecon
namespace: security:dns:dnsrecon
name: dnsrecon
description: DNS enumeration script that performs SRV record discovery, subdomain bruteforce, DNSSEC testing, zone transfer attempts, and reverse DNS lookups.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - dns.enum.records
  - dns.enum.subdomain
  - dns.enum.zone-transfer
  - dns.enum.reverse
  - dns.test.dnssec
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
  - dnsenum
  - fierce
  - amass
  - sublist3r
  - dig
artifacts:
  - type: dns.records.json
    description: DNS records in JSON format
    mime: application/json
    trust_level: verified
  - type: dns.records.csv
    description: DNS records in CSV format
    mime: text/csv
    trust_level: verified
workflow_edges:
  produces:
    - dns-records
    - zone-transfer-results
  consumes:
    - target-domain
    - target-dns-server
contract:
  inputs:
    - type: domain.name
      description: Target domain name
    - type: network.target.host
      description: Target DNS server
  outputs:
    - type: dns.records.json
      description: Discovered DNS records as JSON
      mime: application/json
    - type: dns.records.csv
      description: Discovered DNS records as CSV
      mime: text/csv
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
  - dnsrecon
  - python3
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
  - name: flag-type
    type: string
    required: false
    description: "Scan type (std, rvl, brd, brt, srv, axfr, zonewalk)"
    aliases:
      - -t
      - --type
  - name: flag-nameserver
    type: string
    required: false
    description: "Target DNS server"
    aliases:
      - -n
      - --name-server
  - name: flag-range
    type: string
    required: false
    description: "IP range for reverse lookup (CIDR)"
    aliases:
      - -r
      - --range
  - name: flag-dictionary
    type: string
    required: false
    description: "Wordlist file for bruteforce"
    aliases:
      - -D
      - --dictionary
  - name: flag-threads
    type: integer
    required: false
    description: "Number of threads for bruteforce"
    aliases:
      - --threads
  - name: flag-csv
    type: boolean
    required: false
    description: "Output in CSV format"
    aliases:
      - -c
      - --csv
  - name: flag-json
    type: boolean
    required: false
    description: "Output in JSON format"
    aliases:
      - -j
      - --json
  - name: flag-db
    type: string
    required: false
    description: "SQLite database file for output"
    aliases:
      - --db
  - name: flag-dnsserver
    type: string
    required: false
    description: "Use specified DNS server for queries"
    aliases:
      - -s
      - --dnsserver
execution:
  template: "dnsrecon {flag-type} {flag-threads} {flag-csv} {flag-json} {flag-db} {flag-dnsserver} {flag-range} {flag-nameserver} {flag-dictionary} {domain}"
  sandbox: execFile
  timeout_seconds: 300
  shell: false
examples:
  - description: "Standard DNS enumeration"
    command: dnsrecon -d example.com
  - description: "Zone transfer attempt"
    command: dnsrecon -d example.com -t axfr
  - description: "Reverse DNS lookup on IP range"
    command: dnsrecon -r 192.168.1.0/24
  - description: "Subdomain bruteforce with wordlist"
    command: dnsrecon -d example.com -D subdomains.txt -t brt
  - description: "SRV record discovery"
    command: dnsrecon -d example.com -t srv
references:
  - label: "dnsrecon GitHub"
    url: "https://github.com/darkoperator/dnsrecon"
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

# dnsrecon — DNS Enumeration Script

dnsrecon is a Python-based DNS enumeration tool that performs various types of DNS reconnaissance including standard record enumeration, zone transfers, SRV record discovery, subdomain bruteforce, reverse lookups, and DNSSEC testing.

## Usage

```bash
# Standard enumeration
dnsrecon -d example.com

# Zone transfer
dnsrecon -d example.com -t axfr

# Brute force subdomains
dnsrecon -d example.com -D wordlist.txt -t brt

# Reverse lookup
dnsrecon -r 10.0.0.0/24

# JSON output
dnsrecon -d example.com -j output.json
```
