---
id: security-web-cmsmap
namespace: security:web:cmsmap
name: cmsmap
description: Content Management System security scanner supporting WordPress, Joomla,
  Drupal, and Moodle fingerprinting and enumeration.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - web.discovery.asset
  - web.fingerprint.cms
  - web.enumeration.component
  - web.vulnerability.scanner
  - web.enumeration.user
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
  - wpscan
  - joomscan
  - whatweb
artifacts:
  - type: report.json
    description: Scan results as JSON
    mime: application/json
    trust_level: verified
  - type: report.csv
    description: Scan results as CSV
    mime: text/csv
    trust_level: verified
workflow_edges:
  produces:
    - cms-fingerprint
    - vulnerability-list
    - user-list
    - component-list
  consumes:
    - target-url
    - target-domain
contract:
  inputs:
    - type: web.target.url
      description: Target CMS URL to scan
    - type: web.target.domain
      description: Target domain for CMS detection
    - type: network.target.file
      description: File containing list of target URLs
  outputs:
    - type: report.json
      description: CMS scan report as JSON
      mime: application/json
    - type: report.csv
      description: CMS scan report as CSV
      mime: text/csv
  side_effects:
    - network_traffic
    - network_traffic
  resource_cost:
    cpu: low
    memory_mb: 128
    network: medium
    disk_io: low
resource_profile:
  cpu: low
  memory_mb: 128
  network: medium
  disk_io: low
allowed-tools:
  - cmsmap
  - Bash
  - execFile
parameters:
  - name: target
    type: string
    required: true
    description: "Target URL or hostname"
    aliases:
      - -t
      - --target
  - name: url
    type: string
    required: false
    description: "Full URL to scan (alternative to -t)"
    aliases:
      - -u
      - --url
  - name: force
    type: boolean
    required: false
    description: "Force scan even if CMS detection fails"
    aliases:
      - -f
      - --force
  - name: force-ssl
    type: boolean
    required: false
    description: "Force HTTPS connection"
    aliases:
      - -F
      - --force-ssl
  - name: user-agent
    type: string
    required: false
    description: "Custom User-Agent header"
    aliases:
      - -a
      - --user-agent
  - name: headers
    type: string
    required: false
    description: "Additional HTTP headers (comma-separated)"
    aliases:
      - -H
      - --headers
  - name: proxy
    type: string
    required: false
    description: "HTTP proxy address"
    aliases:
      - -p
      - --proxy
  - name: verbose
    type: boolean
    required: false
    description: "Verbose output"
    aliases:
      - -v
      - --verbose
  - name: output
    type: string
    required: false
    description: "Output file for results"
    aliases:
      - -o
      - --output
  - name: input-file
    type: file
    required: false
    description: "File containing list of target URLs"
    aliases:
      - -i
      - --input-file
  - name: detect
    type: boolean
    required: false
    description: "Detect CMS type only (no deep scan)"
    aliases:
      - -d
      - --detect
  - name: enumerate
    type: boolean
    required: false
    description: "Enable enumeration of users and components"
    aliases:
      - -E
      - --enumerate
  - name: extensions
    type: string
    required: false
    description: "File extensions to check (comma-separated)"
    aliases:
      - -x
      - --extensions
  - name: wordlist
    type: file
    required: false
    description: "Custom wordlist for brute force"
    aliases:
      - -w
      - --wordlist
  - name: recursive
    type: boolean
    required: false
    description: "Recursive directory enumeration"
    aliases:
      - -r
      - --recursive
execution:
  template: "cmsmap -t {target}"
  sandbox: execFile
  timeout_seconds: 600
  shell: false
global_vars:
  target: url
examples:
  - description: "Basic CMS scan"
    command: cmsmap -t http://target.com
  - description: "Force WordPress scan over HTTPS"
    command: cmsmap -t http://target.com -F -f
  - description: "CMS scan with proxy and verbose output"
    command: cmsmap -t http://target.com -p http://127.0.0.1:8080 -v
  - description: "Enumerate users and components"
    command: cmsmap -t http://target.com -E
  - description: "Scan multiple targets from file"
    command: cmsmap -i targets.txt -o results.csv
  - description: "CMS detection only"
    command: cmsmap -t http://target.com -d
references:
  - label: "CMSMap GitHub"
    url: "https://github.com/Dionach/CMSmap"
  - label: "CMSMap on Kali"
    url: "https://www.kali.org/tools/cmsmap/"
phase: enumeration
techniques:
  - recon
  - enumeration
  - discovery
items:
  - NoCreds
services: []
attack_types:
  - Enumeration
install:
    - method: pip
      package_name: "cmsmap"
      commands:
        - "pip install cmsmap"
---

# CMSMap — CMS Security Scanner

CMSMap is a security scanner for popular Content Management Systems (WordPress, Joomla, Drupal, and Moodle) that performs fingerprinting, version detection, user enumeration, and vulnerability scanning.

## Basic Usage

```bash
# Basic scan of a CMS website
cmsmap -t http://target.com

# Enumerate users and components
cmsmap -t http://target.com -E

# Scan through a proxy
cmsmap -t http://target.com -p http://127.0.0.1:8080 -v

# Scan multiple targets from a file
cmsmap -i targets.txt -o results.csv
```

## Supported CMS

| CMS | Detection | Enumeration |
|-----|-----------|-------------|
| WordPress | Core version, plugins, themes | Users, vulnerable plugins |
| Joomla | Core version, components | Users, vulnerable extensions |
| Drupal | Core version, modules | Users, vulnerable modules |
| Moodle | Core version, plugins | Users, courses |
