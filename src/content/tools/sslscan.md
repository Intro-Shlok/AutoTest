---
id: security-tls-sslscan
namespace: security:tls:sslscan
name: sslscan
description: Fast C-based TLS/SSL scanner that checks protocol support, cipher suites, certificate information, and performs comprehensive server configuration analysis.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - tls.scan.certificate
  - tls.scan.cipher
  - tls.scan.protocol
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
dependencies: []
related_tools:
  - testssl.sh
  - sslyze
  - openssl
  - nmap
artifacts:
  - type: report.txt
    description: TLS scan results as text
    mime: text/plain
    trust_level: verified
  - type: report.xml
    description: TLS scan results as XML
    mime: text/xml
    trust_level: verified
workflow_edges:
  produces:
    - tls-scan-results
    - cipher-info
  consumes:
    - target-host
    - target-port
contract:
  inputs:
    - type: network.target.host
      description: Target hostname or IP
    - type: network.port
      description: Target port (default 443)
  outputs:
    - type: report.txt
      description: Scan results in text
      mime: text/plain
    - type: report.xml
      description: Scan results in XML
      mime: text/xml
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
  - sslscan
  - Bash
  - execFile
parameters:
  - name: target
    type: string
    required: true
    description: "Target hostname:port"
  - name: flag-xml
    type: boolean
    required: false
    description: "Output in XML format"
    aliases:
      - --xml
  - name: flag-xmlfile
    type: string
    required: false
    description: "Output XML to file"
    aliases:
      - --xml-file
  - name: flag-no-colour
    type: boolean
    required: false
    description: "Disable colored output"
    aliases:
      - --no-colour
  - name: flag-no-heartbleed
    type: boolean
    required: false
    description: "Skip Heartbleed check"
    aliases:
      - --no-heartbleed
  - name: flag-ssl2
    type: boolean
    required: false
    description: "Only check SSLv2"
    aliases:
      - --ssl2
  - name: flag-ssl3
    type: boolean
    required: false
    description: "Only check SSLv3"
    aliases:
      - --ssl3
  - name: flag-tls10
    type: boolean
    required: false
    description: "Only check TLSv1.0"
    aliases:
      - --tls10
  - name: flag-tls11
    type: boolean
    required: false
    description: "Only check TLSv1.1"
    aliases:
      - --tls11
  - name: flag-tls12
    type: boolean
    required: false
    description: "Only check TLSv1.2"
    aliases:
      - --tls12
  - name: flag-tls13
    type: boolean
    required: false
    description: "Only check TLSv1.3"
    aliases:
      - --tls13
  - name: flag-starttls
    type: string
    required: false
    description: "STARTTLS protocol (smtp, imap, pop3, etc.)"
    aliases:
      - --starttls
  - name: flag-sni
    type: string
    required: false
    description: "Server Name Indication hostname"
    aliases:
      - --sni
execution:
  template: "sslscan {flag-xml} {flag-xmlfile} {flag-no-colour} {flag-no-heartbleed} {flag-ssl2} {flag-ssl3} {flag-tls10} {flag-tls11} {flag-tls12} {flag-tls13} {flag-starttls} {flag-sni} {target}"
  sandbox: execFile
  timeout_seconds: 120
  shell: false
examples:
  - description: "Basic TLS scan"
    command: sslscan example.com:443
  - description: "XML output to file"
    command: sslscan --xml-file scan.xml example.com:443
  - description: "Check STARTTLS IMAP"
    command: sslscan --starttls imap mail.example.com:143
references:
  - label: "sslscan GitHub"
    url: "https://github.com/rbsec/sslscan"
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
    - method: apt
      package_name: "sslscan"
      commands:
        - "apt-get install -y sslscan"
---

# sslscan — TLS/SSL Scanner

sslscan is a fast, lightweight C-based TLS/SSL scanner that tests services for supported cipher suites, protocol versions, certificate information, and known vulnerabilities. It is commonly included in Kali Linux and other pentesting distributions.

## Usage

```bash
# Basic scan
sslscan example.com:443

# XML output
sslscan --xml-file scan.xml example.com:443

# Scan with SNI
sslscan --sni example.com 192.168.1.100:443

# Check STARTTLS
sslscan --starttls smtp mail.example.com:25
```
