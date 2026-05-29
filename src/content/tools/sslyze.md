---
id: security-tls-sslyze
namespace: security:tls:sslyze
name: sslyze
description: Python-based SSL/TLS scanner that analyzes server configurations for protocol support, cipher strength, certificate validation, and known vulnerabilities.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - tls.scan.certificate
  - tls.scan.cipher
  - tls.scan.protocol
  - tls.scan.vulnerability
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
  - testssl.sh
  - sslscan
  - openssl
  - nmap
artifacts:
  - type: report.json
    description: TLS scan results as JSON
    mime: application/json
    trust_level: verified
  - type: report.txt
    description: TLS scan results as text
    mime: text/plain
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
    - type: report.txt
      description: Scan results in text
      mime: text/plain
  side_effects:
    - network_traffic
  resource_cost:
    cpu: low
    memory_mb: 128
    network: low
    disk_io: low
resource_profile:
  cpu: low
  memory_mb: 128
  network: low
  disk_io: low
allowed-tools:
  - sslyze
  - python3
  - Bash
  - execFile
parameters:
  - name: target
    type: string
    required: true
    description: "Target hostname or IP:port"
  - name: flag-json
    type: boolean
    required: false
    description: "Output in JSON format"
    aliases:
      - --json_out
  - name: flag-regular
    type: boolean
    required: false
    description: "Run regular scan (all cipher suites)"
    aliases:
      - --regular
  - name: flag-certinfo
    type: boolean
    required: false
    description: "Retrieve certificate information"
    aliases:
      - --certinfo
  - name: flag-sslv2
    type: boolean
    required: false
    description: "Check SSLv2 support"
    aliases:
      - --sslv2
  - name: flag-sslv3
    type: boolean
    required: false
    description: "Check SSLv3 support"
    aliases:
      - --sslv3
  - name: flag-tlsv1
    type: boolean
    required: false
    description: "Check TLSv1.0 support"
    aliases:
      - --tlsv1
  - name: flag-tlsv11
    type: boolean
    required: false
    description: "Check TLSv1.1 support"
    aliases:
      - --tlsv1_1
  - name: flag-tlsv12
    type: boolean
    required: false
    description: "Check TLSv1.2 support"
    aliases:
      - --tlsv1_2
  - name: flag-tlsv13
    type: boolean
    required: false
    description: "Check TLSv1.3 support"
    aliases:
      - --tlsv1_3
  - name: flag-starttls
    type: string
    required: false
    description: "STARTTLS protocol (smtp, ftp, xmpp, etc.)"
    aliases:
      - --starttls
  - name: flag-timeout
    type: integer
    required: false
    description: "Connection timeout in seconds"
    aliases:
      - --timeout
execution:
  template: "sslyze {flag-regular} {flag-certinfo} {flag-sslv2} {flag-sslv3} {flag-tlsv1} {flag-tlsv11} {flag-tlsv12} {flag-tlsv13} {flag-starttls} {flag-json} {target}:{port}"
  sandbox: execFile
  timeout_seconds: 120
  shell: false
examples:
  - description: "Basic TLS scan on default port"
    command: sslyze example.com
  - description: "Scan specific port with JSON output"
    command: sslyze --json_out results.json example.com:8443
  - description: "Full scan with certificate info"
    command: sslyze --regular --certinfo example.com
  - description: "Check STARTTLS for SMTP"
    command: sslyze --starttls smtp example.com:25
references:
  - label: "sslyze GitHub"
    url: "https://github.com/nabla-c0d3/sslyze"
  - label: "sslyze Documentation"
    url: "https://nabla-c0d3.github.io/sslyze/documentation/"
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
install:
    - method: pip
      package_name: "sslyze"
      commands:
        - "pip install sslyze"
---

# sslyze — SSL/TLS Scanner

sslyze is a fast and comprehensive Python-based TLS/SSL scanner that analyzes server configurations. It checks protocol support (SSLv2, SSLv3, TLS 1.0-1.3), cipher suite strength, certificate validity, and known vulnerabilities like Heartbleed, ROBOT, and others.

## Usage

```bash
# Basic scan
sslyze example.com

# Full scan with JSON output
sslyze --regular --certinfo --json_out scan.json example.com

# Check STARTTLS on SMTP
sslyze --starttls smtp mail.example.com:25

# Check specific TLS version
sslyze --tlsv1_2 --tlsv1_3 example.com
```
