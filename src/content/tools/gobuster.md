---
id: security-web-gobuster
namespace: security:web:gobuster
name: gobuster
description: Multi-purpose brute-force tool for directory/file discovery, DNS subdomain
  enumeration, and cloud bucket enumeration.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - web.discovery.path
  - web.discovery.file
  - web.discovery.vhost
  - web.discovery.dns
  - web.discovery.bucket
  - web.content.brute
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
  - dirsearch
  - feroxbuster
  - ffuf
  - wfuzz
artifacts:
  - type: web.discovery.results
    description: Discovered paths or subdomains
    mime: application/json
    trust_level: verified
  - type: web.discovery.dns
    description: DNS subdomain enumeration results
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - discovered-paths
    - discovered-subdomains
    - discovered-vhosts
  consumes:
    - target-url
    - target-domain
    - wordlist
contract:
  inputs:
    - type: web.target.url
      description: Target URL
    - type: network.target.domain
      description: Target domain for DNS enumeration
    - type: file.wordlist
      description: Wordlist for brute-forcing
  outputs:
    - type: web.discovery.results
      description: Discovered paths or subdomains
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
  - gobuster
  - Bash
  - execFile
parameters:
  - name: mode
    type: string
    required: true
    description: "Mode: dir, dns, vhost, s3"
    aliases: []
  - name: url
    type: string
    required: false
    description: "Target URL (dir, vhost modes)"
    aliases:
      - -u
  - name: domain
    type: string
    required: false
    description: "Target domain (dns mode)"
    aliases:
      - -d
  - name: wordlist
    type: file
    required: true
    description: "Path to wordlist file"
    aliases:
      - -w
  - name: threads
    type: integer
    required: false
    description: "Number of concurrent threads"
    default_value: "10"
    aliases:
      - -t
  - name: extensions
    type: string
    required: false
    description: "File extensions to search (dir mode)"
    aliases:
      - -x
  - name: output
    type: file
    required: false
    description: "Output file path"
    aliases:
      - -o
  - name: status-codes
    type: string
    required: false
    description: "Status codes to include (positive)"
    aliases:
      - -s
  - name: insecure
    type: boolean
    required: false
    description: "Skip TLS certificate verification"
    aliases:
      - -k
  - name: no-redirect
    type: boolean
    required: false
    description: "Do not follow redirects"
    aliases:
      - -n
  - name: cookies
    type: string
    required: false
    description: "Cookies to include in requests"
    aliases:
      - -c
  - name: headers
    type: string
    required: false
    description: "Custom HTTP headers"
    aliases:
      - -H
  - name: timeout
    type: integer
    required: false
    description: "HTTP request timeout in seconds"
    aliases:
      - --timeout
  - name: wildcard
    type: boolean
    required: false
    description: "Force wildcard detection"
    aliases:
      - --wildcard
  - name: exclude-length
    type: integer
    required: false
    description: "Exclude results of given content length"
    aliases:
      - --exclude-length
  - name: quiet
    type: boolean
    required: false
    description: "Quiet mode (no banner or progress)"
    aliases:
      - -q
  - name: follow-redirect
    type: boolean
    required: false
    description: "Follow HTTP redirects"
    aliases:
      - -r
execution:
  template: "gobuster dir -u {target} -w {wordlist} -t {threads}"
  sandbox: execFile
  timeout_seconds: 1800
  shell: false
global_vars:
  target: url
  wordlist: "/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt"
  threads: "10"
examples:
  - description: "Directory brute-force with common wordlist"
    command: gobuster dir -u https://example.com -w /usr/share/wordlists/dirb/common.txt -t 50
  - description: "Directory scan with file extensions"
    command: gobuster dir -u https://example.com -w wordlist.txt -x php,html,asp -t 30
  - description: "DNS subdomain enumeration"
    command: gobuster dns -d example.com -w /usr/share/wordlists/amass/subdomains-top1mil-5000.txt -t 20
  - description: "Virtual host enumeration"
    command: gobuster vhost -u https://example.com -w vhost-wordlist.txt -t 20
  - description: "S3 bucket enumeration"
    command: gobuster s3 -w bucket-names.txt
  - description: "Scan with custom headers and cookies"
    command: 'gobuster dir -u https://example.com -w wordlist.txt -H "Authorization: Bearer token" -c "session=abc123"'
  - description: "Quiet mode with status code filtering"
    command: gobuster dir -u https://example.com -w wordlist.txt -s 200,204,301,302,307 -q
references:
  - label: "Gobuster GitHub"
    url: "https://github.com/OJ/gobuster"
phase: enumeration
techniques:
  - discovery
  - enumeration
  - discovery
items:
  - NoCreds
services: []
attack_types:
  - Enumeration
install:
    - method: go
      repo_url: "github.com/OJ/gobuster/v3"
      commands:
        - "go install github.com/OJ/gobuster/v3@latest"
    - method: apt
      package_name: "gobuster"
      commands:
        - "apt-get install -y gobuster"
---

# Gobuster — Multi-Purpose Brute-Force Tool

Gobuster is a fast, multi-purpose brute-force tool written in Go. It supports directory/file discovery, DNS subdomain enumeration, virtual host discovery, and cloud bucket enumeration.

## Modes

| Mode | Command | Description |
|------|---------|-------------|
| Directory | `gobuster dir -u URL -w WORDLIST` | Find hidden directories/files |
| DNS | `gobuster dns -d DOMAIN -w WORDLIST` | Enumerate DNS subdomains |
| VHost | `gobuster vhost -u URL -w WORDLIST` | Discover virtual hosts |
| S3 | `gobuster s3 -w WORDLIST` | Find S3 buckets |

## Basic Usage

```bash
# Directory brute-force
gobuster dir -u https://example.com -w /usr/share/wordlists/dirb/common.txt -t 50

# DNS subdomain enumeration
gobuster dns -d example.com -w subdomains.txt -t 20

# Virtual host discovery
gobuster vhost -u https://example.com -w vhosts.txt -t 30
```

## Operational Security

- High thread counts can overwhelm target servers
- Use `-k` to skip TLS verification on internal networks
- DNS queries can be logged by the DNS server
- Scanning without authorization is illegal
