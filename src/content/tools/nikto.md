---
id: security-web-nikto
namespace: security:web:nikto
name: nikto
description: Web server scanner that tests for dangerous files, outdated server software,
  and misconfigurations on web servers.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - web.scan.vulnerability
  - web.fingerprint.server
  - web.discovery.path
  - web.scan.config
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
  - whatweb
  - wpscan
  - burpsuite
  - owasp-zap
artifacts:
  - type: web.scan.report
    description: Nikto scan report
    mime: text/html
    trust_level: verified
  - type: web.scan.text
    description: Nikto text output
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - scan-results
    - server-fingerprint
    - vuln-list
  consumes:
    - target-url
    - target-host
contract:
  inputs:
    - type: web.target.url
      description: Target web server URL
    - type: web.target.host
      description: Target hostname or IP
    - type: network.port
      description: Target port number
  outputs:
    - type: web.scan.report
      description: HTML scan report
      mime: text/html
    - type: web.scan.text
      description: Text output of findings
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
  - nikto
  - Bash
  - execFile
parameters:
  - name: host
    type: string
    required: true
    description: "Target hostname or IP address"
    aliases:
      - -h
  - name: port
    type: integer
    required: false
    description: "Target port (default 80)"
    default_value: "80"
    aliases:
      - -p
  - name: ssl
    type: boolean
    required: false
    description: "Force SSL/TLS mode (port 443)"
    aliases:
      - -ssl
  - name: Format
    type: string
    required: false
    description: "Output format: html, xml, csv, txt, json"
    aliases:
      - -Format
  - name: output
    type: file
    required: false
    description: "Output file for scan results"
    aliases:
      - -output
  - name: Tuning
    type: string
    required: false
    description: "Tuning options (1-9) to control scan scope"
    aliases:
      - -Tuning
  - name: idhost
    type: string
    required: false
    description: "Hostname to use in HTTP Host header"
    aliases:
      - -idhost
  - name: evasion
    type: string
    required: false
    description: "Evasion technique (1-9)"
    aliases:
      - -evasion
  - name: mutate
    type: integer
    required: false
    description: "Mutate technique for more checks"
    aliases:
      - -mutate
  - name: root
    type: string
    required: false
    description: "Prepend root path to all requests"
    aliases:
      - -root
  - name: timeout
    type: integer
    required: false
    description: "Request timeout in seconds"
    aliases:
      - -timeout
  - name: no404
    type: boolean
    required: false
    description: "Disable 404 detection heuristic"
    aliases:
      - -no404
  - name: useragent
    type: string
    required: false
    description: "Custom User-Agent header value"
    aliases:
      - -useragent
  - name: Display
    type: integer
    required: false
    description: "Display verbosity level (1-4)"
    aliases:
      - -Display
execution:
  template: "nikto -h {target} -p {port}"
  sandbox: execFile
  timeout_seconds: 900
  shell: false
global_vars:
  target: ip
  port: "80"
examples:
  - description: "Basic scan of a web server on default port"
    command: nikto -h example.com
  - description: "Scan on a non-standard port with SSL"
    command: nikto -h example.com -p 8443 -ssl
  - description: "Output results to HTML report"
    command: nikto -h example.com -p 443 -ssl -Format html -output report.html
  - description: "Scan with specific tuning options"
    command: nikto -h example.com -Tuning 123
  - description: "Evasion technique for WAF bypass"
    command: nikto -h example.com -evasion 1
  - description: "Custom virtual host scan"
    command: nikto -h 10.0.0.1 -idhost vhost.example.com
  - description: "Scan with custom user agent and timeout"
    command: nikto -h example.com -useragent "Mozilla/5.0" -timeout 10
references:
  - label: "Nikto GitHub"
    url: "https://github.com/sullo/nikto"
  - label: "Nikto Documentation"
    url: "https://github.com/sullo/nikto/wiki"
phase: enumeration
techniques:
  - recon
  - discovery
items:
  - NoCreds
services: []
attack_types:
  - Enumeration
install:
    - method: apt
      package_name: "nikto"
      commands:
        - "apt-get install -y nikto"
---

# Nikto — Web Server Scanner

Nikto is an open-source web server scanner that performs comprehensive tests against web servers for multiple items, including dangerous files/CGIs, outdated server software, and misconfigurations.

## Key Features

- **Server Fingerprinting**: Identify web server type and version
- **Vulnerability Checks**: 6700+ potentially dangerous files/programs
- **Config Assessment**: Check for outdated or misconfigured software
- **SSL/TLS Checks**: Test HTTPS configurations
- **Multiple Output Formats**: HTML, XML, CSV, TXT, JSON

## Scan Tuning Options

| Tuning Value | Category |
|-------------|----------|
| 1 | Interesting File / Seen in logs |
| 2 | Misconfiguration / Default File |
| 3 | Information Disclosure |
| 4 | Injection (XSS/Script/HTML) |
| 5 | Remote File Retrieval |

## Basic Usage

```bash
# Basic scan
nikto -h example.com

# HTTPS with HTML report
nikto -h example.com -ssl -Format html -output report.html

# Custom port with evasion
nikto -h example.com -p 8080 -evasion 1
```

## Operational Security

- Nikto can be noisy and easily detected by IDS/IPS
- Use `-evasion` techniques for stealth
- Scanning without authorization is illegal
