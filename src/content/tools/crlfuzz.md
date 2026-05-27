---
id: security-web-crlfuzz
namespace: security:web:crlfuzz
name: crlfuzz
description: Fast CRLF injection scanner written in Go that detects HTTP response splitting and header injection vulnerabilities.
author: "Repository Maintainers"
version: "1.0.0"
capabilities:
  - web.crlf.detect
  - web.injection.header
  - web.response.split
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
  - smuggler
  - burpsuite
  - nmap
artifacts:
  - type: web.crlf.report
    description: CRLF injection scan results
    mime: text/plain
    trust_level: verified
workflow_edges:
  produces:
    - crlf-scan-results
  consumes:
    - target-url
contract:
  inputs:
    - type: web.target.url
      description: Target URL
  outputs:
    - type: web.crlf.report
      description: Scan results with vulnerable endpoints
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
  - crlfuzz
  - Bash
  - execFile
parameters:
  - name: target
    type: string
    required: true
    description: "Target URL or host:port"
  - name: flag-verbose
    type: boolean
    required: false
    description: "Verbose output"
    aliases:
      - -v
      - --verbose
  - name: flag-threads
    type: integer
    required: false
    description: "Number of concurrent threads"
    aliases:
      - -t
      - --threads
  - name: flag-timeout
    type: integer
    required: false
    description: "Request timeout in seconds"
    aliases:
      - --timeout
  - name: flag-output
    type: string
    required: false
    description: "Output file for results"
    aliases:
      - -o
      - --output
  - name: flag-concurrency
    type: integer
    required: false
    description: "Concurrent scan level"
    aliases:
      - -c
      - --concurrency
execution:
  template: "crlfuzz {flag-verbose} {flag-threads} {flag-timeout} {flag-concurrency} {flag-output} {target}"
  sandbox: execFile
  timeout_seconds: 120
  shell: false
examples:
  - description: "Basic CRLF scan"
    command: crlfuzz -u https://example.com
  - description: "Verbose scan with threads"
    command: crlfuzz -u https://example.com -v -t 50
  - description: "Save results to file"
    command: crlfuzz -u https://example.com -o results.txt
references:
  - label: "CRLFuzz GitHub"
    url: "https://github.com/dwisiswant0/crlfuzz"
phase: exploitation
techniques:
  - execution
  - discovery
items:
  - NoCreds
services:
  - HTTP
attack_types:
  - Exploitation
---

# CRLFuzz — CRLF Injection Scanner

CRLFuzz is a fast Go-based tool for scanning CRLF (Carriage Return Line Feed) injection vulnerabilities. It tests for HTTP response splitting and header injection by injecting CRLF sequences into request parameters and headers.

## Usage

```bash
# Basic scan
crlfuzz -u https://example.com

# Verbose with concurrent threads
crlfuzz -u https://example.com -v -t 100

# Save to file
crlfuzz -u https://example.com -o vulnerable.txt
```
