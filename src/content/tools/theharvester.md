---
id: security-recon-theharvester
namespace: security:recon:theharvester
name: theHarvester
description: OSINT tool for gathering emails, subdomains, IP addresses, and URLs from
  public data sources for a target domain.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - security.intel.email
  - network.discovery.subdomain
  - security.recon.passive
  - security.intel.osint
  - security.intel.host
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
  - recon-ng
  - spiderfoot
  - amass
  - subfinder
artifacts:
  - type: security.intel.email.list
    description: Discovered email addresses
    mime: text/plain
    trust_level: community
  - type: security.recon.subdomain.list
    description: Discovered subdomains
    mime: text/plain
    trust_level: verified
  - type: security.intel.host.list
    description: Discovered hosts and IP addresses
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - email-addresses
    - subdomains
    - hosts
    - urls
  consumes:
    - domain
contract:
  inputs:
    - type: network.target.domain
      description: Company name or domain to search
  outputs:
    - type: security.intel.email.list
      description: Found email addresses
      mime: text/plain
    - type: security.recon.subdomain.list
      description: Found subdomains
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
  - theHarvester
  - Bash
  - execFile
parameters:
  - name: flag-d
    type: string
    required: true
    description: "Company name or domain to search"
    aliases:
      - -d
      - --domain
  - name: flag-b
    type: string
    required: true
    description: "Data source (baidu, brave, crtsh, dnsdumpster, google, shodan, etc.)"
    aliases:
      - -b
      - --source
  - name: flag-l
    type: integer
    required: false
    description: "Limit the number of search results"
    default_value: "500"
    aliases:
      - -l
      - --limit
  - name: flag-S
    type: integer
    required: false
    description: "Start with result number X"
    default_value: "0"
    aliases:
      - -S
      - --start
  - name: flag-p
    type: boolean
    required: false
    description: "Use proxies for requests"
    aliases:
      - -p
      - --proxies
  - name: flag-s
    type: boolean
    required: false
    description: "Use Shodan to query discovered hosts"
    aliases:
      - -s
      - --shodan
  - name: flag-e
    type: string
    required: false
    description: "DNS server to use for lookup"
    aliases:
      - -e
      - --dns-server
  - name: flag-t
    type: boolean
    required: false
    description: "Check for subdomain takeovers"
    aliases:
      - -t
      - --take-over
  - name: flag-r
    type: string
    required: false
    description: "Perform DNS resolution on subdomains"
    aliases:
      - -r
      - --dns-resolve
  - name: flag-n
    type: boolean
    required: false
    description: "Enable DNS server lookup"
    aliases:
      - -n
      - --dns-lookup
  - name: flag-c
    type: boolean
    required: false
    description: "Perform DNS brute force on the domain"
    aliases:
      - -c
      - --dns-brute
  - name: flag-f
    type: string
    required: false
    description: "Save results to XML and JSON file"
    aliases:
      - -f
      - --filename
  - name: flag-w
    type: string
    required: false
    description: "Wordlist for API endpoint scanning"
    aliases:
      - -w
      - --wordlist
  - name: flag-q
    type: boolean
    required: false
    description: "Suppress missing API key warnings"
    aliases:
      - -q
      - --quiet
execution:
  template: "theHarvester -d {domain} -b {source} -l {limit}"
  sandbox: execFile
  timeout_seconds: 300
  shell: false
global_vars:
  target: domain
  domain: "example.com"
  source: "all"
  limit: "500"
examples:
  - description: "Gather emails and subdomains from all sources"
    command: theHarvester -d example.com -b all
  - description: "Search Google for email addresses"
    command: theHarvester -d example.com -b google -l 200
  - description: "Query certificate transparency logs for subdomains"
    command: theHarvester -d example.com -b crtsh
  - description: "Use Shodan to find host information"
    command: theHarvester -d example.com -b shodan -s
  - description: "DNS brute force with custom wordlist"
    command: theHarvester -d example.com -c -w /usr/share/wordlists/subdomains.txt
  - description: "Check for subdomain takeover vulnerabilities"
    command: theHarvester -d example.com -b crtsh -t
  - description: "Save results to file"
    command: theHarvester -d example.com -b all -f results
  - description: "Use proxies to avoid rate limiting"
    command: theHarvester -d example.com -b google -p
references:
  - label: "theHarvester GitHub"
    url: "https://github.com/laramies/theHarvester"
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

# theHarvester — OSINT Intelligence Gathering

theHarvester is a comprehensive OSINT tool designed for gathering emails, subdomains, IP addresses, and URLs from over 50 public data sources. It is widely used in the reconnaissance phase of penetration testing and red team engagements.

## Data Sources

theHarvester supports 50+ data sources including:
- Search engines: Google, Bing, Yahoo, DuckDuckGo, Baidu
- Certificate transparency: crt.sh, CertSpotter
- Threat intelligence: VirusTotal, AlienVault, Shodan
- DNS: DNSDumpster, SecurityTrails
- Code repos: GitHub, GitLab

## Output

```bash
# Save results to XML and JSON
theHarvester -d example.com -b all -f output

# DNS resolution and brute forcing
theHarvester -d example.com -c -n
```
