---
id: security-tls-testssl-sh
namespace: security:tls:testssl-sh
name: testssl.sh
description: Shell script for TLS/SSL testing that checks protocol support, cipher suites, certificate issues, and known vulnerabilities on any TLS server.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - tls.scan.certificate
  - tls.scan.cipher
  - tls.scan.protocol
  - tls.scan.vulnerability
  - tls.scan.heartbleed
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
  - bash
  - openssl
related_tools:
  - sslyze
  - sslscan
  - openssl
  - nmap
artifacts:
  - type: report.json
    description: TLS scan results as JSON
    mime: application/json
    trust_level: verified
  - type: report.html
    description: TLS scan results as HTML
    mime: text/html
    trust_level: verified
  - type: report.csv
    description: TLS scan results as CSV
    mime: text/csv
    trust_level: verified
workflow_edges:
  produces:
    - tls-scan-results
    - certificate-info
    - cipher-info
  consumes:
    - target-host
    - target-port
contract:
  inputs:
    - type: network.target.host
      description: Target hostname or IP address
    - type: network.port
      description: Target port (default 443)
  outputs:
    - type: report.json
      description: Scan results in JSON
      mime: application/json
    - type: report.html
      description: Scan results in HTML
      mime: text/html
    - type: report.csv
      description: Scan results in CSV
      mime: text/csv
  side_effects:
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
  - testssl.sh
  - bash
  - Bash
  - execFile
parameters:
  - name: target
    type: string
    required: true
    description: "Target URI, hostname, or IP (optionally with port)"
  - name: flag-uri
    type: string
    required: false
    description: "Auto-detect port (https://host, ftps://host, etc.)"
    aliases:
      - --uri
  - name: flag-json
    type: boolean
    required: false
    description: "Output in JSON format"
    aliases:
      - --jsonfile
  - name: flag-html
    type: boolean
    required: false
    description: "Output in HTML format"
    aliases:
      - --htmlfile
  - name: flag-csv
    type: boolean
    required: false
    description: "Output in CSV format"
    aliases:
      - --csvfile
  - name: flag-severity
    type: string
    required: false
    description: "Only display findings of severity (LOW, MEDIUM, HIGH, CRITICAL)"
    aliases:
      - --severity
  - name: flag-quiet
    type: boolean
    required: false
    description: "Quiet mode, less verbose output"
    aliases:
      - --quiet
  - name: flag-color
    type: boolean
    required: false
    description: "Force colored output"
    aliases:
      - --color
  - name: flag-starttls
    type: string
    required: false
    description: "STARTTLS protocol (smtp, ftp, imap, pop3, xmpp, etc.)"
    aliases:
      - --starttls
  - name: flag-protocols
    type: boolean
    required: false
    description: "Check only protocol support"
    aliases:
      - --protocols
  - name: flag-ciphers
    type: boolean
    required: false
    description: "Check only cipher suites"
    aliases:
      - --ciphers
execution:
  template: "testssl.sh {flag-quiet} {flag-color} {flag-severity} {flag-protocols} {flag-ciphers} {flag-json} {flag-html} {flag-csv} {flag-starttls} {target}"
  sandbox: execFile
  timeout_seconds: 300
  shell: false
examples:
  - description: "Basic TLS scan"
    command: testssl.sh example.com
  - description: "Scan with JSON and HTML output"
    command: testssl.sh --jsonfile scan.json --htmlfile scan.html example.com
  - description: "Quick check for protocol support only"
    command: testssl.sh --protocols example.com
  - description: "Check STARTTLS SMTP"
    command: testssl.sh --starttls smtp mail.example.com:25
  - description: "Scan with severity filter"
    command: testssl.sh --severity HIGH example.com
references:
  - label: "testssl.sh GitHub"
    url: "https://github.com/drwetter/testssl.sh"
  - label: "testssl.sh Documentation"
    url: "https://testssl.sh/docs/"
phase: enumeration
techniques:
  - discovery
  - enumeration
items:
  - NoCreds
services:
  - HTTPS
attack_types:
  - Enumeration
  - Discovery
---

# testssl.sh — TLS/SSL Testing Tool

testssl.sh is a free command-line tool that checks a server's TLS/SSL configuration for protocol support, cipher suites, certificate issues, and known vulnerabilities. Written as a shell script, it requires only bash and openssl.

## Usage

```bash
# Basic scan
testssl.sh example.com

# Output to JSON and HTML
testssl.sh --jsonfile scan.json --htmlfile scan.html example.com

# Check only protocols
testssl.sh --protocols example.com:8443

# Check STARTTLS
testssl.sh --starttls ftp ftp.example.com:21
```
