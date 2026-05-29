---
id: security-web-joomscan
namespace: security:web:joomscan
name: joomscan
description: Joomla CMS vulnerability scanner that detects component versions, known
  vulnerabilities, and security misconfigurations.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - web.discovery.asset
  - web.fingerprint.cms
  - web.vulnerability.scanner
  - web.enumeration.component
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
  - cmsmap
  - whatweb
artifacts:
  - type: report.json
    description: Scan results as JSON
    mime: application/json
    trust_level: verified
  - type: report.html
    description: HTML-formatted scan report
    mime: text/html
    trust_level: verified
workflow_edges:
  produces:
    - cms-fingerprint
    - vulnerability-list
    - component-list
  consumes:
    - target-url
contract:
  inputs:
    - type: web.target.url
      description: Target Joomla URL to scan
    - type: web.target.cookie
      description: Session cookie for authenticated scanning
    - type: network.proxy
      description: HTTP proxy for routing traffic
  outputs:
    - type: report.json
      description: Joomscan scan report as JSON
      mime: application/json
    - type: report.html
      description: Joomscan scan report as HTML
      mime: text/html
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
  - joomscan
  - Bash
  - execFile
parameters:
  - name: url
    type: string
    required: true
    description: "Target Joomla URL (e.g. http://target.com/joomla)"
    aliases:
      - -u
      - --url
  - name: threads
    type: integer
    required: false
    description: "Number of threads for concurrent scanning"
    default_value: "10"
    aliases:
      - -t
      - --threads
  - name: verbose
    type: boolean
    required: false
    description: "Enable verbose output"
    aliases:
      - -v
      - --verbose
  - name: output
    type: string
    required: false
    description: "Save scan report to file"
    aliases:
      - -o
      - --output
  - name: cookie
    type: string
    required: false
    description: "HTTP cookie for authenticated scanning"
    aliases:
      - --cookie
  - name: user-agent
    type: string
    required: false
    description: "Custom User-Agent header"
    aliases:
      - --user-agent
  - name: proxy
    type: string
    required: false
    description: "HTTP proxy address (e.g. http://127.0.0.1:8080)"
    aliases:
      - --proxy
  - name: timeout
    type: integer
    required: false
    description: "Request timeout in seconds"
    default_value: "30"
    aliases:
      - --timeout
  - name: follow-redirects
    type: boolean
    required: false
    description: "Follow HTTP redirects"
    aliases:
      - --follow-redirects
  - name: no-check-certificate
    type: boolean
    required: false
    description: "Skip SSL certificate validation"
    aliases:
      - --no-check-certificate
execution:
  template: "joomscan -u {target}"
  sandbox: execFile
  timeout_seconds: 300
  shell: false
global_vars:
  target: url
examples:
  - description: "Basic Joomla scan"
    command: joomscan -u http://target.com/joomla
  - description: "Scan with authenticated cookie"
    command: joomscan -u http://target.com/joomla --cookie "session=abc123"
  - description: "Scan using proxy with verbose output"
    command: joomscan -u http://target.com/joomla --proxy http://127.0.0.1:8080 -v
  - description: "Save scan report to file"
    command: joomscan -u http://target.com/joomla -o report.html
  - description: "Multi-threaded scan"
    command: joomscan -u http://target.com/joomla -t 20
references:
  - label: "OWASP Joomla Vulnerability Scanner"
    url: "https://github.com/rezasp/joomscan"
  - label: "Joomscan on Kali"
    url: "https://www.kali.org/tools/joomscan/"
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
    - method: apt
      package_name: "joomscan"
      commands:
        - "apt-get install -y joomscan"
---

# Joomscan — Joomla CMS Vulnerability Scanner

Joomscan is a specialized vulnerability scanner for Joomla CMS that detects the core version, installed components, known vulnerabilities, and security misconfigurations.

## Basic Usage

```bash
# Basic scan
joomscan -u http://target.com/joomla

# Scan with proxy through Burp Suite
joomscan -u http://target.com/joomla --proxy http://127.0.0.1:8080

# Authenticated scan
joomscan -u http://target.com/joomla --cookie "session=abc123"

# Save HTML report
joomscan -u http://target.com/joomla -o report.html
```

## Key Features

- **Version fingerprinting**: Detects Joomla core and extension versions
- **Vulnerability database**: Checks against known CVE database
- **Component enumeration**: Lists installed third-party components
- **Security checks**: Detects common misconfigurations and sensitive files
