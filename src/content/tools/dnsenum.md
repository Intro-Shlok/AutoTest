---
id: security-recon-dnsenum
namespace: security:recon:dnsenum
name: dnsenum
description: Perl-based DNS enumeration tool that performs comprehensive DNS record
  queries, brute forcing, reverse lookups, and zone transfers.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - network.discovery.dns
  - network.discovery.subdomain
  - security.recon.dns
  - service.dns.zone-transfer
platforms:
  - linux
  - cross-platform
risk_level: low
trust_level: verified
execution_policy: enabled
architectures:
  - amd64
  - arm64
dependencies: []
related_tools:
  - fierce
  - dnsrecon
  - amass
  - subfinder
artifacts:
  - type: security.recon.dns.records
    description: DNS records discovered during enumeration
    mime: text/plain
    trust_level: verified
  - type: security.recon.subdomain.list
    description: Discovered subdomains
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - dns-records
    - subdomains
    - ptr-records
  consumes:
    - domain
contract:
  inputs:
    - type: network.target.domain
      description: Target domain name
  outputs:
    - type: security.recon.dns.records
      description: Collected DNS records
      mime: text/plain
    - type: security.recon.subdomain.list
      description: Discovered subdomains
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
  - dnsenum
  - Bash
  - execFile
parameters:
  - name: domain
    type: string
    required: true
    description: "Target domain name"
  - name: dnsserver
    type: string
    required: false
    description: "Use this DNS server for A, NS and MX queries"
    aliases:
      - --dnsserver
  - name: enum
    type: boolean
    required: false
    description: "Shortcut equivalent to --threads 5 -s 15 -w"
    aliases:
      - --enum
  - name: noreverse
    type: boolean
    required: false
    description: "Skip the reverse lookup operations"
    aliases:
      - --noreverse
  - name: nocolor
    type: boolean
    required: false
    description: "Disable ANSI color output"
    aliases:
      - --nocolor
  - name: private
    type: boolean
    required: false
    description: "Show and save private IPs in domain_ips.txt"
    aliases:
      - --private
  - name: flag-t
    type: integer
    required: false
    description: "TCP and UDP timeout in seconds"
    default_value: "10"
    aliases:
      - -t
      - --timeout
  - name: threads
    type: integer
    required: false
    description: "Number of threads for queries"
    default_value: "5"
    aliases:
      - --threads
  - name: flag-v
    type: boolean
    required: false
    description: "Verbose output"
    aliases:
      - -v
      - --verbose
  - name: flag-p
    type: integer
    required: false
    description: "Google search pages to process"
    default_value: "5"
    aliases:
      - -p
      - --pages
  - name: flag-s
    type: integer
    required: false
    description: "Max subdomains to scrape from Google"
    default_value: "15"
    aliases:
      - -s
      - --scrap
  - name: flag-f
    type: file
    required: false
    description: "Subdomain wordlist file for brute force"
    aliases:
      - -f
      - --file
  - name: flag-u
    type: string
    required: false
    description: "Update file with valid subdomains (a|g|r|z)"
    aliases:
      - -u
      - --update
  - name: flag-r
    type: boolean
    required: false
    description: "Recursively brute force subdomains with NS records"
    aliases:
      - -r
      - --recursion
  - name: flag-d
    type: integer
    required: false
    description: "Max delay between whois queries"
    default_value: "3"
    aliases:
      - -d
      - --delay
  - name: flag-w
    type: boolean
    required: false
    description: "Perform whois queries on C class network ranges"
    aliases:
      - -w
      - --whois
  - name: flag-e
    type: string
    required: false
    description: "Exclude PTR records matching regexp"
    aliases:
      - -e
      - --exclude
  - name: flag-o
    type: string
    required: false
    description: "Output in XML format"
    aliases:
      - -o
      - --output
execution:
  template: "dnsenum {domain}"
  sandbox: execFile
  timeout_seconds: 600
  shell: false
global_vars:
  target: domain
  domain: "example.com"
examples:
  - description: "Basic DNS enumeration"
    command: dnsenum example.com
  - description: "Enumeration with Google scraping and whois"
    command: dnsenum --enum example.com
  - description: "DNS brute force with custom wordlist"
    command: dnsenum -f /usr/share/wordlists/subdomains.txt example.com
  - description: "Recursive brute force on subdomains"
    command: dnsenum -r example.com
  - description: "Use specific DNS server"
    command: dnsenum --dnsserver 8.8.8.8 example.com
  - description: "Output results to XML file"
    command: dnsenum -o results.xml example.com
references:
  - label: "dnsenum Kali package"
    url: "https://www.kali.org/tools/dnsenum/"
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

# dnsenum — DNS Enumeration Tool

dnsenum is a comprehensive DNS enumeration Perl script that automates the process of gathering DNS information about a target domain. It performs zone transfers, brute forces subdomains, conducts reverse lookups, and can integrate with Google scraping.

## Key Features

- **DNS record enumeration**: A, NS, MX, TXT, CNAME records
- **Zone transfer**: Attempts DNS zone transfers
- **Subdomain brute forcing**: Uses a wordlist for brute force discovery
- **Reverse lookups**: Discovers PTR records for IP ranges
- **Google scraping**: Extracts subdomains from search results
- **Recursive mode**: Brute forces discovered subdomains recursively
