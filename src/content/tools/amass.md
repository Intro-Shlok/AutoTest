---
id: security-recon-amass
namespace: security:recon:amass
name: amass
description: In-depth DNS enumeration, subdomain discovery, and attack surface mapping
  tool from the OWASP project.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - network.discovery.dns
  - network.discovery.subdomain
  - security.fingerprint.certificate
  - security.recon.attack-surface
  - network.discovery.host
platforms:
  - linux
  - macos
  - cross-platform
risk_level: medium
trust_level: verified
execution_policy: enabled
architectures:
  - amd64
  - arm64
dependencies: []
related_tools:
  - subfinder
  - assetfinder
  - dnsenum
  - fierce
artifacts:
  - type: security.recon.subdomain.list
    description: List of discovered subdomains
    mime: text/plain
    trust_level: verified
  - type: security.recon.graph
    description: Graph visualization of domain relationships
    mime: text/html
    trust_level: community
workflow_edges:
  produces:
    - subdomains
    - domain-graph
    - dns-records
  consumes:
    - domain
contract:
  inputs:
    - type: network.target.domain
      description: Target domain name
  outputs:
    - type: security.recon.subdomain.list
      description: Discovered subdomains
      mime: text/plain
    - type: security.recon.graph
      description: Visual relationship graph
      mime: text/html
  side_effects:
    - network_traffic
    - network_traffic
  resource_cost:
    cpu: medium
    memory_mb: 256
    network: medium
    disk_io: low
resource_profile:
  cpu: medium
  memory_mb: 256
  network: medium
  disk_io: low
allowed-tools:
  - amass
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
  - name: flag-dL
    type: file
    required: false
    description: "File containing list of domains"
    aliases:
      - -dL
      - --list
  - name: config
    type: file
    required: false
    description: "Configuration file"
    aliases:
      - -config
  - name: flag-o
    type: string
    required: false
    description: "Output file for discovered subdomains"
    aliases:
      - -o
      - --output
  - name: flag-json
    type: boolean
    required: false
    description: "JSON output format"
    aliases:
      - -json
  - name: flag-dir
    type: string
    required: false
    description: "Output directory for multiple domains"
    aliases:
      - -dir
  - name: flag-nf
    type: boolean
    required: false
    description: "Do not include the domain root in output"
    aliases:
      - -nf
      - --no-root-domain
  - name: flag-r
    type: string
    required: false
    description: "IP address of trusted DNS resolver"
    aliases:
      - -r
      - --resolver
  - name: flag-rf
    type: file
    required: false
    description: "File containing list of DNS resolvers"
    aliases:
      - -rf
      - --resolver-file
  - name: active
    type: boolean
    required: false
    description: "Perform active enumeration (DNS queries, zone transfer)"
    aliases:
      - -active
  - name: flag-bl
    type: boolean
    required: false
    description: "Blacklist ASN from the enumeration"
    aliases:
      - -bl
      - --blacklist
  - name: flag-blf
    type: file
    required: false
    description: "File containing blacklist data"
    aliases:
      - -blf
      - --blacklist-file
  - name: brute
    type: boolean
    required: false
    description: "Enable brute forcing of subdomains"
    aliases:
      - -brute
  - name: flag-w
    type: file
    required: false
    description: "Wordlist file for brute forcing"
    aliases:
      - -w
      - --wordlist
  - name: flag-aw
    type: file
    required: false
    description: "Additional wordlist for alterations"
    aliases:
      - -aw
      - --alt-wordlist
  - name: flag-src
    type: boolean
    required: false
    description: "Print source for each discovered subdomain"
    aliases:
      - -src
  - name: flag-ip
    type: boolean
    required: false
    description: "Show IP addresses for discovered names"
    aliases:
      - -ip
  - name: flag-org
    type: boolean
    required: false
    description: "Show organization information"
    aliases:
      - -org
  - name: flag-asn
    type: boolean
    required: false
    description: "Show ASN data"
    aliases:
      - -asn
  - name: flag-time
    type: integer
    required: false
    description: "Maximum execution time in minutes"
    aliases:
      - -time
  - name: flag-max-dns-queries
    type: integer
    required: false
    description: "Maximum DNS queries per minute"
    aliases:
      - -max-dns-queries
execution:
  template: "amass enum -d {domain} -o {output}"
  sandbox: execFile
  timeout_seconds: 3600
  shell: false
global_vars:
  target: domain
  domain: "example.com"
  output: "amass-results.txt"
examples:
  - description: "Basic subdomain enumeration"
    command: amass enum -d example.com
  - description: "Enumeration with active techniques"
    command: amass enum -d example.com -active
  - description: "Brute force subdomains with custom wordlist"
    command: amass enum -d example.com -brute -w /usr/share/wordlists/subdomains.txt
  - description: "Save results to file"
    command: amass enum -d example.com -o results.txt
  - description: "JSON output for programmatic processing"
    command: amass enum -d example.com -json results.json
  - description: "Use a specific DNS resolver"
    command: amass enum -d example.com -r 8.8.8.8
  - description: "Enumerate across multiple domains from a file"
    command: amass enum -dL domains.txt
  - description: "Visualize results as a graph"
    command: amass viz -d example.com -o graph.html
  - description: "Track new subdomains over time"
    command: amass track -d example.com
references:
  - label: "OWASP Amass GitHub"
    url: "https://github.com/owasp-amass/amass"
  - label: "Amass Documentation"
    url: "https://amass.readthedocs.io/"
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

# Amass — Attack Surface Mapping & Asset Discovery

Amass is the OWASP project's premier tool for in-depth DNS enumeration, subdomain discovery, and external attack surface mapping. It uses a wide range of techniques including DNS zone transfers, certificate transparency logs, search engine scraping, and brute forcing.

## Enumeration Modes

| Mode | Command | Description |
|------|---------|-------------|
| Subdomain enumeration | `amass enum -d example.com` | Passive and active subdomain discovery |
| Visualize | `amass viz -d example.com` | Generate HTML graph of relationships |
| Track | `amass track -d example.com` | Identify new assets over time |
| Database | `amass db -d example.com` | Interact with the local Amass database |

## Data Sources

Amass queries dozens of sources including:
- Certificate Transparency logs (crt.sh, CertSpotter, Google)
- Search engines (Bing, Google, Yahoo, Shodan)
- DNS datasets (DNSDumpster, Riddler, PTR archives)
- Threat intelligence (AlienVault OTX, VirusTotal)
- ASN/Whois data (RADIUS, TeamCymru, BGPTools)

## Output

```bash
# List subdomains
amass enum -d example.com

# With IP addresses and sources
amass enum -d example.com -ip -src

# Full JSON output for pipeline processing
amass enum -d example.com -json results.json
```
